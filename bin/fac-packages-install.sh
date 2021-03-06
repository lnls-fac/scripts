#!/bin/bash

if [ -z $FACCODE ]; then
  FACCODE=/home/fac_files/code
fi
PYTHON3LIB=/usr/local/lib/python3.4/dist-packages

packages_setup="mathphys lnls fieldmaptrack pyaccel sirius va"
packages_makefile="scripts/bin scripts/etc scripts/experiments trackcpp trackcpp/python_package"

function print_installing {
  COLOR='\033[0;33m'
  NC='\033[0m' # No Color
  printf "\n"
  printf "${COLOR}installing "; printf $1; printf " ... ${NC}\n"
  printf "\n"
}

function install_packages_makefile {
  local install_type=$1
  for package in ${packages_makefile[@]}
  do
    print_installing $package
    cd $FACCODE"/"$package
    make $install_type
  done
}

function install_packages_setup {
  local install_type=$1
  for package in ${packages_setup[@]}
  do
    print_installing $package
    cd $FACCODE"/"$package
    if [ $install_type == "install" ]; then
      ./setup.py $install_type -f
    elif [ $install_type == "develop" ]; then
      ./setup.py $install_type
    elif [ $install_type == "uninstall" ]; then
      cd $PYTHON3LIB
      rm -rf $package*i
    fi
  done
}

if [ $# == 0 ]; then
  install_packages_makefile install
  install_packages_setup install
elif [ $# == 1 ]; then
  if [ $1 == "install" ]; then
    install_packages_makefile install
    install_packages_setup install
  elif [ $1 == "develop" ]; then
    install_packages_makefile develop
    install_packages_setup develop
  elif [ $1 == "uninstall" ]; then
    install_packages_makefile uninstall
    install_packages_setup uninstall
  fi
else
  echo $0": invalid arguments!"
fi
