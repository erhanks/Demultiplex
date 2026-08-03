#!/bin/bash

#SBATCH --time=5:00:00    
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8

LOC=/projects/bgmp/shared/2017_sequencing
R1=$LOC/1294_S1_L008_R1_001.fastq.gz
R2=$LOC/1294_S1_L008_R2_001.fastq.gz
R3=$LOC/1294_S1_L008_R3_001.fastq.gz
R4=$LOC/1294_S1_L008_R4_001.fastq.gz
TEST=/projects/bgmp/penhanks/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/R1.fq

#histograms

./part_1.py -f $TEST -d "TEST" -l 101 -u
#./part_1.py -f $R1 -d "Read_1" -l 101
#./part_1.py -f $R2 -d "Index_1" -l 8
#./part_1.py -f $R3 -d "Index_2" -l 8
#./part_1.py -f $R4 -d "Read_2" -l 101

#Indexes with Ns
#zcat $R2 | sed -n '2~4p' | grep "N" | wc
#zcat $R3 | sed -n '2~4p' | grep "N" | wc