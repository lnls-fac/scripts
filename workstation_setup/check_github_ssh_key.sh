#!/bin/bash

# Check ssh key and prompt user for action
if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
	echo 'In order to continue you need an ssh-key configured to yout GitHub account.'
	read -p "Copy from existing host[y/N]:" answer
	if [ $answer == 'y' ] ; then
		echo '\n\nEnter host information'
		read -p "User:" user
		read -p "Host:" host
		scp -r $user@$host:/home/$user/.ssh /home/$(whoami)/
	else
		read -p "Create one[y/N]:" answer
		if [ $answer == 'y' ] ; then
			ssh-keygen
			./set_ssh_key_github.sh
		fi
	fi
fi
# Check ssh key
if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
	echo 'No SSH key found. Aborting.'
	exit 1
fi
