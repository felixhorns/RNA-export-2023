#!/bin/bash

# Aggregate barcodes and metrics of merging and parsing barcodes from multiple libraries

## Resources

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/population_dynamics/  # home directory for pipeline

### Scripts
AGGREGATE_BARCODES=$MY_HOME/aggregate_barcodes/aggregate_barcodes.py
AGGREGATE_METRICS=$MY_HOME/aggregate_barcodes/aggregate_metrics.py

## Input and output files

### Sample sheet (specifies sample name and directory)
SAMPLE_SHEET=$1

### Output directory
OUTDIR=$2

### Output files
OUTFILE_BARCODES=$OUTDIR/barcodes.tsv.gz
OUTFILE_METRICS=$OUTDIR/merge_parse_barcode_metrics.tsv

## Do aggregate

### Aggregate barcodes
python $AGGREGATE_BARCODES $SAMPLE_SHEET $OUTFILE_BARCODES

### Aggregate metrics
python $AGGREGATE_METRICS $SAMPLE_SHEET $OUTFILE_METRICS

echo "Done!"
