import networkx as nx
import numpy as np
from ast import literal_eval

def getAverageDegree(G):
    degrees = dict(G.degree())
    n = len(G)
    return sum(degrees.values())/n

def getMaxDegree(G):
    degrees = sorted([d for n, d in G.degree()], reverse=True)
    return max(degrees)

def getDegrees(G):
    degrees = sorted(G.degree(), key=lambda x:x[1], reverse=True)
    return degrees

def getEPL(G, N):
    """ Calculation of the expected path length """
    n = len(G)
    M = nx.to_numpy_matrix(G)
    res = 0
    D = dict(nx.all_pairs_shortest_path_length(N))
    for i in range(n):
        for j in range(n):
            res += M[i, j] * D[i][j]
    return res

def getDistances(G):
    n = len(G)
    res = dict(nx.all_pairs_shortest_path_length(G))
    return np.array([[res[i][j] for i in range(n)] for j in range(n)])

def getOutgoingDistribution(G):
    outDegrees = list(dict(G.out_degree()).values())
    return np.array(outDegrees)

def getIncomingDistribution(G):
    inDegrees = list(dict(G.in_degree()).values())
    return np.array(inDegrees)