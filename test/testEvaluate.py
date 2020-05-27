import unittest
import importlib

from src import evaluate as ev
from test import customAssertions as ca

class TestEvaluate(unittest.TestCase, ca.CustomAssertions):

    """Test case for evaluate functions"""

    def test_linear(self):
        N = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        
        expected = [
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0]
        ]

        res = ev.getDistances(N)
        self.assertEqualMatrix(expected, res)

    def test_circular(self):
        N = [
            [0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0]
        ]
        
        expected = [
            [0, 1, 2, 3, 2, 1],
            [1, 0, 1, 2, 3, 2],
            [2, 1, 0, 1, 2, 3],
            [3, 2, 1, 0, 1, 2],
            [2, 3, 2, 1, 0, 1],
            [1, 2, 3, 2, 1, 0]
        ]

        res = ev.getDistances(N)
        self.assertEqualMatrix(expected, res)

    def test_random(self):
        N = [
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0]
        ]
        
        expected = [
            [0, 1, 1, 2, 3],
            [1, 0, 1, 1, 2],
            [1, 1, 0, 2, 3],
            [2, 1, 2, 0, 1],
            [3, 2, 3, 1, 0]
        ]

        res = ev.getDistances(N)
        self.assertEqualMatrix(expected, res)

    def test_random2(self):
        N = [
            [0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0]
        ]
        
        expected = [
            [0, 3, 2, 3, 1, 2, 1, 4],
            [3, 0, 1, 2, 3, 2, 2, 1],
            [2, 1, 0, 1, 2, 1, 1, 2],
            [3, 2, 1, 0, 3, 2, 2, 3],
            [1, 3, 2, 3, 0, 1, 2, 4],
            [2, 2, 1, 2, 1, 0, 2, 3],
            [1, 2, 1, 2, 2, 2, 0, 3],
            [4, 1, 2, 3, 4, 3, 3, 0]
        ]

        res = ev.getDistances(N)
        self.assertEqualMatrix(res, expected)

if __name__ == '__main__':
    unittest.main()