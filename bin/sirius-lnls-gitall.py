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
            cmd = 'cd ' + siriuspy.envars.org_folders[org] + '; git clone git@gitgub.com:' + org + '/' + repo
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
                    print('invalid: "' + repo_sel + '"!')
        return repos

    repos = get_repos(args)
    for org, repo_list in repos.items():
        for repo in repo_list:
            path = os.path.join(siriuspy.envars.org_folders[org], repo)
            if cmd == 'commit':
                msg = input('commit message for "' + repo + '": ')
                if not msg:
                    syscmd = 'cd ' + path + '; git commit -a -m "' + msg + '"'
                else:
                    syscmd = ''
            else:
                syscmd = 'cd ' + path + '; git ' + cmd
            print('['+repo+']')
            if syscmd:
                print(syscmd)
                text = subprocess.call([syscmd], shell=True, stdout=sys.stdout)
            else:
                print('cannot commit with empty message')


def run():
    parser = argparse.ArgumentParser(description="Run git commands for sets of repositories")
    parser.add_argument("--clone", type=str, nargs='+', help="clone repositories")
    parser.add_argument("--status", type=str, nargs='+', help="pull repositories")
    parser.add_argument("--pull", type=str, nargs='+', help="pull repositories")
    parser.add_argument("--commit", type=str, nargs='+', help="pull repositories")
    parser.add_argument("--push", type=str, nargs='+', help="pull repositories")
    args = parser.parse_args()
    if args.clone:
        run_git_clone(args.clone)
    if args.pull:
        run_git_cmd('pull', args.pull)
    if args.status:
        run_git_cmd('status', args.status)
    if args.commit:
        run_git_cmd('commit', args.commit)
    if args.push:
        run_git_cmd('push', args.push)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, stop_now)
    run()
