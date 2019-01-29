#!/bin/bash

# Create fac working directories

cd /home
mkdir -p fac_files
chown -R fac fac_files
sed -i -e 's/\(remount-ro\)/&,acl/; s/\(defaults\)/&,acl/' /etc/fstab
mount -oremount /
mount -oremount /home/ # in case your /home is in a different partition
chgrp -R fac fac_files
setfacl -Rdm u::rwx,g:fac:rwx,o::r /home/fac_files
setfacl -Rm u::rwx,g:fac:rwx,o::r /home/fac_files
cd /home/fac_files/
mkdir lnls-fac lnls-sirius lnls-ima
