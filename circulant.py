import networkx as nx

from src import algorithms as al
from src import draw as dr

n = 10
m = 2

G = nx.circulant_graph(n, [i for i in range(1, m+1)], create_using=nx.DiGraph)
M = nx.to_numpy_matrix(G)

dr.printInput(M)
res = al.sparseToBND(M)

dr.printRes(M, res, None)