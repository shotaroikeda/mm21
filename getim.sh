#!/bin/bash
if [ $1 == "-dev" ]; then
    ./clean.sh
    python src/gamerunner.py -c ubot1 -b -s
elif [ $1 == "-self" ]; then
    ./clean.sh
    python src/gamerunner.py -t 5 -c ubot1 -c ubot1 -c ubot1 -c ubot1 -c ubot1 -b -s
else
    ./clean.sh
    python src/gamerunner.py $*
fi
