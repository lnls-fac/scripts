#!/bin/bash

# User interaction
./1_create_users.sh

# Optional args
./2_install_git.sh

./3_fac_directories.sh
./4_install_bashrc.sh
./5_install_python.sh
./6_install_epics.sh
./7_install_python_deps.sh
# User interaction
./8_intall_qt.sh

./9_install_sip.sh
./10_install_pyqt.sh
./11_install_fac_deps.sh

# ./12_install_repository.sh