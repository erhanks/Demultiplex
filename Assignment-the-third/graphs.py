#!/usr/bin/env python

import bioinfo as bi
import argparse as arg
import matplotlib.pyplot as plt
import numpy as np

axes = []
with open("/scratch/bgmp/penhanks/Demultiplex_out/count_index_pairs.tsv") as fh:
    for line in fh:
        line_lst = line.strip().split()
        if line_lst[0] not in axes:
            axes.append(line_lst[0])

with open("/scratch/bgmp/penhanks/Demultiplex_out/count_index_pairs.tsv") as fh:
    matched = []
    heatmap_values = np.zeros((24,24), dtype=int)
    for line in fh:
        line_lst = line.strip().split()
        x = axes.index(line_lst[0]) 
        #print(x)
        y = axes.index(line_lst[1])
        #print(y)
        heatmap_values[x,y] = line_lst[2]
        if x == y:
            matched.append(int(line_lst[2]))

for i,val in enumerate(matched):
    print(f'{round(val/331757402 * 100,3)}% of the total matched reads were from index {axes[i]}')

fig,ax = plt.subplots()
im = ax.imshow(heatmap_values)
ax.set_xticks(range(24),axes, rotation=45,rotation_mode="xtick")
plt.yticks(range(24),axes)
plt.tick_params(axis="both", labelsize = 7)
plt.title("Heatmap of index pair frequencies")
plt.ylabel("Index")
plt.savefig("heatmap")

fig,ax = plt.subplots()
plt.bar(axes, matched)
ax.set_xticks(range(24),axes, rotation=45,rotation_mode="xtick")
plt.tick_params(axis="x", labelsize = 7)
plt.yscale("log")
plt.title("Frequencies of matched indices")
plt.ylabel("Number of appearances (log scale)")
plt.savefig("matched_bar")

