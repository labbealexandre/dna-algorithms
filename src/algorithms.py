def buildTrees(M, reverseM, root, parent, visited, N, outgoing):

    if visited[root] == 1:
        return

    visited[root] = 1
    n = len(M)

    def buildTree(children, root, N, start, outgoing):
        """
        build optimal tree from the children of a node
        """

        total = sum(children)
        m = len(children)
        if total != 0:
            # Mehlhorn method to find nearly optimal binary search trees
            # We search for a node which divides the tree
            # in two approximately equal sub-trees
            s, i = children[0], 0
            while s < total / 2:
                i+=1
                s+= children[i]
            # We update the N graph by adding a child to 
            if outgoing:
                N[root][start+i] = 1
            else:
                N[start+i][root] = 1
            # We once we found it we recursively call this method
            # for the subtrees at the left and the right of this node
            # (if there is at least one node in both cases)
            if i > 0 and sum(children[:i]) > 0:
                buildTree(children[:i], start+i, N, start, outgoing)
            if i < m-1 and sum(children[i+1:]) > 0:
                buildTree(children[i+1:], start+i, N, start+i+1, outgoing)

    children = []
    if outgoing:
        for i in range(n):
            if i != parent:
                children.append(M[root][i])
            else:
                children.append(0)
    else:
        for i in range(n):
            if i != parent:
                children.append(M[i][root])
            else:
                children.append(0)

    buildTree(children, root, N, 0, outgoing)

    for i in range(n):
        if (i != parent):
            if M[root][i] > 0:
                buildTrees(M, reverseM, i, root, visited, N, outgoing)
            if M[i][root] > 0:
                buildTrees(M, reverseM, i, root, visited, N, outgoing)

def treeToBND(M):
    """
    Theorem 3 : get a Bounded Network Design from
    a request distribution such as the graph is a tree
    """

    n = len(M)
    reverseM = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            reverseM[j][i] = M[i][j]

    # N will be he result the result unweighted graph
    N = [[0 for i in range(n)] for j in range(n)]
            
    # We arbitrary set the root as 0
    visited = [0 for i in range(n)]
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, True)

    visited = [0 for i in range(n)]
    root = 0
    buildTrees(M, reverseM, root, -1, visited, N, False)

    return N
        