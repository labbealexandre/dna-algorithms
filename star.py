import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy

from src import algorithms as al
from src import draw as dr
from src import evaluate as ev
from src import export as ex
from src import utils as ut

def simpleStar(subset, center, direction="outgoing"):
    """ create a star graph on the input nodes subset
    with node i as the center
    """

    n = len(subset)

    if n == 0:
        raise NameError('There needs to be at least one node')

    res = np.where(subset == center)
    if len(res[0]) == 0:
        raise NameError('node ' + str(center) + ' is not in the subset')
    centerIndex = res[0][0]


    D = dict(zip(np.array([i for i in range(n)]), subset))
    D[0], D[centerIndex] = center, subset[0]

    G = nx.star_graph(n-1)
    G = nx.to_directed(G)

    if direction == "outgoing":
        G.remove_edges_from([(i, 0) for i in range(n)])
    elif direction == "incoming":
        G.remove_edges_from([(0, i) for i in range(n)])
    else:
        raise NameError(str(direction) + ' is not a valid value for direction')

    G = nx.relabel_nodes(G, D)
    return G

def simpleCycleGraph(subset):
    n = len(subset)

    D = dict(zip(np.array([i for i in range(n)]), subset))

    G = nx.cycle_graph(n)
    G = nx.to_directed(G)

    G = nx.relabel_nodes(G, D)
    return G

def severalStarGraphs(m, k, highSubsets):
    graphs = []
    centers = []

    for i in range(k):
        center = i*(m+1)
        centers.append(center)
        nodes = np.array([j+center for j in range(m+1)])

        if (highSubsets[i] == 1):
            graphs.append(simpleStar(nodes, center, direction="outgoing"))
        else:
            graphs.append(simpleStar(nodes, center, direction="incoming"))
    
    graphs.append(simpleCycleGraph(centers))

    G = nx.compose_all(graphs)

    return G

choice = 1

### Simple test for one star
if choice == 0:
    n = 10
    center = 0
    nodes = np.array([i for i in range(n)])

    G = simpleStar(nodes, center, direction="outgoing")
    M = nx.to_numpy_matrix(G)
    M /= M.sum()

    dr.printInput(M)
    res = al.sparseToBND(M)

    dr.printRes(M, res, None)

### Simple test for several stars ###
elif choice == 1:
    k = 5
    m = 3

    graphs = []
    centers = []

    highSubsets = np.array([0, 0, 1, 0, 1])
    G = severalStarGraphs(m, k, highSubsets)

    # for i in range(k):
    #     center = i*(m+1)    
    #     centers.append(center)
    #     nodes = np.array([j+center for j in range(m+1)])

    #     graphs.append(simpleStar(nodes, center, direction="incoming"))
    
    # graphs.append(simpleCycleGraph(centers))

    # G = nx.compose_all(graphs)

    M = nx.to_numpy_matrix(G)
    M /= M.sum()

    dr.printInput(M)
    res = al.sparseToBND(M)
    G = nx.from_numpy_matrix(res)

    dr.printRes(M, res, None)

    if not nx.is_connected(G):
        subgraphs = list(nx.connected_component_subgraphs(G))
        for H in subgraphs:
            nx.draw_networkx(H)
            plt.show()
        raise NameError('The result graph is not connected')

### All permutations of k high degree nodes and n = k*m nodes
elif choice == 2:
    k = 5 # nb of stars
    m = 3 # branches per star

    nodes = np.array([i for i in range(k*m)])

    results = []
    index = [0]
    tot = 2**k
    step = tot / 100.
    checkpointIndex = [1]
    checkpoint = [step]

    def launch(nodes, highSubsets, i):

        G = severalStarGraphs(m, k, highSubsets)

        M = nx.to_numpy_matrix(G)
        M /= M.sum()

        res = al.sparseToBND(M)
        G = nx.from_numpy_matrix(res)

        if not nx.is_connected(G):
            subgraphs = list(nx.connected_component_subgraphs(G))
            for H in subgraphs:
                nx.draw_networkx(H)
                plt.show()
            raise NameError('The result graph is not connected')

        EPL = ev.getEPL(M, G)
        _max = ev.getMaxDegree(G)
        results.append([i, EPL, _max])

        if index[0] > checkpoint[0]:
            print(str(checkpointIndex[0]) + '%')
            checkpointIndex[0] += 1
            checkpoint[0] += step

        index[0]+=1

    def aux(tmp, left):

        if left == len(tmp):
            i = ut.binaryArrayToInt(tmp)
            launch(nodes, tmp, i)
            return

        _tmp = copy.copy(tmp)
        _tmp[left] = 0
        aux(_tmp, left+1)

        _tmp = copy.copy(tmp)
        _tmp[left] = 1
        aux(_tmp, left+1)

    aux(np.zeros(k), 0)
    headers = ['highIndex', 'EPL', 'max degree']
    file = 'composed_stars_k5_m3.csv'
    ex.exportToCSV(file, headers, results)