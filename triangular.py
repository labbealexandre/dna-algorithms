import numpy as np
import networkx as nx

from src import algorithms as al
from src import draw as dr

def triangular(n):
    """ graph construction : node i is connected to (0, ..., n-1) """

    # add edges with arbitratry weight
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(i):
            M[i, j] = 1
    
    # Normalization
    M /= M.sum()
    return M

n = 5
M = triangular(n)

dr.printInput(M)
res = al.sparseToBND(M)

dr.printRes(M, res, None)