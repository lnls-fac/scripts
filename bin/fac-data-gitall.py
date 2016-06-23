#!/usr/bin/env python3

import sh
import lnls


repos = sh.find(lnls.folder_data,'-name','.git')

repos = repos.stdout.splitlines()

for repo in repos:
    rep  = repo.decode().rpartition('/')[0]
    sh.cd(rep)
    print(rep.rpartition('/')[-1])
    status_repo = sh.git.status()
    print(status_repo)
    print(sh.ls(sh.HOME))
