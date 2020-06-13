from math import log

def getWeigtedPathLength(N, weights, root, length):
    n, _ = N.shape
    res = length*weights[root]
    for i in range(n):
        if N[root, i] == 1:
            res+=getWeigtedPathLength(N, weights, i, length+1)
    return res

def getEntropia(weights):
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