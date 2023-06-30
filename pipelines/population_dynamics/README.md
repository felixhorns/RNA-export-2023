# Population dynamics pipeline

## Overview

To analyze population dynamics tracking	data, we perform the following steps, which we refer to	as preprocessing:

1. Merge paired end reads (using FLASH) and parse the barcodes (find barcode sequence within merged read).
2. Aggregate barcodes across samples.
3. Count and collapse identical barcode sequences, and call the viral library index.
4. Merge similar barcodes using sequence clustering (using Starcode).
5. Filter to identify genuine barcodes using knee point detection.

This workflow is managed by a shell script. In addition, we use custom scripts written in Bash and Python to deploy individual steps and aggregate results.

The output of the pipeline is:
1. Counts of unique barcode sequences annotated with sample metadata (tab-separated text) (`clones.error_corrected.genuine_called.tsv.gz`).

## Citation

If you use this code, please cite this paper.

Horns *et al.*, Engineering RNA export for measurement and manipulation of living cells, *Cell* **186** (2023).

## Configuration

### Environment

Python 3.7.7 is the primary environment. Required packages include Conda, BioPython, and pandas. All required packages are specified in `analysis/environment.txt`, which can be used to create an environment using Conda.

FLASH is a required software tool that merges paired-end reads. FLASH may be installed from `https://ccb.jhu.edu/software/FLASH/`. This pipeline was developed using FLASH v.1.2.11.

Starcode is a required software tool that clusters sequences based on identity. Starcode may be installed from `https://github.com/gui11aume/starcode`. This pipeline was developed using Starcode v.1.4.

### Data

Barcode sequencing data to track population dynamics from our paper can be downloaded from either Data.Caltech (recommended) or the Sequence Read Archive (SRA) of the National Center for Biotechnology Information (NCBI) (accession PRJNA943434).

We recommend moving each sample into its own directory for preprocessing. This pipeline treats the all reads within a directory together as a sample. If you download the data from Data.Caltech, the reads are already organized in this way.

## Using the population dynamics pipeline

Most of the pipeline is run using the script `run_pipeline.sh`, such as by calling `source run_pipeline.sh`.

Prior to running the pipeline, the script should be edited to ensure that paths are correct, including the following variables.
* `MY_HOME`, the home directory for analysis.
* `WDIR`, the working directory for analysis, typically where the data are located.
* `SAMPLESHEET_AGGREGATE`, a sample sheet that specifies correspondence between samples and data files.

When the shell script is complete, the final step (filtering barcodes using knee point detection) is performed using a Jupyter notebook `filter_knee/filter_knee.ipynb`. In this notebook, variables specifying paths to the data should be updated.

## Disclaimer

This project is not maintained. Software is provided as is and requests for support may not be addressed.

## Contact

If you have questions or comments, please contact Felix Horns at rfhorns@gmail.com.
