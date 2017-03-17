#!/usr/bin/env python3

import os
import siriuspy
import argparse
import signal
import sys
import subprocess


def stop_now(signum, frame):
    print(' - SIGINT received.')
    sys.exit(1)

def run_git_clone(args):

    def get_all(args):
        repos = {}
        for org, folder in siriuspy.envars.org_folders.items():
            repos[org] = []
            if not os.path.exists(folder):
                print('sirius-lnls-gitall.py: please create ' + folder + ' folder with correct permissions first!')
                continue
            for repo in siriuspy.envars.repo_names[org]:
                path = os.path.join(folder,repo)
                if os.path.exists(path):
                    #print('skipping: folder {0:s} already exists.'.format(path))
                    pass
                else:
                    #print('including: folder {0:s}.'.format(path))
                    repos[org].append(repo)
        return repos

    def get_repos(args):
        repos = {}
        if not args:
            return get_all(args)
        else:
            for arg in args:
                found = False
                if arg.lower() == 'all':
                    return get_all(args)
                else:
                    for org, folder in siriuspy.envars.org_folders.items():
                        repos[org] = []
                        if arg.lower() == org:
                            found = True
                            for repo in siriuspy.envars.repo_names[org]:
                                path = os.path.join(folder,repo)
                                if os.path.exists(path):
                                    print('skipping: folder {0:s} already exists.'.format(path))
                                else:
                                    print('including: folder {0:s}.'.format(path))
                                    repos[org].append(repo)
                        else:
                            for repo in siriuspy.envars.repo_names[org]:
                                if arg.lower() == repo:
                                    found = True
                                    path = os.path.join(folder,repo)
                                    if os.path.exists(path):
                                        pass
                                    else:
                                        repos[org].append(repo)
                if not found:
                    print('invalid: "' + repo_sel + '"!')
        return repos

    repos = get_repos(args)
    for org, repo_list in repos.items():
        for repo in repo_list:
            path = os.path.join(siriuspy.envars.org_folders[org], repo)
            cmd = 'cd ' + siriuspy.envars.org_folders[org] + '; git clone git@github.com:' + org + '/' + repo
            print(cmd)
            os.system(cmd)
            print('')


def run_git_cmd(cmd,args):

    def get_all(args):
        repos = {}
        for org, folder in siriuspy.envars.org_folders.items():
            repos[org] = []
            if not os.path.exists(folder):
                print('sirius-lnls-gitall.py: please create ' + folder + ' folder with correct permissions first!')
                continue
            for repo in siriuspy.envars.repo_names[org]:
                path = os.path.join(folder,repo)
                if os.path.exists(path):
                    repos[org].append(repo)
                else:
                    pass
        return repos

    def get_repos(args):
        repos = {}
        if not args:
            return get_all(args)
        else:
            for arg in args:
                found = False
                if arg.lower() == 'all':
                    return get_all(args)
                else:
                    for org, folder in siriuspy.envars.org_folders.items():
                        repos[org] = []
                        if arg.lower() == org:
                            found = True
                            for repo in siriuspy.envars.repo_names[org]:
                                path = os.path.join(folder,repo)
                                if os.path.exists(path):
                                    repos[org].append(repo)
                                else:
                                    pass
                        else:
                            for repo in siriuspy.envars.repo_names[org]:
                                if arg.lower() == repo:
                                    found = True
                                    path = os.path.join(folder,repo)
                                    if os.path.exists(path):
                                        repos[org].append(repo)
                                    else:
                                        pass
                if not found:
                    print('invalid: "' + arg + '"!')
        return repos

    repos = get_repos(args)
    for org, repo_list in repos.items():
        for repo in repo_list:
            path = os.path.join(siriuspy.envars.org_folders[org], repo)
            print('\n' + 70*'#')
            print('['+repo+']')
            if cmd == 'commit':
                syscmd = 'cd ' + path + '; git status'
                p = subprocess.Popen([syscmd], shell=True, stdout=subprocess.PIPE)
                out,err = p.communicate()
                syscmd = ''
                if 'modified:' in str(out):
                    print(out.decode('ascii'))
                    msg = input('commit message for "' + repo + '" [empty string to cancel commit]: ')
                    if msg:
                        syscmd = 'cd ' + path + '; git commit -a -m "' + msg + '"'
                    else:
                        print('cannot commit with empty message')
                if 'Untracked files:' in str(out):
                    print('there are untracked files!')
            else:
                syscmd = 'cd ' + path + '; git ' + cmd

            if syscmd:
                print(syscmd)
                p = subprocess.Popen([syscmd], shell=True, stdout=subprocess.PIPE)
                out,err = p.communicate()
                print(out.decode('ascii'))
            print(70*'#'+'\n')



def run():
    parser = argparse.ArgumentParser(description="Run git commands for sets of repositories")
    parser.add_argument('action', help='Which git command to perform on repositories',choices=('clone','status','pull','commit','push'))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--repos", nargs='+', help="List of repositories to perform 'action'",default=[])
    group.add_argument("--orgs", nargs='+', help="Perform 'action' on repositories of the organizations listed",choices=('all','lnls-fac','lnls-sirius','lnls-ima'),default=[])
    args = parser.parse_args()
    option = args.repos.copy()
    option += args.orgs
    if not option: option = ['all']
    if 'clone' == args.action.lower():
        run_git_clone(option)
    else:
        run_git_cmd(args.action.lower(), option)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, stop_now)
    run()
