import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src import sparseToBND as sp
from src import draw as dr
from src import evaluate as ev
from src import export as ex
from src import utils as ut

def randomGraph(n):
    # p the probability of an edge between two nodes
    # is chosen in order to make the number of edges
    # proportionnal to n
    p = 2./(n-1)

    G = nx.fast_gnp_random_graph(n, p, directed=True)
    G.remove_nodes_from(list(nx.isolates(G)))

    _n = nx.number_of_nodes(G)
    nodes = np.array(G.nodes)
    D = dict(zip(nodes, np.array([i for i in range(_n)])))
    G = nx.relabel_nodes(G, D)

    return G

choice = 1

### a simple random graph
if choice == 0:
    n = 20 
    G = randomGraph(n)
    M = nx.to_numpy_matrix(G)
    M /= M.sum()

    dr.printInput(M)
    res = sp.sparseToBND(M)
    N, layers = res[0], res[1]

    dr.printRes(M, N, None, layers)

### Several test on random graphs
if choice == 1:
    N, n = 100000, 20

    results = []
    index = 0
    tot = N
    step = tot / 100.
    checkpointIndex = 1
    checkpoint = step

    inputs = []
    for i in range(N):
        G = randomGraph(n)
        edges = str(G.edges)
        M = nx.to_numpy_matrix(G)
        avgDegree = ev.getAverageDegree(M)
        M /= M.sum()
        n, _ = M.shape

        res = sp.sparseToBND(M)
        N, layers = res[0], res[1]
        G = nx.from_numpy_matrix(N)

        if nx.is_connected(G):
            EPL = ev.getEPL(M, G)
            _max = ev.getMaxDegree(G)
            results.append([EPL, _max, 12*avgDegree, edges])

        if index > checkpoint:
            print(str(checkpointIndex) + '%')
            checkpointIndex += 1
            checkpoint += step

        index+=1

    headers = ['EPL', 'max degree', 'theorical max degree', 'edges']
    file = 'random_graphs.csv'
    ex.exportToCSV(file, headers, results)



