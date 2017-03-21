#!/usr/bin/env python3

import argparse as _argparse
import va as _va
from siriuspy.envars import vaca_prefix as _vaca_prefix


def get_vaca_pv_database():
    area_structures = _va.server.get_area_structures()
    pv_database = _va.server.get_pv_database(area_structures)
    return pv_database


def get_vaca_pvs():
    pv_database = get_vaca_pv_database()
    return list(pv_database.keys())

def run():
    parser = _argparse.ArgumentParser(description="Run git commands for sets of repositories")
    parser.add_argument('--server', help='Which git command to perform on repositories',
                                    default='vaca',
                                    choices=('vaca','sirius'),
                                    required=False)
    args = parser.parse_args()
    option = args.server
    if option == 'vaca':
        pvs = get_vaca_pvs()
        for pv in pvs:
            print(_vaca_prefix + pv)

if __name__ == '__main__':
    run()
