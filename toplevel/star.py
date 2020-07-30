import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy

from src import sparseToBND as sp
from src import draw as dr
from src import evaluate as ev
from src import export as ex
from src import utils as ut

def simpleStar(subset, center, direction=ut.Direction.OUTGOING):
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
    G = nx.DiGraph(G)

    if direction == ut.Direction.OUTGOING:
        G.remove_edges_from([(i, 0) for i in range(n)])
    elif direction == ut.Direction.INCOMING:
        G.remove_edges_from([(0, i) for i in range(n)])
    else:
        raise NameError(str(direction) + ' is not a valid value for direction')

    G = nx.relabel_nodes(G, D)
    ut.normalizeGraph(G)
    return G

def simpleCycleGraph(subset):
    n = len(subset)

    D = dict(zip(np.array([i for i in range(n)]), subset))

    G = nx.cycle_graph(n)
    G = nx.to_directed(G)

    G = nx.relabel_nodes(G, D)
    ut.normalizeGraph(G)
    return G

def severalStarGraphs(m, k, highSubsets):
    graphs = []
    centers = []

    for i in range(k):
        center = i*(m+1)
        centers.append(center)
        nodes = np.array([j+center for j in range(m+1)])

        if (highSubsets[i] == 1):
            graphs.append(simpleStar(nodes, center, direction=ut.Direction.OUTGOING))
        else:
            graphs.append(simpleStar(nodes, center, direction=ut.Direction.INCOMING))
    
    graphs.append(simpleCycleGraph(centers))

    G = nx.compose_all(graphs)
    ut.normalizeGraph(G)

    return G

def superStar(k, m, highSubsets, direction=ut.Direction.OUTGOING):

    graphs = []
    graphs.append(severalStarGraphs(m, k, highSubsets))

    last = k*(m+1)
    nodes = np.array([j*(m+1) for j in range(k+1)])
    graphs.append(simpleStar(nodes, last, direction=direction))

    G = nx.compose_all(graphs)
    ut.normalizeGraph(G)

    return G

def superStars(k, m, highSubsets, kernelsSubsets):
    graphs = []
    graphs.append(severalStarGraphs(m, k, highSubsets))

    s = len(kernelsSubsets)
    kernels = []
    for i in range(s):
        kernel = (k+i)*(m+1)
        kernels.append(kernel)
        nodes = np.array([j*(m+1) for j in range(k)]+[kernel])

        if (kernelsSubsets[i] == 1):
             graphs.append(simpleStar(nodes, kernel, direction=ut.Direction.OUTGOING))
        else:
            graphs.append(simpleStar(nodes, kernel, direction=ut.Direction.INCOMING))

    if s > 1:
        graphs.append(simpleCycleGraph(kernels))

    G = nx.compose_all(graphs)
    ut.normalizeGraph(G)

    return G

choice = 6

### Simple test for one star
if choice == 0:
    n = 10
    center = 0
    nodes = np.array([i for i in range(n)])

    G = simpleStar(nodes, center, direction=ut.Direction.OUTGOING)

    dr.printInput(G)
    res = sp.sparseToBND(G)
    N, layers = res[0], res[1]

    dr.printRes(G, N, None, layers)

### Simple test for several stars ###
elif choice == 1:
    k = 8 # number of stars
    m = 5 # number of branches per star

    highSubsets = np.array([0,0,0,0,0,0,0,0])
    G = severalStarGraphs(m, k, highSubsets)

    dr.printInput(G)
    res = sp.sparseToBND(G, debug=True)
    N, layers = res[0], res[1]

    dr.printRes(G, N, None, layers)

    if not nx.is_connected(N):
        subgraphs = list(nx.connected_component_subgraphs(N))
        for H in subgraphs:
            nx.draw_networkx(H)
            plt.show()
        raise NameError('The result graph is not connected')

### All permutations of k high degree nodes and n = k*m nodes
elif choice == 2:
    k = 8 # nb of stars
    m = 5 # branches per star

    nodes = np.array([i for i in range(k*m)])

    results = []
    index = [0]
    tot = 2**k
    step = tot / 100.
    checkpointIndex = [1]
    checkpoint = [step]

    def launch(nodes, highSubsets, i):

        G = severalStarGraphs(m, k, highSubsets)

        res = sp.sparseToBND(G)
        N, layers = res[0], res[1]

        if not nx.is_connected(N):
            subgraphs = list(nx.connected_component_subgraphs(N))
            for H in subgraphs:
                nx.draw_networkx(H)
                plt.show()
            raise NameError('The result graph is not connected')

        EPL = ev.getEPL(G, N)
        _max = ev.getMaxDegree(N)
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
    file = 'composed_stars_k8_m5.csv'
    ex.exportToCSV(file, headers, results)

### Simple test for a superstar
elif choice == 3:
    k = 10
    m = 3

    highSubsets = np.array([0,1,0,1,0,1,0,1,0,1])

    G = superStar(k, m, highSubsets)

    dr.printInput(G)
    res = sp.sparseToBND(G, debug=False)
    N, layers = res[0], res[1]

    dr.printRes(G, N, None, layers)

### All permutations of superstars (k, m)
elif choice == 4:
    k = 10 # nb of stars
    m = 3 # branches per star

    nodes = np.array([i for i in range(k*m+1)])

    results = []
    index = [0]
    tot = 2**k
    step = tot / 100.
    checkpointIndex = [1]
    checkpoint = [step]

    def launch(nodes, highSubsets, i):

        G = superStar(k, m, highSubsets)

        res = sp.sparseToBND(G)
        N, layers = res[0], res[1]

        if not nx.is_connected(N):
            subgraphs = list(nx.connected_component_subgraphs(N))
            for H in subgraphs:
                nx.draw_networkx(H)
                plt.show()
            raise NameError('The result graph is not connected')

        EPL = ev.getEPL(G, N)
        _max = ev.getMaxDegree(N)
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
    file = 'superstars_k10_m3.csv'
    ex.exportToCSV(file, headers, results)

### Simple test for a combination of superstars
elif choice == 5:
    k = 10
    m = 4

    highSubsets = np.array([0,1,0,1,0,1,0,1,0,1])
    kernelSubsets = np.array([1,0])

    G = superStars(k, m, highSubsets, kernelSubsets)

    dr.printInput(G)
    res = sp.sparseToBND(G, debug=False)
    N, layers = res[0], res[1]

    dr.printRes(G, N, None, layers)

    ### All permutations of couple superstars (k, m)
elif choice == 6:
    k = 10 # nb of stars
    m = 4 # branches per star

    nodes = np.array([i for i in range(k*m+1)])
    kernelSubsets = np.array([1,0])

    results = []
    index = [0]
    tot = 2**k
    step = tot / 100.
    checkpointIndex = [1]
    checkpoint = [step]

    def launch(nodes, highSubsets, i):

        G = superStars(k, m, highSubsets, kernelSubsets)

        res = sp.sparseToBND(G)
        N, layers = res[0], res[1]

        if not nx.is_connected(N):
            subgraphs = list(nx.connected_component_subgraphs(N))
            for H in subgraphs:
                nx.draw_networkx(H)
                plt.show()
            raise NameError('The result graph is not connected')

        EPL = ev.getEPL(G, N)
        _max = ev.getMaxDegree(N)
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
    file = 'couple_superstars_k10_m4.csv'
    ex.exportToCSV(file, headers, results)