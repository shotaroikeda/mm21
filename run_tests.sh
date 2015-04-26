#!/bin/bash

message(){
    echo ""
    echo "Above is a list of errors detected in your code. Please fix them before committing!"
    echo "You can bypass this check (and incur Ace's wrath) with \'git commit --no-verify\'"
}

trap message 0

# Find working directory + add it to $PYTHONPATH
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )" # resolve $SOURCE until the file is no longer a symlink
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE is relative, resolve it relative to the symlink file's location
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
echo $DIR
export PYTHONPATH=$DIR

# Show errors in bash
set -e

# Run pep8 (Python linter) + unit tests
if hash pep8 2>/dev/null; then
    if [[ $* == *--me-only* ]]; then
        for i in $( git diff --name-only HEAD ); do
            extension="${i##*.}"
            if [ "$extension" == "py" ]; then
                pep8 $i --ignore=E122,E241,W293,W291,W391,E501,E126
            fi
        done
    else
        pep8 src --ignore=E122,E241,W293,W291,W391,E501,E126
        pep8 src_test --ignore=E122,E241,W293,W291,W391,E501,E126
    fi
else
    echo "Error: pep8 not found."
    exit 1
fi
if hash py.test 2>/dev/null; then
        py.test
    else
        echo "Error: pytest not found."
        exit 1
fi
echo "All tests ran!"

# Install pre-commit hook
FILE="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
HOOKPATH=$DIR/".git/hooks/pre-commit"
if [ ! -L $HOOKPATH ]; then
    echo "installing precommit hook"
    # Remove old hook file
    if  [ -f $HOOKPATH ]; then
        rm $HOOKPATH
    fi
    # Symlink to new hook file
    ln -s $DIR/$FILE $HOOKPATH
    echo "pre-commit hoook installed"
fi

# Done!
trap - 0
echo "Done!"
