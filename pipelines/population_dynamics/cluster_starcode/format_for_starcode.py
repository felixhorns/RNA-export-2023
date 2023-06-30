""" Format sequences for input to Starcode. """

# Import packages
import sys
import numpy as np
import pandas as pd

# Set input and output files

## Set input file
infile = sys.argv[1]  # clones.tsv.gz

## Set output files
output_dir = sys.argv[2]  # output directory (temporary directory for Starcode)

# Load data (barcodes with counts)
counts_raw = pd.read_csv(infile, sep="\t", compression="gzip")

# Preprocess data

## Filter for library barcodes used in experiment

library_barcode_calls_to_keep = ["LB1", "LB2"]  # names of library barcodes to keep
counts = counts_raw.set_index(["lib", "library_barcode_call", "clone_barcode"])
counts = counts.loc[:, library_barcode_calls_to_keep, :]

## Reset index
counts = counts.reset_index()

# Write barcodes into files that are formatted for input to Starcode

for (lib, library_barcode_call), group in counts.groupby(["lib", "library_barcode_call"]):
    
    outfile = output_dir + "/" + "barcode_counts." + lib + "." + library_barcode_call + ".tsv.tmp"
    group_clean = group[["clone_barcode", "count"]]
    group_clean.to_csv(outfile, sep="\t", index=False, header=False)
