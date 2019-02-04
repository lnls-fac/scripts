#!/bin/bash

# User interaction
sudo ./1_create_users.sh

# Optional args
sudo ./2_install_git.sh

# sudo ./3_fac_directories.sh
sudo ./4_install_bashrc.sh
sudo ./5_install_python.sh
sudo ./6_install_epics.sh
sudo -HE ./7_install_python_deps.sh
# User interaction
sudo ./8_intall_qt.sh

sudo ./9_install_sip.sh
sudo ./10_install_pyqt.sh
sudo ./11_install_fac_deps.sh

./12_install_repository.sh trackcpp
./12_install_repository.sh control-system-constants
./12_install_repository.sh dev-packages
./12_install_repository.sh pydm
./12_install_repository.sh hla
./12_install_repository.sh machine-applications
./12_install_repository.sh pyjob
