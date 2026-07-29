#!/usr/bin/env python

import bioinfo as bi
import argparse as arg
import itertools as it
import gzip

def get_args():
    parser = arg.ArgumentParser(description="Takes in 2 __ fastq files and 2 index __ fastq files, " \
    "the file name of the indexes, and the file location of the output")
    parser.add_argument('-r1', '--read_1', type = str, required=True)
    parser.add_argument('-i1', '--index_1', type = str, required=True)
    parser.add_argument('-r2', '--read_2', type = str, required=True)
    parser.add_argument('-i2', '--index_2', type = str, required=True)
    parser.add_argument('-f', '--indexes_file', type = str, required=True)
    parser.add_argument('-l', "--output_location", type = str, required=True)
    return parser.parse_args()

def write_output_file(fh, read_record: list, indx1:str, indx2:str):
    '''Takes in a file handle of a fastq file, and a list containing each line of a fastq record. Default index inputs are variables named index1 and index2.'''
    add_index_to_header = indx1 + "-" + indx2 + "\n"
    fh.write(read_record[0] + add_index_to_header)
    fh.write(read_record[1] + "\n")
    fh.write(read_record[2] + "\n")
    fh.write(read_record[3] + "\n") 

args = get_args()
read1 = args.read_1
read2 = args.read_2
index_R1 = args.index_1
index_R2 = args.index_2
output = args.output_location

index_file = args.indexes_file
single_indexes = []

with open(index_file, "rt") as inf:
    for index in inf:
        single_indexes.append(index)

index_pairs = it.product(single_indexes, repeat=2)
count_index_pairs = dict.fromkeys(index_pairs,0)

matched_files= {}
for inx in single_indexes:
    matched_files[str(inx)+"_R1"] = output + "/R1_" + str(inx) + ".fastq"
    matched_files[str(inx)+"_R2"] = output + "/R2_" + str(inx) + ".fastq"

r1 = gzip.open(read1,"rt")
r2 = gzip.open(read2,"rt")
i1 = gzip.open(index_R1, "rt")
i2 = gzip.open(index_R2, "rt")
hop_R1 = open(output + "/R1_hopped.fastq", "a")
hop_R2 = open(output + "/R2_hopped.fastq", "a")
unkn_R1 = open(output + "/R1_unknown.fastq", "a")
unkn_R2 = open(output + "/R2_unknown.fastq", "a")

for handle, name in matched_files.items():
    handle = open (name, "a")

count_matched_indices = 0
count_hopped_indices = 0
count_unknown = 0

while True:
    r1_rec = []
    r2_rec = []
    i1_rec = []
    i2_rec = []
    for i in range(4):
        r1_rec.append(r1.readline().strip()) 
        r2_rec.append(r2.readline().strip())
        i1_rec.append(i1.readline().strip())
        i2_rec.append(i2.readline().strip()) 
    if r1_rec == ["", "", "", ""]:
        break

    inx1 = i1_rec[1]
    inx2 = bi.reverse_complement(i2_rec[1])
    qual_i1 = bi.qual_score(i1_rec[3])
    qual_i2 = bi.qual_score(i2_rec[3])

    if "N" in inx2 or "N" in inx2: #or quality score stuff
        count_unknown += 1
        write_output_file(unkn_R1,read1,inx1,inx2)
        write_output_file(unkn_R2,read2,inx1,inx2)
    elif inx1==inx2 and inx1 in single_indexes:
        count_matched_indices += 1
        count_index_pairs[inx1,inx2] += 1
        out_R1 = inx1 + "_R1"
        out_R2 = inx2 + "_R2"
        write_output_file(out_R1,read1,inx1,inx2)
        write_output_file(out_R2,read2,inx1,inx2)

    elif inx1 in single_indexes and inx2 in single_indexes:
        count_hopped_indices += 1
        write_output_file(hop_R1,read1,inx1,inx2)
        write_output_file(hop_R2,read2,inx1,inx2)
    else:
        count_unknown += 1
        write_output_file(unkn_R1,read1,inx1,inx2)
        write_output_file(unkn_R2,read2,inx1,inx2)

r1.close()
r2.close()
i1.close()
i2.close()
hop_R1.close()
hop_R2.close()
unkn_R1.close()
unkn_R2.close()
#i do not know if this is how thats supposed to be done
for handle, name in matched_files.items():
    handle.close()

total = count_matched_indices + count_hopped_indices + count_unknown

print(f"Number of properly matched read-pairs: {count_matched_indices}")
print(f"Proportion of read-pairs that were properly matched: {count_matched_indices / total}")
print(f"Number of pairs with index-hopping observed: {count_hopped_indices}")
print(f"Proportion of read-pairs with index-hopping observed: {count_hopped_indices / total}")
print(f"Number of pairs with one or more unknown indices: {count_unknown}")
print(f"Proportion of read-pairs with one or more unknown indices: {count_unknown / total}")