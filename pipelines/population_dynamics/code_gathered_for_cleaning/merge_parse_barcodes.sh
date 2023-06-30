#!/bin/bash

# Parse barcodes from sequencing reads by 1) merging paired end reads using FLASH and 2) parsing barcodes from reads.

WDIR=$1

FLASH_LOG=$WDIR/flash.log

FLASH=/scratch/resources/FLASH-1.2.11-Linux-x86_64/flash
PARSE_BARCODES=/scratch/CellFreeReporter/scripts/parse_barcodes.py

# Merge reads
$FLASH $WDIR/*_R1_*.fastq.gz $WDIR/*_R2_*.fastq.gz --max-overlap=75 --max-mismatch-density=0.5 --compress --output-directory=$WDIR > $FLASH_LOG

# Parse barcodes
python $PARSE_BARCODES $WDIR/out.extendedFrags.fastq.gz $WDIR
