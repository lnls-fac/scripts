#!/bin/bash

# Install Pcaspy and PyEpics

# Run with sudo -HE

apt-get install -y python3-pip swig
pip3 install pyepics==3.3.3
pip3 install pcaspy==0.7.2

