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

function create_repo_dir {
	if [ ! -d $1/repos ]; then
		mkdir $1/repos
		chown -R $2:$2 $1/repos
	fi
}

# Sirius
dir=/home/sirius
if [ -d $dir ]; then
    sudo setfacl -Rdm u::rwx,g::rwx,g:sirius:rwx,o::rx $dir
    sudo setfacl -Rm u::rwx,g::rwx,g:facs:rwx,o::rx $dir
	create_repo_dir $dir sirius
else
    echo '/home/sirius does not exist. Aborting.'
    exit 1
fi

users=(facs imas)
for user in ${users[@]}; do
	dir="/home/$user"
	if [ -d $dir ]; then
		sudo setfacl -Rdm u::rwx,u:sirius:rwx,g::rwx,g:$user:rwx,o::rx $dir
		sudo setfacl -Rm u::rwx,u:sirius:rwx,g::rwx,g:$user:rwx,o::rx $dir
		create_repo_dir $dir $user
	else
	    echo "/home/$user does not exist. Aborting."
	    exit 1
	fi
done

exit 0
