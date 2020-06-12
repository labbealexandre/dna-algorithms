import networkx as nx
import numpy as np
from ast import literal_eval

def getMaxDegree(G):
    degrees = sorted([d for n, d in G.degree()], reverse=True)
    return max(degrees)

def getEPL(M, G):
    """ Calculation of the expected path length """
    n, _ = M.shape
    res = 0
    D = getDistances(G)
    for i in range(n):
        for j in range(n):
            res += M[i, j] * D[i, j]
    return res

def getDistances(G):
    n = len(G)
    res = dict(nx.all_pairs_shortest_path_length(G))
    return np.array([[res[i][j] for i in range(n)] for j in range(n)])

def getOutgoingDistribution(M):
    n, _ = M.shape
    D = np.zeros(n)
    for i in range(n):
        D[i] = np.sum(M[i,:])
    return D

def getIncomingDistribution(M):
    n, _ = M.shape
    D = np.zeros(n)
    for i in range(n):
        D[i] = np.sum(M[:,i])
    return D