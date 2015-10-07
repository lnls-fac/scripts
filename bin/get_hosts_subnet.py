#!/usr/bin/env python3

import nmap
import socket
import optparse
from wakeonlan import wol
from uuid import getnode as get_mac

STRFORMAT = '{0:18s} {1:6s} {2:15s}'
AVAILABLE_HOSTS = dict(
    {'10.0.7':{
         'lnls350':'00:25:90:E7:58:8B',
         'lnls343':'00:25:90:E7:55:92',
         'lnls340':'08:2E:5F:01:68:3A',
         'lnls138':'3C:D9:2B:6F:33:2C',
         'lnls119':'08:2E:5F:01:67:AE',
         'lnls346':'2C:41:38:8E:EF:A2',
         'lnls116':'08:2E:5F:01:58:67',
         'lnls340-virtual':'08:00:27:F8:38:3A',
         'lnls343-1-virtual':'08:00:27:86:C6:0F',
         'lnls343-2-virtual':'08:00:27:34:7C:12',
         'lnls138-virtual':'08:00:27:35:25:D6',
         'lnls119-virtual':'08:00:27:10:29:80',
         'lnls116-virtual':'08:00:27:84:59:65',
         'lnls350-1-virtual':'08:00:27:CB:3D:D7',
         'lnls350-2-virtual':'08:00:27:13:93:5D',
         'lnls346-virtual':'08:00:27:3F:9E:DB',
     },'10.0.21':{
         'lnls210-linux':'AC:16:2D:34:C8:A5',
         'lnls208-linux':'AC:16:2D:34:C8:F3',
         'lnls212-linux':'AC:16:2D:34:BD:C5',
         'fac8-linux':'00:1E:C9:21:9C:06',
         'lnls155-virtual':'08:00:27:95:0D:DE',
     },'10.0.28':{
         'lnls209-linux':'AC:16:2D:34:6A:43',
         'lnls82-linux':'3C:D9:2B:70:D2:D8',
         'lnls54-linux':'1C:C1:DE:66:1B:55'
         }})

my_mac = str(hex(get_mac()))[2:]
my_mac = (12-len(my_mac))*'0' + my_mac
my_mac = ':'.join([my_mac[i:i+2].upper() for i in range(0,len(my_mac),2)])

my_name   = socket.gethostname()
my_ip     = socket.gethostbyname_ex(my_name)[-1][-1]
my_subnet = '.'.join(my_ip.split('.')[0:3])

hosts_in_my_subnet = AVAILABLE_HOSTS[my_subnet]


def check_hosts():
    nm = nmap.PortScanner()
    scan = nm.scan(hosts=my_subnet+'.0/24',arguments='-sP',sudo=True)
    result = scan['scan']

    hosts_online = {result[x]['addresses'].get('mac',my_mac):x for x in result.keys()}

    print(STRFORMAT.format('Hosts', 'State', 'IP'))
    for name, mac in hosts_in_my_subnet.items():
        if mac in hosts_online:
            print(STRFORMAT.format(name,'up', hosts_online[mac].replace(':','.')))
        else:
            print(STRFORMAT.format(name,'down',''))

def wake_hosts(hosts):
    print('Sending wake signal for hosts:')
    print(STRFORMAT.format('Hosts', '', 'SIGNAL'))
    wrong_hosts = []
    for host in hosts:
        if host in hosts_in_my_subnet:
            wol.send_magic_packet(hosts_in_my_subnet[host])
            print(STRFORMAT.format(host, '', 'sent'))
        else:
            wrong_hosts.append(host)
    if wrong_hosts:
        print('\nThe following hosts are not in the same subnet as this computer or do not exist:\n'+
              ' '.join(wrong_hosts) + '\n'
              'This program requires you to be logged in the same subnet as the\n'+
              'computer you want to send the wake signal.\n')


if __name__ == '__main__':

    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    parser.add_option('-w','--wake',dest='wake',type='str',
                      help="wake up hosts. [format: host1,host2,...,hostN]")
    parser.add_option('-c','--check',dest='check',action='store_true',
                      help="check which hosts are online.", default=False)
    (opts, _) = parser.parse_args()

    if opts.check:
        check_hosts()
    elif opts.wake:
        wake_hosts(opts.wake.split(','))
