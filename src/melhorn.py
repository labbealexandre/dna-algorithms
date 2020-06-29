import numpy as np

def melhornTree(children, root, N, direction="outgoing", layer=None):
    """
    build optimal tree from the children of a node
    """

    total = sum(children[:, 1])
    m, _ = children.shape

    # Mehlhorn method to find nearly optimal binary search trees
    # We search for a node which divides the tree
    # in two approximately equal sub-trees
    s, i = children[0, 1], 0
    while s < total / 2.:
        i+=1
        s+=children[i, 1]
    # We update the N graph by adding a child to

    index = int(children[i, 0])

    if direction == "outgoing":
        N[root, index] = 1
        if layer is not None: layer[root, index] = 1
    elif direction == "incoming":
        N[index, root] = 1
        if layer is not None: layer[root, index] = 1

    # We once we found it we recursively call this method
    # for the subtrees at the left and the right of this node
    # (if there is at least one node in both cases)
    if i > 0 and sum(children[:i,1]) > 0:
        melhornTree(children[:i,:], index, N, direction, layer)
    if i < m-1 and sum(children[i+1:,1]) > 0:
        melhornTree(children[i+1:,:], index, N, direction, layer)