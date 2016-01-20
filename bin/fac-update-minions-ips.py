#!/usr/bin/env python3

""" this scripts updates minion IPs in lnls82-linux /etc/hosts file """

import subprocess
import sys

def get_minions_ips():
    """ runs salt command to get list of minions IPs """
    cmd = "sudo salt --out=txt '*' network.ip_addrs interface=eth0"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    minions = {}
    for line in p.stdout.readlines():
        line = str(line)
        line = line.replace(':','').replace('b"','').replace("['","").replace("']\\n","").replace('"','')
        name, ip = line.split()
        minions[ip] = name
    retval = p.wait()
    return minions


def get_hosts_content():
    """ gets content of hosts file """
    with open ("/etc/hosts","r") as myfile:
        hosts_text = myfile.readlines()
    return hosts_text


def update_hosts_content(minions, hosts_contents):
    new_content = [line for line in hosts_contents]
    for ip, name in minions.items():
        found = False
        for line in new_content:
            words = line.split()
            if len(words)>1 and name in words[1]:
                if '127.0' not in words[0]:
                    found = True
                    line = line.replace(words[0],ip)
        if not found:
            print('updated ' + name + " with IP '" + ip + "' (added new line)")
            new_content.append(ip + ' ' + name + '  # by fac-update-minions-ips.py') 
        else:
            print('updated ' + name + " with IP '" + ip + "'")
    return new_content

def save_to_hosts(new_hosts_content):
    with open('/etc/hosts','w') as fp:
        for line in new_hosts_content:
            fp.write(line)

def cmd_update_minions_ips():
    minions = get_minions_ips()
    hosts_content = get_hosts_content()
    new_hosts_content = update_hosts_content(minions, hosts_content)
    save_to_hosts(new_hosts_content)

def cmd_list_minions():
    minions = get_minions_ips()
    for ip, name in minions.items():
        print(name + ' ' + ip)

def cmd_print_help():
    print('Usage: fac-update-minions-ips.py  [--list|--help]')
    print('Updates /etc/hosts with current dynamic IP addresses of salt minions')
    print('')
    print('options:')
    print('  <no argument>      update /etc/hosts and exit')
    print('  -l, --list         list salt minion with respective IPs (does not update hosts file)')
    print('  -h, --help         display this help and exit')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        cmd_update_minions_ips()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['--list', '-l']:
            cmd_list_minions()
        else:
            cmd_print_help()
    else:
        cmd_print_help()
