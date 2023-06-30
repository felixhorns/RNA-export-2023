# Generate seedfile for RNA-seq preprocessing pipeline.
#
# Input: directory containing read files (*.fastq.gz).
# Output: full paths to each subdirectory containing read files to standard out.
#
# Crawl directory to find all subdirectories containing read files (*.fastq.gz).
# Print full path to each subdirectory found.

import sys
import fnmatch
import os

dir = sys.argv[1] # directory containing samples (*.fastq.gz)

# Find all *.fastq.gz files within directory
matches = []
for root, dirnames, filenames in os.walk(dir):
    for filename in fnmatch.filter(filenames, '*.fastq.gz'):
        if "_R1" in filename:
            matches.append(root) # directory of match
            # matches.append(os.path.join(root, filename)) # full path to match
            
# Print directory containing each file
for x in sorted(matches):
    print(x)
