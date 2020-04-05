"""
All squares of a board of a specified size (specified numbers of rows and columns) must be colored with the minimum number of colors.
The four corners of any rectangle inside the board must not be assigned the same color.

Execution:
 - python3 BoardColoration
 - python3 BoardColoration -data=[8,10]
"""

from pycsp3 import *

n, m = data or (6, 5)

# x[i][j] is the color at row i and column j
x = VarArray(size=[n, m], dom=range(n * m))

satisfy(
    # at least two corners of different colors for any rectangle inside the board
    [NValues(x[i1][j1], x[i1][j2], x[i2][j1], x[i2][j2]) > 1 for i1, i2 in combinations(range(n), 2) for j1, j2 in combinations(range(m), 2)],

    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)

minimize(
    Maximum(x)
)
