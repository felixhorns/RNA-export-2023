# Transcriptomics pipeline

## Overview

To analyze RNA sequencing data of the whole transcriptome, we perform the following steps, which we refer to as preprocessing:

1. Map the sequencing reads to a reference.
2. Count reads mapping to features (such as genes).
3. Aggregate results from multiple samples.

This pipeline implements these steps using:

1. STAR for alignment.
2. htseq for counting reads mapping to features.

This workflow is managed by Snakemake. In addition, we use custom scripts writen in Bash and Python to generate seedfiles, deploy the pipeline, and aggregate the results.

The output of the pipeline is:
1. Counts of reads mapping to features for each sample (tab-separated text) (`htseq.tab`).
2. Metrics of alignment for each sample (tab-separated text) (`STAR.tab`).

## Citation

If you use this code, please cite this paper.

Horns *et al.*, Engineering RNA export for measurement and manipulation of living cells, *Cell* **186** (2023).

## Configuration

### Environment

Python 3.7.7 is the primary environment. Required packages include Conda, Snakemake, and htseq. All required packages are specified in `environment.txt`, which can be used to create an environment using Conda.

STAR is a sequence aligner that is required. STAR may be installed from `https://github.com/alexdobin/STAR`.

### Data

RNA sequencing data from our paper can be downloaded from either CaltechDATA or the Sequence Read Archive (SRA) of the National Center for Biotechnology Information (NCBI) (accession PRJNA934101).

We recommend moving each sample into its own directory for preprocessing. This pipeline treats the all reads within a directory together as a sample. The directory name is the sample name. If you download the data from Data.Caltech, the reads are already organized in this way.

For example, all of the following reads would be preprocessed as "Sample1":
`/path/to/sequencing_data/Sample1/R1.fastq.gz`
`/path/to/sequencing_data/Sample1/R2.fastq.gz`

## Using the transcriptomics pipeline

### Generate genome reference

The genome reference is provided in `resources/STAR_genome_references/GRCh38.103-ERCC92-Transgenes_210814`.

Alternatively, if you wish to use a different genome reference, you can generate it using the script `STAR_genomeGenerate.sh`.

### Make seedfile

The seedfile `seedfile.txt` is a list of all directories that will be processed. To conveniently generate this seedfile, we use `make_seedfile.py`, which crawls a specified directory, identifies all subdirectories that contain sequencing read files (`*.fastq.gz`), and lists them.

To deploy this generator, we use `make_seedfile.sh` via these steps.

Update variables specifying paths in `make_seedfile.sh`.
* `MY_HOME`, the home directory for analysis.
* `MAKE_SEEDFILE`, the script `make_seedfile.py`.
* Paths to the directories containing sequencing read files (`*.fastq.gz`).
* Paths to the seedfile output `seedfile.txt`.

Run:
`source make_seedfile.sh`

### Run pipeline

The main workflow, managed by Snakemake, performs the following steps:
1. Unzip and concatenate fastq files.
2. Map reads to reference using STAR.
3. Count reads mapping to features using htseq.
4. Delete uncompressed reads (clean up).

This is specified in `Snakefile.py`.

To do this, perform the following steps.

1. Update variables specifying paths in `Snakefile.py`.
* `MY_HOME`
* `PATH_TO_ANACONDA`, path to Conda install containing environment.
* `STAR`, path to `STAR` executable within STAR installation.
* `HTSEQ_COUNT`, path to `count.py` within htseq installation.
* `GENOMEDIR`, path to genome reference.
* `REFERENCE_ANNOTATION`, path to genome reference annotation (`*.gtf`).
* `SEEDFILE`, path to seedfile.

2. Update variables specifying resources in `Snakefile.py` (optional).
To choose how many threads and how much memory should be allocated to jobs, you can edit the `threads` and `mem` variables in `Snakefile.py`. STAR can be accelerated by providing large amounts of memory, especially when using large genome references.

3. Update variables specifying paths in `do.sh`.
* `MY_HOME`
* `SNAKEFILE`, path to `Snakefile.py`.

4. Recommended: Test your run by performing a dry run in Snakemake. Uncomment the "dryrun" line and comment the "run" line in `do.sh`. Run using `source do.sh`. This will list all jobs that Snakemake will run. If this is satisfactory, proceed with running.

5. Run snakemake. Comment the "dryrun" line and uncomment the "run" line in `do.sh`. Run using `source do.sh`.

Progress is written to a log file at `MY_HOME/log/Snakefile.time_of_run.log`. To monitor progress, this command is useful: `watch tail -n30 /path/to/logfile.log`.

### Aggregate samples

To aggregate the results across samples, we use `make_summary.sh` via the following steps.

1. Update variables in `make_summary.sh`.
* `MAKE_HTSEQ_TABLE`, path to `make_htseq_table.py`.
* `MAKE_STAR_TABLE`, path to `make_STAR_table.py`.
* Paths to output files `htseq.tab` and `STAR.tab`.

2. Perform aggregation: `source make_summary.sh`

## Disclaimer

This project is not maintained. Software is provided as is and requests for support may not be addressed.

## Contact

If you have questions or comments, please contact Felix Horns at rfhorns@gmail.com.
