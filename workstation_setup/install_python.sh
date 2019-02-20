#!/bin/bash

set -e
set -x

function install_python_deps {
	sudo apt-get install -y build-essential 
	sudo apt-get install -y checkinstall
	sudo apt-get install -y libreadline-gplv2-dev
	sudo apt-get install -y libncursesw5-dev
	sudo apt-get install -y libssl-dev
	sudo apt-get install -y libsqlite3-dev 
	sudo apt-get install -y tk-dev
	sudo apt-get install -y libgdbm-dev
	sudo apt-get install -y libc6-dev
	sudo apt-get install -y libbz2-dev 
}


if [[ "$(python-sirius --version)" =~ ^Python\ 3\.6\.[0-9]$ ]]; then
	echo "Python already installed. Passing."
	exit 0
fi

install_python_deps

if [[ "$(python3 --version)" =~ ^Python\ 3\.6\.[0-9]$ ]]; then
	sudo ln -sf /usr/bin/pip3 /usr/local/bin/pip-sirius
	sudo ln -sf /usr/bin/python3.6 /usr/local/bin/python-sirius
	sudo apt-get install -y python-dev python-pip
else
	# Download Python
	if [ ! -f ./Python-3.6.7.tgz ]; then
		wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz
	fi
	tar xzf Python-3.6.7.tgz
	cd Python-3.6.7/
	./configure --enable-shared --with-ensurepip=install
	make -j8
	# make -j8 test
	sudo make altinstall
	# Create sym links
	sudo ln -sf /usr/local/bin/pip3.6 /usr/local/bin/pip-sirius
	sudo ln -sf /usr/local/bin/python3.6 /usr/local/bin/python-sirius
	cd ..
	sudo rm -rf Python-3.6.7.tgz Python-3.6.7
fi

exit 0

