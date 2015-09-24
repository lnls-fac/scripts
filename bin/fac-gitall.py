#!/usr/bin/env python3

import sys
import os
import lnls
#import git
from termcolor import colored
import subprocess

git_functions = ('pull','push','status','diff','clone')



def run_git_clone():

    if not os.path.exists(lnls.folder_code):
        print('fac-gitall.py: please create ' + lnls.folder_code + ' folder with correct permissions first!')
        return

    all_repos = ('apsuite',
                 'collective_effects',
                 'fieldmaptrack',
                 'job_manager',
                 'lnls',
                 'mathphys',
                 'MatlabMiddleLayer',
                 'pyaccel',
                 'scripts',
                 'sirius',
                 'sirius_wiki',
                 'tools',
                 'trackcpp',
                 'tracy_sirius',
                 'va',
                 'magfield',
                 )

    for repo in all_repos:
        cmd = 'git clone ssh://git@github.com/lnls-fac/' + repo + '.git'
        os.system(cmd)

def run_git(func):

    if func == 'clone': return run_git_clone()

    fnames = os.listdir(lnls.folder_code)
    for fname in fnames:
        repo_folder = os.path.join(lnls.folder_code, fname)
        if not os.path.exists(os.path.join(repo_folder,'.git')): continue
        print('processing ' + func + colored(' <'+fname+'>','yellow')+'...')
        cmd = 'cd ' + repo_folder + '; git ' + func
        text = subprocess.call([cmd], shell=True, stdout=sys.stdout)
        print('...ok')
        print()


if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] not in git_functions:
        print('usage: fac-gitall.py [' + '|'.join(git_functions) + ']')
    else:
        print()
        run_git(sys.argv[1])
