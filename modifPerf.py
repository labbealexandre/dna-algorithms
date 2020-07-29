import numpy as np
import networkx as nx
import random as rd
from tqdm import tqdm

from src import sparseToBND2 as sp
from src import evaluate as ev
from src import export as ex

def randomGraph(n, m):
  G = nx.gnm_random_graph(n, m, directed=True)
  total = 0
  for (u,v,w) in G.edges(data=True):
    weight = rd.random()
    w['weight'] = weight
    total+=weight
  for (u,v,w) in G.edges(data=True):
    w['weight'] /= total
  
  return G

def randomGraph2(inDegrees, outDegrees):
  G = nx.directed_configuration_model(inDegrees, outDegrees)
  total = 0
  for (u,v,w) in G.edges(data=True):
    weight = rd.random()
    w['weight'] = weight
    total+=weight
  for (u,v,w) in G.edges(data=True):
    w['weight'] /= total
  
  return G

n = 100
m = 500
N = 1000

inDegrees = [7 for i in range(75)] + [99 for i in range(25)]
outDegrees = [7 for i in range(60)] + [99 for i in range(25)] + [7 for i in range(15)]

results = []

i = 0
for i in tqdm(range(N)):
  # input = randomGraph(n, m)
  input = randomGraph2(inDegrees, outDegrees)
  M = nx.to_numpy_matrix(input)
  res = sp.sparseToBND2(input)
  result = res[0]

  avgDegree = ev.getAverageDegree(M)
  initialMaxDegree = ev.getMaxDegree(input)
  maxDegree = ev.getMaxDegree(result)/2 #because undirected
  EPL = ev.getEPL(M, result)
  firstDegreeBound = 3*avgDegree
  secondDegreeBound = firstDegreeBound+6

  line = [
    str(n),
    str(m),
    str(avgDegree),
    str(initialMaxDegree),
    str(maxDegree),
    str(EPL),
    str(firstDegreeBound),
    str(secondDegreeBound)
  ]
  results.append(line)

  i+=1

headers = [ 'n',
            'm',
            'average degree',
            'initial max degree',
            'final max degree',
            'EPL',
            '3 * average degree',
            '3 * average degree + 6'
          ]
file = 'modif_results.csv'
ex.exportToCSV(file, headers, results)