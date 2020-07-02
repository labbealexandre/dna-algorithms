from math import log
import numpy as np
import operator as op
from functools import reduce
from enum import Enum

class Direction(Enum):
    INCOMING = 0
    OUTGOING = 1

def getWeigtedPathLength(N, weights, root, length):
    n, _ = N.shape
    res = length*weights[root]
    for i in range(n):
        if N[root, i] == 1:
            res+=getWeigtedPathLength(N, weights, i, length+1)
    return res

def getEntropy(weights):
    H = 0
    n = weights.size
    for i in range(n):
        if weights[i] != 0:
            H+=weights[i]*log(1.0/weights[i], 2)
    return H

def round_to_n(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    as_string = format % x
    return float(as_string)

def intToBinaryArray(n, size):
    res = np.zeros(size)

    for i in range(size):
        res[i] = n%2
        n//=2

    return res

def binaryArrayToInt(arr):
    res = 0
    power = 1

    for i in range(len(arr)):
        res+=power*arr[i]
        power*=2

    return res

def permutations(n, r):
    return reduce(op.mul, range(n, n-r, -1), 1)

def arrayToDictArray(arr):
    n = len(arr)
    indexes = np.arange(n)
    res = np.zeros((n, 2))
    res[:,0], res[:,1] = indexes, arr

    # Then we sort the result by the second column
    return res[res[:,1].argsort()]