import unittest
import importlib

from src import algorithms as al
from test import customAssertions as ca

class TestAlgorithm(unittest.TestCase, ca.CustomAssertions):

    """Test case for algorithms functions"""

    def test_uniform(self):
        N = [[0 for i in range(6)] for i in range(6)]
        root = 0
        children = [0, 0.2, 0.2, 0.2, 0.2, 0.2]

        expected = [
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0]
        ]

        al.buildTree(children, root, N, 0)
        self.assertEqualMatrix(expected, N)

    def test_uniform2(self):
        N = [[0 for i in range(7)] for i in range(7)]
        root = 5
        children = [0.25, 0.25, 0, 0.25, 0, 0, 0.25]

        expected = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        al.buildTree(children, root, N, 0)
        self.assertEqualMatrix(expected, N)

    def test_simple(self):
        N = [[0 for i in range(5)] for i in range(5)]
        root = 1
        children = [0.3, 0, 0.1, 0.4, 0.2]

        expected = [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0]
        ]

        al.buildTree(children, root, N, 0)
        self.assertEqualMatrix(expected, N)
        

if __name__ == '__main__':
    unittest.main()