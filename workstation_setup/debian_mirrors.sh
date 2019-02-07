#!/bin/bash

source='/etc/apt/sources.list'

function append_to_source {
	echo $1 | sudo tee -a $source
}

sudo rm $source
sudo touch $source
append_to_source 'deb http://deb.debian.org/debian stretch main contrib non-free'
append_to_source 'deb http://deb.debian.org/debian stretch-updates main contrib non-free'
append_to_source 'deb http://deb.debian.org/debian-security stretch/updates main contrib non-free'

sudo apt-get update
sudo apt-get -y install nvidia-driver

echo 'Please reboot.'
exit 0
