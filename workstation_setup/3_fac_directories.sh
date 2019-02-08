#!/bin/bash

# Create fac working directories

# cd /home
# mkdir -p fac_files
# chown -R fac fac_files
# sed -i -e 's/\(remount-ro\)/&,acl/; s/\(defaults\)/&,acl/' /etc/fstab
# mount -oremount /
# mount -oremount /home/ # in case your /home is in a different partition
# chgrp -R fac fac_files
# setfacl -Rdm u::rwx,g:fac:rwx,o::r /home/fac_files
# setfacl -Rm u::rwx,g:fac:rwx,o::r /home/fac_files
# cd /home/fac_files/
# mkdir lnls-fac lnls-sirius lnls-ima

set -e
set -x

# Sirius
dir=/home/sirius
if [ -d $dir ]; then
    sudo setfacl -Rdm u::rwx,g:sirius:rwx,o::r $dir
    sudo setfacl -Rm u::rwx,g:fac:rwx,o::r $dir
else
    echo '/home/sirius does not exist. Aborting.'
    exit 1
fi

users=(fac ima)
for user in ${users[@]}; do
	dir="/home/$user"
	if [ -d $dir ]; then
		sudo setfacl -Rdm u::rwx,u:sirius:rwx,g:$user:rwx,o::r $dir
		sudo setfacl -Rm u::rwx,u:sirius:rwx,g:$user:rwx,o::r $dir
	else
	    echo "/home/$user does not exist. Aborting."
	    exit 1
	fi
done

exit 0
