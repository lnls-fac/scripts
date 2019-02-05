#!/bin/bash

set -e
set -x

sudo apt-get install -y libffi6 libffi-dev libfreetype6 \
	libfreetype6-dev libpng3 nmap dvipng
sudo -HE pip3 install python-nmap wakeonlan requests pyqtgraph pandas \
	                  psutil termcolor sh cairocffi matplotlib scipy jupyter

