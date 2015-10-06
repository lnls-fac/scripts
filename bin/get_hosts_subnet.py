#!/usr/bin/env python3

import nmap
import socket
from uuid import getnode as get_mac

STRFORMAT = '{0:18s} {1:6s} {2:15s}'
AVAILABLE_HOSTS = dict(
    {'10.0.7':
        {'00:25:90:E7:58:8B':'lnls350',
         '00:25:90:E7:55:92':'lnls343',
         '08:2E:5F:01:68:3A':'lnls340',
         '3C:D9:2B:6F:33:2C':'lnls138',
         '08:2E:5F:01:67:AE':'lnls119',
         '2C:41:38:8E:EF:A2':'lnls346',
         '08:2E:5F:01:58:67':'lnls116',
         '08:00:27:F8:38:3A':'lnls340-virtual',
         '08:00:27:86:C6:0F':'lnls343-1-virtual',
         '08:00:27:34:7C:12':'lnls343-2-virtual',
         '08:00:27:35:25:D6':'lnls138-virtual',
         '08:00:27:10:29:80':'lnls119-virtual',
         '08:00:27:84:59:65':'lnls116-virtual',
         '08:00:27:CB:3D:D7':'lnls350-1-virtual',
         '08:00:27:13:93:5D':'lnls350-2-virtual',
         '08:00:27:3F:9E:DB':'lnls346-virtual'},
     '10.0.21':
        {'AC:16:2D:34:C8:A5':'fernando-linux',
         'AC:16:2D:34:C8:F3':'ximenes-linux',
         'AC:16:2D:34:BD:C5':'luana-linux',
         '00:1E:C9:21:9C:06':'afonso-linux',
         '08:00:27:95:0D:DE':'lnls155-virtual'},
     '10.0.28':
        {'AC:16:2D:34:6A:43':'liu-linux',
         '3C:D9:2B:70:D2:D8':'lnls82-linux',
         '1C:C1:DE:66:1B:55':'lnls54-linux'}
         })

my_mac = str(hex(get_mac()))[2:]
if len(my_mac) != 12: my_mac = '0'+my_mac
my_mac = ':'.join([my_mac[i:i+2].upper() for i in range(0,len(my_mac),2)])

my_ip  = socket.gethostbyname(socket.gethostname())
if my_ip.startswith('127.0.'):
    my_ip  = socket.gethostbyname_ex(socket.gethostname())[2][1]

my_subnet = '.'.join(my_ip.split('.')[0:3])

hosts_in_my_subnet = AVAILABLE_HOSTS[my_subnet]

nm = nmap.PortScanner()
scan = nm.scan(hosts=my_subnet+'.0/24',arguments='-sP',sudo=True)
result = scan['scan']

hosts_online = {result[x]['addresses']['mac']:x
                for x in result.keys() if not x.startswith(my_ip)}


print(STRFORMAT.format('Hosts', 'State', 'IP'))
for mac, name in hosts_in_my_subnet.items():
    if mac in hosts_online.keys():
        print(STRFORMAT.format(name,'up', hosts_online[mac]))
    else:
        if not mac.startswith(my_mac):
            print(STRFORMAT.format(name,'down',''))
        else:
            print(STRFORMAT.format(name,'up', my_ip))
