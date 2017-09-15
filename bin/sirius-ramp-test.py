#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-

import math
import time
import sys
from epics import caput
import matplotlib.pyplot as plt
from siriuspy.magnet.util import generate_normalized_ramp

max_current = 10.0  # [A]
ref_current_3gev = max_current/1.05 # [A]
ramp = ref_current_3gev * generate_normalized_ramp()

def ramp_plot():
    plt.plot(ramp)
    plt.show()

def sync_disable():
    caput("AS-Inj:TI-EVG1:STOPSEQ", 1)
    time.sleep(2.0)
    caput("SerialNetwork1:Sync", "Off")

def sync_enable():
    caput("SerialNetwork1:Sync", "On")
    time.sleep(2.0)
    caput("AS-Inj:TI-EVG1:RUNSEQ", 1)

def opmode_set(opmode):
    caput("BO-01U:PS-CH:OpMode-Sel", opmode)
    caput("BO-03U:PS-CH:OpMode-Sel", opmode)

def wfmdata_send():
    sync_disable()
    opmode_set('SlowRef')
    caput("BO-01U:PS-CH:WfmData-SP", ramp)
    caput("BO-03U:PS-CH:WfmData-SP", ramp)
    time.sleep(2)

def test_start():
    sync_disable()
    wfmdata_send()
    opmode_set('RmpWfm')
    sync_enable()

def test_stop():
    sync_disable()

if __name__ == '__main__':
    actions = {'start': test_start,
               'stop': test_stop,
               'plot': ramp_plot}
    if len(sys.argv) != 2 or sys.argv[1] not in actions.keys():
        print('Invalid syntax! Please specify action.')
        print('Valid actions:', list(actions.keys()))
    else:
        actions[sys.argv[1]]()
