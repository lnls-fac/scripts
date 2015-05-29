#!/bin/bash

packages_setup="mathphys lnls fieldmaptrack pyaccel job_manager"
packages_makefile="scripts/bin scripts/etc scripts/experiments scripts/fieldmap_analysis trackcpp trackcpp/python_package"

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
    sudo make $install_type
  done
}

function install_packages_setup {
  local install_type=$1
  for package in ${packages_setup[@]}
  do
    print_installing $package
    cd $FACCODE"/"$package
    sudo ./setup.py $install_type -f
  done
}

function trackcpp_package {
  echo "installing trackcpp..."
  cd $FACCODE"/"trackcpp
  make
  sudo make install
}

if [ $# == 0 ]; then
  install_packages_makefile install
  install_packages_setup install
elif [ $# == 1]; then
  if [ $1 == "install" ]; then
    trackcpp_package
    python_packages install
  elif [ $1 == "develop" ]; then
    trackcpp_package
    python_packages develop
  fi
else
  echo $0": invalid arguments!"
fi
