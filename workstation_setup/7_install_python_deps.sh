#!/bin/bash

# Install Pcaspy and PyEpics

# Run with sudo -HE

set -e
set -x

sudo apt-get install -y python3-pip swig

export EPICS_BASE=/opt/epics/base
export EPICS_HOST_ARCH=linux-x86_64

sudo -HE pip3 install pyepics==3.3.3
sudo -HE pip3 install pcaspy==0.7.2
exit 0
