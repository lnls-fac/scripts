# This file should be sources with a prefix argument so that
# completions for epics commands are implemented.

PREFIX=$1
ALLPVS="`sirius-pvs-li.py $PREFIX` `sirius-pvs-bo.py $PREFIX` `sirius-pvs-si.py $PREFIX` `sirius-pvs-ti.py $PREFIX`"
complete -W "$ALLPVS" caget
complete -W "$ALLPVS" camonitor
complete -W "$ALLPVS" caput
