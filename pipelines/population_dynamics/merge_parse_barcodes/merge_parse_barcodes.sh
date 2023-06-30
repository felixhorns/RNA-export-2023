#!/bin/bash

# Parse barcodes from sequencing reads by 1) merging paired end reads using FLASH and 2) parsing barcodes from reads.
# Input: Working directory containing paired end reads (named *_R1_*.fastq.gz and *_R2_*.fastq.gz)
# Output: (1) Barcode sequences with annotations in csv, and (2) Summary metrics of barcodes in csv.

WDIR=$1

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/population_dynamics/  # home directory for pipeline

FLASH_LOG=$WDIR/flash.log  # log file for FLASH

FLASH=/scratch/resources/FLASH-1.2.11-Linux-x86_64/flash  # path to FLASH executable
PARSE_BARCODES=$MY_HOME/merge_parse_barcodes/parse_barcodes.py  # path to script that parses barcodes from merged reads

# Merge reads
$FLASH $WDIR/*_R1_*.fastq.gz $WDIR/*_R2_*.fastq.gz --max-overlap=75 --max-mismatch-density=0.5 --compress --output-directory=$WDIR > $FLASH_LOG

# Parse barcodes
python $PARSE_BARCODES $WDIR/out.extendedFrags.fastq.gz $WDIR
