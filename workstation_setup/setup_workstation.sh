#!/bin/bash

set -e
set -x

function execute {
    echo "Executing $1"
    if "./$1" $2; then
        echo "Finished $1 with sucess."
    else
        echo "$1 failed. Aborting."
        exit 1
    fi
}

# Check write permission
if [ ! -w ./ ]; then
	echo 'You do not have write permission for the current directory. Aborting.'
	exit 1
fi

execute set_vlans.sh
execute debian_mirrors.sh

execute create_groups.sh
# execute create_users.sh
execute directories_permissions.sh

execute install_git.sh

# execute install_bashrc.sh

execute install_python.sh
execute install_epics.sh
execute install_pyepics.sh
execute install_qt.sh
execute install_sip.sh
execute install_pyqt.sh

execute install_fac_deps.sh

execute install_repository.sh mathphys install
execute install_repository.sh sirius-scripts install
execute install_repository.sh control-system-constants install
execute install_repository.sh dev-packages install
execute install_repository.sh pydm install
execute install_repository.sh hla install
execute install_repository.sh machine-applications install
execute install_repository.sh pruserial485 install
execute install_repository.sh sirius-scripts install
execute install_repository.sh pyjob install
execute install_repository.sh cs-studio install