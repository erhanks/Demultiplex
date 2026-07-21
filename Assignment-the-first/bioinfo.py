#!/usr/bin/env python

# Author: <penhanks> <penhanks@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''Bioinformatics functions written in class or for assignments
(or otherwise)'''

__version__ = "0.3"   
# Read way more about versioning here:
# https://en.wikipedia.org/wiki/Software_versioning

DNAbases = set('ATGCNatcgn')
RNAbases = set('AUGCNaucgn')

def validate_base_seq(seq: str, RNAflag=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq) <= (RNAbases if RNAflag else DNAbases)

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return(ord(letter) - 33)
    
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

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
if __name__ == "__main__": 
    #this lets us check function when run in terminal
    #but not show up when the function is used
    #This is called a unit test
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")

if __name__ == "__main__":
    assert reverse_complement("ATCTA") == "TAGAT", "Not successfully complemented"
    assert reverse_complement("ATCG") == "CGAT", "Not successfully reversed"
    print("Reverse complementation works!")