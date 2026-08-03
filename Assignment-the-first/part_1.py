#!/usr/bin/env python
import bioinfo as bi
import argparse as arg
import matplotlib.pyplot as plt

def get_args():
    parser = arg.ArgumentParser(description="")
    parser.add_argument('-f', '--file', type = str, required=True)
    parser.add_argument("-d", "--file_descriptor" , type = str, required = True)
    parser.add_argument("-l", "--length_of_read", type = int, required = True)
    parser.add_argument("-u", "--uncompressed", action="store_false")
    return parser.parse_args()

args = get_args()
file = args.file
descript = args.file_descriptor
lent = args.length_of_read
uncomp = args.uncompressed

# Using functions from PS4

sum_score, num_lines = bi.populate_list(file, compressed=uncomp, lent=lent)

avg_score = []
avg_score = bi.init_list(avg_score, lent=lent)
for i,chr in enumerate(sum_score):
    avg_score[i] = (chr/(num_lines/4))

plt.scatter(range(lent), avg_score)
plt.xlabel("Base position") 
plt.ylabel("Phred quality score (mean)")
plt.title("Mean quality scores of base pairs by position in sequence")
plt.savefig(descript)