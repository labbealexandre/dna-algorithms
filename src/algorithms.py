from src import utils as ut
from src import melhorn as ml
from src import chrono as ch
from src import draw as dr
import numpy as np
import networkx as nx
from time import time

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

def chooseHelpingNode(helpingList, lowDegrees, src, dst, M, way=0):
    if way == 0:
        amin = np.argmin(helpingList)

    elif way == 1:
        i = 0
        amin = -1
        _min = -1
        while i < len(lowDegrees):
            node = lowDegrees[i][0]
            if M[src, node] > 0 and (amin == -1 or helpingList[i] < _min):
                _min, amin = helpingList[i], i
            i+=1

        if amin == -1:
            # print(str(src) + ' -> ' + str(dst) + ' failed to find in the neighbourhood')
            amin = np.argmin(helpingList)

    elif way == 2:
        i = 0
        amin = np.argmin(helpingList)
        _min = np.min(helpingList)
        while i < len(lowDegrees):
            node = lowDegrees[i][0]
            if M[src, node] > 0 and helpingList[i] == _min:
                _min, amin = helpingList[i], i
                # print('found in the neighbourhood')
                break
            i+=1

    elif way == 3:
        i = 0
        amin = np.argmin(helpingList)
        _min = np.min(helpingList)
        while i < len(lowDegrees):
            node = lowDegrees[i][0]
            if M[node, dst] > 0 and helpingList[i] == _min:
                _min, amin = helpingList[i], i
                # print('found in the neighbourhood')
                break
            i+=1

    elif way == 4:
        i = 0
        amin = -1
        _min = -1
        while i < len(lowDegrees):
            node = lowDegrees[i][0]
            if M[src, node] == 0 and (amin == -1 or helpingList[i] < _min):
                _min, amin = helpingList[i], i
            i+=1

        if amin == -1:
            # print(str(src) + ' -> ' + str(dst) + ' failed to find outside the neighbourhood')
            amin = np.argmin(helpingList)

    helpingList[amin]+=1

    return lowDegrees[amin]

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

def sparseToBND(M, time_stats=False, debug=False):

    """
    Theorem 4 : get a Bounded Network Design from
    a request distribution such as the graph is sparse
    """

    t0 = ch.initRecord()
    tLast = t0
    records = []

    n = len(M)

    # N will be the result unweighted graph
    N = np.zeros((n, n))
    auxM = np.ceil(M)

    auxG = nx.from_numpy_matrix(auxM, create_using=nx.MultiDiGraph())
    avgDegrees = 2.*nx.number_of_edges(auxG)/n

    ### begin time stat ###
    if time_stats: tLast = tLast = ch.addRecord(records, tLast, "initialization")
    ### end time stat ###

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
        if auxG.out_degree(i[0]) >= 2*avgDegrees:
            highOutDegrees.append(i)
        if auxG.in_degree(i[0]) >= 2*avgDegrees:
            highInDegrees.append(i)

    # highDegrees = np.array(highDegrees)
    # print(highDegrees)
    # print('original', highInDegreesOld, highOutDegreesOld)
    # highOutFilter = auxG.out_degree(highDegrees[:,0]) >= 2*avgDegrees
    # highInFilter = auxG.in_degree(highDegrees[:,0]) >= 2*avgDegrees

    # print('filter', highInFilter, highOutFilter)

    # highOutDegrees = highDegrees[highOutFilter]
    # highInDegrees = highDegrees[highInFilter]
    # print('new', highInDegrees, highOutDegrees)

    ### begin time stat ###
    if time_stats: tLast = ch.addRecord(records, tLast, "sorting by degrees")
    ### end time stat ###

    # Create a copy of a M, which will represents the G' distribution
    _M = np.copy(M)
    if debug: dr.printInput(_M)

    # Search for edges from highOutDegree to highInDegree
    edges = []
    for i in highOutDegrees:
        for j in highInDegrees:
            if auxM[i[0], j[0]] > 0:
                edges.append((i[0], j[0]))

    # Create an helping history
    # register for each lowDegree the number of times
    # it serves for an helping node
    # it will be at most avgDegree
    helpingList = np.zeros(len(lowDegrees))

    ### Compute G' distribution ###

    for edge in edges:
        src, dst = edge[0], edge[1]

        # find the next volunteer
        volunteer = chooseHelpingNode(helpingList, lowDegrees, src, dst, M, way=2)

        _M[src, dst] = 0
        _M[src, volunteer] += M[src, dst]
        _M[volunteer, dst] += M[src, dst]

    ### begin time stat ###
    if time_stats: tLast = ch.addRecord(records, tLast, "compute G'")
    ### end time stat ###, headers
    # Initialization of N according to _M

    N = np.ceil(_M)

    # Binary trees from highOutDegrees and highInDegrees
    for i in highOutDegrees:
        # We remove from N the out-neigbourhood of i in M
        # We do not want to remove edges we have already created
        aux = np.ceil(_M[i[0],:])
        N[i[0],:] -= aux

        ml.melhornTree(_M[i[0],:], i[0], N, 0, "outgoing")

    for i in highInDegrees:
        # We remove from N the in-neigbourhood of i in M
        aux = np.ceil(_M[:,i[0]])
        N[:,i[0]] -= aux

        ml.melhornTree(_M[:,i[0]], i[0], N, 0, "incoming")

    ### begin time stat ###
    if time_stats: tLast = ch.addRecord(records, tLast, "compute N")
    ### end time stat ###

    ### begin time stat ###
    if time_stats: ch.addRecord(records, t0, "total")
    ### end time stat ###

    if time_stats:
        return [n] + records
        
    return N