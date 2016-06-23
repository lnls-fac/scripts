#!/usr/bin/env python3

import sh
import lnls


repos = sh.find(lnls.folder_data,'-name','.git')

repos = repos.stdout.splitlines()

for repo in repos:
    rep  = repo.decode().rpartition('/')[0]
    sh.cd(rep)
    print(rep.rpartition('/')[-1])
    status_repo = sh.git.status(porcelain=True).stdout.decode()
    if status_repo:
        add_repo    = sh.git.add('*')
        commit_repo = sh.git.commit(a=True,m=msg_commit)


    pull_repo   = sh.git.pull()

    print(sh.ls(sh.HOME))
