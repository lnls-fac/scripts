#!/bin/bash

# Install Pcaspy and PyEpics

# Run with sudo -HE

sudo apt-get install -y python3-pip swig
sudo -HE pip3 install pyepics==3.3.3
sudo -HE pip3 install pcaspy==0.7.2
exit 0
