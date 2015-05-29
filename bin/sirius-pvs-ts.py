#!/usr/bin/env python3

import sys
import sirius
import va

"""Return one-line string with Sirius TS proccess variables"""

try:
    prefix = sys.argv[1]
except:
    prefix = ''

fake_names = va.ts_fake_record_names.get_record_names()
record_names = sirius.ts.record_names.get_record_names()
pvs_list = list(record_names.keys()) + list(fake_names.keys())
pvs_string = prefix + (' '+prefix).join(pvs_list)
print(pvs_string, end='')
