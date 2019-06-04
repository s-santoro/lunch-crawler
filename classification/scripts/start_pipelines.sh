#!/bin/bash

# get end of pipeline
end="$1"
# get amount of cpu-cores
cores=$(fgrep -c processor /proc/cpuinfo)

# get length of configs-list from python-script
amountPipes=$(($(python3 get_configsSize.py)-1))
echo 
echo "starting $((1+${amountPipes})) pipelines with pipeline-end: ${end} ..."
echo 
time parallel -j${cores} ./pipeline.sh $end ::: $(seq 0 $amountPipes)
