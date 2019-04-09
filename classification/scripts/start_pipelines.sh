#!/bin/bash

# get amount of cpu-cores
cores=$(fgrep -c processor /proc/cpuinfo)

# get length of configs-list from python-script
amountPipes=$(($(python3 get_configsSize.py)-1))

parallel -j${cores} ./pipeline.sh ::: $(seq 0 $amountPipes)
