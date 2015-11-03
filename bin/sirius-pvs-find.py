#!/usr/bin/env python3

"""Finds pvs"""

import sys
import va
import re

try:
    regexp = sys.argv[1]
except:
    regexp = '.+'
p = re.compile(regexp)


rnames = {}
rnames.update(va.pvs.li.get_all_record_names())
rnames.update(va.pvs.tb.get_all_record_names())
rnames.update(va.pvs.bo.get_all_record_names())
rnames.update(va.pvs.ts.get_all_record_names())
rnames.update(va.pvs.si.get_all_record_names())
pvs = list(rnames.keys())
for pv in pvs:
    if p.match(pv):
        print(pv)
