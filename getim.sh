#!/bin/bash
if [ $1 == "-dev" ]; then
    ./clean.sh
    python src/gamerunner.py -c jacob -b -s
else
    ./clean.sh
    python src/gamerunner.py $*
fi
