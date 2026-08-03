#!/usr/bin/env python
import bioinfo as bi
import argparse as arg
import matplotlib.pyplot as plt

def get_args():
    parser = arg.ArgumentParser(description="")
    parser.add_argument('-f', '--file', type = str, required=True)
    parser.add_argument("-d", "--file_descriptor" , type = str)
    return parser.parse_args()

args = get_args()
file = args.file
descript = args.file_descriptor

# Using functions from PS4

my_list, num_lines = bi.populate_list(file)

plt.scatter(range(101), my_list)
plt.xlabel("Base position") 
plt.ylabel("Phred quality score (mean)")
plt.title("Mean quality scores of base pairs by position in sequence")
plt.savefig(descript)