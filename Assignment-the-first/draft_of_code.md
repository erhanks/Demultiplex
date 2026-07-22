index_list = []
with open (index_file.txt)
    for line in index_file
        index_list.append(line)

with open (read1)
with open (read2)
with open (index1)
with open (index2)

count_matched = 0
count_hopped = 0
count_unkn = 0

while True: (look thru all the lines at the same time)

r1_rec = []
r2_rec = []
i1_rec = []
i2_rec = []

r1_rec.append(read1.readline().strip('n')) times 4
r2_rec.append(read2.readline().strip('n')) times 4
i1_rec.append(index1.readline().strip('n')) times 4
i2_rec.append(index2.readline().strip('n')) times 4

ind1 = i1_rec[1]
ind2 = i2_rec[2]

    
if ind1==ind2 and ind1 is in index_list:
    count_matched += 1
    fh = open("./{index}_R1", a)
        fh.write(r1_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r1_rec[1,2,3] + "\n")
    fh.close()
    
    fh = open("./{index}_R2", a)
        fh.write(r2_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r2_rec[1,2,3] + "\n")
    fh.close()

elif index1 and index2 are in index_list:
    count_hopped += 1
    fh = open("./hopped_R1", a)
        fh.write(r1_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r1_rec[1,2,3] + "\n")
    fh.close()
    
    fh = open("./hopped_R2", a)
        fh.write(r2_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r2_rec[1,2,3] + "\n")
    fh.close()
else:
    count_unkn += 1
    fh = open("./unkn_R1", a)
        fh.write(r1_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r1_rec[1,2,3] + "\n")
    fh.close()
    
    fh = open("./unkn_R2", a)
        fh.write(r2_rec[0] + " " + ind1 + "-" + ind2 + "\n")
        fh.write(r2_rec[1,2,3] + "\n")
    fh.close()

