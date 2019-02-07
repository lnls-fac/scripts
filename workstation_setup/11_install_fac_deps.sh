#!/bin/bash

set -e
set -x

sudo apt-get install -y libffi6
sudo apt-get install -y libffi-dev libfreetype6
sudo apt-get install -y libfreetype6-dev
# sudo apt-get install -y libpng3
sudo apt-get install -y nmap
sudo apt-get install -y dvipng

sudo -HE pip-sirius install python-nmap wakeonlan requests pyqtgraph pandas \
	                    psutil termcolor sh cairocffi matplotlib scipy jupyter

