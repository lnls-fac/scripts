#!/bin/bash

set -e
set -x

# Clone scripts repository and intall sirius-bashrc

# Check if git is installed
command -v git >/dev/null 2>&1 || { echo >&2 "Git not found. Aborting."; exit 1; }
# Check ssh key
#if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
#	echo 'No ssh key found. Please create one using ssh-keygen and add it to your github account.'
#	exit 1
#fi
# Check if bashrc is already installed
if [ -f '/usr/local/etc/bashrc-sirius' ]; then
	echo 'bashrc-sirius already installed. Passing.'
	exit 0
fi

sudo apt-get install -y make

# dir=/home/fac_files/lnls-fac
dir=/home/fac
if [ -d $dir ]; then
	cd $dir
	if [ ! -d $dir/scripts ]; then
			git clone https://github.com/lnls-fac/scripts.git
	fi
	cd scripts
	sudo make develop

	users=(fernando ximenes guilherme liulin ana alexandre murilo sirius facs)
	for user in ${users[@]}; do
		bash_path="/home/$user/.bashrc"
		sudo sed -i -e '5i #Sirius bashrc' $bash_path
		sudo sed -i -e '6i SIRIUSBASHRC=/usr/local/etc/bashrc-sirius' $bash_path
		sudo sed -i -e '7i if [ -f "$SIRIUSBASHRC" ] ; then' $bash_path
		sudo sed -i -e '8i \ \ \ \ source "$SIRIUSBASHRC"' $bash_path
		sudo sed -i -e '9i fi\n' $bash_path
	done

	cd ..
	# sudo rm -rf "$dir/scripts"

	exit 0
else
	echo "$dir not found please run fac_directories.sh. Aborting."
	exit 1
fi

