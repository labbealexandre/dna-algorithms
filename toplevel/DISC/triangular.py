import numpy as np
import networkx as nx

from src import sparseToBND as sp
from src import draw as dr
from src import utils as ut

def triangular(n):
    """ graph construction : node i is connected to (0, ..., n-1) """

    # add edges with arbitratry weight
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(i):
            M[i, j] = 1
    
    G = nx.from_numpy_matrix(M, create_using=nx.DiGraph)
    ut.normalizeGraph(G)
    return G

n = 5
G = triangular(n)

dr.printInput(G)
N, _ = sp.sparseToBND(G)

dr.printRes(G, N, None)