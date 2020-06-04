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