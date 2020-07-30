import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

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
    ut.normalizeGraph(G)

    return G

choice = 1

### a simple random graph
if choice == 0:
    n = 20 
    G = randomGraph(n)

    dr.printInput(G)
    res = sp.sparseToBND(G)
    N, layers = res[0], res[1]

    dr.printRes(G, N, None, layers)

### Several test on random graphs
if choice == 1:
    N, n = 100000, 20

    results = []

    inputs = []
    for i in tqdm(range(N)):
        G = randomGraph(n)
        edges = str(G.edges)
        avgDegree = ev.getAverageDegree(G)
        n = len(G)

        res = sp.sparseToBND(G)
        N, layers = res[0], res[1]

        if nx.is_connected(N):
            EPL = ev.getEPL(G, N)
            _max = ev.getMaxDegree(N)
            results.append([EPL, _max, 12*avgDegree, edges])

    headers = ['EPL', 'max degree', 'theorical max degree', 'edges']
    file = 'results/' + 'random_graphs.csv'
    ex.exportToCSV(file, headers, results)
