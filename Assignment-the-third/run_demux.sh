#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp

LOC=/projects/bgmp/shared/2017_sequencing
R1=$LOC/1294_S1_L008_R1_001.fastq.gz
R2=$LOC/1294_S1_L008_R2_001.fastq.gz
R3=$LOC/1294_S1_L008_R3_001.fastq.gz
R4=$LOC/1294_S1_L008_R4_001.fastq.gz
INDEX=/projects/bgmp/shared/2017_sequencing/indexes.txt
OUT=/scratch/bgmp/penhanks/Demultiplex_out/

/usr/bin/time -v ./demux.py -f $R1 -fi $R2 -ri $R3 -r $R4 -i $INDEX -l $OUT