# This file should be sources with a prefix argument so that
# completions for epics commands are implemented.

PREFIX=$1
ALLPVS="`pvs_si.py $PREFIX` `pvs_bo.py $PREFIX`"
complete -W "$ALLPVS" caget
complete -W "$ALLPVS" camonitor
complete -W "$ALLPVS" caput
