import numpy as np

class Tree(object):
    def __init__(self):
        self.child = []
        self.data = []
                                     
    def createChildren(self,amount):
        for i in range(amount):
            self.child.append(Tree())
                                                                 
    def setChildrenValues(self,list):
        for i in range(len(list)):
            self.data.append(list[i])

def nw(A,B):
    m = len(A) + 1
    n = len(B) + 1
    M = np.zeros((m,n))

    match = 0
    mismatch = 1
    indel = 1

    for i in range(m):
        M[i][0] = i * mismatch
    for i in range(n):
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
                gapA = gapB = 0
            elif c == c2:
                gapB += 1
            elif c == c3:
                gapA += 1

    print(M)

    T_A = Tree()
    T_A.createChildren(1)
    T_A.setChildrenValues([A[-1]])
    T_B = Tree()
    T_B.createChildren(1)
    T_B.setChildrenValues([B[-1]])

    def gen_branches(S,TA,TB):
        ML = np.transpose(np.transpose(S)[:-1])
        MU = S[:-1]
        MD = ML[:-1]
        i = len(S) - 1
        j = len(S[0]) - 1

        if i == 1 and j == 1:
            TA.createChildren(1)
            TA.setChildrenValues([A[0]])
            TB.createChildren(1)
            TB.setChildrenValues([B[0]])
            return(0)

        if j == 1 and i > 1:
            TA.createChildren(1)
            TA.setChildrenValues([A[i-2]])
            TB.createChildren(1)
            TB.setChildrenValues(['-'])
            gen_branches(MU,TA.child[-1],TB.child[-1])

        if i == 1 and j > 1:
            TA.createChildren(1)
            TA.setChildrenValues(['-'])
            TB.createChildren(1)
            TB.setChildrenValues([B[j-2]])
            gen_branches(ML,TA.child[-1],TB.child[-1])

        L = S[i - 1][j]
        U = S[i][j - 1]
        D = S[i - 1][j - 1]
        check = min(L,U,D)
        while(i > 1 and j > 1):
            if L == check:
                TA.createChildren(1)
                TA.setChildrenValues([A[i-2]])
                TB.createChildren(1)
                TB.setChildrenValues(['-'])
                j -= 1
                gen_branches(ML,TA.child[-1],TB.child[-1])
            if U == check:
                TA.createChildren(1)
                TA.setChildrenValues(['-'])
                TB.createChildren(1)
                TB.setChildrenValues([B[j-2]])
                i -= 1
                gen_branches(MU,TA.child[-1],TB.child[-1])
            if D == check:
                TA.createChildren(1)
                TA.setChildrenValues([A[i-2]])
                TB.createChildren(1)
                TB.setChildrenValues([B[j-2]])
                i -= 1
                j -= 1
                gen_branches(MD,TA.child[-1],TB.child[-1])

    gen_branches(M,T_A.child[0],T_B.child[0])
    print(T_A.child[0].child[0].child[0].data)

    
    return(0)

A = ['A','T','G','A']
B = ['A','T','A']

nw(A,B)
