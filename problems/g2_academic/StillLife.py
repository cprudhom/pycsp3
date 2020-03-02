from pycsp3 import *

"""
 Problem 032 at CSPLib
"""

n, m = data.n, data.m

if not variant():
    # x[i][j] is 1 iff the cell at row i and col j is alive
    x = VarArray(size=[n, m], dom={0, 1})

    # a[i][j] is the number of alive neighbours
    a = VarArray(size=[n, m], dom=range(9))

    table = {(v, 0) for v in range(9) if v != 3} | {(2, 1), (3, 1)}


    def scope(i, j):
        return [x[k][l] for k in range(n) for l in range(m) if i - 1 <= k <= i + 1 and j - 1 <= l <= j + 1 and (k, l) != (i, j)]


    satisfy(
        # computing the numbers of alive neighbours
        [Sum(scope(i, j)) == a[i][j] for i in range(n) for j in range(m)],

        # imposing rules of the game
        [(a[i][j], x[i][j]) in table for i in range(n) for j in range(m)],

        # imposing rules for ensuring valid dead cells around the board
        [
            Slide(x[0][i:i + 3] not in [(1, 1, 1)] for i in range(m - 2)),
            Slide(x[n - 1][i: i + 3] not in [(1, 1, 1)] for i in range(m - 2)),
            Slide(x[i:i + 3, 0] not in [(1, 1, 1)] for i in range(n - 2)),
            Slide(x[i:i + 3, m - 1] not in [(1, 1, 1)] for i in range(n - 2))
        ],

        # tag(symmetry-breaking)
        [x[0][0] >= x[n - 1][n - 1], x[0][n - 1] >= x[n - 1][0]] if n == m else None
    )

    maximize(
        Sum(x)
    )

elif variant("wastage"):
    assert n == m
    #  x[i][j] is 1 iff the cell at row i and col j is alive (note that there is a border)
    x = VarArray(size=[n + 2, n + 2], dom={0, 1})

    #  w[i][j] is the wastage for the cell at row i and col j
    w = VarArray(size=[n + 2, n + 2], dom={0, 1, 2})

    # ws[i] is the wastage sum for cells at row i
    ws = VarArray(size=n + 2, dom=range(2 * (n + 2) * (n + 2) + 1))

    # z is the number of alive cells
    z = Var(dom=range(n * n + 1))


    def condition_for_tuple(t):
        s1 = t[0] + t[1] + t[2] + t[3] + t[5] + t[6] + t[7] + t[8]
        s2 = t[0] * t[2] + t[2] * t[8] + t[8] * t[6] + t[6] * t[0] + t[1] + t[3] + t[5] + t[7]
        s3 = t[1] + t[3] + t[5] + t[7]
        return (t[4] != 1 or s1 >= 2) and (t[4] != 1 or s1 <= 3) and (t[4] != 0 or s1 != 3) and (t[4] != 1 or s2 > 1 or t[9] >= 1) and \
               (t[4] != 1 or s2 > 0 or t[9] >= 2) and (t[4] != 0 or s3 < 4 or t[9] >= 2) and (t[4] != 0 or s3 > 1 or t[9] >= 1) and \
               (t[4] != 0 or s3 > 0 or t[9] >= 2)


    table = {(*t, i) for t in product(range(2), repeat=9) for i in range(3) if condition_for_tuple((*t, i))}


    def neighbors(i, j):
        return [x[k][l] for k in range(i - 1, i + 2) for l in range(j - 1, j + 2)]


    satisfy(
        # cells at the border are assumed to be dead
        [
            [x[0][j] == 0 for j in range(n + 2)],
            [x[n + 1][j] == 0 for j in range(n + 2)],
            [x[i][0] == 0 for i in range(n + 2)],
            [x[i][n + 1] == 0 for i in range(n + 2)]
        ],

        # ensuring that cells at the border remain dead
        [
            Slide([x[1][j], x[1][j + 1], x[1][j + 2]] not in [(1, 1, 1)] for j in range(n)),
            Slide([x[n][j], x[n][j + 1], x[n][j + 2]] not in [(1, 1, 1)] for j in range(n)),
            Slide([x[i][1], x[i + 1][1], x[i + 2][1]] not in [(1, 1, 1)] for i in range(n)),
            Slide([x[i][n], x[i + 1][n], x[i + 2][n]] not in [(1, 1, 1)] for i in range(n))
        ],

        # still life + wastage constraints
        [neighbors(i, j) + [w[i][j]] in table for i in range(1, n + 1) for j in range(1, n + 1)],

        # managing wastage on the border
        [
            [w[0][j] + x[1][j] == 1 for j in range(1, n + 1)],
            [w[n + 1][j] + x[n][j] == 1 for j in range(1, n + 1)],
            [w[i][0] + x[i][1] == 1 for i in range(1, n + 1)],
            [w[i][n + 1] + x[i][n] == 1 for i in range(1, n + 1)]
        ],

        # summing wastage
        [Sum(w[0] if i == 0 else [ws[i - 1], w[i]]) == ws[i] for i in range(n + 2)],

        # setting the value of the objective
        Sum([z, ws[-1]] * [4, 1]) == 2 * n * n + 4 * n,

        # tag(redundant-constraints)
        [(ws[n + 1] - ws[i]) >= 2 * ((n - i) // 3) + n // 3 for i in range(n + 1)]
    )

    maximize(
        #  maximizing the number of alive cells
        z
    )
