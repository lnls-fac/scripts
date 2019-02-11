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
		echo "$user:boo500mev" | sudo chpasswd
	fi
done

sudo usermod -aG sirius facs
sudo usermod -aG sirius imas

users=(fernando ximenes guilherme liulin ana alexandre murilo)
for user in ${users[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		sudo adduser $user --ingroup facs --gecos '' --disabled-password
		sudo usermod -aG sudo $user
		sudo usermod -aG sirius $user
		echo "$user:boo500mev" | sudo chpasswd
	fi
done

# add fac users in group ima
users_ima=(fernando ximenes)
for user in ${users_ima[@]}; do
	echo $user
	sudo usermod -aG imas $user
done

exit 0
