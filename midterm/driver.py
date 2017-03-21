# Bioinformatics - Midterm project. Danny Nguyen. This is the main driver file.
from functions import *
from problem_3 import *
import time

# Main function to run the program. Currently running problems 1, 2, and 3.
def main():
    information = info("input1.txt") # information that contains a word dictionary and PWM
    with open("input2.txt") as file: # checking input file 2 for problems 1 and 2 of midterm assignment.
        i = 1   # keep track of which line we are on in the file. (used for sequence number)
        information.FormatPrint()
        print("Consensus: %s\n" % information.getConsensus())

        for line in file:
            print("Sequence Number: %d" % i)
            calculateBestMatch(information.PWM, line)
            i += 1
    

    # Starting testing for problem 3
    words = possibleWords(7, wordMatrix("input2.txt"))
    lowestMM = 2048             # keep track of the lowest number of mismatches through ALL patterns.
    start_time = time.time()    # get the starting time of the problem 3.
    for word in words: # for each possible pattern.
        report = mismatches(word, wordMatrix("input2.txt")) # get a report of the current pattern.

        # If the current report mismatch is lower than the lowest pattern we current have, update the information.
        if report.lowestMismatch < lowestMM:
            bestReport = report
    # print out the best report we have stored.
    bestReport.printReport()

    # record end time for the program and print out the runtime.
    end_time = time.time()
    print("--- %s seconds to find best pattern with lowest amount of mismatches ---" % (end_time - start_time))


'''
Main function 2 to run just problem 1. 
'''
def main2():
    information = info()

# Initialziation
if __name__ == '__main__':
    main()