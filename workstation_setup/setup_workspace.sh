#!/bin/bash

# User interaction
sudo ./1_create_users.sh

# Optional args
sudo ./2_install_git.sh

sudo ./3_fac_directories.sh
sudo ./4_install_bashrc.sh
sudo ./5_install_python.sh
sudo ./6_install_epics.sh
sudo -HE ./7_install_python_deps.sh
# User interaction
sudo ./8_intall_qt.sh

sudo ./9_install_sip.sh
sudo ./10_install_pyqt.sh
sudo ./11_install_fac_deps.sh

sudo ./12_install_repository.sh trackcpp
sudo ./12_install_repository.sh control-system-constants
sudo ./12_install_repository.sh dev-packages
sudo ./12_install_repository.sh pydm
sudo ./12_install_repository.sh hla
sudo ./12_install_repository.sh machine-applications
sudo ./12_install_repository.sh pyjob
