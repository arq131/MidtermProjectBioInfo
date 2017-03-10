# Midterm Project for Bioinformatics - Danny Nguyen
import sys
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
    m = 4                       # Number of rows (A, T, C, G)
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
            
            colCount += 1   # Increase the count after processing each word
    formatPrint(PWM) # After finish calculating data, print out the PWM

# Format the printing of the PWM
def formatPrint(PWM):
    chars = ['A', 'C', 'G', 'T']
    for x in range(0, 4):
        sys.stdout.write("%c " %chars[x])
        for y in range(0, file_len("input1.txt")):
            sys.stdout.write("%.2f " %PWM[x][y])
        sys.stdout.write("\n")


def main():
    create_PWM()

if __name__ == '__main__':
    main()
