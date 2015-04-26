#!/bin/bash

# Colors (the ones we use)
CGRN="\033[92m"
CRED="\033[91m"
CEND="\033[0m"
FBOLD="\033[1m"

# Initial message
message(){
    echo ""
    echo "$CREDAbove is a list of errors detected in your code. $FBOLD Please fix them before committing!$CEND"
    echo "You can bypass this check (and incur Ace's wrath) with \'git commit --no-verify\'"
}

trap message 0

# Find working directory + add it to $PYTHONPATH
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )" # Resolve $SOURCE until its no longer a symlink
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # If $SOURCE is relative, resolve it relative to the symlink
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
    echo "$CRED $FBOLD Error: pep8 not found. $CEND"
    exit 1
fi
if hash py.test 2>/dev/null; then
        py.test
    else
        echo "$CGRN $FBOLD Error: pytest not found. $CEND"
        exit 1
fi
echo "$CGRN All tests ran! $CEND"

# Install pre-commit hook
FILE="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
HOOKPATH=$DIR/".git/hooks/pre-commit"
if [ ! -L $HOOKPATH ]; then
    echo "Installing pre-commit hook..."
    # Remove old hook file
    if  [ -f $HOOKPATH ]; then
        rm $HOOKPATH
    fi
    # Symlink to new hook file
    ln -s $DIR/$FILE $HOOKPATH
    echo "Pre-commit hoook installed!"
fi

# Done!
trap - 0
echo "$CGRN $FBOLD Done! $CEND"
