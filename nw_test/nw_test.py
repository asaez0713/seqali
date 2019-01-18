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
    if type(A) != list or type(B) != list:
        print('Invalid input.',
                'Input should be a list of base pairs (strings).')
        return(0)
    for item in A:
        if type(item) != str:
            print('Invalid input.',
                    'Input should be a list of base pairs (strings).')
            return(0)
        else:
            pass
    for item in B:
        if type(item) != str:
            print('Invalid input.',
                    'Input should be a list of base pairs(strings).')
            return(0)
        else:
            pass

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
        for j in range(1,len(B)+1):
            if A[i-1] == B[j-1]:
                score = match
            else:
                score = mismatch
            c1 = M[i-1][j-1] + score
            c2 = M[i-1][j] + indel
            c3 = M[i][j-1] + indel
            c = np.min([c1,c2,c3])
            M[i][j] = c
    
    paths = Tree()
    count = 0

    def gen_branches(S,T,ct,A,B):
        ML = np.transpose(np.transpose(S)[:-1])
        MU = S[:-1]
        MD = ML[:-1]
        i = len(S) - 1
        j = len(S[0]) - 1

        L = S[i][j - 1]
        U = S[i - 1][j]
        D = S[i - 1][j - 1]
        check = S[i][j]

        m = bool(A[i-1] == B[j-1])

        if i == 1 and j == 1:
            T.createChildren(2)
            T.setChildrenValues(['END',ct])
            return(0)

        if j == 1 and i > 1:
            T.createChildren(1)
            T.setChildrenValues(['U'])
            ct += U
            gen_branches(MU,T.child[-1],ct,A,B)

        if i == 1 and j > 1:
            T.createChildren(1)
            T.setChildrenValues(['L'])
            ct += L
            gen_branches(ML,T.child[-1],ct,A,B)
        
        while(i > 1 and j > 1):
            if L == check - indel:
                if 'L' in T.data:
                    j -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['L'])
                    ct += L
                    j -= 1
                    gen_branches(ML,T.child[-1],ct,A,B)
            if U == check - indel:
                if 'U' in T.data:
                    i -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['U'])
                    ct += U
                    i -= 1
                    gen_branches(MU,T.child[-1],ct,A,B)
            if not m and D == check - mismatch:
                if 'D' in T.data:
                    i -= 1
                    j -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['D'])
                    ct += D
                    i -= 1
                    j -= 1
                    gen_branches(MD,T.child[-1],ct,A,B)
            if m and D == check - match:
                if 'D' in T.data:
                    i -= 1
                    j -= 1
                    pass
                else:
                    T.createChildren(1)
                    T.setChildrenValues(['D'])
                    ct += D
                    i -= 1
                    j -= 1
                    gen_branches(MD,T.child[-1],ct,A,B)


    gen_branches(M,paths,count,A,B)
    path_lst = []

    def get_paths(paths,current):
        n = len(paths.data)
        if paths.data[0] == 'END':
            path_lst.append([current,paths.data[1]])
            return(0)
        else:
            current = [current[:] for i in range(n)]
            for i in range(n):
                current[i].append(paths.data[i])
                get_paths(paths.child[i],current[i])

    get_paths(paths,path_lst)

#    depth = [path[1] for path in path_lst]
#    copy = path_lst[:]
#    for pair in copy:
#        if pair[1] != np.min(depth):
#            path_lst.remove(pair)

    def get_align(path,A,B):
        A_new = []
        B_new = []
        i = len(A) - 1
        j = len(B) - 1
        n = len(path[0])
        while n > 0:
            for d in path[0]:
                if d == 'L':
                    A_new.append('-')
                    B_new.append(B[j])
                    j -= 1
                    n -= 1
                if d == 'U':
                    A_new.append(A[i])
                    B_new.append('-')
                    i -= 1
                    n -= 1
                if d == 'D':
                    A_new.append(A[i])
                    B_new.append(B[j])
                    i -= 1
                    j -= 1
                    n -= 1

        A_new.append(A[0])
        A_new.reverse()
        B_new.append(B[0])
        B_new.reverse()

        return(A_new,B_new)


    aligns = []
    for path in path_lst:
        aligns.append([get_align(path,A,B)[0],get_align(path,A,B)[1]])
    
    return(aligns)

A = ['A','G','C','T','G','C','A']
B = ['A','G','C','T','C','G','A']

print(nw(A,B))
