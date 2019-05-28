#!/bin/bash

# get configId from parameter-passing
end="$1"
id="$2"
# run luigi pipeline with given configId
python3 -m luigi --module ${end} ${end} --configId ${id} --local-scheduler