#!/usr/bin/env python-sirius

import sh
from datetime import datetime
import argparse
import logging as _log
import sys as _sys

folder_data = '/home/fac_files/data'
file_name = '/var/log/fac-data-gitall/sync_log'


def _print_log_file(msg_error):
    agora = datetime.now()
    with open(file_name, 'w') as fi:
        fi.write('#'*60 + '\n')
        fi.write('\n' + agora.strftime('%y/%m/%d-%H:%M') +
                 ' -> RESULTS FROM FAC DATA REPOSITORIES SYNC:\n\n')
        if not msg_error:
            fi.write('\tAll repositories synced!\n')
        else:
            fi.write(msg_error)
        fi.write('\n'+'#'*60 + '\n')


def _add_and_commit_files(status_repo):
    """Add each file checking if there are conflicts from previous attempts."""
    unmerged = False
    agora = datetime.now()
    msg_commit = 'Automatic Commit: ' + agora.strftime('%y-%m-%d_%H:%M')
    for line in status_repo.splitlines():
        if line[:2] in {'DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'}:
            unmerged = True
            continue
        idx = line.find('->')
        if idx >= 0:
            sh.git.add('-A', line[idx+3:].strip('"'))
        elif line.startswith(' D'):
            sh.git.rm(line[3:].strip('"'))
        elif not line.startswith('D '):
            sh.git.add('-A', line[3:].strip('"'))
    # Try to commit the files without conflict.
    # If there are none, generate error message
    try:
        sh.git.commit(m=msg_commit)
        _log.warning('\tChanges commited.')
    except sh.ErrorReturnCode:
        _log.warning('\tNone of the changes were committed. Solve Conflicts!')
    return unmerged


def update_data_repos(repo_sel=None):
    """Update repositories."""
    repos = sh.find(folder_data, '-name', '.git')
    repos = repos.stdout.decode().splitlines()
    if repo_sel is not None:
        repos = [x for x in repos if [y for y in repo_sel if x.find(y) >= 0]]

    msg_error = ''
    _log.warning('\nUpdating Working Tree and Syncing repository:')
    for repo in repos:
        rep = repo.rpartition('/')[0]
        sh.cd(rep)
        _log.warning('\n' + rep + ': ')
        status_repo = sh.git.status(porcelain=True).stdout.decode()
        if not status_repo:
            _log.warning('\tNothing to commit.')
            # If there are unmerged files from previous attempts:
        if status_repo and _add_and_commit_files(status_repo):
            _log.warning('\tStill have unmerged files. Solve it!')
            msg_error += '\n' + rep + ': Still have unmerged files. Solve it!'
            continue
        # Try to pull the changes if there are no conflicts
        # yet and identify new conflicts
        try:
            sh.git.pull()
            _log.warning('\tRepository fetched and merged.')
        except sh.ErrorReturnCode as error:
            _log.warning('\tThere are unmerged files.')
            msg_error += '\n' + rep + ': There are unmerged files.'
            continue

        # If no new conflicts were identified, try to push
        try:
            sh.git.push()
            _log.warning('\tRepository pushed.')
        except sh.ErrorReturnCode as error:
            _log.warning('\tProblem pushing repository.')
            msg_error += '\n' + rep + ': Problem pushing repository.'

    return msg_error


if __name__ == '__main__':
    # configuration of the parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--print', action='store_true', default=True,
                        help="Print summary on the Screen.", dest='display')
    parser.add_argument('-e', '--error', action='store_true', default=False,
                        help="Save file in "+file_name)
    parser.add_argument('-r', '--repos', action='store', nargs='+',
                        help="Select the repositories to sync. Default is all")
    args = parser.parse_args()

    level = _log.WARNING if args.display else _log.ERROR
    _log.basicConfig(format='%(message)s', level=level, stream=_sys.stdout)

    msg_error = update_data_repos(repo_sel=args.repos)
    if args.error:
        _print_log_file(msg_error)
