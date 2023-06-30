# Execute generating seedfile for RNA-seq preprocessing pipeline.
# Helper script that calls make_seedfile.py.

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023  # path to home directory for analysis
MAKE_SEEDFILE=$MY_HOME/pipelines/transcriptomics/scripts/make_seedfile.py  # path to script that generates seedfile

# Make seedfile for supernatant RNA-seq samples
python $MAKE_SEEDFILE $MY_HOME/sequencing_data_preprocessing/transcriptomics_supernatant > $MY_HOME/pipelines/transcriptomics/seedfile.txt

# Append seedfile for cellular RNA-seq samples
python $MAKE_SEEDFILE $MY_HOME/sequencing_data_preprocessing/transcriptomics_cell >> $MY_HOME/pipelines/transcriptomics/seedfile.txt
