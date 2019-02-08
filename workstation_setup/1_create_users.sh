#!/bin/bash
# Create users.

function user_exists {
	id -u $1 >/dev/null 2>&1
	echo $?
}

groups=(sirius fac ima)
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

usermod -aG sirius fac
usermod -aG sirius ima

users=(fernando ximenes guilherme liulin ana alexandre murilo)
for user in ${users[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		sudo adduser $user --ingroup fac --gecos '' --disabled-password
		sudo usermod -aG sudo $user
		sudo usermod -aG sirius $user
		echo "$user:boo500mev" | sudo chpasswd
	fi
done

exit 0
