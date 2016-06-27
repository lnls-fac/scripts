#!/bin/bash

if [ ! -d /var/log/fac-data-gitall ]; then
    mkdir /var/log/fac-data-gitall
    chmod o+rwx /var/log/fac-data-gitall
fi

# Put the name of the user you want to use here:
su -c "fac-data-gitall.py -e" fernando > /var/log/fac-data-gitall/extended_log 2>&1
