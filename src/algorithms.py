from src import utils as ut
from src import melhorn as ml
import numpy as np
import networkx as nx

def buildTrees(M, reverseM, root, parent, visited, N, direction):

    if visited[root] == 1:
        return

    visited[root] = 1
    n = len(M)

    children = np.zeros(n)
    if direction == "outgoing":
        for i in range(n):
            if i != parent:
                children[i] = M[root, i]
            else:
                children[i] = 0
    elif direction == "incoming":
        for i in range(n):
            if i != parent:
                children[i] = M[i, root]
            else:
                children[i] = 0

    ml.melhornTree(children, root, N, 0, direction)

    for i in range(n):
        if (i != parent):
            if M[root, i] > 0:
                buildTrees(M, reverseM, i, root, visited, N, direction)
            if M[i, root] > 0:
                buildTrees(M, reverseM, i, root, visited, N, direction)


def treeToBND(M):
    """
    Theorem 3 : get a Bounded Network Design from
    a request distribution such as the graph is a tree
    """

    n = len(M)
    reverseM = np.transpose(M)

    # N will be the result the result unweighted graph
    N = np.zeros((n, n))
            
    # We arbitrary set the root as 0
    visited = np.zeros(n)
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, "outgoing")

    visited = np.zeros(n)
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, "incoming")

    return N

def sparseToBND(M):

    """
    Theorem 4 : get a Bounded Network Design from
    a request distribution such as the graph is sparse
    """

    n = len(M)

    # N will be the result unweighted graph
    N = np.zeros((n, n))
    auxM = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if M[i, j] > 0:
                auxM[i, j] = 1

    auxG = nx.from_numpy_matrix(auxM, create_using=nx.MultiDiGraph())
    avgDegrees = 2.*nx.number_of_edges(auxG)/n

    degrees = sorted(auxG.degree(), key=lambda x: x[1])

    # Fill the lowDegrees and highDegrees lists
    m = n//2
    lowDegrees = degrees[:m]
    highDegrees = degrees[m:]

    # Optionnal sort, to be sure of the result
    lowDegrees.sort()
    highDegrees.sort()

    # Fill the highOutDegrees and highInDegrees lists
    highOutDegrees, highInDegrees = [], []
    for i in highDegrees:
        if np.sum(auxG.out_degree(i[0])) >= 2*avgDegrees:
            highOutDegrees.append(i)
        if np.sum(auxG.in_degree(i[0])) >= 2*avgDegrees:
            highInDegrees.append(i)

    # Create a copy of a M, which will represents the G' distribution
    _M = np.copy(M)

    # Search for edges from highOutDegree to highInDegree
    edges = []
    for i in highOutDegrees:
        for j in highInDegrees:
            if auxM[i[0], j[0]] == 1:
                edges.append((i[0], j[0]))

    # Create an helping history
    # register for each lowDegree the number of times
    # it serves for an helping node
    # it will be at most avgDegree
    helpingHist = np.zeros(len(lowDegrees))

    ### Compute G' distribution ###

    for edge in edges:
        high, low = edge[0], edge[1]

        # the next volunteer to help
        # is the first lowDegree which has least helped
        volunteer = lowDegrees[np.argmin(helpingHist)]

        _M[high, low] = 0
        _M[high, volunteer] += M[high, low]
        _M[volunteer, low] += M[high, low]

    ### Construction of N from G' ###

    # Initialization of N according to _M

    for i in range(n):
        for j in range(n):
            if _M[i, j] > 0:
                N[i, j] = 1

    # Binary trees from highOutDegrees and highInDegrees
    for i in highOutDegrees:
        N[i[0],:] = np.zeros(n)
        ml.melhornTree(_M[i[0],:], i[0], N, 0, "outgoing")

    for i in highInDegrees:
        N[:,i[0]] = np.zeros(n)
        ml.melhornTree(_M[:,i[0]], i[0], N, 0, "incoming")

    return N