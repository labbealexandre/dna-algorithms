import unittest
import importlib
import numpy as np

from src import treeToBND as tr
from src import sparseToBND as sp
from src import draw as dr

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
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        
        res = tr.treeToBND(M)
        np.testing.assert_array_equal(expected, res)
        dr.printInput(M)
        dr.printRes(M, res, expected)

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
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
        ])

        dr.printInput(M)
        res = sp.sparseToBND(M)
        N, layers = res[0], res[1]
        dr.printRes(M, N, expected, layers)
        np.testing.assert_array_equal(expected, N)
        

if __name__ == '__main__':
    unittest.main()