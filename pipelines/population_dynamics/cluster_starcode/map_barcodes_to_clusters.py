""" Map barcodes to cluster consensus sequences """

# Import packages
import sys
import os
import glob
import numpy as np
import pandas as pd

# Set input and output files

## Set input files
infile = sys.argv[1]  # clones.tsv.gz
wdir_starcode = sys.argv[2]  # starcode working directory containing output files from starcode named "*.out"

## Set output files
outfile_clones = sys.argv[3]  # clones.error_corrected.tsv.gz

# Load data (barcodes with counts)
counts_raw = pd.read_csv(infile, sep="\t", compression="gzip")

# Load starcode clustering results

## Find starcode output files
infiles = sorted(glob.glob(wdir_starcode + "/*.out"))

## Build mapping from (sample, library barcode, clone_barcode) to cluster consensus sequence

barcode_to_consensus = {}

for infile in infiles:

    lib = os.path.basename(infile).split(".")[1]  # Get library from filename
    library_barcode = os.path.basename(infile).split(".")[2]  # Get library index from filename

    with open(infile) as f:
        for line in f:

            fields = line.split("\t")

            consensus = fields[0]  # consensus sequence of cluster
            members = fields[2].rstrip().split(",")  # members of cluster

            key = (lib, library_barcode, consensus)
            barcode_to_consensus[key] = consensus

            for member in members:

                key = (lib, library_barcode, member)
                barcode_to_consensus[key] = consensus

# Map individual barcodes to their cluster consensus sequences

counts_raw = counts_raw.set_index(["lib", "library_barcode_call", "clone_barcode"])
keys = counts_raw.index

clone_barcode_consensus = []

for key in keys:
        
    try:
        consensus = barcode_to_consensus[key]
    except: 
        # consensus is not found, use barcode itself
        consensus = key[2]
    
    clone_barcode_consensus.append(consensus)

counts_raw["clone_barcode_consensus"] = clone_barcode_consensus

# Sum barcode counts for clusters
counts = counts_raw.reset_index().groupby(["lib", "library_barcode_call", "clone_barcode_consensus"])["count"].sum()

# Sort by sample

counts = counts.reset_index()

index_ordered = ["sFH11-1",
                "sFH11-2",
                "sFH11-3",
                "sFH11-4",
                "sFH11-5",
                "sFH11-6",
                "sFH11-7",
                "sFH11-8",
                "sFH11-9",
                "sFH11-10",
                "sFH11-11",
                "sFH11-12",
                "sFH11-13",
                "sFH11-14",
                "sFH11-15",
                "sFH11-16",
                "sFH11-17",
                "sFH11-18",
                "sFH11-19",
                "sFH11-20",
                "sFH11-21",
                "sFH12-9",
                "sFH12-10",
                "sFH12-11",
                "sFH12-12",
                "sFH12-13",
                "sFH12-14"]

## Filter to only keep rows from these experiments (drop rows that lack library annotation)
counts = counts.loc[counts["lib"].isin(index_ordered)]

## Convert lib to categorical for sorting
counts["lib"] = pd.Categorical(counts["lib"], categories=index_ordered, ordered=True)

## Sort rows
counts = counts.sort_values(by=["lib", "library_barcode_call", "count"], ascending=[True, True, False])

# Write output
counts.to_csv(outfile_clones, sep="\t", header=True, index=False)
