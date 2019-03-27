#!/usr/bin/env python3

import os
import time
import epics
import signal
import subprocess
import multiprocessing

server_timeout = 1
wait_timeout = 100

def set_stop_event(signum, frame):
    global stop_event
    stop_event.set()

def wait_server_initialization():
    global stop_event
    server_found = False
    pv = epics.pv.PV('VA-SIDI-CURRENT')
    print('\nWaiting VA Server initialisation...')
    while not server_found and not stop_event.is_set():
        time.sleep(server_timeout)
        pv_value = pv.get()
        if pv_value != None:
            pv.disconnect()
            server_found = True

global stop_event
stop_event = multiprocessing.Event()
signal.signal(signal.SIGINT, set_stop_event)

# Start virtual acelerator server
command = 'sirius-vaca.py 2>&1 > vaca-log.txt &'
server_process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
wait_server_initialization()
print('VA Server initiated!')

print('\nLoading default machine state...')
load_state_process = subprocess.Popen('sirius-load-state.py', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
load_state_process.communicate()[0]
print('Load state done!')

# Start virtual IOCs
print('\nStarting VIOCS')
viocs_start = subprocess.Popen('sirius-viocs start 2>&1 > viocs-log.txt &', shell=True)

while not stop_event.is_set():
    time.sleep(wait_timeout)

# kill all process
print('\nStoping VA Server and VIOCs')
os.killpg(os.getpgid(server_process.pid), signal.SIGINT)
try:
    os.killpg(os.getpgid(load_state_process.pid), signal.SIGKILL)
except:
    pass
viocs_stop = subprocess.Popen('sirius-viocs stop 2>&1 > viocs-log.txt &', shell=True)
