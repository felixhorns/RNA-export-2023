#!/bin/bash

# Aggregate barcodes and metrics of merging and parsing barcodes from multiple libraries

# Set sample sheet (specifies library name and input directory)
SAMPLE_SHEET=/scratch/CellFreeReporter/pipelines/220513_Demo6_aggregate_barcodes/sample_sheet.txt

# Set output directory
OUTDIR=/scratch/CellFreeReporter/processed_seq/220513_Demo6

# Specify output files
OUTFILE_BARCODES=$OUTDIR/barcodes.tsv.gz
OUTFILE_METRICS=$OUTDIR/merge_parse_barcode_metrics.tsv

# Specify scripts
AGGREGATE_BARCODES=/scratch/CellFreeReporter/scripts/aggregate_barcodes.py
AGGREGATE_METRICS=/scratch/CellFreeReporter/scripts/aggregate_merge_parse_barcode_metrics.py

# Aggregate barcodes
python $AGGREGATE_BARCODES $SAMPLE_SHEET $OUTFILE_BARCODES

# Aggregate metrics
python $AGGREGATE_METRICS $SAMPLE_SHEET $OUTFILE_METRICS

