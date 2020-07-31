import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.gridspec as grid
import math
import random as rd
import time

from src import melhorn as ml
from src import utils as ut
from src import sparseToBND2 as sp
from src import evaluate as ev

def randomGraph(n, m):
  G = nx.gnm_random_graph(n, m, directed=True)
  print(G)
  ut.normalizeGraph(G)
  return G

n = 10
m = 15

# Initialization of the graph

_input = randomGraph(n, m)
avgDegree = ev.getAverageDegree(_input)

res = sp.sparseToBND2(_input)
result, edges, rerouters, finalSubGraphs = res[0], res[1], res[2], res[3]

# Initialization of the plot

DrawInput = _input.copy()
subGraphs = [nx.empty_graph(n, create_using=nx.DiGraph) for i in range(n)]

fig = plt.figure()
outer = grid.GridSpec(1, 2)
leftInner = grid.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[0])
left = fig.add_subplot(leftInner[0], aspect="equal")

middles = []
nSquared = int(math.sqrt(n))
row, col = nSquared+1, nSquared
middleInner = grid.GridSpecFromSubplotSpec(row, col, subplot_spec=outer[1])

for i in range(n):
  middles.append(fig.add_subplot(middleInner[i], aspect="equal"))

colors = [(rd.random(), rd.random(), rd.random()) for i in range(n)]

#End of plot initialization

nx.draw_circular(DrawInput, ax=left, arrowstyle='->', arrowsize=10, with_labels=True, node_color=colors)

for i in range(n):
  nx.draw_circular(subGraphs[i], ax=middles[i], with_labels=True, node_color="#d3d3d3")

def init():
  print("Start")

def update(num):

  if num < 3*m:
    if num % 3 == 0:
      left.clear()
      index = num//3
      edge = edges[index]
      rerouter = rerouters[index]
      left.set_title(f"I - Rerouting of the edge : ({edge[0]}, {edge[1]}) -> helper : {rerouter}")
      DrawInput.remove_edge(edge[0], edge[1])
      nx.draw_circular(DrawInput, ax=left, arrowstyle='->', arrowsize=10, with_labels=True, node_color=colors)
      for i in range(len(middles)):
        middle = middles[i]
        middle.clear()
        subGraph = subGraphs[i]
        if i == edge[0] or i == edge[1]:
          nx.draw_circular(subGraph, ax=middle, edge_color=colors[i], with_labels=True, node_color=colors)
        else:
          nx.draw_circular(subGraph, ax=middle, edge_color="#d3d3d3", with_labels=True, node_color="#d3d3d3")
    elif num % 3 == 1:
      index = num//3
      edge = edges[index]
      node = edge[0]
      middle = middles[node]
      middle.clear()
      rerouter = rerouters[index]
      subGraph = subGraphs[node]
      subGraph.add_edge(node, rerouter)
      
      nx.draw_circular(subGraph, ax=middle, edge_color=colors[node], with_labels=True, node_color=colors)

    elif num % 3 == 2:
      index = num//3
      edge = edges[index]
      node = edge[1]
      middle = middles[node]
      middle.clear()
      rerouter = rerouters[index]
      subGraph = subGraphs[node]
      subGraph.add_edge(rerouter, node)
      nx.draw_circular(subGraph, ax=middle, edge_color=colors[node], with_labels=True, node_color=colors)

  if num == 3*m:
    for i in range(len(middles)):
      middle = middles[i]
      middle.clear()
      subGraph = subGraphs[i]
      nx.draw_circular(subGraph, ax=middle, edge_color="#d3d3d3", with_labels=True, node_color="#d3d3d3")
  
  if num >= 3*m and num < 3*m + n:
    index = num - 3*m
    left.set_title(f"II - Formation of the MTs from the node {index}")
    
    middle = middles[index]
    middle.clear()
    nx.draw_circular(finalSubGraphs[index], ax=middle, edge_color=colors[index], with_labels=True, node_color=colors)

  if num == 3*m + n:
    EPL = ev.getEPL(_input, result)
    maxDegree = ev.getMaxDegree(result)
    left.clear()
    left.set_title(f"III - Combination of all the MTs (EPL: {EPL}, max degree: {maxDegree}), avg degree: {avgDegree}")
    nx.draw_circular(result, ax=left, with_labels=True, node_color=colors)

framesNb = 3*m + n + 1
ani = anim.FuncAnimation(fig, update, frames=framesNb, init_func=init, interval=1000, repeat=False)
plt.show()  