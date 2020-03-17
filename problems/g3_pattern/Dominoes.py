from pycsp3 import *

nRows, nCols, nValues = len(data.grid), len(data.grid[0]), len(data.grid)
positions = [[i * nCols + j for i in range(nRows) for j in range(nCols) if data.grid[i][j] == value] for value in range(nValues)]


def adjacency(d1, d2):
    va = abs(d1 - d2) == nCols  # vertical adjacency
    ha = (abs(d1 - d2) == 1) & (d1 // nCols == d2 // nCols)  # horizontal adjacency
    return va | ha


# x[i][j] concerns the domino (having values) i-j; this is the position of the value i in the grid for this domino
x = VarArray(size=[nValues, nValues], dom=lambda i, j: range(nRows * nCols) if i <= j else None)

# y[i][j] concerns the domino (having values) i-j; this is the position of the value j in the grid for this domino
y = VarArray(size=[nValues, nValues], dom=lambda i, j: range(nRows * nCols) if i <= j else None)

satisfy(
    # each part of each domino in a different cell
    AllDifferent(x + y),

    # unary constraints
    [(x[i][j] in positions[i], y[i][j] in positions[j]) for i in range(nValues) for j in range(i, nValues)],

    # adjacency constraints
    [adjacency(x[i][j], y[i][j]) for i in range(nValues) for j in range(i, nValues)]
)
