#!/bin/bash

# Do merge and parse barcodes on all libraries in seedfile

SEEDFILE=$1

MERGE_PARSE=/scratch/CellFreeReporter/scripts/merge_parse_barcodes.sh

cat $SEEDFILE | while read WDIR
do
    date
    echo Processing $WDIR ...
    source $MERGE_PARSE $WDIR
    echo Done!!
    echo
done
