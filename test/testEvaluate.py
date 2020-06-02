import unittest
import importlib
import numpy as np
import networkx as nx

from src import evaluate as ev
from test import customAssertions as ca

class TestEvaluate(unittest.TestCase):

    """Test case for evaluate functions"""

    def test_linear(self):
        N = np.array([
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ])
        GN = nx.from_numpy_matrix(N)
        
        expected = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0]
        ])

        res = ev.getDistances(GN)
        np.testing.assert_array_equal(expected, res)

    def test_circular(self):
        N = np.array([
            [0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0]
        ])
        GN = nx.from_numpy_matrix(N)
        
        expected = np.array([
            [0, 1, 2, 3, 2, 1],
            [1, 0, 1, 2, 3, 2],
            [2, 1, 0, 1, 2, 3],
            [3, 2, 1, 0, 1, 2],
            [2, 3, 2, 1, 0, 1],
            [1, 2, 3, 2, 1, 0]
        ])

        res = ev.getDistances(GN)
        np.testing.assert_array_equal(expected, res)

    def test_random(self):
        N = np.array([
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0]
        ])
        GN = nx.from_numpy_matrix(N)
        
        expected = np.array([
            [0, 1, 1, 2, 3],
            [1, 0, 1, 1, 2],
            [1, 1, 0, 2, 3],
            [2, 1, 2, 0, 1],
            [3, 2, 3, 1, 0]
        ])

        res = ev.getDistances(GN)
        np.testing.assert_array_equal(expected, res)

    def test_random2(self):
        N = np.array([
            [0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0]
        ])
        GN = nx.from_numpy_matrix(N)
        
        expected = np.array([
            [0, 3, 2, 3, 1, 2, 1, 4],
            [3, 0, 1, 2, 3, 2, 2, 1],
            [2, 1, 0, 1, 2, 1, 1, 2],
            [3, 2, 1, 0, 3, 2, 2, 3],
            [1, 3, 2, 3, 0, 1, 2, 4],
            [2, 2, 1, 2, 1, 0, 2, 3],
            [1, 2, 1, 2, 2, 2, 0, 3],
            [4, 1, 2, 3, 4, 3, 3, 0]
        ])

        res = ev.getDistances(GN)
        np.testing.assert_array_equal(expected, res)

if __name__ == '__main__':
    unittest.main()