"""
File that contains the code to solve the general string edit problem
with dynamic programming.
"""

import numpy as np
import string
from sssp_r import apsp_r

def fill_matrices(min_oe, chosen_ops, my_apsp_r, min_irc, a, b, S, n_rows, n_cols):
    # The rest of the matrices are filled out with the recurrence.
    for i in range(1, n_rows):
        for j in range(1, n_cols):
            # strings are indexed from 0
            iai = S.index(a[i - 1])
            ibj = S.index(b[j - 1])
            target = b[j - 1]
            if a[i - 1] == target:
                min_oe[i, j] = min_oe[i - 1, j - 1]
            else:
                op1 = D[iai] + min_oe[i - 1, j]
                min_reps = my_apsp_r[iai, ibj]
                op2 = min_reps + min_oe[i - 1, j - 1]
                op3 = min_irc[ibj] + min_oe[i, j - 1]
                # Sorted ops.
                sops = sorted([op1, op2, op3])
                chosen_op = sops[0]
                if chosen_op == op1:
                    chosen_ops[i, j] = 1
                elif chosen_op == op2:
                    chosen_ops[i, j] = 2
                else:
                    chosen_ops[i, j] = 3
                min_oe[i, j] = chosen_op 


# Minimun n of operations for string edit
def mino_sedit(a: str, b: str, S: list, D: list, I: list, C: np.ndarray) -> tuple:
    """
    Arguments: 
        a: str (The first string)
        b: str (The second string, both strings should be matched)
        S: list (The list of characters S_i in the vocabulary)
        D: list (The list of costs to delete D_i character S_i in 
            vocabulary S)
        I: list (The list of costs to insert I_i character S_i)
        C: numpy.ndarray (The matrix with costs to replace character
            S_i with another character S_j, noted that C_ii = 0)

    Returns: 
        A tuple of numpy.ndarray, where the first matrix is the dp 
        matrix and the second matrix describes the operations chosen at
        each step to rebuild the solution.
    """

    n_rows = len(a) + 1
    n_cols = len(b) + 1
    min_oe = np.zeros((n_rows, n_cols))
    chosen_ops = np.zeros((n_rows, n_cols))
    
    # We first fill out the column 0, where the only way to get b_0...0
    # the empty string, is to delete all the characters.
    for i in range(1, n_rows):
        cost_delall = 0
        for char in a[0:i]:
            ichar = S.index(char)
            cost_delall += D[ichar]
        min_oe[i, 0] = cost_delall
        chosen_ops[i, 0] = 1

    # my_apsp_r is the result of the all-pairs shortest paths,
    # it has the guaranteed minimum cost for replacing characters.
    my_apsp_r = apsp_r(S, C)

    # min_irc is a list of same size as the vocabulary, where it is
    # saving the minimum cost to insert a character and possibly 
    # replace it to get a target character.
    v = len(S)
    min_irc = [0] * v
    for target in S:
        possible_costs = []
        ind_t = S.index(target)
        for char in S:
            ind_char = S.index(char)
            # Insertion-replacement cost.
            irc = I[ind_char] + my_apsp_r[ind_char, ind_t]
            possible_costs += [irc]
        min_irc[ind_t] = min(possible_costs)        

    # Now we fill out the row 0, where the mininum number of operations
    # to get from substring a_0...0 to b_0...j is just m[0, j - 1] + 
    # the cost to get the empty string to b_j.
    for j in range(1, n_cols):
        target = b[j - 1]
        itarget = S.index(target)
        cost_ttarget = min_irc[itarget]
        min_oe[0, j] = cost_ttarget + min_oe[0, j - 1]  
        chosen_ops[0, j] = 3     

    fill_matrices(min_oe, chosen_ops, my_apsp_r, min_irc, a, b, S, n_rows, n_cols)
    return min_oe, chosen_ops


# Testing the code with an example:
C = np.array([[0, 1, 5, 1], [1, 0, 5, 5], [5, 5, 0, 5], [1, 5, 5, 0]])
#C = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
oS = ['a', 'b', 'c', 'd']
I = [5, 20, 5, 1]
#I = [1, 1, 1, 1]
#D = [1, 1, 1, 1]
D = [1, 1, 1, 1]
a = 'cccda'
b = 'bbbb'
print('----------------------------------------------------')
print('Initial conditions are: ')
print(f'a: {a}')
print(f'b: {b}')
print(f'S: {oS}')
print(f'I {I}')
print(f'D: {D}')
print(f'C: {C}')
print('----------------------------------------------------')


m, ops = mino_sedit(a, b, oS, D, I, C)

# The dynamic programming matrix and the chosen operations matrix.
print('----------------------------------------------------')
print('The dynamic programming matrix min_oe with the minimum cost')
print(m)
print('The matrix with the chosen operation at each step to reconstruct \
      the solution')
print(ops)
print('----------------------------------------------------')

print('----------------------------------------------------')
print('Solution reconstruction:')
leftover_a = ''
leftover_b = ''
i = len(a)
j = len(b)
while i >= 0 and j >= 0:
    chosen_op = ops[i, j]

    if chosen_op == 1:
        a = a[:i - 1] + a[i:]
        i -= 1
    elif chosen_op == 2:
        a = a[:i - 1] + b[j - 1] + a[i:]
        #b = b[:j - 2]
        i -= 1
        j -= 1
    elif chosen_op == 3:
        a = a[:i] + b[j - 1] + a[i:]
        j -= 1
    else:
        i -= 1
        j -= 1
    print(f'a is a {a}')
print(f'b is {b}')
print('----------------------------------------------------')
    
