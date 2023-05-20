#!/bin/bash

LOG="./log"
CONFIGS="$LOG/*.xpi"

if [ $# -ne 0 ]; then
    for CONFIG in "$@"; do
        python3 ./util/pad.py $CONFIG
    done
else
    if [ -z $(ls $LOG | grep ".xpi" 2> /dev/null) ]; then
        echo "Nothing to do"
        exit 1
    fi

    for CONFIG in $CONFIGS/*; do
        CONFIG=${CONFIG##*log/}
        python3 ./util/pad.py $CONFIG
    done
fi
