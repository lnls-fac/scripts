#!/bin/bash

# Install Qt (change to 5.12!!! when there is matching pyqt)

# Needs user interaction

cd ~/Downloads
wget http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
chmod +x qt-unified-linux-x64-online.run
./qt-unified-linux-x64-online.run --platform-minimal --verbose

# Create designet-qt symlink
ln -sf /opt/Qt/5.11.3/gcc_64/bin/designer /usr/local/bin/designer-qt5
