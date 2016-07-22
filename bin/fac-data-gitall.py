#!/usr/bin/env python3

import sh
from datetime import datetime
import optparse
import lnls

file_name = '/var/log/fac-data-gitall/sync_log'

def update_data_repos(display=True, err=False):
    repos = sh.find(lnls.folder_data,'-name','.git')
    repos = repos.stdout.decode().splitlines()

    agora = datetime.now()
    msg_commit = 'Automatic Commit: ' + agora.strftime('%y-%m-%d_%H:%M')
    msg_error = ''
    if display: print('\nUpdating Working Tree and Syncing repository:')
    for repo in repos:
        rep  = repo.rpartition('/')[0]
        sh.cd(rep)
        if display: print('\n' + rep + ': ')
        status_repo = sh.git.status(porcelain=True).stdout.decode()
        if status_repo:
            # Add file by file checking if there are conflicts from previous attempts
            unmerged = False
            for line in status_repo.splitlines():
                if line[:2] in {'DD','AU','UD','UA','DU','AA','UU'}:
                    unmerged = True
                    continue

                idx = line.find('->')
                if  idx >= 0:                   add_repo = sh.git.add('-A',line[idx+3:].strip('"'))
                elif line.startswith(' D'):     add_repo = sh.git.rm(line[3:].strip('"'))
                elif not line.startswith('D '): add_repo = sh.git.add('-A',line[3:].strip('"'))

            # Try to commit the files without conflict. If there are none, generate error message
            try:
                commit_repo = sh.git.commit(m=msg_commit)
                if display: print('\tChanges commited.')
            except sh.ErrorReturnCode:
                if display: print('\tNone of the changes were committed. Solve Conflicts!')

            #If there are unmerged files from previous attempts:
            if unmerged:
                if display: print('\tStill have unmerged files. Solve it!')
                msg_error += '\n' + rep + ': Still have unmerged files. Solve it!'
                continue
        else:
            if display: print('\tNothing to commit.')

        # Try to pull the changes if there are no conflicts yet and identify new conflicts
        try:
            pull_repo   = sh.git.pull()
            if display: print('\tRepository fetched and merged.')
        except sh.ErrorReturnCode as error:
            if display: print('\tThere are unmerged files.')
            msg_error += '\n' + rep + ': There are unmerged files.'
            continue

        # If no new conflicts were identified, try to push
        try:
            push_repo   = sh.git.push()
            if display: print('\tRepository pushed.')
        except sh.ErrorReturnCode as error:
            if display: print('\tProblem pushing repository.')
            msg_error += '\n' + rep + ': Problem pushing repository.'

    if err:
        with open(file_name,'w') as fi:
            fi.write('#'*60 + '\n')
            fi.write('\n' + agora.strftime('%y/%m/%d-%H:%M') +
                     ' -> RESULTS FROM FAC DATA REPOSITORIES SYNC:\n\n')
            if not msg_error:
                fi.write('\tAll repositories synced!\n')
            else:
                fi.write(msg_error)
            fi.write('\n'+'#'*60 + '\n')
    return None

if __name__ == '__main__':

    # configuration of the parser for the arguments
    parser = optparse.OptionParser()
    parser.add_option('-p','--print',dest='display',action='store_true',
                      help="Print summary on the Screen.", default=True)
    parser.add_option('-e','--error',dest='error',action='store_true',
                      help="Save file in $HOME/"+file_name,
                      default=False)
    (opts, _) = parser.parse_args()

    update_data_repos(display=opts.display,err=opts.error)
