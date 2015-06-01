#!/usr/bin/python3
# EASY-INSTALL-DEV-SCRIPT: 'va==0.6.0-dev','sirius-vaca.py'
__requires__ = 'va==0.6.0-dev'
import sys
from pkg_resources import require
require('va==0.6.0-dev')
del require
__file__ = '/home/fac_files/code/va/scripts/sirius-vaca.py'
if sys.version_info < (3, 0):
    execfile(__file__)
else:
    exec(compile(open(__file__).read(), __file__, 'exec'))
