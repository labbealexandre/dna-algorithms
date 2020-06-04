def melhornTree(children, root, N, start, direction="outgoing"):
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
        while s < total / 2.:
            i+=1
            s+= children[i]
        # We update the N graph by adding a child to

        if direction == "outgoing":
            N[root, start+i] = 1
        elif direction == "incoming":
            N[start+i, root] = 1
        # We once we found it we recursively call this method
        # for the subtrees at the left and the right of this node
        # (if there is at least one node in both cases)
        if i > 0 and sum(children[:i]) > 0:
            melhornTree(children[:i], start+i, N, start, direction)
        if i < m-1 and sum(children[i+1:]) > 0:
            melhornTree(children[i+1:], start+i, N, start+i+1, direction)