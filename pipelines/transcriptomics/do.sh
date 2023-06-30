#!/bin/bash

conda activate RNA_export_magic  # activate Conda environment

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023  # path to home directory for analysis
SNAKEFILE=$MY_HOME/pipelines/transcriptomics/Snakefile.py

# Specify log file
DATETIME=$(date "+%Y_%m_%d_%H_%M_%S")
LOGFILE=$MY_HOME/log/Snakefile.$DATETIME.log

# Unlock dir
# snakemake all --snakefile $SNAKEFILE --configfile $CONFIGFILE --cluster "sbatch --ntasks=1 --job-name={params.name} --cpus-per-task={threads} --partition={params.partition} --mem={params.mem} -o {params.name}.%j.log" --keep-target-files -j 200 -w 100 -k -r -n --rerun-incomplete --unlock

# Dry run snakemake
# snakemake all --snakefile $SNAKEFILE --keep-target-files --cores 12 --latency-wait 10 --keep-going --reason --rerun-incomplete --dryrun

# Run snakemake
nohup snakemake all --snakefile $SNAKEFILE --keep-target-files --cores 12 --latency-wait 10 --keep-going --reason --rerun-incomplete > $LOGFILE &

echo Log is
echo $LOGFILE
echo
