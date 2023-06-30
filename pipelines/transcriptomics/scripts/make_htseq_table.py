# Aggregate count outputs of htseq into a file
#
# Inputs: directory containing htseq output files (htseq.tab) and path to output file.
# Outputs: tab-separated text file containing counts from all input files.
#
# Crawl directory to find all htseq.tab files contained within it.
# Parse counts from each of those files.
# Combine counts from all files into a table written into output file.

import sys
import fnmatch
import os

dir = sys.argv[1] # directory containing htseq output files (htseq.tab)
outfile = sys.argv[2] # output file

# Find all htseq.tab files within directory
matches = []
for root, dirnames, filenames in os.walk(dir):
    for filename in fnmatch.filter(filenames, 'htseq.tab'):
        matches.append(root+"/"+filename) # full path of match

matches = sorted(matches)  # sort filenames
        
# Print directory containing each file
print(len(matches), "files")

# Get gene list from first column of first file (assumes that gene lists are the same for all files)
genes = []
with open(matches[0]) as f:
    for line in f:
        gene = line.rstrip().split("\t")[0]
        genes.append(gene)

# Get counts from each file
samples = []
counts = []

for match in matches:

    sample = match.split("/")[-3]

    with open(match) as f:
        
        my_counts = []
        
        for line in f:
            count = line.rstrip().split("\t")[1]
            my_counts.append(count)

    samples.append(sample)
    counts.append(my_counts)

# Print output
with open(outfile, 'w') as out:

    header = ["symbol"] + samples # header
    out.write("\t".join(header) + "\n")

    for i in range(len(genes)):

        my_counts = [counts[x][i] for x in range(len(counts))]
        line = "\t".join([genes[i]] + my_counts)
        out.write(line + "\n")
