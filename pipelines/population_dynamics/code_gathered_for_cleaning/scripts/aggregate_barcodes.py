""" Aggregate parsed barcodes from multiple libraries """

import sys
import pandas as pd

infile = sys.argv[1]  # sample sheet (specifies library name and barcode file)
outfile = sys.argv[2]  # output file

### Load library names and files

names = []
infiles_barcodes = []

with open(infile) as f:
    for line in f:

        name = line.rstrip().split("\t")[0]
        input_dir = line.rstrip().split("\t")[1]
        infile_barcodes = input_dir + "/barcodes.tsv.gz"
        
        names.append(name)
        infiles_barcodes.append(infile_barcodes)

### Load files

dfs = []

for name, infile_barcodes in zip(names, infiles_barcodes):

    # Load reads
    barcodes = pd.read_csv(infile_barcodes, header=0, index_col=None, compression="gzip", sep="\t")

    # Set library name
    barcodes["lib"] = name

    # Move column to left
    col = barcodes["lib"]
    barcodes = barcodes.drop(labels="lib", axis=1)
    barcodes.insert(0, "lib", col)

    # Append to list
    dfs.append(barcodes)

### Concatenate all files
barcodes_all = pd.concat(dfs, axis=0)

### Write output file
barcodes_all.to_csv(outfile, index=False, sep="\t", compression="gzip")    

