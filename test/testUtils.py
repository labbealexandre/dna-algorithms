import unittest
import random as rd

from src import utils as ut
from test import customAssertions as ca

# class TestMergeSort(unittest.TestCase, ca.CustomAssertions):

#     """Test case for mergeSort method"""

#     def test_dumb(self):
#         L = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
#         res = ut.mergeSort(L)
#         self.assertEqualMatrix(L, res)

#     def test_reverse(self):
#         L = [[4, 4], [3, 3], [2, 2], [1, 1], [0, 0]]
#         expected = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
#         res = ut.mergeSort(L)
#         self.assertEqualMatrix(expected, res)