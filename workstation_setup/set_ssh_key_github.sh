#!/bin/bash

echo '\n\nPlease use yours Github credentials.'
read -p "Username:" username
read -s -p "Password:" password

ssh_key=$(cat $HOME/.ssh/id_rsa.pub)
title="$(whoami) on $(hostname)"

curl -u "$username:$password" --data "{\"title\": \"$title\",\"key\":\"$ssh_key\"}" https://api.github.com/user/keys

