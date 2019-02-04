#!/bin/bash

# Install Epics base

# Check if git is installed
command -v git >/dev/null 2>&1 || { echo >&2 "Git not found. Aborting."; exit 1; }
# Check ssh key
if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
	echo 'No ssh key found. Please create one using ssh-keygen and add it to your github account.'
	exit 1
fi
# Instal epics base
dir=/home/sirius
if [ -d $dir ]; then
	cd $dir
	git clone ssh://git@github.com/lnls-sirius/epics-dev.git
	cd epics-dev/
	git checkout base-3.15
	./run-all.sh -a no -e yes -x no -s yes -i -o -c
	exit 0
else
	echo "$dir not found. Aborting."
	exit 1
fi


