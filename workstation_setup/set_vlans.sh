#!/bin/bash

con_name="VLAN Rede CON"
if [ "$(nmcli connection show | grep "$con_name")" == "" ]; then
	nmcli connection add type vlan con-name 'VLAN Rede CON' ifname vlan-rede-con dev enp4s0 id 2
fi

con_name="VLAN Rede TIC"
if [ "$(nmcli connection show | grep "$con_name")" == "" ]; then
	nmcli connection add type vlan con-name 'VLAN Rede TIC' ifname vlan-rede-tic dev enp4s0 id 254
fi
