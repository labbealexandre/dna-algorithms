import networkx as nx
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
    MG = nx.from_numpy_matrix(M)

    fig = plt.figure()

    MFig = fig.add_subplot(111, aspect='equal')
    MFig.title.set_text("input distribution")
    pos = nx.spring_layout(MG)
    nx.draw_networkx_nodes(MG, pos)
    nx.draw_networkx_edges(MG, pos)
    nx.draw_networkx_labels(MG, pos)
    labels = nx.get_edge_attributes(MG, 'weight')
    nx.draw_networkx_edge_labels(MG, pos, edge_labels=labels)

    plt.plot()
    plt.show()

def printRes(M, res, expected):
    
    resG = nx.from_numpy_matrix(res)
    expectedG = nx.from_numpy_matrix(expected)

    resEPL = ev.getEPL(M, resG)
    expectedEPL = ev.getEPL(M, expectedG)

    fig = plt.figure()

    resFig = fig.add_subplot(121,aspect='equal')
    resFig.title.set_text("result (EPL = " + str(resEPL) + ")")
    nx.draw_circular(resG, with_labels=True)

    expectedFig = fig.add_subplot(122,aspect='equal')
    expectedFig.title.set_text("expected (EPL = " + str(expectedEPL) + ")")
    nx.draw_circular(expectedG, with_labels=True)

    plt.plot()
    plt.show()