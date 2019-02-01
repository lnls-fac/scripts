#!/bin/bash

# Install selected repository

# --- Run with sudo -HE ---

if [ -z $1 ]; then
	echo 'Please select a repository:'
	echo 'MML'
	echo 'apsuite'
	echo 'lnls'
	echo 'mathphys'
	echo 'trackcpp'
	echo 'pyjob'
	echo 'pyaccel'
	echo 'pymodels'
	echo 'control-system-constants'
	echo 'dev-packages'
	echo 'pydm'
	echo 'hla'
	echo 'machine-applications'
	echo 'va'
	exit 1
fi

action='develop'
repo="$1"

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


if [ $repo == 'MML' ]; then
	if [ ! -d '/home/fac_files/lnls-fac/trackcpp/MatlabMiddleLayer' ]; then
		change_directory '/home/fac_files/lnls-fac'
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
	dir='/home/fac_files/lnls-fac/'
	repo='apsuite'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'lnls' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='lnls'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'mathphys' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='mathphys'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'trackcpp' ]; then
	sudo apt-get install -y g++ libgsl0-dev swig liblapack-dev
	if [ ! -d '/home/fac_files/lnls-fac/trackcpp' ]; then
		change_directory '/home/fac_files/lnls-fac'
		clone_repo ssh://git@github.com/lnls-fac/trackcpp.git
	fi
	change_directory '/home/fac_files/lnls-fac/trackcpp'
	sudo make clean
	sudo make -j8 PYTHON=python-sirius PYTHON_VERSION=python3.6
	sudo make install PYTHON=python-sirius PYTHON_VERSION=python3.6
elif [ $repo == 'pyaccel' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='pyaccel'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'pymodels' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='pymodels'
	link="ssh://git@github.com/lnls-fac/$repo.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'control-system-constants' ]; then
	if [ ! -d '/home/fac_files/lnls-sirius/control-system-constants' ]; then
		change_directory '/home/fac_files/lnls-sirius'
		clone_repo ssh://git@github.com/lnls-sirius/control-system-constants.git
	fi
elif [ $repo == 'dev-packages' ]; then
	dir='/home/fac_files/lnls-sirius/'
	repo='dev-packages/siriuspy/'
	link="ssh://git@github.com/lnls-sirius/dev-packages.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'pydm' ]; then
	dir='/home/fac_files/lnls-sirius/'
	repo='pydm'
	link="ssh://git@github.com/lnls-sirius/pydm.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'hla' ]; then
	if [ ! -d '/home/fac_files/lnls-sirius/hla' ]; then
		change_directory '/home/fac_files/lnls-sirius'
		clone_repo ssh://git@github.com/lnls-sirius/hla.git
	fi
	change_directory "/home/fac_files/lnls-sirius/hla/pyqt-apps"
	make install-resources
	sudo make develop
elif [ $repo == 'pruserial485' ]; then
	if [ ! -d '/home/fac_files/lnls-sirius/pru-serial485' ]; then
		change_directory '/home/fac_files/lnls-sirius/'
		clone_repo ssh://git@github.com:/lnls-sirius/pru-serial485.git
	fi
	change_directory '/home/fac_files/lnls-sirius/pru-serial485/src'
	sudo ./library_build.sh
	sudo ./overlay.sh
elif [ $repo == 'machine-applications' ]; then
	if [ ! -d '/home/fac_files/lnls-sirius/machine-applications' ]; then
		change_directory '/home/fac_files/lnls-sirius'
		clone_repo ssh://git@github.com/lnls-sirius/machine-applications.git
	fi
elif [ $repo == 'va' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='va'
	link="ssh://git@github.com/lnls-fac/va.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'pyjob' ]; then
	if [ ! -d '/home/fac_files/lnls-fac/job_manager' ]; then
		change_directory '/home/fac_files/lnls-fac'
		clone_repo ssh://git@github.com/lnls-fac/job_manager.git
	fi
	change_directory '/home/fac_files/lnls-fac/job_manager/apps'
	sudo make install
	cd ..
	sudo ./install_services.py
	sudo systemctl start pyjob_run.service
else
	echo "Repository $repo not found"
fi
