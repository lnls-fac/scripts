#!/bin/bash

# Install selected repository

# --- Run with sudo -HE ---
set -e
set -x

function change_directory {
	if [ -d $1 ]; then
		cd $1
	else
		echo "$1 not found. Aborting"
		exit 1
	fi
}

function clone_repo {
	command -v git >/dev/null 2>&1 || { echo >&2 "Git not found. Aborting."; exit 1; }
	./check_github_ssh_key.sh
	git clone $1
}

function clone_and_develop {
	dir="$1/$2"
	if [ ! -d $dir ]; then
		change_directory $1
		clone_repo $3
	fi
	change_directory $dir
	python-sirius setup.py build
	sudo python-sirius setup.py $action
}

if [ -z $1 ]; then
	echo 'Please select a repository:'
	echo '## FAC ##'
	echo 'MML'
	echo 'apsuite'
	echo 'lnls'
	echo 'mathphys'
	echo 'trackcpp'
	echo 'fieldmaptrack'
	echo 'pyjob'
	echo 'pyaccel'
	echo 'pymodels'
	echo 'va'
	echo '## SIRIUS ##'
	echo 'control-system-constants'
	echo 'dev-packages'
	echo 'pydm'
	echo 'hla'
	echo 'pruserial485'
	echo 'machine-applications'
	echo 'sirius-scripts'
	echo '## MISC ##'
	echo 'pyjob'
	echo 'cs-studio'
	exit 1
fi

action='develop'
repo="$1"

fac_repos='/home/facs/repos'
sirius_repos='/home/sirius/repos'


#if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
#	echo 'No ssh key found. Please create one using ssh-keygen and add it to your github account.'
#	exit 1
#fi

# FAC
if [ $repo == 'MML' ]; then
	if [ ! -d "$fac_repos/trackcpp/MatlabMiddleLayer" ]; then
		change_directory "$fac_repos"
		clone_repo ssh://git@github.com/lnls-fac/MatlabMiddleLayer.git
	fi
	echo 'Repo clone. Please follow instructions:'
	echo '1 - open matlab as root: sudo matlab'
	echo '2 - Edit the path to include the folder: /home/fac_files/lnls-fac/MatlabMiddleLayer/Release/lnls/startup_scripts'
	echo '3 - Close matlab and open matlab in user mode: matlab'
	echo '4 - Compile the .mex files in matlab: '
	echo '	>> sirius;
		>> atmexall;
		>> naff_cc;'
elif [ $repo == 'apsuite' ]; then
	repo='apsuite'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'lnls' ]; then
	repo='lnls'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'mathphys' ]; then
	repo='mathphys'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'fieldmaptrack' ]; then
	repo='fieldmaptrack'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'trackcpp' ]; then
	sudo apt-get install -y g++ libgsl0-dev swig liblapack-dev
	if [ ! -d "$fac_repos/trackcpp" ]; then
		change_directory $fac_repos
		clone_repo ssh://git@github.com/lnls-fac/trackcpp.git
	fi
	change_directory "$fac_repos/trackcpp"
	sudo make clean
	sudo make -j8 PYTHON=python-sirius PYTHON_VERSION=python3.6
	sudo make install PYTHON=python-sirius PYTHON_VERSION=python3.6
elif [ $repo == 'pyaccel' ]; then
	repo='pyaccel'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'pymodels' ]; then
	repo='pymodels'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $fac_repos $repo $link
elif [ $repo == 'va' ]; then
	repo='va'
	link="ssh://git@github.com/lnls-fac/va.git"
	clone_and_develop $fac_repos $repo $link

# SIRIUS
elif [ $repo == 'control-system-constants' ]; then
	if [ ! -d '/home/fac_files/lnls-sirius/control-system-constants' ]; then
		change_directory $sirius_repos
		clone_repo ssh://git@github.com/lnls-sirius/control-system-constants.git
	fi
elif [ $repo == 'dev-packages' ]; then
	repo='dev-packages/siriuspy/'
	link="ssh://git@github.com/lnls-sirius/dev-packages.git"
	clone_and_develop $sirius_repos $repo $link
elif [ $repo == 'pydm' ]; then
	repo='pydm'
	link="ssh://git@github.com/lnls-sirius/pydm.git"
	clone_and_develop $sirius_repos $repo $link
elif [ $repo == 'hla' ]; then
	if [ ! -d "$sirius_repos/hla" ]; then
		change_directory $sirius_repos
		clone_repo ssh://git@github.com/lnls-sirius/hla.git
	fi
	change_directory "$sirius_repos/hla/pyqt-apps"
	make install-resources
	sudo make $action
elif [ $repo == 'pruserial485' ]; then
	if [ ! -d "$sirius_repos/pru-serial485" ]; then
		change_directory $sirius_repos
		clone_repo ssh://git@github.com:/lnls-sirius/pru-serial485.git
	fi
	change_directory "$sirius_repos/pru-serial485/src"
	sudo ./library_build.sh
	sudo ./overlay.sh
elif [ $repo == 'machine-applications' ]; then
	if [ ! -d "$sirius_repos/machine-applications" ]; then
		change_directory $sirius_repos
		clone_repo ssh://git@github.com/lnls-sirius/machine-applications.git
	fi
	change_directory $sirius_repos/machine-applications
	sudo make $action
elif [ $repo == 'sirius-scripts' ]; then
	change_directory '/home/sirius'
	clone_repo "ssh://git@github.com/lnls-sirius/scripts.git"
	change_directory '/home/sirius/scripts'
	sudo make $action

# MISC
elif [ $repo == 'cs-studio' ]; then
	version='4.6.1.12'
	file="cs-studio-ess-$version-linux.gtk.x86_64.tar.gz"
	if [ -d '/opt/cs-studio' ]; then 
		echo 'CS Studio installed. Passing.'
		exit 0
	fi
	if [ ! -f ./$file ]; then
		wget "https://artifactory.esss.lu.se/artifactory/CS-Studio/production/$version/$file"
	fi
	sudo tar xzvf $file
	sudo mv ./cs-studio /opt/cs-studio
	sudo ln -sf /opt/cs-studio/ESS\ CS-Studio /usr/local/bin/cs-studio
	sudo rm -rf $file
elif [ $repo == 'pyjob' ]; then
	if [ ! -d "$fac_repos/job_manager" ]; then
		change_directory $fac_repos
		clone_repo ssh://git@github.com/lnls-fac/job_manager.git
	fi
	change_directory "$fac_repos/job_manager/apps"
	sudo make install
	cd ..
	sudo ./install_services.py
	sudo systemctl start pyjob_run.service
else
	echo "Repository $repo not found"
fi

exit 0
