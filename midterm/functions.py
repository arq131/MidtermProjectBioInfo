# Midterm Project for Bioinformatics - Danny Nguyen. This is the file that contains all of the functions.
import sys
import math

# Class containing the PWM and the word matrix.
class info():
    def __init__(self):
        self.PWM = create_PWM()
        self.stringMatrix = wordMatrix("input1.txt")

# Store the information of all the different word combinations.
def wordMatrix(fileName):
    words = []
    with open(fileName) as file:
        for line in file:
            words.append(line)
    return words

# Zero's the matrix and returns a matrix.
def zero(matrix):
    returnVal = []
    for x in range(matrix[0]):
        returnVal.append([])
        for y in range(matrix[1]):
            returnVal[-1].append(0)
    return returnVal

# return the file length. This is used to determine the number of columns for a matrix.
def file_len(fName):
    with open(fName) as f:
        for i, l in enumerate(f):
            pass
        return i+1

# Creating PWM - Problem 1
def create_PWM():
    m = 7                       # Number of rows (A, T, C, G, Highest P, H, I)
    n = file_len("input1.txt")  # Number of words to check
    PWM = zero((m+1, n+1))      # Create PWM matrix
    colCount = 0

    # Open up file for reading
    with open("input1.txt") as file:
        for line in file:
            c_A, c_C, c_G, c_T = 0, 0, 0, 0
            for char in line: # Keep count of how many occurances in word
                #sys.stdout.write(char)
                if (char == 'A'):
                    c_A += 1
                if (char == 'C'):
                    c_C += 1
                if (char == 'G'):
                    c_G += 1
                if (char == 'T'):
                    c_T += 1
            total = (c_A + c_C + c_G + c_T + 4)
            p_A = (float)(c_A + 1) / total         # probability for A
            p_C = (float)(c_C + 1) / total         # probability for C
            p_G = (float)(c_G + 1) / total         # probability for G
            p_T = (float)(c_T + 1) / total         # probability for T
            
            # Add the values into the matrix
            PWM[0][colCount] = p_A
            PWM[1][colCount] = p_C
            PWM[2][colCount] = p_G
            PWM[3][colCount] = p_T

            # Adding information content into the matrix.
            PWM[4][colCount] = calculateH(PWM, colCount) 
            PWM[5][colCount] = 2 - PWM[4][colCount]      
                
            colCount += 1   # Increase the count after processing each word
    formatPrint(PWM) # After finish calculating data, print out the PWM
    return PWM

# Calculate the H for the word column.
def calculateH(PWM, colCount):
    H = 0
    P_A, P_C, P_G, P_T = PWM[0][colCount], PWM[1][colCount], PWM[2][colCount], PWM[3][colCount]
    
    # Calculating the entropy of each character.
    H_A = (-P_A * math.log(P_A, 2))
    H_C = (-P_C * math.log(P_C, 2))
    H_G = (-P_G * math.log(P_G, 2))
    H_T = (-P_T * math.log(P_T, 2))

    # Getting summation of all the entropies and returning the value
    H = H_A + H_C + H_G + H_T
    return H

# Calculates the best match with a PWM against a sequence.
def calculateBestMatch(PWM, wordlist, sequence, seqLen):
    score = (float) (0)                     # Best score.
    n = len(PWM)                            # How many different word to check with.
    subString = [0, 0]                      # Position of best match.
    word = ''                               # The word that best matched the sequence.
    repeat = len(sequence) - seqLen + 1     # Number of times to repeat the search for the sequence.

    # For each word in the PWM
    for i in range(0, n):
        start = 0       # Starting position
        end = seqLen    # Ending position

        # Probability of each A, C, G, T
        p_A, p_C, p_G, p_T = PWM[0][i], PWM[1][i], PWM[2][i], PWM[3][i]
        
        # Number of repeats for the sequence
        for temp in range(0, repeat):
            matchScore = (float) (1)                # The match score for the individual sequence.

            # For each word in the sequence
            for j in range(start, end):
                if (sequence[j] == 'A'):
                    matchScore *= (float) (p_A)
                if (sequence[j] == 'C'):
                    matchScore *= (float) (p_C)
                if (sequence[j] == 'G'):
                    matchScore *= (float) (p_G)
                if (sequence[j] == 'T'):
                    matchScore *= (float) (p_T)

            # If the match score is greater than the current max score
            if (matchScore > score):  
                score = matchScore              # Update all the information for current max  
                subString[0] = start            # ^
                subString[1] = end              # ^
                word = wordlist[i]              # ^

            # Update position checking
            start += 1
            end += 1

    # Print out information for best match.        
    print('Best Match: %sPosition: %d - %d\nScore: %s\n' % (word, subString[0], subString[1], score))

# Format the printing of the PWM
def formatPrint(PWM):
    chars = ['A', 'C', 'G', 'T', 'H', 'I']
    for x in range(0, 6):
        sys.stdout.write("%c " %chars[x])
        for y in range(0, file_len("input1.txt")):
            sys.stdout.write("%.2f " % PWM[x][y])
        sys.stdout.write("\n")
