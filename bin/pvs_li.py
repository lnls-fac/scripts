#!/usr/bin/env python3

import sys
import sirius
import va

"""Return one-line string with Sirius LI proccess variables"""

try:
    prefix = sys.argv[1]
except:
    prefix = ''

fake_names = va.li_fake_record_names.get_record_names()
record_names = sirius.li.record_names.get_record_names()
pvs_list = list(record_names.keys()) + list(fake_names.keys())
pvs_string = prefix + (' '+prefix).join(pvs_list)
print(pvs_string, end='')
