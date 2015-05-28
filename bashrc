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

FACPATHS=~/.fac_paths
if [ -f $FACPATHS ] ; then
    source $FACPATHS
else
    export FACCODE=$FACROOT/code
    export FACDATA=$FACROOT/data
    export FACLIBS=$FACROOT/lib
fi

# PYTHON
export PYTHONPATH=$PYTHONPATH:$FACLIBS/python:$FACCODE/job_manager/src:$FACCODE/tools:$FACCODE

# arquivo de definições para o rpn do elegant
export RPN_DEFNS=/usr/local/epics_oag/defns.rpn

#Variaveis necessarias para rodar elegant e afins (entre eles o geneticOptimizer)
export HOST_ARCH=linux-x86_64
export EPICS_HOST_ARCH=linux-x86_64
export OAG_TOP_DIR=/usr/local/epics_oag
export EPICS_BASE=/usr/local/epics/R3.14/base

# FAC SCRIPTS
export PATH=$PATH:$FACCODE/scripts:$FACCODE/job_manager/apps:$FACROOT/bin
export PATH=$PATH:$FACCODE/scripts/fieldmap_analysis

# EPICS
export EV4_BASE=/usr/local/epics/v4
export PVDATABASE=$EV4_BASE/pvDatabaseCPP
export PVASRV=$EV4_BASE/pvaSrv
export PVACCESS=$EV4_BASE/pvAccessCPP
export NORMATIVETYPES=$EV4_BASE/normativeTypesCPP
export PVDATA=$EV4_BASE/pvDataCPP
export PVCOMMON=$EV4_BASE/pvCommonCPP
export PATH=$PATH:$EPICS_BASE/bin/$EPICS_HOST_ARCH
export PATH=$PATH:$PVACCESS/bin/$EPICS_HOST_ARCH

#ELEGANT AND OAG CONFIGS:

export PATH=$PATH:/usr/local/epics_oag/epics/base/bin/linux-x86_64:/usr/local/epics_oag/epics/extensions/bin/linux-x86_64:/usr/local/epics_oag/oag/apps/bin/linux-x86_64
export TCLLIBPATH="/usr/local/epics_oag/oag/apps/lib/linux-x86_64 /usr/local/epics_oag/epics/extensions/lib/linux-x86_64 /usr/local/epics_oag/oag/apps/lib/linux-x86_64/sdds /usr/local/epics_oag/oag/apps/lib/linux-x86_64/os /usr/local/epics_oag/oag/apps/lib/linux-x86_64/ca /usr/local/epics_oag/oag/apps/lib/linux-x86_64/rpn"
export PYTHONPATH=$PYTHONPATH:/usr/local/epics_oag/oag/apps/lib/linux-x86_64:/usr/local/epics_oag/epics/extensions/lib/linux-x86_64

# LIBRARIES

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$EPICS_BASE/lib/$EPICS_HOST_ARCH

# COMPLETIONS FOR JOBMANAGER FUNCTIONS
complete -W "--description --exec --inputFiles --workingDirectory --priority --possibleHosts --help"                                    pyjob_qsub.py
complete -W "--clients --showCalendar --help"                                                                                           pyjob_configs_get.py
complete -W "--clients --niceness --shutdown --remove --MoreJobs --defnumproc --calendar --weekday --initial --final --num_proc --help" pyjob_configs_set.py
complete -W "--sure --help"                                                                                                             pyjob_shutdown.py
complete -W "--jobs --status --user --description --explicate --choose --help"                                                          pyjob_qstat.py
complete -W "--jobs --status --user --description --signal --priority --possibleHosts --help"                                           pyjob_qsig.py
complete -W "--just-print --si --bo --tb --ts --li --help --list-all --sort"                                                            updatewiki
complete -W "help clean edit run summary rawfield trajectory multipoles model summary"                                                  fma_analysis.py
complete -W "--input-file"                                                                                                              fma_rawfield.py

# COMPLETIONS FOR VA

complete -W "stop start list vaca si_current si_lifetime si_bpms si_ps si_tune topup"  va

# USEFULL ALIAS
alias gocode='cd $FACCODE'
alias godata='cd $FACDATA'
alias golnls='cd $FACCODE/lnls'
alias gotrackcpp='cd $FACCODE/trackcpp'
alias gova='cd $FACCODE/va'
alias goscripts='cd $FACCODE/scripts'
alias gofieldmap='cd $FACDATA/sirius/si/magnet_modelling'
alias gopyaccel='cd $FACCODE/pyaccel'
alias gocalcs='cd $FACDATA/sirius/si/beam_dynamics/calcs/v07/c05'
alias gooficial='cd $FACDAT/sirius/si/beam_dynamics/oficial/v07/c05'
