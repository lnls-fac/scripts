#!/bin/bash

packages="mathphys lnls fieldmaptrack sirius trackcpp/python_package"

function python_packages {
  local install_type=$1
  for package in ${packages[@]}
  do
    >&2 echo "installing" $package "..."
    cd $FACCODE"/"$package
    sudo ./setup.py install_type -f
  done
}

function trackcpp_package {
  >&2 echo "installing trackcpp..."
  cd $FACCODE"/"trackcpp
  make
  sudo make install
}

if [ $# == 0 ]; then
  trackcpp_package
  python_packages install
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
