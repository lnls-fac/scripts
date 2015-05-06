#!/usr/bin/env python3

import sirius

record_names = sirius.si.record_names.get_record_names()
pvs_list = list(record_names.keys())
pvs_string = ' '.join(pvs_list)
print(pvs_string)
