""" Call library index based on sequence """

# Import packages
import sys
import numpy as np
import pandas as pd

# Set input and output files

## Set input file
infile = sys.argv[1]  # barcodes.tsv.gz

## Set output files
outfile_barcodes = sys.argv[2]  # barcodes.library_barcode_called.tsv.gz
outfile_clones = sys.argv[3]  # clones.tsv.gz
outfile_standards = sys.argv[4]  # counts_STD.tsv

# Define useful functions
def hamming_distance(s1, s2):
    """ Return the Hamming distance between equal-length sequences """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

# Load data (barcodes)

barcodes_raw = pd.read_csv(infile, sep="\t", compression="gzip")

# Preprocess data

## Filter for reads containing full-length barcodes
barcodes = barcodes_raw.loc[barcodes_raw.len_barcode == 32]

print("Reads with full-length barcodes:", 100 * barcodes.shape[0] / barcodes_raw.shape[0], "%")

# Map library barcode sequences to references

## Define reference library barcodes
reference_library_barcodes = {"LB1": "GGATG",
                              "LB2": "CTCAT",
                              "LB3": "TAGGA",
                              "LB4": "ACTCC",
                              "STD": "CCTAA"}

## Aggregate and count reads that share library barcodes
library_barcodes = barcodes.library_barcode.value_counts().reset_index()
library_barcodes = library_barcodes.rename(columns={"index": "library_barcode", "library_barcode": "count"})

## Calculate distance of each barcode to each reference
for key, ref_seq in reference_library_barcodes.items():
    column = "dist_to_" + key  # name of column    
    library_barcodes[column] = library_barcodes["library_barcode"].apply(lambda x: hamming_distance(x, ref_seq))
    
## Find nearest reference to each barcode
columns = ["dist_to_" + key for key in reference_library_barcodes.keys()]
library_barcodes["min_dist_to_ref"] = library_barcodes[columns].min(axis=1)

## Get name of nearest reference
library_barcodes["nearest_ref"] = library_barcodes[columns].idxmin(axis=1).str.replace("dist_to_", "")

## Call matches to reference

### Set flag to indicate successful call if minimum distance <= CUTOFF_MIN_DIST_TO_REF
CUTOFF_MIN_DIST_TO_REF = 0  # cutoff distance
library_barcodes["has_call"] = library_barcodes["min_dist_to_ref"] <= CUTOFF_MIN_DIST_TO_REF

### Set call (name of nearest reference barcode, if distance <= CUTOFF_MIN_DIST_TO_REF, else np.nan)
library_barcodes["call"] = np.nan
library_barcodes.loc[library_barcodes["has_call"], "call"] = library_barcodes.loc[library_barcodes["has_call"], "nearest_ref"]

# Map individual reads to reference

## Propagate mapping from unique barcodes to individual reads
barcodes["library_barcode_call"] = library_barcodes.set_index("library_barcode").loc[barcodes["library_barcode"], "call"].values

# Collapse reads into clones

## Group reads by sample and library barcode, then count unique clone barcodes
clones = barcodes.groupby(["lib", "library_barcode_call"])["clone_barcode"].value_counts()
clones.name = "count"
clones = clones.reset_index()

# Count spike-in standard reads per sample

clone_barcode_STD = "GACTGAGTCACTGTCAGACTGTCACTG"  # sequence of spike-in standard
selector = (barcodes["library_barcode"] == reference_library_barcodes["STD"]) & (barcodes["clone_barcode"] == clone_barcode_STD)
counts_STD = barcodes.loc[selector]["lib"].value_counts()  # count reads per sample

libs_ordered = ["sFH11-1",
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
# counts_STD = counts_STD[libs_ordered]  # reorder rows

# Write output files

## Write barcodes
barcodes.to_csv(outfile_barcodes, sep="\t", index=False)

## Write clones
clones.to_csv(outfile_clones, sep="\t", header=True, index=False)

## Write spike-in standard reads per sample
counts_STD.to_csv(outfile_standards, sep="\t", index=True, header=False)
