import networkx as nx

from src import algorithms as al

n = 10

G = nx.star_graph(n)
M = nx.to_numpy_matrix(G)

