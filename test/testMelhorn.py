import unittest
import numpy as np
import random as rd

from src import melhorn as ml
from src import utils as ut

class TestMelhornTree(unittest.TestCase):

    """ Test case for melhornTree method """

    def test_simple(self):
        N = np.zeros((4, 4))
        children = np.array([0, 1, 2, 3])

        children = ut.arrayToDictArray(children)

        expected = np.array([
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 0, 0],
        ])

        ml.melhornTree(children, 0, N, direction="outgoing")
        np.testing.assert_array_equal(expected, N)
        
    def test_simple2(self):
        N = np.zeros((4, 4))
        children = np.array([1, 2, 0, 3])

        children = ut.arrayToDictArray(children)

        expected = np.array([
            [0, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 0],
            [0, 0, 0, 0]
        ])

        ml.melhornTree(children, 2, N, direction="outgoing")
        np.testing.assert_array_equal(expected, N)

    def test_simple3(self):
        N = np.zeros((4, 4))
        children = np.array([1, 2, 0, 3])

        children = ut.arrayToDictArray(children)

        expected = np.array([
            [0, 0, 0, 0],
            [1, 0, 0, 1],
            [0, 1, 0, 0],
            [0, 0, 0, 0]
        ])

        ml.melhornTree(children, 2, N, direction="outgoing")
        np.testing.assert_array_equal(expected, N)

    
    def test_random(self):
        tries = 10
        minLength = 0
        maxLength = 1000
        maxWeight = 100
        for _ in range(tries):
            n = rd.randint(minLength, maxLength)
            N = np.zeros((n, n))
            children = np.random.random_integers(1, maxWeight, size=n)
            total = np.sum(children)
            children = np.true_divide(children, total)

            root = rd.randint(0, n-1)
            children[root] = 0

            childrenDict = ut.arrayToDictArray(children)

            ml.melhornTree(childrenDict, root, N, direction="outgoing")
            length = ut.getWeigtedPathLength(N, children, root, 0)

            H = ut.getEntropy(children)
            bound = 2 +1.44*H # melhorn bound

            self.assertTrue(length < bound)