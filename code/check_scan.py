"""Cross-check integer accumulation against a direct implementation of the test."""
import math
from itertools import product
import random

from score_test import score_scan


def check(condition):
    """Fail loudly (also under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED")


def literal_scan(wins):
    n = len(wins)
    m = n // 3
    fractions = [sum(row) / (n-1) for row in wins]
    data = []
    for i, j in product(range(m), repeat=2):
        a, b, c = i, m + j, 2*m + (i+j) % m
        directions = wins[a][b], wins[b][c], wins[c][a]
        if directions == (1, 1, 1) or directions == (0, 0, 0):
            data.append(((fractions[a], fractions[b], fractions[c]), 2*directions[0]-1))
    answer = 0.0
    for r in range(n.bit_length()):
        q = 2**r
        for cell in product(range(q+1), repeat=3):
            signed = var = 0.0
            for point, sign in data:
                weight = math.prod(max(0.0, 1 - abs(q*z-b)) for z, b in zip(point,cell))
                signed += weight * sign
                var += weight**2
            if var:
                answer = min(answer, math.log(2**(r+2)*(q+1)**3) - signed**2/(2*var))
    return answer


def cyclic_blocks(m):
    n = 3*m
    rows = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            one, two = i//m, j//m
            win = int((j-i) % m <= m//2) if one == two else int((two-one) % 3 == 1)
            rows[i][j], rows[j][i] = win, 1-win
    return rows


if __name__ == '__main__':
    # These regular tournaments have m² identical cyclic signs and constant
    # score 1/2, so every nonempty cell at level 0 has S²/V=m².
    for m in (1, 3, 5, 25):
        rows = cyclic_blocks(m)
        got = score_scan(rows)['log_p_bound']
        expected = min(0.0, math.log(32) - m*m/2)
        check(math.isclose(got, expected, abs_tol=1e-11))
        if m <= 3:
            check(math.isclose(got, literal_scan(rows), abs_tol=1e-11))
    # Irregular scores and nonconstant weights exercise cell addressing.
    rng = random.Random(9701)
    rows = cyclic_blocks(5)
    for _ in range(4):
        a,b = rng.sample(range(15), 2)
        rows[a][b], rows[b][a] = rows[b][a], rows[a][b]
        check(math.isclose(score_scan(rows)['log_p_bound'], literal_scan(rows), abs_tol=1e-10))
    print("The sparse scan matches direct evaluation on six examples.")
    print("Cyclic three-block positive control, 75 vertices: log(p bound) =",
          round(score_scan(cyclic_blocks(25))['log_p_bound'], 6))
