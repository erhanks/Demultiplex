#!/usr/bin/env python

# Author: <penhanks> <penhanks@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''Bioinformatics functions written in class or for assignments
(or otherwise)'''

__version__ = "1.2" 
#version 0.0: Creation in Bi621 (Template)
    #version 0.1: added convert_phred(), qual_score(), validate_base_seq()
    #version 0.2: added gc_content(), calc_median()
    #version 0.3: added oneline_fasta()

#version 1.0: feedback received and revised on all previous versions
    #version 1.1: added reverse_complement()
    #version 1.2: added init_list and populate_list from PS4, with some revisons

# ----- Upcoming versions ----- #

# Read way more about versioning here:
# https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set('ATGCNatcgn')
RNA_bases = set('AUGCNaucgn')
import gzip

def validate_base_seq(seq: str, RNAflag=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq) <= (RNA_bases if RNAflag else DNA_bases)

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return (ord(letter) - 33)
    
def qual_score(phr_score: str) -> float:
    """Takes in a string of Phred+33 scores and returns 
    the average quality score for the sequence as a float"""
    tot_score = 0
    for i in phr_score:
        tot_score += convert_phred(i)
    return tot_score / len(phr_score)

def gc_content(DNA: str) -> float:
    '''Returns GC content of a DNA sequence as a decimal between 0 and 1. Case insensitive'''
    assert validate_base_seq(DNA) , "Not a DNA sequence"
    DNA = DNA.upper()         #Make sure sequence is all uppercase
    Gs = DNA.count("G")       #count the number of Gs
    Cs = DNA.count("C")       #count the number of Cs
    return (Gs+Cs)/len(DNA)


def calc_median(lst: list) -> float:
    """ Provides median of list provided list is already sorted"""
    half = len(lst)//2
    if len(lst)%2 == 1:
        median = lst[half]
    else:
    #if len(lst)%2 == 0:
        median = (lst[half] + lst[half-1]) / 2
    return median

def oneline_fasta(in_file: str, out_file: str):
    '''Takes a fasta file with sequences on more than one line 
    and outputs that file with sequences all on one line'''
    with open(in_file) as inf, open(out_file, "w") as ouf:
        dna_line = ''
        for line in inf:
            line = line.strip()
            if line.startswith(">"):
                if dna_line != '':
                    ouf.write(dna_line + "\n")
                ouf.write(line + "\n")
                dna_line = ''
            else:
                dna_line += line
    
def reverse_complement(DNA: str) -> str:
    ''' Takes in a 5'-3' string of DNA and outputs the 5'-3' reverse complement.
    Case insensitive.'''
    assert validate_base_seq(DNA) , "Not a DNA sequence"
    DNA = DNA.upper()         #Make sure sequence is all uppercase
    bases = {"A":"T", "C":"G", "G":"C","T":"A","N":"N"}
    reverse = str()
    for letter in DNA:
        reverse += bases[letter]
    reverse = reverse[::-1]
    return reverse

def init_list(lst: list, value: float=0.0, lent: int=101) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    i = 0
    while i < lent:
        lst.append(value)
        i +=1
    return lst

def populate_list(in_file: str, printer = False, compressed = False, lent: int=101) -> tuple[list, int]:
    """Takes in a FASTQ file and outputs a tuple containing a list, 
    which contains the sum total of quality scores for the index 
    position base pair, and an integer stating the number of lines in the file."""
    pop_lst = []
    pop_lst = init_list(pop_lst, lent=lent)
    if compressed:
        with gzip.open(in_file, "rt") as fq:
            i = 0
            r = 0 #running check
            for line in fq:
                line = line.strip()
                i += 1
                if i%4 == 0:
                    r += 1
                    for j,letter in enumerate(line):
                        pop_lst[j] += convert_phred(letter)
                if r%500000 == 0 and printer == True: #to check if/how function is running
                    print(r)
            return (pop_lst, i)

    else:
        with open(in_file, "rt") as fq:
            i = 0
            r = 0 #running check
            for line in fq:
                line = line.strip()
                i += 1
                if i%4 == 0:
                    r += 1
                    for j,letter in enumerate(line):
                        pop_lst[j] += convert_phred(letter)
                if r%500000 == 0 and printer == True: #to check if/how function is running
                    print(r)
            return (pop_lst, i)



# --- Unit Tests --- #

# validate base seq
if __name__ == "__main__": 
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")

# convert phred
if __name__ == "__main__":
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

# quality score
if __name__ == "__main__":
    assert qual_score("@@@@@@") == 31.0, "wrong average quality score"
    assert qual_score("IC2@$") == 25.0, "wrong average quality score"
    print("Your qual_score function is working!")

# gc content
if __name__ == "__main__":
    assert gc_content("GGCCGC") == 1.0, "Couldn't identify sequence of only Gs and Cs"
    assert gc_content("ATATAT") == 0.0, "Couldn't identify sequence with no Gs or Cs"
    assert gc_content("ATGC") == 0.5, "Wrong ratio"
    print("Your gc_content function is working!")

# calculate median
if __name__ == "__main__":
    assert calc_median([1,1,2,3,3]) == 2, "Wrong median of odd list"
    assert calc_median([1,1,2,3,3,4]) == 2.5, "Wrong median of even list"    
    print("Your calc_median function is working!")

# one line fasta
if __name__ == "__main__":
    oneline_fasta("contigs.fa", "contigs_oneline.fa")
    i = 0
    with open("contig_oneline.fa") as co:
        for line in co:
            line = line.strip()
            i += 1
    assert i == 2, "One line fasta output the wrong number of lines"  

# reverse complement
if __name__ == "__main__":
    assert reverse_complement("ATCTA") == "TAGAT", "Not successfully complemented"
    assert reverse_complement("ATCG") == "CGAT", "Not successfully reversed"
    print("Reverse complementation works!")