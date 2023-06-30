#!/bin/bash

# Cluster barcodes using Starcode

STARCODE="/scratch/resources/starcode/starcode"

INPUT=$1
OUTPUT=$2

# Cluster using message passing
$STARCODE --dist 1 --threads 16 --print-clusters --input $INPUT --output $OUTPUT
