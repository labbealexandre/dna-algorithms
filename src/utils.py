# def mergeSort(K):

#     """merge sort for dictionnary [(key, value)]"""

#     n = len(K)
#     if n <= 1:
#         return K
    
#     m = n//2
#     L = mergeSort(K[:m])
#     R = mergeSort(K[m:])

#     i, j = 0, 0
#     res = []
#     while (i < len(L) and j < len(R)):
#         if L[i][1] < R[j][1]:
#             res.append(L[i])
#             i+=1
#         else:
#             res.append(R[j])
#             j+=1

#     while i < len(L):
#         res.append(L[i])
#         i+=1

#     while j < len(R):
#         res.append(R[j])
#         j+=1

#     return res

def copyMatrix(M):
    n = len(M)
    m = len(M[0])
    _M = [[0 for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            _M[i][j] = M[i][j]
    return _M

def initMatrix(n):
    return [[0 for i in range(n)] for j in range(n)]

def buildTree(children, root, N, start, outgoing):
    """
    build optimal tree from the children of a node
    """

    total = sum(children)
    m = len(children)
    if total != 0:
        # Mehlhorn method to find nearly optimal binary search trees
        # We search for a node which divides the tree
        # in two approximately equal sub-trees
        s, i = children[0], 0
        while s < total / 2:
            i+=1
            s+= children[i]
        # We update the N graph by adding a child to 
        if outgoing:
            N[root][start+i] = 1
        else:
            N[start+i][root] = 1
        # We once we found it we recursively call this method
        # for the subtrees at the left and the right of this node
        # (if there is at least one node in both cases)
        if i > 0 and sum(children[:i]) > 0:
            buildTree(children[:i], start+i, N, start, outgoing)
        if i < m-1 and sum(children[i+1:]) > 0:
            buildTree(children[i+1:], start+i, N, start+i+1, outgoing)

def reverseMatrix(M):
    n = len(M)
    reverseM = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            reverseM[i][j] = M[j][i]
    return reverseM