import random

possibilities = [0, 0]

def randomBoard(n):
    matrix = []
    for i in range(n):
        inner_matrix = []
        for j in range(n):
            inner_matrix.append(random.choice(possibilities))
        matrix.append(inner_matrix)
    return matrix
