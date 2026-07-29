# Objective:
 Determine if a pair of reads had index-hopping occur, and add the corresponding fastq records to files for each correct pair of indices, for hopped indices, and for unknown indices.  


# DEFINITIONS

```
def reverse_complement(DNA: str) -> str:
    ''' Takes in a 5'-3' string of DNA and outputs a string of the 5'-3' reverse complement.'''
    bases = dict with bases as keys and complementary base as value
    for letter in DNA:
        complement += bases[letter]
    reverse(complement)
    return complement
```
Input: "ATGC"

Expected output: "GCAT"

```
def write_output_file(file_handle: str, read_record: lst, ix1 = index1: str, ix2 = index2: str)
    ''' Takes in a file handle of a fastq file, and a list containing each line of a fastq record. Default index inputs are variables named index1 and index2.'''

    add_index_to_header = ix1 + "-" + ix2 
    write/append (read_record[header] + add_index_to header) to file_handle
    write/append (read_record[sequence, + line, quality scores]) to file_handle
```
Input: fh, read1_record

Expected output: lines from read1_record appended to the end of fh, with the indexes added to the header line


# ALGORITHM
```
Open fastq files:
- for reading
    - both read files
    - both index files
- for writing
    - R1_
        - file per index in index_list
        - hopped_indices
        - unknown_indices 
    - R2_
        - file per index in index_list
        - hopped_indices
        - unknown_indices

Open index_file (text file)
    index_dict = {}
    for index in index_file
        add index to index_dict as keys with values of 0
    index_list = keys_from(index_dict)

count_matched_indices = 0
count_hopped_indices = 0
count_unknown = 0

dict_hopped_indices = {}
for this_index in index_list:
    index_list_without_this_index = index_list.pop(index)
    for that_index in index_list_without_this_index:
        add this_index, that_index to dict_hopped_indices as keys with values of 0
#look into itertools

While true loop:

    read1_record = []
    read2_record= []
    index1_record = []
    index2_record = []

    if the next line isn't empty:
        add next four lines of each file to each empty list (dont forget to strip)
    else:
        exit while loop

    index1 = sequence from index1_record
    index2 = reverse_complement(sequence from index2_record)

    quality_score1 = index1_record[3]
    quality_score2 = index2_record[3]

    quality_threshold = (determine in part 1)

    #do average quality score

    if index1 or index2 contains "N" or quality_score1 or quality_score2 is below quality_threshold:
        count_unknown += 1
        write_output_file(R1_unknown_indices, read1_record)
        write_output_file(R2_unknown_indices, read2_record)

    elif indexes match and index1 is in index_list:
        count_matched_indices += 1
        index_dict[index1] += 1
        
        write_output_file(R1_index1, read1_record)
        write_output_file(R2_index1, read2_record)

    elif index1 and index2 are in index_list:
        count_hopped_indices += 1
        dict_hopped_indices[index1, index2] += 1

        write_output_file(R1_hopped_indices, read1_record)
        write_output_file(R2_hopped_indices, read2_record)

    else:
        count_unknown += 1
        write_output_file(R1_unknown_indices, read1_record)
        write_output_file(R2_unknown_indices, read2_record)

```

# Outputs
## Print:
Number of properly matched read-pairs: {value}
Proportion of read-pairs that were properly matched: {value/total}

Number of pairs with index-hopping observed: {value}
Proportion of read-pairs with index-hopping observed: {value/total}

Number of pairs with one or more unknown indices: {value}
Proportion of read-pairs with one or more unknown indices: {value/total}

## Graph: 
Histogram or bar graph of index_dict
Histogram or bar graph of dict_hopped_indices
Histogram or bar graph of index_dict and dict_hopped_indices
