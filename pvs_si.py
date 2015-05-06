#!/usr/bin/env python3

import sys
import sirius

"""Return one-line string with Sirius SI proccess variables"""

try:
    prefix = sys.argv[1]
except:
    prefix = ''

record_names = sirius.si.record_names.get_record_names()
pvs_list = list(record_names.keys())
pvs_string = prefix + (' '+prefix).join(pvs_list)
print(pvs_string, end='')


