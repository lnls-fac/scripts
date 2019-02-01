#!/bin/bash

# Install SIP

sip='sip-4.19.13'

wget "https://sourceforge.net/projects/pyqt/files/sip/$sip/$sip.tar.gz"
tar -xvf $sip.tar.gz
cd $sip
python-sirius configure.py --sip-module=PyQt5.sip --no-tools
make -j32
make install

cd ..
rm -rf "$sip" "$sip.tar.gz"
