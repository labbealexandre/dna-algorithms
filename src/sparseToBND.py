from src import utils as ut
from src import melhorn as ml
from src import chrono as ch
from src import draw as dr
import numpy as np
import networkx as nx
from time import time

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

def getSortedNodes(degrees, n, auxG):
    # avgDegrees will be usefull to find high-out-degree nodes
    # and high-in-degree nodes
    avgDegrees = 2.*nx.number_of_edges(auxG)/n

    # Fill the lowDegrees and highDegrees lists
    m = n//2
    lowDegrees = degrees[:m]
    highDegrees = degrees[m:]

    # Optionnal sort, to be sure of the result
    lowDegrees.sort()
    highDegrees.sort()

    highDegrees = np.array(highDegrees)

    outDegrees = np.array(auxG.out_degree(highDegrees[:,0]))
    aux = outDegrees[:,1]
    mask = aux >= 2*avgDegrees
    highOutDegrees = outDegrees[mask]

    inDegrees = np.array(auxG.in_degree(highDegrees[:,0]))
    aux = inDegrees[:,1]
    mask = aux >= 2*avgDegrees
    highInDegrees = inDegrees[mask]

    return [lowDegrees, highOutDegrees, highInDegrees]

def addHelpingNodes(_M, highOutDegrees, highInDegrees, lowDegrees, M):
    # Search for edges from highOutDegree to highInDegree
    edges = []
    for i in highOutDegrees:
        for j in highInDegrees:
            if M[i[0], j[0]] > 0:
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
        volunteer = chooseHelpingNode(helpingList, lowDegrees, src, dst, M, way=0)

        _M[src, dst] = 0
        _M[src, volunteer] += M[src, dst]
        _M[volunteer, dst] += M[src, dst]

def addBinarytrees(_M, N, highOutDegrees, highInDegrees):
    n, _ = N.shape
    layers = [] # used to save the sub-graphs generated
    # by the melhorn algorithm
    # Binary trees from highOutDegrees and highInDegrees
    for i in highOutDegrees:
        # We remove from N the out-neigbourhood of i in M
        # We do not want to remove edges we have already created
        aux = np.ceil(_M[i[0],:])
        N[i[0],:] -= aux

        layer = np.zeros((n, n))

        # In order to keep in mind the indexes
        # we change the array into an array of two figures [[index, value], ...]
        children = ut.arrayToDictArray(_M[i[0],:])

        ml.melhornTree(children, i[0], N, "outgoing", layer)
        layers.append(layer)

    for i in highInDegrees:
        # We remove from N the in-neigbourhood of i in M
        aux = np.ceil(_M[:,i[0]])
        N[:,i[0]] -= aux

        layer = np.zeros((n, n))

        # In order to keep in mind the indexes
        # we change the array into an array of two figures [[index, value], ...]
        children = ut.arrayToDictArray(_M[:,i[0]])

        ml.melhornTree(children, i[0], N, "incoming", layer)
        layers.append(layer)

    return layers

def sparseToBND(M, debug=False):

    """
    Theorem 4 : get a Bounded Network Design from
    a request distribution such as the graph is sparse
    """

    n = len(M)

    # N will be the result unweighted graph
    N = np.zeros((n, n))
    auxM = np.ceil(M)

    auxG = nx.from_numpy_matrix(auxM, create_using=nx.MultiDiGraph())
    degrees = sorted(auxG.degree(), key=lambda x: x[1])

    res = getSortedNodes(degrees, n, auxG)
    lowDegrees, highOutDegrees, highInDegrees = res[0], res[1], res[2]

    # Create a copy of a M, which will represents the G' distribution
    _M = np.copy(M)
    if debug: dr.printInput(_M)

    # Find edges from high-out to high-in-degree nodes
    # And remove it thanks to an helping node wisely chosen
    addHelpingNodes(_M, highOutDegrees, highInDegrees, lowDegrees, M)

    # Initialization of N according to _M
    N = np.ceil(_M)

    # Creat melhorn trees from high-out and high-in degree nodes
    layers = addBinarytrees(_M, N, highOutDegrees, highInDegrees)

    return [N, layers]