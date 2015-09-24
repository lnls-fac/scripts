#!/bin/bash

if [ ! -z $FACCODE ] ; then
    echo "\$FACCODE found; will clone in '$FACCODE'."
    CURRENTDIR=$(pwd)
    cd "$FACCODE"
else
    echo "\$FACCODE not found; will clone in '$PWD'."
fi

echo "Cloning repositories..."

for REPOSITORY in \
    apsuite \
    collective_effects \
    fieldmaptrack \
    job_manager \
    lnls \
    mathphys \
    MatlabMiddleLayer \
    pyaccel \
    scripts \
    sirius \
    sirius_wiki \
    tools \
    trackcpp \
    tracy_sirius \
    va
do
    if [ ! -d "$REPOSITORY" ] ; then
        git clone ssh://git@github.com/lnls-fac/"$REPOSITORY".git
    fi
done

echo "Finished cloning repositories."

if [ ! -z $FACCODE ] ; then
    cd "$CURRENTDIR"
fi
