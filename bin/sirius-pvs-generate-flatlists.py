#!/usr/bin/env python3

import va
import os
import lnls
import time
import datetime

_max_pv_name_length = 50
_pvs_flatlists_folder = os.path.join(lnls.folder_db, 'pvs_flatlists')
_rname_functions = {
    'li':va.pvs.li.get_all_record_names,
    'tb':va.pvs.tb.get_all_record_names,
    'bo':va.pvs.bo.get_all_record_names,
    'ts':va.pvs.ts.get_all_record_names,
    'si':va.pvs.si.get_all_record_names,
}

def read_flatlist(machine):
    pvs, lines = {}, []
    fname = os.path.join(_pvs_flatlists_folder, 'pvs_flatlist_' + machine.lower() + '.txt')
    if os.path.isfile(fname):
        lines = [line.strip() for line in open(fname, encoding='latin-1')]
        for line in lines:
            if not line or line[0] == '#': continue
            pv, description = line.split(None,1)
            pvs[pv] = description
    return pvs, lines

def get_all_defined_pvs(machine):
    record_names = _rname_functions[machine.lower()]()
    return sorted(list(record_names.keys()))

def insert_new_pv(pv, pv_before, lines):
    text = pv + ' ' * (_max_pv_name_length - len(pv)) + 'DESCRIPTION_IS_MISSING'
    if pv_before is None:
        lines.insert(0, text)
    else:
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith(pv_before):
                lines.insert(i, text)
                break


def set_missing_pv(pv, lines):
    for i in range(len(lines)):
        line = lines[i]
        idx = line.find(pv)
        if idx>=0:
            pv, description = line.split(None,1)
            lines[i] = '# [MISSING] ' + line
            break

def update_pvs_flatlist(machine):

    pvs_prev, lines = read_flatlist(machine)
    pvs_prev_list = sorted(list(pvs_prev.keys()))
    pvs_next = get_all_defined_pvs(machine)

    # inserts new PVs
    for i in range(len(pvs_next)):
        if pvs_next[i] not in pvs_prev_list:
            print('inserting ' + pvs_next[i] + '...')
            if i == 0:
                insert_new_pv(pvs_next[i], None, lines)
            else:
                insert_new_pv(pvs_next[i], pvs_next[i-1], lines)

    # flags old PVs that are no longer defined
    for pv in pvs_prev_list:
        if pv not in pvs_next:
            print('listed ' + pv + ' is missing...')
            set_missing_pv(pv, lines)

    # update timestatmp in file
    tsstr = 'timestamp'
    ts_found = False
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '  (by sirius-pvs-generate-flatlist.py)'
    for i in range(len(lines)):
        line = lines[i]
        idx = len(tsstr) + line.lower().find(tsstr)
        if idx < len(tsstr): continue
        ts_found = True
        line = line[:idx+1] + ' ' + ts
        lines[i] = line
        break
    if not ts_found:
        lines.insert(0, '')
        lines.insert(0, '# timestamp: ' + ts)

    fname = os.path.join(_pvs_flatlists_folder, 'pvs_flatlist_' + machine.lower() + '.txt')
    try:
        f = open(fname, "w")
        for line in lines:
            print(line, file=f)
    except IOError:
        print('could not open file "' + fname + '"')



print('updating LI'); update_pvs_flatlist('li'); print()
print('updating TB'); update_pvs_flatlist('tb'); print()
print('updating BO'); update_pvs_flatlist('bo'); print()
print('updating TS'); update_pvs_flatlist('ts'); print()
print('updating SI'); update_pvs_flatlist('si'); print()
