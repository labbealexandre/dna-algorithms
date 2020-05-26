def getEPL(M, N):
    """ Calculation of the expected path length """
    n = len(M)
    res = 0
    D = getDistances(N)
    for i in range(n):
        for j in range(n):
            res += M[i][j] * D[i][j]
    return res

def getDistances(N):
    """
    Calculation of the distances between of a graph
    thanks to djikstra algorithm
    N is an adjacency matrix
    graph must be connected
    TODO: use more efficient algorithm to calculate shortest paths from ALL nodes
    """

    def getNeighbours(node):
        neighbours = []
        L = N[node]
        for i in range(n):
            if L[i] == 1:
                neighbours.append(i)
        return neighbours
        
    def getNearestNode(distances, visited):
        _min = -1
        index = -1
        for i in range(n):
            if  visited[i] == 0 and (
                _min == -1 or (
                distances[i] != -1 and distances[i] < _min)):

                _min = distances[i]
                index = i
        
        if (index == -1):
            print("debug: something expeted append, index = -1")
        else:
            return index

    n = len(N)
    D = [-1 for i in range(n)]
    for node in range(n):
        distances = [-1 for i in range(n)] # -1 means +oo
        visited = [0 for i in range(n)]

        distances[node] = 0

        while sum(visited) < n:
            current = getNearestNode(distances, visited)
            visited[current] = 1
            for nb in getNeighbours(current):
                newDist = distances[current] + 1
                if (distances[nb] == -1 or distances[nb] > newDist):
                    distances[nb] = newDist
        
        D[node] = distances
    return D
