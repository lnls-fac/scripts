#!/usr/bin/env bash


function checkout_commits {

  cd $FACCODE/va; ans1=$(git status | grep "nothing to commit");
  cd $FACCODE/sirius; ans2=$(git status | grep "nothing to commit");
  cd $FACROOT/siriusdb; ans3=$(git status | grep "nothing to commit");

  if [ -z "$ans1" -o -z "$ans2" -o -z "$ans3" ]; then
    printf "At least one of the repositories has modifications. bailing out...\n"
  else
    printf "checking va: "; cd $FACCODE/va; git checkout 127d000; sudo python3 ./setup.py develop
    printf "checking sirius: "; cd $FACCODE/sirius; git checkout 6bbfffe; sudo python3 ./setup.py develop
    printf "checking siriusdb: "; cd $FACROOT/siriusdb; git checkout d76088f
  fi

}

function checkout_masters {

  cd $FACCODE/va; ans1=$(git status | grep "nothing to commit");
  cd $FACCODE/sirius; ans2=$(git status | grep "nothing to commit");
  cd $FACROOT/siriusdb; ans3=$(git status | grep "nothing to commit");

  if [ -z "$ans1" -o -z "$ans2" -o -z "$ans3" ]; then
    printf "At least one of the repositories has modifications. bailing out...\n"
  else
    printf "checking va: "; cd $FACCODE/va; git checkout master; sudo python3 ./setup.py develop
    printf "checking sirius: "; cd $FACCODE/sirius; git checkout master; sudo python3 ./setup.py develop
    printf "checking siriusdb: "; cd $FACROOT/siriusdb; git checkout master
  fi

}

if [ "$#" -eq 0 ]; then
  checkout_commits
elif [ "$#" -eq 1 -a "$1" == "commits" ]; then
  checkout_commits
elif [ "$#" -eq 1 -a "$1" == "masters" ]; then
  checkout_masters
else
  printf "Invalid number of arguments!\n"
fi
