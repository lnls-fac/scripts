#!/usr/bin/env python-sirius

"""Test lattice models.

This script is used to generate tracking data from pyaccel lattice models
in ordre for AT comparisons.

(see Matlab 'lnls_compare_at_pyaccel.m')

"""

import pymodels
import pyaccel
import sys

def run_test_si():

    f = open('si-linepass.txt', 'w')
    p0 = [0.001, 0, 0.0002, 0, 0.0003, 0.0]
    print('si initial condition: ', p0)
    sys.stdout = f
    latt = pymodels.si.create_accelerator()
    girders = pyaccel.lattice.find_indices(latt, attribute_name='fam_name',
                                           value='girder')
    non_girders = list(set(range(len(latt))) - set(girders))
    latt = latt[non_girders]
    r = pyaccel.tracking.line_pass(latt, p0, indices='open')
    traj = r[0]
    for i in range(traj.shape[1]):
        t = traj[:,i]; print('{0:+.17e} {1:+.17e} {2:+.17e} {3:+.17e} {4:+.17e} {5:+.17e}'.format(t[0],t[1],t[2],t[3],t[4],t[5]))
    f.close()

def run_test_ts():
    f = open('ts-linepass.txt', 'w')
    p0 = [0.001, 0, 0.0002, 0, 0.0003, 0.0]
    print('ts initial condition: ', p0)
    sys.stdout = f
    latt = pymodels.ts.create_accelerator()
    girders = pyaccel.lattice.find_indices(latt, attribute_name='fam_name', value='girder')
    non_girders = list(set(range(len(latt))) - set(girders))
    latt, twiss0 = latt[non_girders]
    r = pyaccel.tracking.line_pass(latt, p0, indices='open')
    traj = r[0]
    for i in range(traj.shape[1]):
        t = traj[:,i]; print('{0:+.17e} {1:+.17e} {2:+.17e} {3:+.17e} {4:+.17e} {5:+.17e}'.format(t[0],t[1],t[2],t[3],t[4],t[5]))
    f.close()

def run_test_bo():
    f = open('bo-linepass.txt', 'w')
    p0 = [0.001, 0, 0.0002, 0, 0.0003, 0.0]
    print('bo initial condition: ', p0)
    sys.stdout = f
    latt = pymodels.bo.create_accelerator()
    girders = pyaccel.lattice.find_indices(latt, attribute_name='fam_name', value='girder')
    non_girders = list(set(range(len(latt))) - set(girders))
    latt = latt[non_girders]
    r = pyaccel.tracking.line_pass(latt, p0, indices='open')
    traj = r[0]
    for i in range(traj.shape[1]):
        t = traj[:,i]; print('{0:+.17e} {1:+.17e} {2:+.17e} {3:+.17e} {4:+.17e} {5:+.17e}'.format(t[0],t[1],t[2],t[3],t[4],t[5]))
    f.close()

def run_test_tb():
    f = open('tb-linepass.txt', 'w')
    p0 = [0.001, 0, 0.0002, 0, 0.0003, 0.0]
    print('tb initial condition: ', p0)
    sys.stdout = f
    latt, twiss0 = pymodels.tb.create_accelerator()
    girders = pyaccel.lattice.find_indices(latt, attribute_name='fam_name', value='girder')
    non_girders = list(set(range(len(latt))) - set(girders))
    latt = latt[non_girders]
    r = pyaccel.tracking.line_pass(latt, p0, indices='open')
    traj = r[0]
    for i in range(traj.shape[1]):
        t = traj[:,i]; print('{0:+.17e} {1:+.17e} {2:+.17e} {3:+.17e} {4:+.17e} {5:+.17e}'.format(t[0],t[1],t[2],t[3],t[4],t[5]))
    f.close()

if len(sys.argv) < 2 or sys.argv[1] == 'si':
    run_test_si()
elif sys.argv[1] == 'ts':
    run_test_ts()
elif sys.argv[1] == 'bo':
    run_test_bo()
elif sys.argv[1] == 'tb':
    run_test_tb()
elif sys.argv[1] == 'li':
    run_test_li()
