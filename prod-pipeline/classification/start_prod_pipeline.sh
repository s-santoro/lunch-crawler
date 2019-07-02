#!/bin/bash

# run luigi pipeline in local mode
python3 -m luigi --module Classifier Classifier --configId 0 --local-scheduler