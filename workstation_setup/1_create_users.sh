#!/bin/bash

# Create users.

# Needs user interaction
function user_exists {
	id -u $1 >/dev/null 2>&1
	echo $?
}

if [ $(user_exists fac) -eq 0 ]; then
	echo 'fac user already exists'
else
	# echo 'fac user does not exist'
	adduser --system fac
	usermod -aG sudo fac
fi

users=(fernando ximenes guilherme liulin ana alexandre murilo)

for user in ${users[@]}; do
	if [ $(user_exists $user) -eq 0 ]; then
		echo $user' user already exists'
	else
		# echo $user' does not exist'
		adduser $user --ingroup fac
		usermod -aG sudo $user
	fi
done
