import unittest
import importlib

from src import evaluate as ev
from test import customAssertions as ca

def compareMatrices(A, B, _self):
    nA1, nA2 = len(A), len(A[0])
    nB1, nB2 = len(B), len(B[0])
    _self.assertEqual(nA1, nB1)
    _self.assertEqual(nA2, nB2)

    for i in range(nA1):
        for j in range(nA2):
            _self.assertEqual(A[i][j], B[i][j])

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