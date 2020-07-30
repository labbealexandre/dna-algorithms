import networkx as nx

from src import sparseToBND as sp
from src import draw as dr
from src import utils as ut

n = 10
m = 2

G = nx.circulant_graph(n, [i for i in range(1, m+1)], create_using=nx.DiGraph)
ut.normalizeGraph(G)

dr.printInput(G)
res = sp.sparseToBND(G)
N = res[0]

dr.printRes(G, N, None)