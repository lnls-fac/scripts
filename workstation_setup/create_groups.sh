#!/bin/bash
# Create users and set permission.

function user_exists {
	id -u $1 >/dev/null 2>&1
	echo $?
}

groups=(sirius facs imas)
for user in ${groups[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		if ! sudo adduser $user --gecos '' --disabled-password; then
			sudo adduser $user --ingroup $user --gecos '' --disabled-password
		fi 
		sudo usermod -aG sudo $user
		echo "$user:sirius3gev" | sudo chpasswd
	fi
done
sudo usermod -aG sirius facs
sudo usermod -aG sirius imas

exit 0
