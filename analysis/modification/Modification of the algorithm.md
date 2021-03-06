Modification of the algorithm
===

## Bound degree of the low degree nodes

For each low degree node i, let note :
- $\alpha_i$ its degree
- $\beta_i$ the number of edges this low degree node can help
- $\gamma_i$ its final degree

In the worst case we will have : $$\gamma_i = 3(2\beta_i + \alpha_i)$$

We have to choose $\beta_i$, ie how many edges each low degree node can help. Let note B the number of edges we have to help.

So we have to choose $\beta_i$ in order to have $$B <= \sum_{i} \beta_i$$

### In the paper, we chose $\beta_i$ = $\Delta_{avg}$

So $$\sum_{i} \beta_i = \frac{n*\Delta_{avg}}{2} = m >= B$$

And we have $$\gamma_i <= 12\Delta_{avg}$$ because $$\alpha_i <= 2\Delta_{avg}$$

### But we can choose a lesser value : $\beta_i$ = $\Delta_{avg}$ - $\frac{\alpha_i}{2}$

Let note A the number of edges in which a low degree node is involved.
We have $$A <= \sum_{i} \alpha_i <= 2A$$

So $$\sum_{i} \beta_i = \frac{n*\Delta_{avg}}{2} - \frac{1}{2}\sum_{i} \alpha_i >= m - A$$

But we can also say that $$ A + B <= m$$

because A corresponds to edges into at least one low degree node is involved and B corresponds to edges into none is involved.

So we have $$\sum_{i} \beta_i >= B$$

And we have too $$\gamma_i <= 3(2*\Delta_{avg}-2*\frac{\alpha_i}{2}+\alpha_i) = 6\Delta_{avg}$$

## Bound degree of the high degree nodes which are neither high-in nor high-out degree

Let's call strict High degree node an high degree node which is neither high-in nor high-out degree

Acording to the paper, they keep their degree from the initial distribution, which is at most $4\Delta_{avg}$. But these neighbours can be high-out or high-in degree nodes. So we can imagine a case even worst where a strict high degree node is involved into $4\Delta_{avg}$ melhorn trees which makes its final degree at $12\Delta_{avg}$

So let's do a second modification to keep this bounded degree of $6\Delta_{avg}$

Originally we changed edges only from High-out degree nodes to High-in degree nodes. we can extend the rule that way :

~~We now change edges from High-out degree nodes to all High degree nodes and also from all High degree nodes to High-in degree nodes.~~

We now change all edges between high degree nodes.

The final degree of a strict high degree node is at most $4\Delta_{avg}$. Because it is not connected to any high-in or high-out degree nodes.

By doing so the previous modification is still possible because there are more edges to replace. But still we have $$ A + B <= m$$ because the edges to replace are between High degree nodes.

Also this doesn't change the final degree of high-in or high-out degree nodes which is at most $6\Delta_{avg} + 1$