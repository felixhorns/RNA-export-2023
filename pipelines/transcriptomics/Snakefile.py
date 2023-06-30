include: "Snakefile_utils.py"

##### Paths
MY_HOME=                      '/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023'
workdir:                      MY_HOME+'/log'

PATH_TO_ANACONDA=             '/scratch/resources/'
ANACONDA=		      PATH_TO_ANACONDA+'/anaconda3/envs/RNA_export_magic'
ANACONDA_ACTIVATE=            PATH_TO_ANACONDA+'/anaconda3/bin/activate'

RESOURCES=                    MY_HOME+'/resources'
STAR=                         RESOURCES+'/STAR-2.7.8a/bin/Linux_x86_64/STAR'
HTSEQ_COUNT=                  RESOURCES+'/htseq-0.13.5/HTSeq/scripts/count.py'

##### Parameters
REFS=                         MY_HOME+'/resources/STAR_genome_references'
GENOMEDIR=                    REFS+'/GRCh38.103-ERCC92-Transgenes_210814/'
REFERENCE_ANNOTATION=         REFS+'/GRCh38.103-ERCC92-Transgenes_210814/GRCh38.103-ERCC92-Transgenes_210814.gtf'

SEEDFILE=                     '/scratch/CellFreeReporter/magic_Horns_RNA_Export_2023/pipelines/transcriptomics/seedfile.txt'

# Load samples
SEEDS = []
with open(SEEDFILE) as f:
    for line in f:
        SEEDS.append(line.strip())

##### Rules

rule all:
  input: expand("{dir}/done", dir=SEEDS)
  params: name='all', partition='general', mem='1024'

rule zcat_R1:
  """ Concatenate fastq files """
  input: get_all_fastq_gzs_R1
  output: temp('{dir}/R1.fastq')
  params: name='zcat', partition="general", mem="5300"
  shell: 'zcat {input} > {output[0]}'

rule zcat_R2:
  """ Concatenate fastq files """
  input: get_all_fastq_gzs_R2
  output: temp('{dir}/R2.fastq')
  params: name='zcat', partition="general", mem="5300"
  shell: 'zcat {input} > {output[0]}'
  
rule star:
  """ Map reads to genome using STAR  """
  input:  rules.zcat_R1.output, rules.zcat_R2.output
  output: '{dir}/STAR_output/Aligned.sortedByCoord.out.bam'
  params: name='star', partition='general', mem='64000'
  threads: 12
  run:
      wdir = os.path.dirname(str(output[0])) + '/'
      shell("{STAR} "
            "--genomeDir {GENOMEDIR} "
            "--readFilesIn {input[0]} {input[1]} "
            "--runThreadN {threads} "
            "--outFileNamePrefix {wdir} "
            "--outSAMtype BAM SortedByCoordinate "
            "--outSAMattributes NH HI AS NM MD "
            "--outReadsUnmapped Fastx "
            "--outFilterMultimapNmax 20 "
            "--outFilterScoreMinOverLread 0.3 "
            "--outFilterMatchNminOverLread 0.3 "
            "--outFilterMismatchNmax 20 "
            "--outFilterMismatchNoverLmax 0.3 "
            "--alignIntronMin 20 "
            "--alignIntronMax 1000000 "
            "--alignMatesGapMax 1000000 "
            "--alignSJoverhangMin 5 "
            "--alignSJDBoverhangMin 3 ")

rule htseq:
  """ Count reads mapping to features using htseq """
  input:  rules.star.output
  output: '{dir}/htseq_output/htseq.tab'
  params: name='htseq', partition='general', mem='5300'
  shell: "set +eu && source {ANACONDA_ACTIVATE} {ANACONDA} && "
         "python {HTSEQ_COUNT} -s no -r pos -f bam -m intersection-strict "
         "{input} {REFERENCE_ANNOTATION} > {output}"

rule clean:
  input: rules.htseq.output
  output: "{dir}/done"
  params: name='all', partition='general', mem='1024'
  shell: 'touch {output[0]}'
