#!/usr/bin/env python3

import sh
import lnls


repos = sh.find(lnls.folder_data,'-name','.git')

repos = repos.stdout.splitlines()

for repo in repos:
    rep  = repo.decode().rpartition('/')[0]
    sh.cd(rep)
    print(rep.rpartition('/')[-1])
    status_repo = sh.git.status().stdout.decode()
    if status_repo.find('nothing to commit, working directory clean') < 0:
        add_repo    = sh.git.add('*')
        commit_repo = sh.git.commit(m=msg_commit)
        pull_repo   = sh.git.pull()

    print(sh.ls(sh.HOME))
