#!/usr/bin/env python3

"""Return one-line string with Sirius kingdom process variables"""

import sys
import va


_rname_functions = {
    'li':va.pvs.li.get_all_record_names,
    'tb':va.pvs.tb.get_all_record_names,
    'bo':va.pvs.bo.get_all_record_names,
    'ts':va.pvs.ts.get_all_record_names,
    'si':va.pvs.si.get_all_record_names,
}


try:
    kingdom = sys.argv[1].lower()
except:
    print('invalid syntax invocation of ' + sys.argv[0])
    sys.exit(1)

try:
    prefix = sys.argv[2]
except:
    prefix = ''

record_names = _rname_functions[kingdom]()
pvs_list = sorted(list(record_names.keys()))
pvs_string = prefix + ('\n'+prefix).join(pvs_list)
print(pvs_string, end='')
