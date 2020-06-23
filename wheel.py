import numpy as np
import networkx as nx
import math
import matplotlib.pyplot as plt
import random as rd
import copy

from src import algorithms as al
from src import draw as dr
from src import evaluate as ev
from src import export as ex
from src import utils as ut

def simpleWheel(subset, center, direction="outgoing"):
    """ create a wheel graph on the input nodes subset
    with node i as the center
    """

    n = len(subset)

    res = np.where(subset == center)
    if len(res[0]) == 0:
        raise NameError('node ' + str(center) + ' is not in the subset')
    centerIndex = res[0][0]

    D = dict(zip(np.array([i for i in range(n)]), subset))
    D[0], D[centerIndex] = center, subset[0]

    G = nx.wheel_graph(n)
    G = nx.to_directed(G)

    if direction == "outgoing":
        G.remove_edges_from([(i, 0) for i in range(n)])
    elif direction == "incoming":
        G.remove_edges_from([(0, i) for i in range(n)])
    else:
        raise NameError(str(direction) + ' is not a valid value for direction')

    G = nx.relabel_nodes(G, D)
    return G

def severalWheels(subset, highOutSubsets, highInSubsets):
    """ combination of simples wheels """

    graphs = []

    for highOutNode in highOutSubsets:
        graphs.append(simpleWheel(subset, highOutNode, direction="outgoing"))

    for highInNode in highInSubsets:
        graphs.append(simpleWheel(subset, highInNode, direction="incoming"))

    G = nx.compose_all(graphs)
    return G

choice = 4

### Simple Test for one wheel ###
if choice == 0:
    n = 10
    center = 0
    nodes = np.array([i for i in range(n)])

    G = simpleWheel(nodes, center, direction="outgoing")
    M = nx.to_numpy_matrix(G)
    M /= M.sum()

    dr.printInput(M)
    res = al.sparseToBND(M)

    dr.printRes(M, res, None)

### Simple Test for several wheels ###
elif choice == 1:
    n = 10
    nodes = np.array([i for i in range(n)])
    highOutSubsets = [0]
    highInSubsets = [5]

    G = severalWheels(nodes, highOutSubsets, highInSubsets)
    M = nx.to_numpy_matrix(G)
    M /= M.sum()

    dr.printInput(M)
    res = al.sparseToBND(M)

    dr.printRes(M, res, None)

### All tests for one wheel ###
elif choice == 2:
    n = 500
    EPLs = np.zeros(n)
    maxs = np.zeros(n)

    for m in range(2, n):
        center = 0
        nodes = np.array([i for i in range(m)])

        G = simpleWheel(nodes, center, direction="outgoing")
        M = nx.to_numpy_matrix(G)
        M /= M.sum()

        res = al.sparseToBND(M)
        G = nx.from_numpy_matrix(res)
        EPL = ev.getEPL(M, G)
        _max = ev.getMaxDegree(G)
        EPLs[m] = EPL
        maxs[m] = _max
        print("n = " + str(m) + " EPL = " + str(EPL) + ", max degree = " + str(_max))

    headers = ['nodes', 'EPL', 'max degree']
    file = 'simple_wheel.csv'
    results = []
    for m in range(1, n):
        line = [str(m), str(EPLs[m]), str(maxs[m])]
        results.append(line)
    ex.exportToCSV(file, headers, results)

### All tests for several wheels ###
elif choice == 3:
    n = 10
    nodes = np.array([i for i in range(n)])

    results = []
    index = 0 
    tot = 4**n
    step = tot / 100.
    checkpointIndex = 1
    checkpoint = step

    nbResults = 1000.
    p = nbResults / tot

    for i in range(2**n):
        aux = ut.intToBinaryArray(i, n)
        res = np.where(aux == 1)
        highOutSubsets = res[0]
        
        for j in range(2**n):

            hasard = rd.random()
            if i+j > 0:
            # if i+j > 0 and hasard < p: #(i, j) = (0, 0) leads to error
                aux = ut.intToBinaryArray(j, n)
                res = np.where(aux == 1)
                highInSubsets = res[0]
                
                G = severalWheels(nodes, highOutSubsets, highInSubsets)
                M = nx.to_numpy_matrix(G)
                M /= M.sum()

                res = al.sparseToBND(M)
                G = nx.from_numpy_matrix(res)
                EPL = ev.getEPL(M, G)
                _max = ev.getMaxDegree(G)
                results.append([i, j, EPL, _max])
                # print("highOutIndex = " + str(i) + " highInIndex = " + str(j) + " EPL = " + str(EPL) + ", max degree = " + str(_max))
                if index > checkpoint:
                    print(str(checkpointIndex) + '%')
                    checkpointIndex += 1
                    checkpoint += step

                index+=1

    headers = ['highOutIndex', 'highInIndex', 'EPL', 'max degree']
    file = 'composed_wheels_n10.csv'
    ex.exportToCSV(file, headers, results)

### All permutations of n nodes and k high degree nodes
elif choice == 4:
    k = 2
    n = 48
    nodes = np.array([i for i in range(n)])

    results = []
    index = [0]
    tot = ut.permutations(n, k)
    step = tot / 100.
    checkpointIndex = [1]
    checkpoint = [step]

    def launch(nodes, highOutSubsets, highInSubsets, i, j):
        G = severalWheels(nodes, highOutSubsets, highInSubsets)
        M = nx.to_numpy_matrix(G)
        M /= M.sum()

        res = al.sparseToBND(M)
        G = nx.from_numpy_matrix(res)
        EPL = ev.getEPL(M, G)
        _max = ev.getMaxDegree(G)
        results.append([i, j, EPL, _max])

        if index[0] > checkpoint[0]:
            print(str(checkpointIndex[0]) + '%')
            checkpointIndex[0] += 1
            checkpoint[0] += step

        index[0]+=1

    def aux(tmpOut, tmpIn, left, _k):

        if _k == 0:
            res = np.where(tmpOut == 1)
            highOutSubsets = res[0]

            res = np.where(tmpIn == 1)
            highInSubsets = res[0]
            
            i, j = ut.binaryArrayToInt(tmpOut), ut.binaryArrayToInt(tmpIn)
            launch(nodes, highOutSubsets, highInSubsets, i, j)
            return

        for j in range(left, n):
            _tmpOut = copy.copy(tmpOut)
            _tmpIn = copy.copy(tmpIn)

            _tmpOut[j] = 1
            aux(_tmpOut, _tmpIn, j+1, _k-1)

            _tmpOut = copy.copy(tmpOut)
            _tmpIn[j] = 0, 1
            aux(_tmpOut, _tmpIn, j+1, _k-1)

    aux(np.zeros(n), np.zeros(n), 0, k)
    headers = ['highOutIndex', 'highInIndex', 'EPL', 'max degree']
    file = 'composed_wheels_n48_k2.csv'
    ex.exportToCSV(file, headers, results)

    print(tot, index)

elif choice == 5:
    res = ut.permutations(5, 3)
    print(res)
