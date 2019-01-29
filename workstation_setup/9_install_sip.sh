#!/bin/bash

# Install SIP

sip='sip-4.19.13'

cd ~/Downloads
wget "https://sourceforge.net/projects/pyqt/files/sip/$sip/$sip.tar.gz"
tar -xvf $sip.tar.gz
cd $sip
python3.6 configure.py
make -j32
make install
