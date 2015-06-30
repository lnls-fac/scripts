#!/usr/bin/env python3

import sys
import sirius
import va

"""Return one-line string with Sirius TI proccess variables"""

try:
    prefix = sys.argv[1]
except:
    prefix = ''

fake_names = va.fake_rnames_ti.get_record_names()
record_names = sirius.ti.record_names.get_record_names()
pvs_list = list(record_names.keys()) + list(fake_names.keys())
pvs_string = prefix + (' '+prefix).join(pvs_list)
print(pvs_string, end='')
