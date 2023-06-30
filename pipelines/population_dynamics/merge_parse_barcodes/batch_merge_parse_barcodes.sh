#!/bin/bash

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/population_dynamics/  # home directory for pipeline

# Do merge and parse barcodes on all libraries in seedfile

SEEDFILE=$1

MERGE_PARSE=$MY_HOME/merge_parse_barcodes/merge_parse_barcodes.sh

cat $SEEDFILE | while read WDIR
do
    date
    echo Processing $WDIR ...
    source $MERGE_PARSE $WDIR
    echo Done!!
    echo
done
