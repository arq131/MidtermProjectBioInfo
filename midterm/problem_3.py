# Bioinformatics midterm Project - Danny Nguyen. This file contains methods for problems 3-4.
from functions import *

# Class containing a report of a pattern against a series of sequences
class report():
    def __init__(self):
        self.lowestMismatch = 2048      # lowest num of mismatch, default at 2k
        self.pattern = ''               # pattern 
        self.location = []              # location if there were no mismatches
        self.sequenceNum = 0            # sequence number if there were no mismatches

    # print report will print out a report of the information that is stored in this class.
    def printReport(self):
        print("Number of mismatches: %d" % self.lowestMismatch)
        print("Pattern: %s" % self.pattern)
        if (len(self.location) != 0):
            print("Location of pattern on sequence #%d: %d - %d" % (self.sequenceNum, self.location[0], self.location[1]))
        else:
            print("No pattern matched a sequence.")
### ---------------------------------- ###
# possibleWords will return all of the possible patterns within a sequence.
# Parameters:
#       motifLen - Length of pattern to use.
#       wordDict - Dictionary containing all sequences.
# Returns:
#       words - Dictionary containing all possible pattern with length motifLen
### ---------------------------------- ###
def possibleWords(motifLen, wordDict):
    words = []
    newWord = ''
    for word in wordDict:
        start = 0           # start of word
        end = motifLen      # end of word
        repeat = len(word) - motifLen + 1     # Number of times to repeat the search for the sequence.
        for temp in range(0, repeat):
            for i in range(start, end):
                newWord += word[i]
            words.append(newWord) # add new word into dictionary
            newWord = ''    # reset new word
            start += 1      # update start position by 1
            end += 1        # update ending position by 1
    return words
### ------------------------------------ ###
# mismatches will calculate the number of mismatches for a certain pattern against a sequence(s).
# Parameters:
#       pattern - the pattern to check against sequence(s)
#       seqDict - Dictionary of sequences to check
# Returns:
#       Number of mismatches for the pattern.
#### ----------------------------------- ###
def mismatches(pattern, seqDict):
    reports = report()                  # Create a new report to return
    mismatch = 0                        # total number of mismatch for the pattern
    patternLen = len(pattern)           # Pattern length
    seqNum = 0                          # Sequence number
    for sequence in seqDict: 
        lowestMM = 2048                 # set lowest amount of mismatches to be 2k
        start = 0                       # start of sequence location
        end = patternLen                # end of sequence location
        repeat = len(sequence) - patternLen + 1         # number of times to repeat through the sequence
        for temp in range(0, repeat):   
            curMismatch = 0             # Number of current mismatches for the current word comparing to pattern
            for i in range(start, end):
                if (pattern[i % patternLen] != sequence[i]):    # if mismatch, add 1
                    curMismatch += 1

            # if there are no mismatches, record info into report        
            if curMismatch == 0:                                
                reports.location.append(start)
                reports.location.append(end)
                reports.sequenceNum = seqNum

            # if current mismatch is lower than the lowest mismatch, update
            if curMismatch < lowestMM:
                lowestMM = curMismatch
        # add total number of mismatches from sequence
        mismatch += lowestMM
        seqNum += 1 # update seq number

    # update report with current pattern and number of mismatches
    reports.pattern = pattern
    reports.lowestMismatch = mismatch
    return reports
