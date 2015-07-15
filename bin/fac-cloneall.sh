#!/bin/bash

if [ ! -z $FACCODE ] ; then
    echo "\$FACCODE found; will clone in '$FACCODE'."
    CURRENTDIR=$(pwd)
    cd "$FACCODE"
else
    echo "\$FACCODE not found; will clone in '$PWD'."
fi

echo "Cloning repositories..."
git clone ssh://git@github.com/lnls-fac/collective_effects.git
git clone ssh://git@github.com/lnls-fac/fieldmaptrack.git
git clone ssh://git@github.com/lnls-fac/job_manager.git
git clone ssh://git@github.com/lnls-fac/lnls.git
git clone ssh://git@github.com/lnls-fac/mathphys.git
git clone ssh://git@github.com/lnls-fac/MatlabMiddleLayer.git
git clone ssh://git@github.com/lnls-fac/pyaccel.git
git clone ssh://git@github.com/lnls-fac/sirius.git
git clone ssh://git@github.com/lnls-fac/sirius_wiki.git
git clone ssh://git@github.com/lnls-fac/tools.git
git clone ssh://git@github.com/lnls-fac/trackcpp.git
git clone ssh://git@github.com/lnls-fac/tracy_sirius.git
git clone ssh://git@github.com/lnls-fac/va.git
echo "Finished cloning repositories."

if [ ! -z $FACCODE ] ; then
    cd "$CURRENTDIR"
fi
