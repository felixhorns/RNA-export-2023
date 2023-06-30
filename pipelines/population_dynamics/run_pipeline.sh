#!/bin/bash

# Population dynamics pipeline

## Resources

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/population_dynamics/  # home directory for pipeline

### Scripts

MERGE_PARSE=$MY_HOME/merge_parse_barcodes/batch_merge_parse_barcodes.sh  # path to wrapper that runs merge and parse on all targets in seedfile
AGGREGATE_BARCODES=$MY_HOME/aggregate_barcodes/aggregate.sh  # path to script that aggregates barcodes across samples
COLLAPSE_IDENTICAL_CALL_INDEX=$MY_HOME/collapse_identical_call_index/collapse_identical_call_index.py  # path to script that collapses identical reads and calls library index

FORMAT_STARCODE=$MY_HOME/cluster_starcode/format_for_starcode.py  # path to script that formats barcodes for input to starcode
STARCODE=$MY_HOME/cluster_starcode/batch_starcode.sh
MAP_BARCODES_TO_CLUSTERS=$MY_HOME/cluster_starcode/map_barcodes_to_clusters.py

### Input and output files

SEEDFILE_MERGE_PARSE=$MY_HOME/merge_parse_barcodes/seedfile.txt

SAMPLESHEET_AGGREGATE=$MY_HOME/aggregate_barcodes/sample_sheet.txt

WDIR=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/sequencing_data_preprocessing/population_dynamics

BARCODES=$WDIR/barcodes.tsv.gz
BARCODES_LIB_BARCODE_CALLED=$WDIR/barcodes.library_barcode_called.tsv.gz
CLONES_EXACT=$WDIR/clones.tsv.gz
STANDARDS_COUNTS=$WDIR/counts_STD.tsv

WDIR_STARCODE=$WDIR/temp_starcode
SEEDFILE_STARCODE=$WDIR/seedfile_starcode.txt

CLONES_CLUSTERED=$WDIR/clones.error_corrected.tsv.gz

## Run pipeline

### Merge paired end reads and parse barcodes
echo "Merging paired end reads and parsing barcodes..."
source $MERGE_PARSE $SEEDFILE_MERGE_PARSE
echo

### Aggregate barcodes across samples
echo "Aggregating barcodes across samples..."
source $AGGREGATE_BARCODES $SAMPLESHEET_AGGREGATE $WDIR
echo

### Collapse identical barcodes and call library index
echo "Collapsing identical barcodes and calling library index..."
python $COLLAPSE_IDENTICAL_CALL_INDEX $BARCODES $BARCODES_LIB_BARCODE_CALLED $CLONES_EXACT $STANDARDS_COUNTS
echo

### Merge barcodes into clones based on sequence clustering
echo "Merging barcodes into clones using sequence clustering..."

#### Create working directory for Starcode if it does not already exist
mkdir -p $WDIR_STARCODE

#### Format barcodes for input into Starcode
python $FORMAT_STARCODE $CLONES_EXACT $WDIR_STARCODE

#### Make seedfile for Starcode (find all input files for Starcode in temporary directory)
find $WDIR_STARCODE/*.tsv.tmp -type f > $SEEDFILE_STARCODE

#### Cluster sequences using Starcode
source $STARCODE $SEEDFILE_STARCODE

#### Map clones after clustering to individual reads
python $MAP_BARCODES_TO_CLUSTERS $CLONES_EXACT $WDIR_STARCODE $CLONES_CLUSTERED

### Call barcodes using knee point detection
# Performed in Jupyter Notebook `filter_knee/filter_knee.ipynb`

echo "Done!"
date

