#!/bin/bash

TIMESTAMP=$(date +%s) # current time
OUTPUT_PATH=$HOME/ai4mat/computing/output

bsub -q cresco6_h144 -o $OUTPUT_PATH/stdout_$TIMESTAMP -e $OUTPUT_PATH/stderr_$TIMESTAMP ./run_using_simg.sh
