# Objective:
 Determine if a pair of reads had index-hopping occur, and add the corresponding fastq records to files for each correct pair of indices, for hopped indices, and for unknown indices.  


# DEFINITIONS

```
def reverse_complement(DNA: str) -> str:
    ''' Takes in a 5'-3' string of DNA and outputs a string of the 5'-3' reverse complement. Case insensitive.'''
    return reverse
```
Input: "ATGC"

Expected output: "GCAT"

```
def write_output_file(file_handle: str, read_record: lst)
    ''' Takes in a file handle and a list containing each line of a record
    '''
    add_index_to_header = index1 + "-" + index2 
    write/append (read_record [0] + add_index_to header) to file_handle
    write/append (read_record[1,2,3]) to file_handle
```
Input: fh, read1_record

Expected output: 


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
    index_list = []
    for index in index_file
        add index to index_dict as keys with values of 0
        add index to index_list

count_matched_indices = 0
count_hopped_indices = 0
count_unknown = 0

dict_hopped_indices = {}

While true loop:

    read1_record = []
    read2_record= []
    index1_record = []
    index2_record = []

    add next four lines of each file to each empty list (dont forget to strip)

    index1 = sequence from index1_record
    index2 = reverse_complement( sequence from index2_record)

    if index1 or index2 contains "N":
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
        dict_hopped_indices[index1 + index2] += 1
        
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
