#!/bin/bash

# View Turn script from mm20 should work with mm21 with little effort
# It assumes that one turn is printer per line and that the fist jone has
# the connection infomaiton. If you ask for a turn higher then the last turn
# it will show the the end of gave infomation

if [ "$1" == "-h" ]; then
  echo "Usage: $0 turn_number (If zero is provided it will show the connection informaiton.)"
  exit 0
fi
let turn=$1+1
head -n $turn serverlog.json | tail -n 1 | python -m json.tool | less
