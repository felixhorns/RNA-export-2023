# Execute aggregating outputs from htseq and STAR.
# Helper script that calls make_htseq_table.py and make_STAR_table.py

MY_HOME=/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023  # path to home directory for analysis
MAKE_HTSEQ_TABLE=$MY_HOME/pipelines/transcriptomics/scripts/make_htseq_table.py  # path to script that aggregates htseq outputs
MAKE_STAR_TABLE=$MY_HOME/pipelines/transcriptomics/scripts/make_STAR_table.py  # path to script that aggregates STAR outputs

# Activate conda environment
conda activate CellFreeReporter

# Make htseq table

python $MAKE_HTSEQ_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_supernatant/ /scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/transcriptomics/temp_output_for_test/htseq_sup.tab

python $MAKE_HTSEQ_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_cell/ /scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/transcriptomics/temp_output_for_test/htseq_cell.tab

# Make STAR table

python $MAKE_STAR_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_supernatant/ /scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/transcriptomics/temp_output_for_test/STAR_sup.tab

python $MAKE_STAR_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_cell/ /scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/transcriptomics/temp_output_for_test/STAR_cell.tab


# Make htseq table

# python $MAKE_HTSEQ_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_supernatant/ $MY_HOME/preprocessed_data/transcriptome_data/transcriptomics_supernatant/htseq.tab

# python $MAKE_HTSEQ_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_cell/ $MY_HOME/preprocessed_data/transcriptome_data/transcriptomics_cell/htseq.tab

# Make STAR table

# python $MAKE_STAR_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_supernatant/ $MY_HOME/preprocessed_data/transcriptome_data/transcriptomics_supernatant/STAR.tab

# python $MAKE_STAR_TABLE $MY_HOME/sequencing_data_preprocessing/transcriptomics_cell/ $MY_HOME/preprocessed_data/transcriptome_data/transcriptomics_cell/STAR.tab
