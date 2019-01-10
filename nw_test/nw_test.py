import numpy as np

def nw(A,B):
    M = np.zeros((len(A)+1,len(B)+1))
    ptr = np.zeros((len(A)+1,len(B)+1))

    match = 0
    mismatch = 1
    indel = 1

    for i in range(len(A)+1):
        M[i][0] = i * mismatch
    for i in range(len(B)+1):
        M[0][i] = i * mismatch

    for i in range(1,len(A)+1):
        gapA = 0
        gapB = 0
        for j in range(1,len(B)+1):
            if A[i-1] == B[j-1]:
                score = match
            else:
                score = mismatch
            c1 = M[i-1][j-1] + score
            c2 = M[i-1][j] + gapB + indel
            c3 = M[i][j-1] + gapA + indel
            c = np.min([c1,c2,c3])
            M[i][j] = c
            if c == c1:
                ptr[i,j] = 0
                gapA = gapB = 0
            elif c == c2:
                ptr[i,j] = 1
                gapB += 1
            elif c == c3:
                ptr[i,j] = -1
                gapA += 1

    i = len(A)
    j = len(B)
    alnA = []
    alnB = []

    while(i > 0 or j > 0):
        if ptr[i][j] == 0:
            alnA.append(A[i-1])
            alnB.append(B[j-1])
            i -= 1
            j -= 1
        elif ptr[i][j] == 1:
            alnA.append(A[i-1])
            alnB.append('-')
            i -= 1
        elif ptr[i][j] == -1:
            alnA.append('-')
            alnB.append(B[j-1])
            j -= 1

    alnA.reverse()
    alnB.reverse()

    return(alnA,alnB)
