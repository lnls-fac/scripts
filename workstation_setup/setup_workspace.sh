#!/bin/bash

function execute {
    echo "Executing $1"
    if "./$1" $2; then
        echo "Finished $1 with sucess."
    else
        echo "$1 failed. Aborting."
        exit 1
    fi
}

# User interaction
execute 1_create_users.sh

if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
	echo 'In order to continue please log as a user with a ssh key configured in GitHub. Aborting.'
	exit 1
fi

execute 2_install_git.sh

# sudo ./3_fac_directories.sh
execute 4_install_bashrc.sh
execute 5_install_python.sh
execute 6_install_epics.sh
execute 7_install_python_deps.sh
# User interaction
execute 8_install_qt.sh

execute 9_install_sip.sh
execute 10_install_pyqt.sh
execute 11_install_fac_deps.sh

execute '12_install_repository.sh' 'trackcpp'
execute '12_install_repository.sh' 'mathphys'
execute '12_install_repository.sh' 'control-system-constants'
execute '12_install_repository.sh' 'dev-packages'
execute '12_install_repository.sh' 'pydm'
execute '12_install_repository.sh' 'hla'
execute '12_install_repository.sh' 'machine-applications'
execute '12_install_repository.sh' 'pruserial485'
execute '12_install_repository.sh' 'pyjob'
