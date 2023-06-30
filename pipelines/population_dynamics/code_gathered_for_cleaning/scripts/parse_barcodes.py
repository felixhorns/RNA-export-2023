""" Parse barcodes from merged reads """

import sys
import gzip
from Bio import SeqIO
import numpy as np
import pandas as pd

infile = sys.argv[1]  # merged reads from FLASH (out.extendedFrags.fastq.gz)
output_dir = sys.argv[2]  # output directory (output file will be output_dir/barcodes.tsv.gz)

outfile = output_dir + "/barcodes.tsv.gz"
outfile_metrics = output_dir + "/parse_barcode_metrics.tsv"

SEQ_FLANK_5P = "GCGGCCGC"  # 5' of BC in reference direction (encompassing NotI)
SEQ_FLANK_3P = "GGCGCGCC"  # 3' of BC in reference direction (encompassing SgsI)

MAX_INPUT_READS = -1  # maximum number of input reads (limits number of reads processed if >-1) (useful for debugging)

### Load reads

ids = []
seqs = []

i = 0

with gzip.open(infile, "rt") as handle:

    for record in SeqIO.parse(handle, "fastq"):

        ids.append(record.id)
        seqs.append(str(record.seq))

        i += 1
        if (MAX_INPUT_READS > -1) and (i >= MAX_INPUT_READS): break
        
reads = pd.DataFrame(data={"id": ids, "seq": seqs})

### Find barcode flanking sequences
reads["pos_seq_flank_5p"] = reads["seq"].str.find(SEQ_FLANK_5P)
reads["pos_seq_flank_3p"] = reads["seq"].str.find(SEQ_FLANK_3P)

### Filter for reads having both flanking sequences
reads["flank_hit"] = (reads["pos_seq_flank_5p"] >= 0) & (reads["pos_seq_flank_3p"] >= 0)

### Extract barcode by getting substring between flanking sequences, and split into library and clone barcodes

reads["barcode"] = np.nan  # initialize all reads with empty barcode

reads_subset = reads.loc[reads["flank_hit"] == True]  # get subset of reads with flanking sequence hit

# Slice sequence to get barcode sequence, split to extract library and clone barcodes

barcodes = []
library_barcodes = []
clone_barcodes = []

for seq, pos_flank_5p, pos_flank_3p in zip(reads_subset["seq"], reads_subset["pos_seq_flank_5p"], reads_subset["pos_seq_flank_3p"]):
    
    start_index = pos_flank_5p + len(SEQ_FLANK_5P)
    end_index = pos_flank_3p
    
    barcode = seq[start_index:end_index]

    library_barcode = barcode[-5:]  # library barcode is final 5 bp
    clone_barcode = barcode[:-5]  # clone barcode is everything before final 5 bp

    barcodes.append(barcode)
    library_barcodes.append(library_barcode)
    clone_barcodes.append(clone_barcode)

reads.loc[reads["flank_hit"] == True, "barcode"] = barcodes
reads.loc[reads["flank_hit"] == True, "library_barcode"] = library_barcodes
reads.loc[reads["flank_hit"] == True, "clone_barcode"] = clone_barcodes

### Calculate length of barcodes
reads["len_barcode"] = reads.barcode.str.len()
reads["len_library_barcode"] = reads.library_barcode.str.len()
reads["len_clone_barcode"] = reads.clone_barcode.str.len()

### Set flag for full-length barcodes
reads["full_length_barcode"] = np.nan
reads["full_length_barcode"] = reads.len_clone_barcode == 27  # full-length clone barcode is 27 bp

### Calculate metrics
metrics = pd.DataFrame(index=[0])
metrics["num_reads_merged"] = reads.shape[0]
metrics["num_reads_flank_hit"] = sum(reads["flank_hit"])
metrics["num_reads_full_length_barcode"] = sum(reads["full_length_barcode"])
metrics["frac_reads_flank_hit"] = np.mean(reads["flank_hit"])
metrics["frac_reads_full_length_barcode"] = np.mean(reads["full_length_barcode"])

### Write output file
reads.to_csv(outfile, index=False, sep="\t", compression="gzip")

### Write metrics to output file
metrics.to_csv(outfile_metrics, index=False, sep="\t")
