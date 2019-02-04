#!/bin/bash

# Check if git is already installed
! command -v git >/dev/null 2>&1 || { echo >&2 "Git already installed. Aborting."; exit 1; }

sudo apt-get install -y git

if [ $# -ne 2 ]; then
	git config --global core.editor vim
	git config --global push.default simple
else
	git config --global core.editor vim
	git config --global push.default simple
	git config --global user.email "$1"
	git config --global user.name "$2"
fi

exit 0

