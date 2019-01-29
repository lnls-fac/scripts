#!/bin/bash

# Check if git is already installed
! command -v git >/dev/null 2>&1 || { echo >&2 "Git already installed. Aborting."; exit 1; }

apt-get install git

if [ $# -ne 2 ]; then
	git config --global core.editor vim
	git config --global push.default simple

	read -p 'Email: ' email
	read -p 'Name: ' name

	git config --global user.email "$email"
	git config --global user.name "$name"

else
	git config --global core.editor vim
	git config --global push.default simple
	git config --global user.email "$1"
	git config --global user.name "$2"
fi


