#!/bin/bash

# Install SIP

# Check wether to install SIP
if command -v sip > /dev/null 2>&1; then # Sip is installed
    sip_tar='sip-4.19.13'
    sip_cur=$(sip - V)
    if [ $sip_tar == $sip_cur ]; then # SIP at target version
        exit 0
    fi
fi

# Get SIP source
wget "https://sourceforge.net/projects/pyqt/files/sip/$sip/$sip.tar.gz"
# Install SIP
tar -xvf $sip.tar.gz
cd $sip
python-sirius configure.py --sip-module=PyQt5.sip --no-tools
make -j32
make install
# Remove SIP source
cd ..
rm -rf "$sip" "$sip.tar.gz"
