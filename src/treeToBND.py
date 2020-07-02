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
    if direction == ut.Direction.OUTGOING:
        for i in range(n):
            if i != parent:
                children[i] = M[root, i]
            else:
                children[i] = 0
    elif direction == ut.Direction.INCOMING:
        for i in range(n):
            if i != parent:
                children[i] = M[i, root]
            else:
                children[i] = 0

    # In order to keep in mind the indexes
    # we change the array into an array of two figures [[index, value], ...]
    children = ut.arrayToDictArray(children)
    rows = children[:,1]
    children = children[np.where(rows > 0)]
    ml.melhornTree(children, root, N, direction)

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
    buildTrees(M, reverseM, root, -1, visited, N, ut.Direction.OUTGOING)

    visited = np.zeros(n)
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, ut.Direction.INCOMING)

    return N