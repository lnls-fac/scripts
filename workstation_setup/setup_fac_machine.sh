#!/bin/bash

set -e
set -x

function execute {
    echo "Executing $1"
    if "./$1" $2 $3; then
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

execute create_groups.sh
execute create_users.sh
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

execute check_github_ssh_key.sh

execute install_repository.sh MML develop ssh
execute install_repository.sh trackcpp develop ssh
execute install_repository.sh mathphys develop ssh
execute install_repository.sh fieldmaptrack develop ssh
execute install_repository.sh sirius-scripts install ssh
execute install_repository.sh control-system-constants develop ssh
execute install_repository.sh dev-packages develop ssh
execute install_repository.sh pydm develop ssh
execute install_repository.sh hla develop ssh
execute install_repository.sh machine-applications develop ssh
execute install_repository.sh pruserial485 develop ssh
execute install_repository.sh pyjob develop ssh
execute install_repository.sh cs-studio ssh

execute misc_applications.sh
