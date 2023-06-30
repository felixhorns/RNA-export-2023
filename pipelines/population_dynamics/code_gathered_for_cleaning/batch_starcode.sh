#!/bin/bash

# Batch deployment of clustering barcodes using Starcode

STARCODE=/scratch/CellFreeReporter/pipelines/220520_Demo6_consensus_error_correct_starcode/starcode.sh

SEEDFILE=$1

cat $SEEDFILE | while read INPUT
do
    LOG=$INPUT.log
    OUTPUT=$INPUT.out
    date
    echo Processing $INPUT ...
    { time $STARCODE $INPUT $OUTPUT ; } 2> $LOG
    echo Done!!
    echo
done
