import unittest
import random as rd
import numpy as np

from src import utils as ut

class TestGetgetWeigtedPathLength(unittest.TestCase):

    """ Test case dor getWeigtedPathLength method """

    def test_simple(self):
        N = np.array([
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        weights = np.array([0, 5, 3, 1])

        res = ut.getWeigtedPathLength(N, weights, 0, 0)
        self.assertEqual(res, 10)

    def test_simple2(self):
        N = np.array([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ])
        weights = np.array([0, 3, 7, 1])

        res = ut.getWeigtedPathLength(N, weights, 0, 0)
        self.assertEqual(res, 20)

    def test_simple3(self):
        N = np.array([
            [0, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        weights = np.array([0, 3, 9, 8])

        res = ut.getWeigtedPathLength(N, weights, 0, 0)
        self.assertEqual(res, 37)

    def test_simple4(self):
        N = np.array([
            [0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ])
        weights = np.array([0, 2, 10, 10, 9, 9, 9])

        res = ut.getWeigtedPathLength(N, weights, 0, 0)
        self.assertEqual(res, 86)