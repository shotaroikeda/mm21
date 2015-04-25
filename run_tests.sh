#!/bin/bash

message(){
    echo ""
    echo "errors found in your code"
    echo "git will not let you commit until it is fixed"
    echo "You can bypass this with git commit --no-verify"
    echo "Try not to as it annoys Ace and makes the code look bad ;)"
}

trap message 0

# find the path to the working directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
    # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
echo $DIR

# Add it to the python path
${PYTHONPATH:==""}
export PYTHONPATH:=$DIR

# turn on errors in bash
set -e
if hash py.test 2>/dev/null; then
        py.test
    else
        echo "Error could not find pytest installed"
        exit 1
fi

if hash pep8 2>/dev/null; then
    pep8 src --ignore=E122,E241,W293,W291,W391,E501,E126
    pep8 src_test --ignore=E122,E241,W293,W291,W391,E501,E126
else
    echo "Error could not find pep8 installed"
    exit 1
fi
echo "All test run successful"

FILE="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
HOOKPATH=$DIR/".git/hooks/pre-commit"
# install pre-commit hook
if [ ! -L $HOOKPATH ]; then
    # remove old hook
    if  [ -f $HOOKPATH ]; then
        rm $HOOKPATH
    fi
    # Symlink to this file
    ln -s $DIR/$FILE $HOOKPATH
    echo "pre-commit hoook installed"
fi
