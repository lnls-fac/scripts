#!/bin/bash

# Create users.

# Needs user interaction
function user_exists {
	id -u $1 >/dev/null 2>&1
	echo $?
}
# # Add user/group fac
# if [ $(user_exists fac) -eq 0 ]; then
# 	echo 'fac user already exists'
# else
# 	adduser fac --gecos
# 	usermod -aG sudo fac
# fi
# # Add user/group sirius
# if [ $(user_exists fac) -eq 0 ]; then
# 	echo 'sirius user already exists'
# else
# 	adduser sirius --gecos '' --disabled-password
# 	usermod -aG sudo sirius
# 	echo "sirius:boo500mev" | sudo chpasswd
# fi

groups=(sirius fac)
for user in ${groups[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		adduser $user --gecos '' --disabled-password
		usermod -aG sudo $user
		echo "$user:boo500mev" | sudo chpasswd
	fi
done

users=(fernando ximenes guilherme liulin ana alexandre murilo)
for user in ${users[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		adduser $user --ingroup fac --gecos '' --disabled-password
		usermod -aG sudo $user
		echo "$user:boo500mev" | sudo chpasswd
	fi
done
