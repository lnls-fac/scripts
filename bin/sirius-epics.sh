# This scripts configure the environment so that any EPICS communication is tunneled to a 
# specific IP that may be passed as an argument.


if [ "$0" != "bash" ]; then
    echo "this script should be sourced insteaf of executed!"
    exit
fi

IP=$1
if [ -z $IP ]; then IP="10.0.7.51"; fi

export EPICS_CA_ADDR_LIST=$IP
export EPICS_CA_AUTO_ADDR_LIST=no
