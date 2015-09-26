# This file should be sources with a prefix argument so that
# completions for epics commands are implemented.

PREFIX=$1
ALLPVS="`sirius-pvs.py li $PREFIX` `sirius-pvs.py tb $PREFIX` `sirius-pvs.py bo $PREFIX` `sirius-pvs.py ts $PREFIX` `sirius-pvs.py si $PREFIX`"
complete -W "$ALLPVS" caget
complete -W "$ALLPVS" camonitor
complete -W "$ALLPVS" caput
complete -W "$ALLPVS" cainfo
