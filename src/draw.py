import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math

from src import evaluate as ev

def matrixToGraph(N, weighted):

    G = nx.DiGraph()
    n = len(N)

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(n):
            if N[i][j] > 0:
                if (weighted):
                    G.add_edge(i, j, weight=N[i][j])
                else:
                    G.add_edge(i, j)
    
    return G

def printInput(M):

    n, _ = M.shape

    MG = nx.from_numpy_matrix(M, create_using=nx.DiGraph)

    MFig = plt.subplot(121, aspect='equal')
    MFig.set_title("Input Distribution")
    pos = nx.spring_layout(MG)
    if (n < 50):
        nx.draw_networkx_nodes(MG, pos)
        nx.draw_networkx_labels(MG, pos)
    if (n < 5):
        labels = nx.get_edge_attributes(MG, 'weight')
        nx.draw_networkx_edge_labels(MG, pos, edge_labels=labels)
    nx.draw_networkx_edges(MG, pos, arrowstyle='->', arrowsize=10)
    plt.plot()

    n, _ = M.shape
    nodes = np.array([i for i in range(n)])

    OFig = plt.subplot(222)
    OFig.set_title("Outgoing nodes distribution")
    outgoingDistribution = ev.getOutgoingDistribution(M)
    plt.plot(nodes, outgoingDistribution)

    IFig = plt.subplot(224)
    IFig.set_title("Incoming nodes distribution")
    incomingDistribution = ev.getIncomingDistribution(M)
    plt.plot(nodes, incomingDistribution)

    plt.show()

def printRes(M, res, expected):

    fig = plt.figure()
    n, _ = res.shape

    ### Parameters
    if (n < 50):
        withLabel = True
        nodeSize = 300
    else:
        withLabel = False
        nodeSize = 0

    resG = nx.from_numpy_matrix(res)
    resEPL = ev.getEPL(M, resG)
    resMax = ev.getMaxDegree(resG)
    if expected is None:
        resFig = fig.add_subplot(111,aspect='equal')
    else:
        resFig = fig.add_subplot(121,aspect='equal')
    resFig.title.set_text("result (EPL = " + str(resEPL) + ", max degree = " + str(resMax) + ")")
    nx.draw_circular(resG, with_labels=withLabel, node_size=nodeSize)

    if not expected is None:
        expectedG = nx.from_numpy_matrix(expected)
        expectedEPL = ev.getEPL(M, expectedG)
        expectedFig = fig.add_subplot(122,aspect='equal')
        expectedFig.title.set_text("expected (EPL = " + str(expectedEPL) + ")")
        nx.draw_circular(expectedG, with_labels=withLabel, node_size=nodeSize)

    plt.plot()
    plt.show()