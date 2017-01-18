# This scripts configure the environment so that any EPICS communication is tunneled to a 
# specific IP that may be passed as an argument.


if [ "$0" != "bash" ]; then
    echo "this script should be sourced instead of executed!"
    exit
fi

IP=$1
if [ -z $IP ]; then
    # descubro o ip da máquina
    IP=$( ifconfig | grep -A 2 eth0 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
    if [ -z "$IP" ]; then
        IP=$( ifconfig | grep -A 2 eth1 | grep "inet add" | cut --delimiter=":" -f 2 | cut --delimiter="B" -f 1 )
    fi
fi

export EPICS_CA_ADDR_LIST=$IP
export EPICS_CA_AUTO_ADDR_LIST=no
