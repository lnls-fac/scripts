#!/usr/bin/env bash


function checkout_release_branches {

  cd $FACCODE/va; ans1=$(git status | grep "nothing to commit");
  cd $FACCODE/sirius; ans2=$(git status | grep "nothing to commit");
  cd $FACROOT/siriusdb; ans3=$(git status | grep "nothing to commit");

  if [ -z "$ans1" -o -z "$ans2" -o -z "$ans3" ]; then
    printf "At least one of the repositories has modifications. bailing out...\n"
  else
    printf "<va>\n"; cd $FACCODE/va; git fetch --all; git checkout release-v0.15.1; sudo python3 ./setup.py develop; printf "\n"
    printf "<sirius>\n"; cd $FACCODE/sirius; git fetch --all; git checkout release-v0.11.2; sudo python3 ./setup.py develop; printf "\n"
    printf "<siriusdb>\n"; cd $FACROOT/siriusdb; git fetch --all; git checkout release-v0.0.1; printf "\n"
  fi

}

function checkout_master_branches {

  printf "<va>\n"; cd $FACCODE/va; git checkout master; sudo python3 ./setup.py develop; printf "\n"
  printf "<sirius>\n"; cd $FACCODE/sirius; git checkout master; sudo python3 ./setup.py develop; printf "\n"
  printf "<siriusdb>\n"; cd $FACROOT/siriusdb; git checkout master; printf "\n"

}

function set_envs {
    # descubro o ip da máquina
    IP=$( ifconfig | grep -A 2 eth0 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
    if [ -z "$IP" ]; then
        IP=$( ifconfig | grep -A 2 eth1 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
    fi
    export EPICS_CA_ADDR_LIST=$IP
    export EPICS_CA_AUTO_ADDR_LIST=no
}


function checkout_release_run {

    checkout_release_branches
    set_envs
    sirius-vaca.py

}


  

if [ "$#" -eq 0 ]; then
  checkout_release_run
elif [ "$#" -eq 1 -a "$1" == "releases" ]; then
  checkout_release_branches
elif [ "$#" -eq 1 -a "$1" == "masters" ]; then
  checkout_master_branches
else
  printf "Invalid number of arguments!\n"
fi
