from src import utils as ut

def buildTrees(M, reverseM, root, parent, visited, N, outgoing):

    if visited[root] == 1:
        return

    visited[root] = 1
    n = len(M)

    children = []
    if outgoing:
        for i in range(n):
            if i != parent:
                children.append(M[root][i])
            else:
                children.append(0)
    else:
        for i in range(n):
            if i != parent:
                children.append(M[i][root])
            else:
                children.append(0)

    ut.buildTree(children, root, N, 0, outgoing)

    for i in range(n):
        if (i != parent):
            if M[root][i] > 0:
                buildTrees(M, reverseM, i, root, visited, N, outgoing)
            if M[i][root] > 0:
                buildTrees(M, reverseM, i, root, visited, N, outgoing)


def treeToBND(M):
    """
    Theorem 3 : get a Bounded Network Design from
    a request distribution such as the graph is a tree
    """

    n = len(M)
    reverseM = ut.reverseMatrix(M)

    # N will be the result the result unweighted graph
    N = [[0 for i in range(n)] for j in range(n)]
            
    # We arbitrary set the root as 0
    visited = [0 for i in range(n)]
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, True)

    visited = [0 for i in range(n)]
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, False)

    return N

def sparseToBND(M):

    """
    Theorem 4 : get a Bounded Network Design from
    a request distribution such as the graph is sparse
    """

    n = len(M)

    # N will be the result unweighted graph
    N = ut.initMatrix(n)
    auxM = ut.initMatrix(n)

    for i in range(n):
        for j in range(n):
            if M[i][j] > 0:
                auxM[i][j] = 1

    reverseAuxM = ut.reverseMatrix(auxM)

    egdesN = 0
    for i in range(n):
        egdesN += sum(auxM[i])
    avgDegrees = 2.*egdesN/n

    # Compute the degrees and sort them
    degrees = [(i, sum(auxM[i]) + sum(reverseAuxM[i])) for i in range(n)]
    degrees.sort(key= lambda t: t[1])

    # Fill the lowDegrees and highDegrees lists
    lowDegrees, highDegrees = [], []
    m = n//2
    i = 0
    while i < m:
        lowDegrees.append(degrees[i][0])
        i+=1
    while i < n:
        highDegrees.append(degrees[i][0])
        i+=1

    lowDegrees.sort()
    highDegrees.sort()

    # Fill the highOutDegrees and highInDegrees lists
    highOutDegrees, highInDegrees = [], []
    for i in highDegrees:
        if sum(auxM[i]) >= 2*avgDegrees:
            highOutDegrees.append(i)
        if sum(reverseAuxM[i]) >= 2*avgDegrees:
            highInDegrees.append(i)

    # Create a copy of a M, which will represents the G' distribution
    _M = ut.copyMatrix(M)

    # Search for edges from highOutDegree to highInDegree
    edges = []
    for i in highOutDegrees:
        for j in range(n):
            if auxM[i][j] == 1 and j in highInDegrees:
                edges.append((i, j))

    # Create an helping history
    # register for each lowDegree the number of times
    # it serves for an helping node
    # it will be at most avgDegree
    helpingHist = [0 for i in range(len(lowDegrees))]

    # Compute G' distribution
    for edge in edges:
        high, low = edge[0], edge[1]

        # the next volunteer to help
        # is the first lowDegree which has least helped
        volunteer = lowDegrees[helpingHist.index(min(helpingHist))]

        _M[high][low] = 0
        _M[high][volunteer] += M[high][low]
        _M[volunteer][low] += M[high][low]

    reverse_M = ut.reverseMatrix(_M)

    for i in highOutDegrees:
        ut.buildTree(_M[i], i, N, 0, True)

    for i in highInDegrees:
        ut.buildTree(reverse_M[i], i, N, 0, False)

    return N