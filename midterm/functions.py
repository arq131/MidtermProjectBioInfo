# Midterm Project for Bioinformatics - Danny Nguyen. This is the file that contains all of the functions.
import sys
import math
from collections import defaultdict

# Class containing the PWM and the word matrix.
class info():
    def __init__(self, fName):
        self.PWM = create_PWM(fName)
        self.stringMatrix = wordMatrix("input1.txt")

    '''
    This will return the consesus of the current PWM in the object. 
    Parameters:
        None.
    Returns:
        A string containing the consensus of the PWM it current has stored.
    '''
    def getConsensus(self):
        consen = []
        with open("input1.txt") as file:
            n = len(file.readline()) - 1
            for i in range(0, n):
                consen.append('0')
                curMax = self.PWM[0][i]

                if curMax < self.PWM[1][i]:
                    curMax = self.PWM[1][i]
                    consen[i] = 'C'

                if curMax < self.PWM[2][i]:
                    curMax = self.PWM[2][i]
                    consen[i] = 'G'

                if curMax < self.PWM[3][i]:
                    curMax = self.PWM[3][i]
                    consen[i] = 'T'

                if curMax == self.PWM[0][i]:
                    consen[i] = 'A'
        return ''.join(consen)


    '''
    Format the printing of the PWM
    Parameters:
        PWM - Position weight matrix that we are printing out.
    Returns:
        None. This will output the matrix.
    '''
    def FormatPrint(self):
        chars = ['A', 'C', 'G', 'T', 'H', 'I']
        for x in range(0, 6):
            sys.stdout.write("%c " % chars[x])
            for y in range(0, 7):
                sys.stdout.write("%.2f " % self.PWM[x][y])
            sys.stdout.write("\n")

'''
Store the information of all the different word combinations.
Parameters: 
    fileName - Name of the file we are getting all the possible word combinations from.
Returns:
    words - A dictionary containing all of the possible words in the file.
'''
def wordMatrix(fileName):
    words = []
    with open(fileName) as file:
        for line in file:
            words.append(line)
    return words

'''
Zero's the matrix and returns a matrix.
Parameters:
    Matrix - A matrix that we are going to zero.
Returns:
    returnValue - A matrix that has all of its data points zeroed.
'''
def zero(matrix):
    returnVal = []
    for x in range(matrix[0]):
        returnVal.append([])
        for y in range(matrix[1]):
            returnVal[-1].append(0)
    return returnVal

'''
Return the file length. This is used to determine the number of columns for a matrix.
Parameters:
    fName - The name of the file we want to find the length of.
Returns:
    i - integer value containing how many lines are in the file.
'''
def file_len(fName):
    with open(fName) as f:
        for i, l in enumerate(f):
            pass
        return i+1

'''
This will create a Position-weight-matrix.
Parameters:
    None.
Returns:
    PWM - a matrix containing the values for a given sequence.
Notes:
    The file we are reading from is hard coded (named "input1.txt"). Could be adjusted to fit any file name however.
'''
def create_PWM(fName):
    # Open up file for reading
    with open(fName) as file:
        m = 7                       # Number of rows (A, T, C, G, Highest P, H, I)
        
        n = len(file.readline()) - 1     # Number of words to check
        file.seek(0, 0)
        PWM = zero((m+1, n+1))      # Create PWM matrix
        colCount = 0
        position = 0
        consenMatrix = defaultdict(list)
        amountMatrix = zero((m, n+1))

        # Create a list of all words and the position count
        for line in file:
            for char in line: # Keep count of how many occurances in word
                if char == '\n':
                    continue
                consenMatrix[position].append(char)
                position += 1

        # Go through each letter and sort by position, then add accordingly.
        for key, value in consenMatrix.iteritems():
            for i in range(0, n):
                if (key % n == i): # used to find which position
                    char = ''.join(value)
                    if (char == 'A'):
                        amountMatrix[0][i] += 1
                    if (char == 'C'):
                        amountMatrix[1][i] += 1
                    if (char == 'G'):
                        amountMatrix[2][i] += 1
                    if (char == 'T'):
                        amountMatrix[3][i] += 1
        
        # Find how many different words we used
        fileLen = file_len("input1.txt") 
        for i in range(0, n):
            # Calculate all probability to add into PWM
            p_A = (float) (amountMatrix[0][i] + 1) / (fileLen + 4)
            p_C = (float) (amountMatrix[1][i] + 1) / (fileLen + 4)
            p_G = (float) (amountMatrix[2][i] + 1) / (fileLen + 4)
            p_T = (float) (amountMatrix[3][i] + 1) / (fileLen + 4)
            # Add data into pwm
            PWM[0][i] = p_A
            PWM[1][i] = p_C
            PWM[2][i] = p_G
            PWM[3][i] = p_T

        # Calculate information content
        for i in range(0, n):
            PWM[4][i] = calculateH(PWM, i) 
            PWM[5][i] = 2 - PWM[4][i]
    return PWM
'''
Calculate the H for the word column.
Parameters:
    PWM - The PWm we are using to calculate H (Entropy) value.
    colCount - Which column in the PWM we are using to calculate the H value.
Returns:
    H - the H (entropy) value.
Notes:
    This only calculates one of the columns in the PWM for the H value.
'''
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

'''
Calculates the best match with a PWM against a sequence.
Parameters:
    PWM - The PWM we are using to compare to the sequence.
    sequence - The sequence we are comparing with
Returns:
    None. This function will output a report with the best match pattern, the position, and the score.
'''
def calculateBestMatch(PWM, sequence):
    score = (float) (0)                     # Best score.
    n = len(PWM)                            # How many different word to check with.
    subString = [0, 0]                      # Position of best match.
    word = ''                               # The word that best matched the sequence.
    repeat = len(sequence) - n              # Number of times to repeat the search for the sequence.
    start = 0                               # Start of the word in sequence
    end = n                                 # End of the word in sequence

    # Number of repeats for the sequence
    for temp in range(0, repeat):        
        matchScore = (float) (1)                # The match score for the individual sequence.
        curWord = ''
        i = 0
        # For each word in the sequence
        for j in range(start, end-1):
            p_A, p_C, p_G, p_T = PWM[0][i], PWM[1][i], PWM[2][i], PWM[3][i]
            curWord += sequence[j]
            if (sequence[j] == 'A'):
                matchScore *= (float) (p_A)
            if (sequence[j] == 'C'):
                matchScore *= (float) (p_C)
            if (sequence[j] == 'G'):
                matchScore *= (float) (p_G)
            if (sequence[j] == 'T'):
                matchScore *= (float) (p_T)
            i += 1

            # If the match score is greater than the current max score
        if (matchScore > score):  
            score = matchScore              # Update all the information for current max  
            subString[0] = start            # ^
            subString[1] = end              # ^
            word = curWord                  # ^

            # Update position checking
        start += 1
        end += 1

    # Print out information for best match.        
    print('Best Match: %s\nPosition: %d - %d\nScore: %s\n' % (word, subString[0], subString[1], score))

