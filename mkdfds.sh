#!/bin/bash

LOG="./log/undefended"
DEFENDED="./defended"

if [ $# -ne 0 ]; then
    for CONFIG in "$@"; do
        python3 ./util/mkdfds.py $CONFIG
    done
else
    if [ -z $(ls $LOG 2> /dev/null) ]; then
        echo "No undefended traces"
    else
        python3 ./util/mkdfds.py $LOG
    fi

    if [ -z $(ls $DEFENDED 2> /dev/null) ]; then
        echo "No defended traces"
    else
        for CONFIG in $DEFENDED/*; do
            python3 ./util/mkdfds.py $CONFIG
        done
    fi
fi
