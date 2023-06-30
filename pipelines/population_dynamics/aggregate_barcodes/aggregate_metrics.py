""" Aggregate metrics of merging and parsing barcodes from multiple libraries """

import sys
import numpy as np
import pandas as pd

infile = sys.argv[1]  # sample sheet (specifies library name and barcode file)
outfile = sys.argv[2]  # output file

### Load library names and files

names = []
infiles_parse_barcode_metrics = []
infiles_flash_log = []

with open(infile) as f:
    for line in f:

        name = line.rstrip().split("\t")[0]
        input_dir = line.rstrip().split("\t")[1]
        infile_parse_barcode_metrics = input_dir + "/parse_barcode_metrics.tsv"
        infile_flash_log = input_dir + "/flash.log"
        
        names.append(name)
        infiles_parse_barcode_metrics.append(infile_parse_barcode_metrics)
        infiles_flash_log.append(infile_flash_log)

### Load files

dfs = []

for name, infile_parse_barcode_metrics, infile_flash_log in zip(names, infiles_parse_barcode_metrics, infiles_flash_log):

    # Load metrics of parsing barcodes
    metrics = pd.read_csv(infile_parse_barcode_metrics, header=0, index_col=None, sep="\t")

    # Set library name
    metrics["lib"] = name

    # Move column to left
    col = metrics["lib"]
    metrics = metrics.drop(labels="lib", axis=1)
    metrics.insert(0, "lib", col)

    # Parse key metrics from FLASH log

    with open(infile_flash_log) as f:
        for line in f:
            
            if "Total pairs:" in line:
                metrics["num_reads"] = int(line.split()[-1])

            elif "Combined pairs:" in line:
                metrics["num_reads_merged"] = int(line.split()[-1])

    # Calculate fraction merged
    metrics["frac_reads_merged"] = metrics["num_reads_merged"] / metrics["num_reads"]

    # Move read columns to left after lib
    col = metrics["num_reads"]
    metrics = metrics.drop(labels="num_reads", axis=1)
    metrics.insert(1, "num_reads", col)

    # Move frac columns to right
    col = metrics["frac_reads_merged"]
    metrics = metrics.drop(labels="frac_reads_merged", axis=1)
    metrics.insert(5, "frac_reads_merged", col)
    
    # Append to list
    dfs.append(metrics)

### Concatenate all files
metrics_all = pd.concat(dfs, axis=0)

### Write output file
metrics_all.to_csv(outfile, index=False, sep="\t")
