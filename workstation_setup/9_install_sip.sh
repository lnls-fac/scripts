#!/bin/bash

set -e
set -x

# Install SIP
sip='sip-4.19.13'
# Check wether to install SIP
if command -v sip > /dev/null 2>&1; then # Sip is installed
    sip_tar="4.19.13"
    sip_cur=$(sip -V)
    if [ $sip_tar == $sip_cur ]; then # SIP at target version
	echo "SIP already at target version $sip_tar. Passing."
        exit 0
    fi
fi

# Get SIP source
wget "https://sourceforge.net/projects/pyqt/files/sip/$sip/$sip.tar.gz"
# Install SIP
tar -xvf $sip.tar.gz
cd $sip
python-sirius configure.py --sip-module=PyQt5.sip
make -j8
sudo make install
# Remove SIP source
cd ..
sudo rm -rf "$sip" "$sip.tar.gz"
exit 0
