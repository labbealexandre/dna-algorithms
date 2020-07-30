import numpy as np
import networkx as nx
import math

from src import sparseToBND as sp
from src import draw as dr
from src import evaluate as ev
from src import export as ex
from src import utils as ut

def highlands(n, m):
    """ graph construction : node is connected to (i+1 mod n, ..., i+h mod n) if i mod m = 0"""

    M = np.zeros((n, n))

    # add edges with arbitratry weight
    for i in range(n):
        if i % m == 0:
            for k in range(1, m+1):
                j = (i + k) % n
                M[i, j] = 1

    G = nx.from_numpy_matrix(M, create_using=nx.DiGraph)
    ut.normalizeGraph(G)

    return G

choice = 0

### Simple Test ###
if choice == 0:
    n, m = 9, 3
    G = highlands(n, m)

    dr.printInput(G)
    res = sp.sparseToBND(G)
    N = res[0]

    dr.printRes(G, N, None)

### All tests ###
elif choice == 1:
    n = 10
    EPLs = np.zeros(n)
    maxs = np.zeros(n)

    for m in range(n):
        _m = m+1
        G = highlands(n, _m)
        res = sp.sparseToBND(G)
        N = res[0]
        EPL = ev.getEPL(G, N)
        _max = ev.getMaxDegree(N)
        EPLs[m] = EPL
        maxs[m] = _max
        print("m = " + str(_m) + ", EPL = " + str(EPL) + ", max degree = " + str(_max))

    headers = ['Highlands number', 'EPL', 'max degree']
    file = str(n) + '_nodes.csv'
    results = []
    for m in range(n):
        line = [str(m+1), str(EPLs[m]), str(maxs[m])]
        results.append(line)
    ex.exportToCSV(file, headers, results)
