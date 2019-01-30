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
	change_directory $1
	clone_repo $3
	change_directory "$1/$2"
	python3.6 setup.py build
	python3.6 setup.py $action
}


if [ $repo == 'MML' ]; then
	echo "$action MML"
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
	apt-get install -y g++ libgsl0-dev swig liblapack-dev
	change_directory '/home/fac_files/lnls-fac'
	clone_repo ssh://git@github.com/lnls-fac/trackcpp.git
	change_directory '/home/fac_files/lnls-fac/trackcpp'
	make -j32 PYTHON=python-sirius PYTHON_VERSION=python-sirius
	make install PYTHON=python-sirius PYTHON_VERSION=python-sirius
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
	change_directory '/home/fac_files/lnls-sirius'
	clone_repo ssh://git@github.com/lnls-sirius/control-system-constants.git
elif [ $repo == 'dev-packages' ]; then
	dir='/home/fac_files/lnls-sirius/'
	repo='dev-packages'
	link="ssh://git@github.com/lnls-sirius/dev-packages.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'pydm' ]; then
	dir='/home/fac_files/lnls-sirius/'
	repo='pydm'
	link="ssh://git@github.com/lnls-sirius/pydm.git"
	clone_and_develop $dir $repo $link
elif [ $repo == 'hla' ]; then
	change_directory '/home/fac_files/lnls-sirius'
	clone_repo ssh://git@github.com/lnls-sirius/hla.git
	change_directory "/home/fac_files/lnls-sirius/hla/pyqt-apps"
	#python-sirius setup.py build
	#python-sirius setup.py $action
	make install-resources
	make develop
elif [ $repo == 'machine-applications' ]; then
	change_directory '/home/fac_files/lnls-sirius'
	clone_repo ssh://git@github.com/lnls-sirius/machine-applications.git
elif [ $repo == 'va' ]; then
	dir='/home/fac_files/lnls-fac/'
	repo='va'
	link="ssh://git@github.com/lnls-fac/va.git"
	clone_and_develop $dir $repo $link
fi

