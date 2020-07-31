import unittest
import importlib
import numpy as np
import networkx as nx

from src import treeToBND as tr
from src import sparseToBND as sp
from src import draw as dr
from src import utils as ut

class TestTreeToBND(unittest.TestCase):

    """Test case for treeToBND method"""

    def test_simple(self):
        M = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0.25, 0, 0, 0, 0, 0, 0, 0, 0],
            [0.1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0.05, 0, 0, 0, 0, 0, 0, 0, 0],
            [0.1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.2, 0, 0.05, 0.1, 0.15],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        expected = np.array([
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
        ])
        
        G = nx.from_numpy_matrix(M, create_using=nx.DiGraph)
        ut.normalizeGraph(G)

        expectedG = nx.from_numpy_matrix(expected)
        ut.normalizeGraph(G)

        resG = tr.treeToBND(M)
        N = nx.to_numpy_matrix(resG)
        np.testing.assert_array_equal(expected, N)

        dr.printInput(G)
        dr.printRes(G, resG, expectedG)

class TestSparseToBND(unittest.TestCase):

    """Test case for sparseToBND method"""

    def test_simple(self):
        M = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.1, 0, 0, 0, 0, 0, 0, 0],
            [0.15, 0, 0, 0, 0, 0, 0, 0],
            [0.05, 0, 0, 0, 0, 0, 0, 0],
            [0.1, 0, 0, 0, 0, 0.05, 0.35, 0.2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])

        expected = np.array([
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 1, 0, 1, 0],
        ])

        G = nx.from_numpy_matrix(M, create_using=nx.DiGraph)
        ut.normalizeGraph(G)

        expectedG = nx.from_numpy_matrix(expected)
        ut.normalizeGraph(G)

        res = sp.sparseToBND(G)
        resG, layers = res[0], res[1]
        N = nx.to_numpy_matrix(resG)

        dr.printInput(G)
        dr.printRes(G, resG, expectedG, layers)
        np.testing.assert_array_equal(expected, N)
        

if __name__ == '__main__':
    unittest.main()