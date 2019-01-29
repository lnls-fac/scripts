#/bin/bash

# Create users.

# Needs user interaction

user_exists=$(id -u 'fac' >/dev/null 2>&1; echo $?)

if [ $user_exists -eq 0 ]; then
	echo 'fac user already exists'
else
	adduser --system fac
	usermod -aG sudo fac
fi

users=(fernando ximenes guilherme liulin ana alexandre murilo)

for user in $users; do
	adduser $user --ingroup fac
	usermod -aG sudo $user
done
