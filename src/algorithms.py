def buildTree(children, root, N, start):
    """
    build optimal tree from the children of a node
    """
    total = sum(children)
    m = len(children)
    if total != 0:
        # We search for a node which divides the tree
        # in two approximately equal sub-trees
        s, i = children[0], 0
        while s < total / 2:
            i+=1
            s+= children[i]
        # We update the N graph by adding a child to root
        N[root][start+i] = 1
        # We once we found it we recursively call this method
        # for the subtrees at the left and the right of this node
        # (if there is at least one node in both cases)
        if i > 0 and sum(children[:i]) > 0:
            buildTree(children[:i], start+i, N, start)
        if i < m-1 and sum(children[i+1:]) > 0:
            buildTree(children[i+1:], start+i, N, start+i+1)

def treeToBND(M):
    """
    Theorem 3 : get a Bounded Network Design from
    a request distribution such as the graph is a tree
    """

    n = len(M)
    N = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        buildTree(M[i], i, N, 0)

    return N
        