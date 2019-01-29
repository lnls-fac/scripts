#!/bin/bash

apt-get install libffi6 libffi-dev libfreetype6 \
	libfreetype6-dev libpng3 nmap dvipng
pip3 install python-nmap wakeonlan pyepics requests pyqtgraph pandas \
	psutil termcolor sh cairocffi matplotlib scipy jupyter

