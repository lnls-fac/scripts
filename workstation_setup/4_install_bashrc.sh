#!/bin/bash

# Clone scripts repository and intall sirius-bashrc

# Check if git is installed
command -v git >/dev/null 2>&1 || { echo >&2 "Git not found. Aborting."; exit 1; }
# Check ssh key
if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
	echo 'No ssh key found. Please create one using ssh-keygen and add it to your github account.'
	exit 1
fi

# dir=/home/fac_files/lnls-fac
dir=/home/fac
if [ -d $dir ]; then
	cd $dir
	git clone ssh://git@github.com/lnls-fac/scripts
	apt-get install -y make
	cd scripts
	make develop
	sed -i -e '5i #Sirius bashrc' ~/.bashrc
	sed -i -e '6i SIRIUSBASHRC=/usr/local/etc/bashrc-sirius' ~/.bashrc
	sed -i -e '7i if [ -f "$SIRIUSBASHRC" ] ; then' ~/.bashrc
	sed -i -e '8i \ \ \ \ source "$SIRIUSBASHRC"' ~/.bashrc
	sed -i -e '9i fi\n' ~/.bashrc

	echo 'sirius-bashrc install please source run the following command.'
	echo 'source ~/.bashrc'
	exit 0
else
	echo "$dir not found please run fac_directories.sh. Aborting."
	exit 1
fi

