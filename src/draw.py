import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import random as rd

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

def printInput(G):

    n = len(G)

    avgDegree = ev.getAverageDegree(G)

    MFig = plt.subplot(121, aspect='equal')
    MFig.set_title("Input Distribution (average degree = " + str(avgDegree) + ")")
    pos = nx.spring_layout(G)
    if (n < 50):
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_labels(G, pos)
    if (n < 5):
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10)
    plt.plot()

    nodes = np.array([i for i in range(n)])

    OFig = plt.subplot(222)
    OFig.set_title("Outgoing nodes distribution")
    outgoingDistribution = ev.getOutgoingDistribution(G)
    plt.plot(nodes, outgoingDistribution)

    IFig = plt.subplot(224)
    IFig.set_title("Incoming nodes distribution")
    incomingDistribution = ev.getIncomingDistribution(G)
    plt.plot(nodes, incomingDistribution)

    plt.show()

def printRes(G, resG, expectedG, layers=[]):

    fig = plt.figure()
    n = len(G)

    ### Parameters
    if (n < 50):
        withLabel = True
        nodeSize = 300
    else:
        withLabel = False
        nodeSize = 0

    if expectedG is None:
        resFig = fig.add_subplot(111,aspect='equal')
    else:
        resFig = fig.add_subplot(121,aspect='equal')

    if nx.is_connected(resG):
        resEPL = ev.getEPL(G, resG)
        resMax = ev.getMaxDegree(resG)
        resFig.title.set_text("result (EPL = " + str(resEPL) + ", max degree = " + str(resMax) + ")")

    # nx.draw_circular(resG, with_labels=withLabel, node_size=nodeSize)
    pos = nx.circular_layout(resG)
    nx.draw_networkx_nodes(resG, pos)
    nx.draw_networkx_labels(resG, pos)
    nx.draw_networkx_edges(resG, pos, edge_color='k')
    for layer in layers:
        subG = nx.from_numpy_matrix(layer)
        elist = nx.to_edgelist(subG)
        nx.draw_networkx_edges(resG, pos, edgelist=elist, edge_color=(rd.random(), rd.random(), rd.random()), width=5*rd.random())

    if expectedG is None:
        resDegrees = ev.getDegrees(resG)
        print("final degrees : " + str(resDegrees))
    else:
        expectedEPL = ev.getEPL(G, expectedG)
        expectedFig = fig.add_subplot(122,aspect='equal')
        expectedFig.title.set_text("expected (EPL = " + str(expectedEPL) + ")")
        nx.draw_circular(expectedG, with_labels=withLabel, node_size=nodeSize)
    
    plt.plot()
    plt.show()