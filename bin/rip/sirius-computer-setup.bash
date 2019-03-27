#!/usr/bin/env bash


declare -a fac_users=("fernando" "ximenes" "guilherme" "liulin" "ana" "alexandre")



function create_groups {
	group=fac
	echo "creating group " $group
	sudo adduser --quiet --disabled-password --shell /bin/bash --home /home/fac --gecos "User" $group --ingroup $group
	sudo passwd $user
	sudo adduser $group --ingroup $group; # need to choose a password for fac user
	sudo usermod -G sudo $group
}

function create_fac_users {
	group=fac
	for user in "${fac_users[@]}"; do
		echo "creating user " $user
		sudo adduser --quiet --disabled-password --shell /bin/bash --home /home/$user --gecos "User" $user
		sudo passwd $user
		sudo usermod -G sudo,$user -g $group $user
	done
}

		
function install_linux_packages {
	printf "\n--- installing git ---\n"; sudo apt-get -y install git
	#echo "installing git..."; sudo apt-get install git	
	printf "\n--- installing g++ ---\n"; sudo apt-get -y install g++ 
	printf "\n--- installing gfortran ---\n"; sudo apt-get -y install gfortran
	printf "\n--- installing libreadline6-dev ---\n"; sudo apt-get -y install libreadline6-dev
	printf "\n--- installing re2c ---\n"; sudo apt-get -y install re2c
	printf "\n--- installing htop ---\n"; sudo apt-get -y install htop
	printf "\n--- installing swig ---\n"; sudo apt-get -y install swig
}

function install_epics_base {
	# epics base
	sudo mkdir -p /usr/local/epics
	sudo mkdir -p /usr/local/epics/R3.14.12.6
	sudo ln -s /usr/local/epics/R3.14.12.6 /usr/local/epics/R3.14
	sudo chown -R $(whoami) /usr/local/epics/
	cd ~/Downloads
	wget  https://www.aps.anl.gov/epics/download/base/baseR3.14.12.6.tar.gz
	tar xzf baseR3.14.12.6.tar.gz
	mv base-3.14.12.6 base
	mv base /usr/local/epics/R3.14.12.6
	cd /usr/local/epics/R3.14.12.6/base
	make -j32
}

function install_epics_extensions {
	source ~/.bashrc
	# epics extensions
	sudo rm -rf /usr/local/epics/R3.14.12.6/extensions
	mkdir -p /usr/local/epics/R3.14.12.6/extensions
	cd /usr/local/epics/R3.14.12.6/extensions
	makeBaseExt.pl -t simple
	# sequencer
	cd ~/Downloads
	wget http://www-csr.bessy.de/control/SoftDist/sequencer/releases/seq-2.2.4.tar.gz
	tar xzf seq-2.2.4.tar.gz
	mv seq-2.2.4 /usr/local/epics/R3.14/extensions
	cd /usr/local/epics/R3.14/extensions/seq-2.2.4
	sed -i 's/\/home\/franksen\/src\/epics-base\/3.14-12-5/\/usr\/local\/epics\/R3.14\/base/g' ./configure/RELEASE
	make -j32
	# procserver
	cd ~/Downloads
	wget https://sourceforge.net/projects/procserv/files/latest/download -O procServ-2.7.0.tar.gz
	tar xzf procServ-2.7.0.tar.gz
	mv procServ-2.7.0 /usr/local/epics/R3.14/extensions
	cd /usr/local/epics/R3.14/extensions/procServ-2.7.0
	./configure
	make -j32
	sudo make install
	# gateway
	cd ~/Downloads
	wget https://launchpad.net/epics-gateway/trunk/2.0.6.0/+download/gateway2_0_6_0.tar.gz
	tar xzf gateway2_0_6_0.tar.gz
	mv gateway2_0_6_0 /usr/local/epics/R3.14/extensions/src
	cd /usr/local/epics/R3.14.12.6/extensions/src/gateway2_0_6_0/configure
	echo "EPICS_BASE = /usr/local/epics/R3.14/base" > RELEASE.local
	cd ../../
	sed -i 's/DIRS +=/DIRS += gateway2_0_6_0/g' ./Makefile
	cd /usr/local/epics/R3.14/extensions
	make -j32
}


function config_git {
	user=$1
	echo "configuring git as " $user " ..."
	sudo apt-get install git
	git config --global core.editor vim
	git config --global push.default simple
	read -p "enter user.name: " git_user_name
	git config --global user.name $git_use_name
	read -p "enter user.email: " git_user_email
	git config --global user.email $git_user_email
}


function create_fac_files {
	read -p "this will delete /home/fac_files if it already exists. continue? (yes/[no]): " user_input
	if [[ "$user_input" != "yes" ]]
	then
		exit
	fi
	sudo rm -rf /home/fac_files
	sudo mkdir -p /home/fac_files; sudo chown -R fac /home/fac_files
	echo "--- !!! MANUALLY configure /etf/fstab ---"
	echo "sudo vi /etc/fstab        # and edit UUID=<some_ID> / ext4 errors=remount-ro,acl 0 1"
	echo "                          # and edit UUID=<some_ID> /home/ ext4 defaults,acl 0 2"
	echo ""
	read -p "type 'ok' and hit <enter> when done to proceed: " user_input
	if [[ "$user_input" != "ok" ]]
	then
		exit
	fi
	echo ""
	sudo mount -oremount /
	#sudo mount -oremount /home/ # in case your /home is in a different partition
	sudo chgrp -R fac /home/fac_files
	sudo setfacl -Rdm u::rwx,g:fac:rwx,o::r /home/fac_files
	sudo setfacl -Rm u::rwx,g:fac:rwx,o::r /home/fac_files
	cd /home/fac_files/
	cd /home/fac_files; mkdir lnls-fac lnls-sirius lnls-ima
	sudo chown -R fac /home/fac_files

}


function install_fac_scripts_repo {
	printf "\n--- installing sirius-fac/scripts ---\n"
	cd /home/fac_files/lnls-fac
	git clone git@github.com:lnls-fac/scripts
	sudo make -C scripts/etc develop
	sudo make -C scripts/bin develop
}


function install_siriusbashrc_for_user {
	echo -e "\n$(cat ~/.bashrc)" > ~/.bashrc
	echo -e "fi\n$(cat ~/.bashrc)" > ~/.bashrc
	echo -e "    source \"\$SIRIUSBASHRC\"\n$(cat ~/.bashrc)" > ~/.bashrc
	echo -e "if [ -f \"\$SIRIUSBASHRC\" ] ; then\n$(cat ~/.bashrc)" > ~/.bashrc
	echo -e "SIRIUSBASHRC=/usr/local/etc/bashrc-sirius\n$(cat ~/.bashrc)" > ~/.bashrc
}	


function install_python {
	printf "\n--- installing build-essential ---\n"; sudo apt-get -y install build-essential 
	printf "\n--- installing checkinstall ---\n"; sudo apt-get -y install checkinstall
	printf "\n--- installing libreadline-gplv2-dev ---\n"; sudo apt-get -y install libreadline-gplv2-dev
	printf "\n--- installing libncursesw5-dev ---\n"; sudo apt-get -y install libncursesw5-dev
	printf "\n--- installing libssl-dev ---\n"; sudo apt-get -y install libssl-dev
	printf "\n--- installing libsqlite3-dev ---\n"; sudo apt-get -y install libsqlite3-dev 
	printf "\n--- installing tk-dev ---\n"; sudo apt-get -y install tk-dev
	printf "\n--- installing libgdbm-dev ---\n"; sudo apt-get -y install libgdbm-dev
	printf "\n--- installing libc6-dev ---\n"; sudo apt-get -y install libc6-dev
	printf "\n--- installing libbz2-dev ---\n"; sudo apt-get -y install libbz2-dev 
	cd ~/Downloads
	wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
	tar xzf Python-3.6.1.tgz
	cd Python-3.6.1/
	./configure --enable-shared --with-ensurepip=install
	make -j32
	#make -j32 test
	sudo make altinstall
	sudo ldconfig
	sudo ln -f -s /usr/local/bin/python3.6 /usr/bin/python-sirius
}

function install_python_packages {
	printf "\n--- installing libffi6 ---\n"; sudo apt-get -y install libffi6	
	printf "\n--- installing libffi-dev ---\n"; sudo apt-get -y install libffi-dev
	printf "\n--- installing libfreetype6 ---\n"; sudo apt-get -y install libfreetype6
	printf "\n--- installing libfreetype6-dev ---\n"; sudo apt-get -y install libfreetype6-dev	
	printf "\n--- installing libpng3 ---\n"; sudo apt-get -y install libpng3
	printf "\n--- installing nmap ---\n"; sudo apt-get -y install nmap
	printf "\n--- installing dvipng ---\n"; sudo apt-get -y install dvipng	
	printf "\n--- installing python-nmap ---\n"; sudo pip3.6 install python-nmap
	printf "\n--- installing wakeonlan ---\n"; sudo pip3.6 install wakeonlan
	printf "\n--- installing requests ---\n"; sudo pip3.6 install requests
	printf "\n--- installing pyqtgraph ---\n"; sudo pip3.6 install pyqtgraph
	printf "\n--- installing pandas ---\n"; sudo pip3.6 install pandas
	printf "\n--- installing psutil ---\n"; sudo pip3.6 install psutil
	printf "\n--- installing termcolor ---\n"; sudo pip3.6 install termcolor
	printf "\n--- installing sh ---\n"; sudo pip3.6 install sh
	printf "\n--- installing cairocffi ---\n"; sudo pip3.6 install cairocffi
	printf "\n--- installing matplotlib ---\n"; sudo pip3.6 install matplotlib
	printf "\n--- installing scipy ---\n"; sudo pip3.6 install scipy
	printf "\n--- installing jupyter ---\n"; sudo pip3.6 install jupyter
}

function configure_hosts {
	source ~/.bashrc
	sudo chown fac.fac /etc/hosts && sudo chmod g+wr /etc/hosts
	fac-hosts-update.py
}

function install_pyepics_pcaspy {
	printf "\n--- installing pyepics ---\n"; sudo pip3.6 install pyepics
	source ~/.bashrc
	sudo -E pip3.6 install pcaspy
}


function clone_lnls_sirius_machine_applications {
	cd /home/fac_files/lnls-sirius/
	printf "\n--- clonning control-system-constants ---\n"; git clone git@github.com:lnls-sirius/control-system-constants.git
	printf "\n--- clonning dev-packages ---\n"; git clone git@github.com:lnls-sirius/dev-packages.git
	printf "\n--- clonning machine-applications ---\n"; git clone git@github.com:lnls-sirius/machine-applications.git
}


function clone_lnls_sirius_hla {
	printf "\n--- clonning hla ---\n"; git clone git@github.com:lnls-sirius/hla.git	
}


function clone_lnls_fac {
	cd /home/fac_files/lnls-fac/		
}





#create_groups
#create_fac_users
#install_linux_packages
#install_epics_base
#install_epics_extensions
#config_git
#create_fac_files
#install_fac_scripts_repo
#install_siriusbashrc_for_user
#install_python
#install_python_packages
#configure_hosts
#install_pyepics_pcaspy
#clone_lnls_sirius_machine_applications
#clone_lnls_sirius_hla
#clone_lnls_fac



