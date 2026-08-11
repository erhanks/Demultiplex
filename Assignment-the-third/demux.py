#!/usr/bin/env python

import bioinfo as bi
import argparse as arg
import itertools as it
import gzip
from typing import TextIO

## CHANGE READ 1 TO FORWARD
## CHANGE READ 2 TO REVERSE
## CHANGE INDEX 1 TO FORWARD INDEX
## CHANGE INDEX 2 TO REVERSE INDEX

def get_args():
    parser = arg.ArgumentParser(description="Takes in 2 read fastq files and 2 index fastq files, " \
    "the file name of the indexes, and the folder location of the output")
    parser.add_argument('-f', '--forward_read', type = str, required=True)
    parser.add_argument('-fi', '--forward_index', type = str, required=True)
    parser.add_argument('-r', '--reverse_read', type = str, required=True)
    parser.add_argument('-ri', '--reverse_index', type = str, required=True)
    parser.add_argument('-i', '--indexes_file', type = str, required=True)
    parser.add_argument('-l', "--output_location", type = str, required=True)
    parser.add_argument("-u", "--uncompressed", action="store_true")
    return parser.parse_args()

def write_output_file(fh, read_record: list, indx1:str, indx2:str):
    '''Takes in a file handle of a fastq file, and a list containing each line of a fastq record. Default index inputs are variables named index1 and index2.'''
    add_index_to_header = " " + indx1 + "-" + indx2 + "\n"
    fh.write(read_record[0] + add_index_to_header)
    fh.write(read_record[1] + "\n")
    fh.write(read_record[2] + "\n")
    fh.write(read_record[3] + "\n") 

args = get_args()
fow = args.forward_read
rev = args.reverse_read
index_forward = args.forward_index
index_reverse = args.reverse_index
output = args.output_location
uncomp = args.uncompressed
min_qual = 33

index_file = args.indexes_file
single_indexes = set() #to make it easier to find things in it

with open(index_file, "rt") as inf:
    for line in inf:
        line = line.strip().split()
        if line[4].isupper():
            single_indexes.add(line[4])
#print(single_indexes)
index_pairs = it.product(single_indexes, repeat=2)
count_index_pairs = dict.fromkeys(index_pairs,0)

handle_f = {}
handle_r = {}
file_loc_f = {}
file_loc_r = {}

for inx in single_indexes:
    file_loc_f[inx] = output + "forward_" + str(inx) + ".fastq"
    file_loc_r[inx] = output + "reverse_" + str(inx) + ".fastq"

for index, name in file_loc_f.items():
    handle = open (name, "w")
    handle_f[index] = handle
for index, name in file_loc_r.items():
    handle = open (name, "w")
    handle_r[index] = handle

if uncomp:
    r1 = open(fow, "rt")
    r2 = open(rev, "rt")
    i1 = open(index_forward, "rt")
    i2 = open(index_reverse, "rt")
else:
    r1 = gzip.open(fow, "rt")
    r2 = gzip.open(rev, "rt")
    i1 = gzip.open(index_forward, "rt")
    i2 = gzip.open(index_reverse, "rt")

hop_f = open(output + "/forward_hopped.fastq", "w")
hop_r = open(output + "/reverse_hopped.fastq", "w")
unkn_f = open(output + "/forward_unknown.fastq", "w")
unkn_r = open(output + "/reverse_unknown.fastq", "w")

count_matched_indices = 0
count_hopped_indices = 0
count_unknown = 0

while True:
    #opening lists to store the fast q records
    f_rec = []
    r_rec = []
    fi_rec = []
    ri_rec = []

    #reading 4 lines
    for i in range(4):
        f_rec.append(r1.readline().strip()) 
        r_rec.append(r2.readline().strip())
        fi_rec.append(i1.readline().strip())
        ri_rec.append(i2.readline().strip()) 
    if f_rec == ["", "", "", ""]:
        break

    #storing indexes and index quality scores
    inx_fow = fi_rec[1]
    inx_rev = bi.reverse_complement(ri_rec[1])
    qual_i1 = bi.qual_score(fi_rec[3])
    qual_i2 = bi.qual_score(ri_rec[3])
    #print(qual_i1)
    #print(qual_i2)
    if inx_fow[1:] == inx_rev[:7]:
        inx_fow = inx_rev[:7] + inx_fow[7]
    if "N" in inx_rev or "N" in inx_rev:
        if inx_fow[1:] == inx_rev[:7] and "N" not in inx_rev[:7] and qual_i1>min_qual and qual_i2>min_qual:
            corrected_inx = inx_rev[:7] + inx_fow[7]
            if corrected_inx in single_indexes:
                inx_fow = corrected_inx
                inx_rev = corrected_inx

                count_matched_indices += 1
                count_index_pairs[inx_fow, inx_rev] += 1
                
                write_output_file(handle_f[inx_fow], f_rec, inx_fow, inx_rev)
                write_output_file(handle_r[inx_rev], r_rec, inx_fow, inx_rev)
        else:
            count_unknown += 1
            write_output_file(unkn_f, f_rec, inx_fow, inx_rev)
            write_output_file(unkn_r, r_rec, inx_fow, inx_rev)

    #they match
    elif inx_fow==inx_rev and inx_fow in single_indexes:
        count_matched_indices += 1
        count_index_pairs[inx_fow, inx_rev] += 1

        write_output_file(handle_f[inx_fow], f_rec, inx_fow, inx_rev)
        write_output_file(handle_r[inx_rev], r_rec, inx_fow, inx_rev)

    #they don't match but theyre in there
    elif inx_fow in single_indexes and inx_rev in single_indexes:
        count_hopped_indices += 1
        count_index_pairs[inx_fow, inx_rev] += 1
        write_output_file(hop_f, f_rec, inx_fow, inx_rev)
        write_output_file(hop_r, r_rec, inx_fow, inx_rev)
    else:
        count_unknown += 1
        write_output_file(unkn_f, f_rec, inx_fow, inx_rev)
        write_output_file(unkn_r, r_rec, inx_fow, inx_rev)

r1.close()
r2.close()
i1.close()
i2.close()
hop_f.close()
hop_r.close()
unkn_f.close()
unkn_r.close()

for index, handle in handle_f.items():
    handle.close()
for index,handle in handle_r.items():
    handle.close()

total = count_matched_indices + count_hopped_indices + count_unknown

with open(output + "/count_index_pairs.tsv", "w") as ct:
    for pair, count in count_index_pairs.items():
        ct.write(f"{pair[0]}\t{pair[1]}\t{count}\n")


#print(count_index_pairs)
print(f"Number of properly matched read-pairs: {count_matched_indices}")
print(f"Proportion of read-pairs that were properly matched: {count_matched_indices / total}")
print(f"Number of pairs with index-hopping observed: {count_hopped_indices}")
print(f"Proportion of read-pairs with index-hopping observed: {count_hopped_indices / total}")
print(f"Number of pairs with one or more unknown indices: {count_unknown}")
print(f"Proportion of read-pairs with one or more unknown indices: {count_unknown / total}")