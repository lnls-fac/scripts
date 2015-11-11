#!/usr/bin/env python3

import epics as _epics
import sirius as _sirius
import numpy as _numpy

_PREFIX = 'VA-'

def _get_machine_pvs(machine):
    pv_dict = {'LI':pvs_li,
               'TB':pvs_tb,
               'BO':pvs_bo,
               'TS':pvs_ts,
               'SI':pvs_si}
    return pv_dict[machine]

def _getpv(pv_name):
    return _epics.caget(pv_name)

def _setpv(pv_name, value):
    #v1 = epics.caget(pv_name)
    _epics.caput(pv_name, value, wait=True)
    #v2 = epics.caget(pv_name)
    #print(pv_name, v1, v2)

def _get_pvnames(machine, error_type, fam_type):
    if machine == 'LI':
        li = _sirius.li.create_accelerator()
        rnames = _sirius.li.record_names.get_element_names(accelerator=li, element = fam_type, prefix = _PREFIX+'LIFK-'+error_type+'-')
    elif machine == 'TB':
        tb = _sirius.tb.create_accelerator()
        rnames = _sirius.tb.record_names.get_element_names(accelerator=tb, element = fam_type, prefix = _PREFIX+'TBFK-'+error_type+'-')
    elif machine == 'BO':
        bo = _sirius.bo.create_accelerator()
        rnames = _sirius.bo.record_names.get_element_names(accelerator=bo, element = fam_type, prefix = _PREFIX+'BOFK-'+error_type+'-')
    elif machine == 'TS':
        ts = _sirius.ts.create_accelerator()
        rnames = _sirius.ts.record_names.get_element_names(accelerator=ts, element = fam_type, prefix = _PREFIX+'TSFFK-'+error_type+'-')
    elif machine == 'SI':
        si = _sirius.si.create_accelerator()
        rnames = _sirius.si.record_names.get_element_names(accelerator=si, element = fam_type, prefix = _PREFIX+'SIFK-'+error_type+'-')
    else:
        rnames = []
    return sorted(list(rnames.keys()))

def get_pvnames_errorx_dipoles(machine):
    return _get_pvnames(machine, 'ERRORX', 'bend')
def get_pvnames_errory_dipoles(machine):
    return _get_pvnames(machine, 'ERRORY', 'bend')
def get_pvnames_errorr_dipoles(machine):
    return _get_pvnames(machine, 'ERRORR', 'bend')
def get_pvnames_errorx_quadrupoles(machine):
    return _get_pvnames(machine, 'ERRORX', 'quad')
def get_pvnames_errory_quadrupoles(machine):
    return _get_pvnames(machine, 'ERRORY', 'quad')
def get_pvnames_errorr_quadrupoles(machine):
    return _get_pvnames(machine, 'ERRORR', 'quad')

def get_values(pvnames):
    values = []
    for pv_name in pvnames:
        values.append(_getpv(pv_name))
    return values

def set_values(pvnames, values):
    for pv_name, value in zip(pvnames, values):
        print(pv_name, value)
        _setpv(pv_name, value)

def generate_random(std, size=1, avg=0.0):
    if std == 0:
        return [0 for i in range(size)]
    else:
        return _numpy.random.normal(loc=avg, scale=std, size=size)

def generate_random_errorx_dipoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errorx_dipoles(machine)
    values = generate_random(std, len(pvnames), avg)
    _dict = {}
    for pv_name, value in zip(pvnames, values):
        _dict[pv_name] = value
    return _dict

def set_random_errorx_dipoles(machine, std, avg=0.0):
    d = generate_random_errorx_dipoles(machine, std, avg)
    set_values(d.keys(), d.values())

def set_random_errory_dipoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errory_dipoles(machine)
    values = generate_random(std, len(pvnames), avg)
    set_values(pvnames, values)
def set_random_errorr_dipoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errorr_dipoles(machine)
    values = generate_random(std, len(pvnames), avg)
    set_values(pvnames, values)

def set_random_errorx_quadrupoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errorx_quadrupoles(machine)
    values = generate_random(std, len(pvnames), avg)
    set_values(pvnames, values)
def set_random_errory_quadrupoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errory_quadrupoles(machine)
    values = generate_random(std, len(pvnames), avg)
    set_values(pvnames, values)
def set_random_errorr_quadrupoles(machine, std, avg=0.0):
    pvnames = get_pvnames_errorr_quadrupoles(machine)
    values = generate_random(std, len(pvnames), avg)
    set_values(pvnames, values)

set_random_errorx_dipoles('SI', std=0.2*40e-6, avg=0.0)
set_random_errorx_quadrupoles('SI', std=0.2*10e-6, avg=0.0)

#set_random_errorx_dipoles('TB', std=800e-6, avg=0.0)
#set_random_errorx_quadrupoles('TB', std=600e-6, avg=0.0)


#d = generate_random_errorx_dipoles('SI', std=10e-6, avg=0.0)
#print(d)

# set_random_errorx_dipoles('SI', std=10e-6, avg=0.0)
# set_random_errory_dipoles('SI', std=10e-6, avg=0.0)
# set_random_errorx_quadrupoles('SI', std=10e-6, avg=0.0)
# set_random_errory_quadrupoles('SI', std=10e-6, avg=0.0)

#_getpv('XVA-SIFK-ERRORX-QFB-16M1')
#_setpv('XVA-SIFK-ERRORX-QFB-16M1', 0)

_epics.ca.finalize_libca()
