#!/bin/bash

# Install PyQt

pyqt_rel='5.11.3'

apt-get install -y checkinstall libreadline-gplv2-dev libncursesw5-dev \
                   libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
                   libbz2-dev swig liblapack-dev libdbus-1-3 libglu1-mesa-dev

cd ~/Downloads
wget "https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$pyqt_rel/PyQt5_gpl-$pyqt_rel.tar.gz"
tar xzf "PyQt5_gpl-$pyqt_rel.tar.gz"
cd ~/Downloads
cd "PyQt5_gpl-$pyqt_rel"/
mkdir -p "/opt/Qt/$pyqt_rel/gcc_64/plugins/PyQt5"
python3.6 configure.py --"qmake=/opt/Qt/$pyqt_rel/gcc_64/bin/qmake" \
                        --sip-incdir=/usr/include/python3.6m \
                        --"designer-plugindir=/opt/Qt/$pyqt_rel/gcc_64/plugins/designer" \
                        --"qml-plugindir=/opt/Qt/$pyqt_rel/gcc_64/plugins/PyQt5" \
                        --confirm-license \
                        --assume-shared \
			--verbose
make -j32
sudo make install
