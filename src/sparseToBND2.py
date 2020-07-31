import numpy as np
import networkx as nx

from src import evaluate as ev
from src import utils as ut
from src import melhorn as ml

def replaceInitialEdges(G, M, subGraphs, avgDegree):

  # By definition of the algorithm, a node can help at most
  # avgDegree / 2
  n = len(M)
  limit = int(avgDegree/2)+1 # this is not usefull in this first naive implementation
  balance = np.zeros(n)
  rerouters = []

  edges = list(G.edges)
  for edge in edges:
    # We need to find a helper node
    # We search for the node which as the less helped yet
    # It can be one of the ends of the edge

    helper = np.argmin(balance)
    rerouters.append(helper)
    if helper != edge[1]:
      weight = M[helper, edge[1]] + M[edge[0], edge[1]]
      subGraphs[edge[1]].add_edge(helper, edge[1], weight=weight)
    if helper != edge[0]:
      weight = M[edge[0], helper] + M[edge[0], edge[1]]
      subGraphs[edge[0]].add_edge(edge[0], helper, weight=weight)
    balance[helper] += 1

  return [edges, rerouters]

def addBinaryTrees(subGraphs, resMarices):

  finalSubGraphs = []

  for i in range(len(subGraphs)):
    subGraph = subGraphs[i]
    M = nx.to_numpy_matrix(subGraph)
    _M = np.copy(M)

    outChildren = ut.arrayToDictArray(_M[i,:])
    rows = np.where(outChildren[:,1] > 0)
    outChildren = outChildren[rows]

    inChildren = ut.arrayToDictArray(_M[:,i])
    rows = np.where(inChildren[:,1] > 0)
    inChildren = inChildren[rows]

    ml.melhornTree(outChildren, i, resMarices[i], direction=ut.Direction.OUTGOING)
    ml.melhornTree(inChildren, i, resMarices[i], direction=ut.Direction.INCOMING)

    finalSubGraph = nx.from_numpy_matrix(resMarices[i])
    finalSubGraphs.append(finalSubGraph)

  return finalSubGraphs

def sparseToBND2(G):
  """
  New algorithm for sparse graphs
  """

  M = nx.to_numpy_matrix(G)
  n = len(M)
  avgDegree = ev.getAverageDegree(G)

  # N will be the result unweighted graph
  N = np.zeros((n, n))

  # For each node we create a auxilliary graph which will be completed
  # with the new edges which replace the initial ones
  subGraphs = [nx.empty_graph(n, create_using=nx.DiGraph) for i in range(n)]
  res = replaceInitialEdges(G, M, subGraphs, avgDegree)
  edges, rerouters = res[0], res[1]

  # Now for each subgraph, we create at most two melhorn trees
  resMatrices = [np.zeros((n,n)) for i in range(n)]
  finalSubGraphs = addBinaryTrees(subGraphs, resMatrices)

  # We now compute the union of these subgraphs
  resGraphs = []
  for matrix in resMatrices:
    resGraphs.append(nx.from_numpy_matrix(matrix))
  res = nx.compose_all(resGraphs)

  return [res, edges, rerouters, finalSubGraphs]