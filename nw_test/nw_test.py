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

    paths = Tree()

    def gen_branches(S,T):
        ML = np.transpose(np.transpose(S)[:-1])
        MU = S[:-1]
        MD = ML[:-1]
        i = len(S) - 1
        j = len(S[0]) - 1

        if i == 1 and j == 1:
            T.createChildren(1)
            T.setChildrenValues(['END'])
            return(0)

        if j == 1 and i > 1:
            T.createChildren(1)
            T.setChildrenValues(['U'])
            gen_branches(MU,T.child[-1])

        if i == 1 and j > 1:
            T.createChildren(1)
            T.setChildrenValues(['L'])
            gen_branches(ML,T.child[-1])

        L = S[i][j - 1]
        U = S[i - 1][j]
        D = S[i - 1][j - 1]
        check = min(L,U,D)
        
        while(i > 1 and j > 1):
            if L == check:
                if 'L' in T.data:
                    j -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['L'])
                    j -= 1
                    gen_branches(ML,T.child[-1])
            if U == check:
                if 'U' in T.data:
                    i -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['U'])
                    i -= 1
                    gen_branches(MU,T.child[-1])
            if D == check:
                if 'D' in T.data:
                    i -= 1
                    j -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['D'])
                    i -= 1
                    j -= 1
                    gen_branches(MD,T.child[-1])

    gen_branches(M,paths)
    path_lst = []

    def get_paths(paths,current):
        n = len(paths.data)
        if paths.data == ['END']:
            path_lst.append(current)
            return(0)
        else:
            current = [current[:] for i in range(n)]
            for i in range(n):
                current[i].append(paths.data[i])
                get_paths(paths.child[i],current[i])

    get_paths(paths,path_lst)
    print('\n')
    print(path_lst)
    print('\n')

    def get_align(path,A,B):
        A_new = [A[-1]]
        B_new = [B[-1]]
        i = len(A) - 1
        j = len(B) - 1
        n = len(path)
        while n > 0:
            for d in path:
                if d == 'L':
                    A_new.append(A[i-1])
                    B_new.append('-')
                    i -= 1
                    n -= 1
                if d == 'U':
                    A_new.append('-')
                    B_new.append(B[j-1])
                    j -= 1
                    n -= 1
                if d == 'D':
                    A_new.append(A[i-1])
                    B_new.append(B[j-1])
                    i -= 1
                    j -= 1
                    n -= 1

        A_new.reverse()
        B_new.reverse()

        return(A_new,B_new)


    aligns = []
    for path in path_lst:
        print('new path')
        aligns.append([get_align(path,A,B)[0],get_align(path,A,B)[1]])
    
    return(aligns)

A = ['A','B','C','D','K','B','C','D','K','B','C','D','K','E','F']                
B = ['A','B','C','D','K','E','F'] 

print(nw(A,B)[-1])
