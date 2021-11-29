import random

possibilities = [0, 0, 0, -1]

def initialBoard(n):
    matrix = []
    for i in range(n):
        inner_matrix = []
        for j in range(n):
            #To block position or not
            choice = random.choice(possibilities)
            inner_matrix.append(choice)
        matrix.append(inner_matrix)
        
    #Making sure starting and ending positions are not blocked 
    matrix[n-1][0] = 0
    matrix[0][n-1] = 0
    return matrix
