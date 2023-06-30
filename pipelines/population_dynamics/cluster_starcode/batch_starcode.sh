#!/bin/bash

# Cluster sequences using Starcode

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/population_dynamics
STARCODE=$MY_HOME/cluster_starcode/starcode.sh

SEEDFILE=$1

cat $SEEDFILE | while read INPUT
do
    LOG=$INPUT.log
    OUTPUT=$INPUT.out
    date
    echo "Clustering using Starcode..."
    echo "Input:" $INPUT
    echo "Output:" $OUTPUT
    { time $STARCODE $INPUT $OUTPUT ; } 2> $LOG
    echo Done!!
    echo
done
