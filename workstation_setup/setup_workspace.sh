#!/bin/bash -i

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

execute create_users.sh
execute install_git.sh
execute fac_directories.sh
execute install_bashrc.sh
execute install_python.sh
execute install_epics.sh
execute install_python_deps.sh
execute install_qt.sh
execute install_sip.sh
execute install_pyqt.sh
execute install_fac_deps.sh
execute 'install_repository.sh' 'MML'
execute 'install_repository.sh' 'trackcpp'
execute 'install_repository.sh' 'mathphys'
execute 'install_repository.sh' 'fieldmaptrack'
execute 'install_repository.sh' 'control-system-constants'
execute 'install_repository.sh' 'dev-packages'
execute 'install_repository.sh' 'pydm'
execute 'install_repository.sh' 'hla'
execute 'install_repository.sh' 'machine-applications'
execute 'install_repository.sh' 'pruserial485'
execute 'install_repository.sh' 'sirius-scripts'
execute 'install_repository.sh' 'pyjob'
execute 'install_repository.sh' 'cs-studio'

