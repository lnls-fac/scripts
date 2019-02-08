#!/bin/bash

# Install PyQt

set -e
set -x

pyqt_rel='5.11.3'

if [ "$(pip-sirius freeze | grep PyQt5==)" == "PyQt5==$pyqt_rel" ]; then
	echo "PyQt5-$pyqt_rel already installed. Passing."
	exit 0
fi


sudo apt-get install -y checkinstall libreadline-gplv2-dev libncursesw5-dev \
                        libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
                        libbz2-dev swig liblapack-dev libdbus-1-3 libglu1-mesa-dev

# cd ~/Downloads
wget "https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$pyqt_rel/PyQt5_gpl-$pyqt_rel.tar.gz"
tar xzf "PyQt5_gpl-$pyqt_rel.tar.gz"
# cd ~/Downloads
cd "PyQt5_gpl-$pyqt_rel"/
if [ ! d "/opt/Qt/$pyqt_rel/gcc_64/plugins/PyQt5"]; then
	mkdir "/opt/Qt/$pyqt_rel/gcc_64/plugins/PyQt5"
fi

# Check python3.6m path
if [ -d '/usr/include/python3.6m' ]; then
	python_m='/usr/include/python3.6m'
elif [ -d '/usr/local/include/python3.6m' ]; then
	python_m='/usr/local/include/python3.6m'
else
	echo 'Python3.6m not found. Aborting.'
	exit 1
fi
python-sirius configure.py --"qmake=/opt/Qt/$pyqt_rel/gcc_64/bin/qmake" \
                        --sip-incdir="$python_m" \
                        --"designer-plugindir=/opt/Qt/$pyqt_rel/gcc_64/plugins/designer" \
                        --"qml-plugindir=/opt/Qt/$pyqt_rel/gcc_64/plugins/PyQt5" \
                        --confirm-license \
                        --assume-shared \
			--verbose

make -j8
sudo make install

cd ..
sudo rm -rf "PyQt5_gpl-$pyqt_rel.tar.gz" "PyQt5_gpl-$pyqt_rel"

