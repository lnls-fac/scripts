#!/bin/bash

printf "all files are owned by group fac...\n"
sudo chown -R :fac $FACROOT

printf "owner and fac users can write all files...\n"
sudo chmod -R ug+w $FACROOT

printf "everyone can read all files...\n"
sudo chmod -R a+r $FACROOT

printf "everyone can execute directory files...\n"
sudo find $FACROOT -type d -exec chmod a+x {} \;

printf "facl attributes: fac users can read and write all files...\n"
sudo setfacl -d -m group:fac:rw $FACROOT





