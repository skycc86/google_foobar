"""
Doomsday Fuel
        =============

        Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

        Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

        Write a function answer(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

        For example, consider the matrix m:
        [
          [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
          [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
          [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
          [0,0,0,0,0,0],  # s3 is terminal
          [0,0,0,0,0,0],  # s4 is terminal
          [0,0,0,0,0,0],  # s5 is terminal
        ]
        So, we can consider different paths to terminal states, such as:
        s0 -> s1 -> s3
        s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
        s0 -> s1 -> s0 -> s5
        Tracing the probabilities of each, we find that
        s2 has probability 0
        s3 has probability 3/14
        s4 has probability 1/7
        s5 has probability 9/14
        So, putting that together, and making a common denominator, gives an answer in the form of
        [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
        [0, 3, 2, 9, 14].
"""


from __future__ import division

def answer(m):
    # your code here
    m_len = len(m)
    if len(m)==1:
      return [1,1]
    
    t = [i for i,s in enumerate(m) if s==[0] * m_len]
    non_t = [i for i in range(m_len) if i not in t]
    non_t_sum = [sum(m[i]) for i in non_t]
    Q = [[m[i][j]/non_t_sum[n] for j in non_t] for n,i in enumerate(non_t)]
    R = [[m[i][j]/non_t_sum[n] for j in t] for n,i in enumerate(non_t)]
    # F = (I-Q)-1
    I_Q = Q
    for i in range(len(Q)):
        for j in range(len(Q)):
            if i==j:
                I_Q[i][j] = 1- I_Q[i][j]
            else:
                I_Q[i][j] = 0 - I_Q[i][j]
    F = getMatrixInverse(I_Q)
    FR = multiplyMatrix(F,R)
    # print(Q,I_Q)
    # print(F,R,FR)
    return findCommonDenominator(FR[0])
  
def findCommonDenominator(m):
    m2 = [i for i in m if i]
    min_m = min(m2)
    done = False
    tmp_m_base = [i/min_m for i in m] + [1/min_m]
    tmp_m = tmp_m_base
    mul = 1
    while not done:
        tmp_m = [i*mul for i in tmp_m_base]
        mul += 1
        done = all(round(i,5)==round(i,0) for i in tmp_m)
    return [int(round(i,0)) for i in tmp_m]
  
  
def multiplyMatrix(m,n):
    res = [[0] * len(n[i]) for i in range(len(m))]
    for i in range(len(m)):
        for j in range(len(n[i])):
            res[i][j] = sum(m[i][k] * n[k][j] for k in range(len(n)))
    return res
  
def transposeMatrix(m):
    if len(m)==0:
        return m
    t = [[0] * len(m) for i in range(len(m[0]))]
    for r in range(len(m)):
        for c in range(len(m[r])):
            t[r][c] = m[c][r]
    return t
    

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
  