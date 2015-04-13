# ---------------------------
# PATHS
# ---------------------------

if [ -d /home ] ; then
    export FACROOT=/home/fac_files
elif [ -d /Users ] ; then
    export FACROOT=/Users/fac_files
else
    echo "FACROOT not defined!"
fi

export FACCODE=$FACROOT/code
export FACDATA=$FACROOT/data
export FACLIBS=$FACROOT/lib

# PYTHON
export PYTHONPATH=$FACCODE/job_manager/src:$FACCODE:$FACCODE/tools:$FACLIBS/python

# FAC SCRIPTS
export PATH=$PATH:$FACCODE/scripts:$FACCODE/job_manager/apps:$FACROOT/bin
export PATH=$PATH:$FACCODE/scripts/fieldmap_analysis

#ELEGANT AND OAG CONFIGS:

export PATH=$PATH:/usr/local/epics_oag/epics/base/bin/linux-x86_64:/usr/local/epics_oag/epics/extensions/bin/linux-x86_64:/usr/local/epics_oag/oag/apps/bin/linux-x86_64

export TCLLIBPATH="/usr/local/epics_oag/oag/apps/lib/linux-x86_64 /usr/local/epics_oag/epics/extensions/lib/linux-x86_64 /usr/local/epics_oag/oag/apps/lib/linux-x86_64/sdds /usr/local/epics_oag/oag/apps/lib/linux-x86_64/os /usr/local/epics_oag/oag/apps/lib/linux-x86_64/ca /usr/local/epics_oag/oag/apps/lib/linux-x86_64/rpn"

export PYTHONPATH=$PYTHONPATH:/usr/local/epics_oag/oag/apps/lib/linux-x86_64:/usr/local/epics_oag/epics/extensions/lib/linux-x86_64

# arquivo de definições para o rpn do elegant
export RPN_DEFNS=/usr/local/epics_oag/defns.rpn

#Variaveis necessarias para rodar elegant e afins (entre eles o geneticOptimizer)
export HOST_ARCH=linux-x86_64
export EPICS_HOST_ARCH=linux-x86_64
export OAG_TOP_DIR=/usr/local/epics_oag

#completion for the JobManager functions
complete -W "--description --exec --inputFiles --workingDirectory --priority --possibleHosts --help"                                    pyjob_qsub.py
complete -W "--clients --showCalendar --help"                                                                                           pyjob_configs_get.py
complete -W "--clients --niceness --shutdown --remove --MoreJobs --defnumproc --calendar --weekday --initial --final --num_proc --help" pyjob_configs_set.py
complete -W "--sure --help"                                                                                                             pyjob_shutdown.py
complete -W "--jobs --status --user --description --explicate --choose --help"                                                          pyjob_qstat.py
complete -W "--jobs --status --user --description --signal --priority --possibleHosts --help"                                           pyjob_qsig.py
complete -W "--just-print --si --bo --tb --ts --li --help --list-all --sort"                                                            updatewiki
complete -W "help clean edit run summary rawfield trajectory multipoles model summary"                                                  fma_analysis.py
complete -W "--input-file"                                                                                                              fma_rawfield.py
