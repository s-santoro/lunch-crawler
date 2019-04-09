#!/bin/bash

# get configId from parameter-passing
id="$1"

# run luigi pipeline with given configId
python3 -m luigi --module Evaluator Evaluator --configId ${id} --local-scheduler