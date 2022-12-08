#!/bin/bash

CONFIGS="./defended"

if [ $# -ne 0 ]; then
    for CONFIG in "$@"; do
        python3 ./util/loh.py $CONFIG
    done
else
    if [ -z $(ls $CONFIGS 2> /dev/null) ]; then
        echo "Nothing to do"
        exit 1
    fi

    for CONFIG in $CONFIGS; do
        CONFIG=${CONFIG##*defended/}
        python3 ./util/loh.py $CONFIG >> loh.txt
    done
fi
