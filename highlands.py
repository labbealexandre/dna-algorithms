import numpy as np
import networkx as nx
import math

from src import algorithms as al
from src import draw as dr
from src import evaluate as ev
from src import export as ex

def highlands(n, m):
    """ graph construction : node is connected to (i+1 mod n, ..., i+h mod n) if i mod m = 0"""

    M = np.zeros((n, n))

    # add edges with arbitratry weight
    for i in range(n):
        if i % m == 0:
            for k in range(1, m+1):
                j = (i + k) % n
                M[i, j] = 1

    # Normalization
    M /= M.sum()
    return M

### Simple Test ###
n, m = 9, 3
M = highlands(n, m)

dr.printInput(M)
res = al.sparseToBND(M)

dr.printRes(M, res, None)

### Time tests ###
# k = 10000
# n = 5

# results = []

# while n < k:
#     m = int(math.sqrt(n))
#     M = highlands(n, m)

#     print("nodes : " + str(n) + ", pics : " + str(m))
#     res = al.sparseToBND(M, time_stats=True)
#     print("")
#     results.append(res)

#     n=int(n*1.2)

# file = 'sparse_perf.csv'
# headers = ['nodes', 'initialization', 'sort by degree', 'compute G\'', 'compute N', 'total']
# ex.exportToCSV(file, headers, results)

### All tests ###
# n = 1000
# EPLs = np.zeros(n)
# maxs = np.zeros(n)

# for m in range(n):
#     _m = m+1
#     M = highlands(n, _m)
#     res = al.sparseToBND(M)
#     G = nx.from_numpy_matrix(res)
#     EPL = ev.getEPL(M, G)
#     _max = ev.getMaxDegree(G)
#     EPLs[m] = EPL
#     maxs[m] = _max
#     print("m = " + str(_m) + ", EPL = " + str(EPL) + ", max degree = " + str(_max))

# headers = ['Highlands number', 'EPL', 'max degree']
# file = str(n) + '_nodes.csv'
# results = []
# for m in range(n):
#     line = [str(m+1), str(EPLs[m]), str(maxs[m])]
#     results.append(line)
# ex.exportToCSV(file, headers, results)
