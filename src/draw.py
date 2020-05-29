import networkx as nx
import matplotlib.pyplot as plt
import math

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

def printRes(M, res, expected):
    MG = matrixToGraph(M, True)
    resG = matrixToGraph(res, False)
    expectedG = matrixToGraph(expected, False)

    fig1 = plt.figure()

    MFig = fig1.add_subplot(111, aspect='equal')
    MFig.title.set_text("input distribution")
    pos = nx.spring_layout(MG)
    nx.draw_networkx_nodes(MG, pos)
    nx.draw_networkx_edges(MG, pos)
    nx.draw_networkx_labels(MG, pos)
    labels = nx.get_edge_attributes(MG, 'weight')
    nx.draw_networkx_edge_labels(MG, pos, edge_labels=labels)
    plt.plot()

    fig2 = plt.figure()

    resFig = fig2.add_subplot(121,aspect='equal')
    resFig.title.set_text("result")
    nx.draw_circular(resG, with_labels=True)

    expectedFig = fig2.add_subplot(122,aspect='equal')
    expectedFig.title.set_text("expected")
    nx.draw_circular(expectedG, with_labels=True)

    plt.show()