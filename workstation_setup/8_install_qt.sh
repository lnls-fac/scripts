#!/bin/bash

# Install Qt (change to 5.12!!! when there is matching pyqt)

# Needs user interaction
qt_rel='5.11'
qt_ver='5.11.3'

qt_folder='/opt/Qt/5.11.3/'
if [ -d $qt_folder ]; then
	echo "Qt folder $qt_folder found. Passing"
	exit 0
fi
# cd ~/Downloads
# wget http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
# chmod +x qt-unified-linux-x64-online.run
# ./qt-unified-linux-x64-online.run --platform-minimal --verbose
if [ ! -f "./qt-opensource-linux-x64-$qt_ver.run" ]; then
	wget "http://download.qt.io/official_releases/qt/$qt_rel/$qt_ver/qt-opensource-linux-x64-$qt_ver.run"
fi
chmod +x "qt-opensource-linux-x64-$qt_ver.run"
sudo "./qt-opensource-linux-x64-$qt_ver.run" --script qt-noninteractive.qs -platform minimal --verbose
# Create designet-qt symlink
sudo ln -sf "/opt/Qt/$qt_ver/gcc_64/bin/designer" /usr/local/bin/designer-qt5
sudo rm -f "./qt-opensource-linux-x64-$qt_ver.run"
exit 0
