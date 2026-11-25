"""Conditional test in the manuscript. Input JSON is a square 0/1 win matrix.

Row i, column j is 1 exactly when i beats j. The diagonal must be 0.
The first three consecutive groups of n//3 vertices supply the fixed packing.
Only the last log/exponential operations use floating-point arithmetic.
"""
import argparse
from collections import defaultdict
from itertools import product
import json
import math


def score_scan(wins):
    n = len(wins)
    if n < 2 or any(len(row) != n for row in wins):
        raise ValueError("provide a square win matrix of order at least two")
    for i, row in enumerate(wins):
        if row[i] != 0 or any(value not in (0, 1) for value in row):
            raise ValueError("entries must be 0 or 1, with diagonal zero")
        if any(row[j] + wins[j][i] != 1 for j in range(i)):
            raise ValueError("each distinct pair must have a single winner")
    degree = [sum(row) for row in wins]
    m = n // 3
    cycles = []
    for i in range(m):
        for j in range(m):
            a, b, c = i, m + j, 2 * m + (i + j) % m
            if wins[a][b] == wins[b][c] == wins[c][a]:
                cycles.append((a, b, c, 2 * wins[a][b] - 1))
    best_log_p = 0.0
    for resolution in range(n.bit_length()):
        q = 1 << resolution
        # Integer numerators for the at most two positive hats at each vertex.
        choices = []
        for d in degree:
            lower, remainder = divmod(q * d, n - 1)
            active = [(lower, n - 1 - remainder)]
            if remainder:
                active.append((lower + 1, remainder))
            choices.append(active)
        cells = defaultdict(lambda: [0, 0])
        for a, b, c, sign in cycles:
            for (i, x), (j, y), (k, z) in product(choices[a], choices[b], choices[c]):
                weight = x * y * z
                totals = cells[i, j, k]
                totals[0] += sign * weight
                totals[1] += weight * weight
        # The common denominator of all weights cancels from S²/V.
        log_penalty = (resolution + 2) * math.log(2) + 3 * math.log1p(q)
        for signed, squares in cells.values():
            best_log_p = min(best_log_p, log_penalty - signed * signed / (2 * squares))
    p_display = math.exp(best_log_p)
    return {"vertices": n, "packed_triangles": m*m, "packed_cycles": len(cycles),
            "log_p_bound": best_log_p, "p_bound": p_display if p_display > 0 else None,
            "p_display_underflow": p_display == 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", help="JSON file containing the labelled win matrix")
    args = parser.parse_args()
    with open(args.matrix, encoding="utf-8") as source:
        print(json.dumps(score_scan(json.load(source)), indent=2))
