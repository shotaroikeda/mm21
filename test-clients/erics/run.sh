#!/bin/bash
if hash python2 2>/dev/null; then
        python2 eric_client.py $1 $2
    else
        python eric_client.py $1 $2
    fi
