"""Exact finite counterexamples for the Harrison-Trainor linearity conjecture.

Run with Python 3.8+. All comparisons use integer or rational arithmetic, and every
check raises SystemExit (so the script also fails correctly under python -O).
Besides the labelled ratios it counts the automorphism groups of the two
78-candidate tournaments exactly, giving the ratio of isomorphism-class
probabilities (labelled probability times n!/|Aut|).
"""
from fractions import Fraction as F
from itertools import combinations


def check(condition):
    """Fail loudly (also under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED")

PI_LO, PI_HI = F(333, 106), F(355, 113)
NORMAL_LO, NORMAL_HI = F(39894, 100000), F(39895, 100000)
check(2 * PI_HI * NORMAL_LO**2 < 1 < 2 * PI_LO * NORMAL_HI**2)


def down(x, digits=10):
    den = 10**digits
    return F(x.numerator * den // x.denominator, den)


def up(x, digits=10):
    return -down(-x, digits)


def normal_cdf_bounds(x):
    """Integrate the global odd/even Taylor lower/upper bounds on exp(-t²/2)."""
    check(x >= 0)
    term = x
    partial = x
    for k in range(1, 102):
        term *= -x*x * (2*k-1) / (2*k * (2*k+1))
        if k == 101:
            upper = partial
        partial += term
    check(0 <= partial <= upper)
    return (down(F(1, 2) + NORMAL_LO * partial),
            min(F(1), up(F(1, 2) + NORMAL_HI * upper)))


def exp_poly(x, degree):
    term = total = F(1)
    for k in range(1, degree + 1):
        term *= x/k
        total += term
    return total


def exp_lower(x):
    """Repeat a rational lower bound over subintervals where |x| <= 1."""
    pieces = max(1, -(-abs(x) // 1))
    per_piece = down(exp_poly(x/pieces, 17), digits=13)
    check(per_piece > 0)
    return per_piece**pieces


def edges(parts):
    return sum(s*(s-1)//2 for s in parts)


def linearity(parts):
    check(all(s > 0 and s % 2 == 1 for s in parts))
    return sum(s*(sum(parts[i+1:])+(s-1)//2)**2 for i, s in enumerate(parts))


def steiner_39():
    """Bose triples on Z/13 x Z/3, each oriented cyclically in the displayed order.

    Returns the 39-vertex tournament as a set of arcs on labels 3*x+i, after checking
    that the 247 triples cover each of the 741 pairs exactly once and that every
    vertex has outdegree 19 (a regular tournament)."""
    triples = [((x, 0), (x, 1), (x, 2)) for x in range(13)]
    for x, y in combinations(range(13), 2):
        for i in range(3):
            triples.append(((x, i), (y, i), ((7*(x+y)) % 13, (i+1) % 3)))
    pairs = [frozenset(edge) for triple in triples for edge in combinations(triple, 2)]
    check(len(triples) == 247)
    check(len(pairs) == len(set(pairs)) == 39*38//2)
    lab = lambda v: 3*v[0] + v[1]
    arcs = set()
    for a, b, c in triples:
        arcs |= {(lab(a), lab(b)), (lab(b), lab(c)), (lab(c), lab(a))}
    check(len(arcs) == 741)
    check(all(sum(1 for (u, _) in arcs if u == v) == 19 for v in range(39)))
    return arcs


def circulant(b):
    """Regular circulant tournament on Z/b: u -> u+k for k = 1, ..., (b-1)/2."""
    return {(u, (u+k) % b) for u in range(b) for k in range(1, (b-1)//2 + 1)}


def circulant_automorphism_count(b):
    """|Aut| of the regular circulant tournament on Z/b with connection set {1..(b-1)/2}.

    Every rotation is an automorphism, so |Aut| >= b.  Conversely the out-neighbourhood
    u+1, ..., u+k of each vertex u (k = (b-1)/2) induces a transitive tournament in this
    order; an automorphism f maps it isomorphically onto the out-neighbourhood of f(u),
    and transitive tournaments have a unique isomorphism, so f(u+i) = f(u)+i.  Hence f is
    the rotation by f(0) and |Aut| = b.  Both facts used are checked here."""
    arcs = circulant(b)
    k = (b-1)//2
    check(all({((u+s) % b, (v+s) % b) for (u, v) in arcs} == arcs for s in range(b)))
    for u in range(b):
        nbhd = [(u+i) % b for i in range(1, k+1)]
        check(all(((nbhd[i], nbhd[j]) in arcs) for i in range(k) for j in range(i+1, k)))
    return b


def automorphism_count(n, arcs):
    """Exact number of automorphisms of a tournament on 0..n-1.

    Backtracking over partial maps; each unassigned vertex keeps the set of images
    still consistent with every assignment made so far, and the most constrained
    vertex is assigned next."""
    beats = [[False]*n for _ in range(n)]
    for u, v in arcs:
        beats[u][v] = True
    out = [sum(row) for row in beats]
    start = {v: frozenset(w for w in range(n) if out[w] == out[v]) for v in range(n)}

    def extend(cands):
        if not cands:
            return 1
        v = min(cands, key=lambda x: len(cands[x]))
        total = 0
        for w in cands[v]:
            nxt = {}
            for x, c in cands.items():
                if x == v:
                    continue
                c2 = frozenset(y for y in c if y != w and beats[x][v] == beats[y][w])
                if not c2:
                    break
                nxt[x] = c2
            else:
                total += extend(nxt)
        return total

    return extend(start)


def witness_78():
    arcs39 = steiner_39()
    a = 39
    A = [a, a]
    B = [7, 7, 49, 5, 5, 5]
    means = [F(x, 100) for x in [-275, -183, -4, 164, 219, 298]]
    n = sum(A)
    check(sum(B) == n and linearity(B) < linearity(A))

    t = F(229, 100)
    cdf_lo, cdf_hi = normal_cdf_bounds(t)
    exponent = -t*t/2
    r_lo = down(NORMAL_LO*exp_poly(exponent, 29)/cdf_hi)
    r_hi = up(NORMAL_HI*exp_poly(exponent, 30)/cdf_lo)
    check(0 < r_lo < r_hi)

    # Square the lower bound so all exponents on positive rational bases are integers.
    internal_gain = F(2)**(2*(edges(A)-edges(B)))
    curvature_gain = (1+2*a/(3*PI_HI))**(2*(a-1))
    ratio_sq = internal_gain*curvature_gain/(n+1)**(n-1)/cdf_hi**(2*a*a)
    tilt = 2*a*a*(t*r_lo-a*r_hi**2)-sum(s*y*y for s, y in zip(B, means))
    ratio_sq *= exp_lower(tilt)
    for j, size_j in enumerate(B):
        for i in range(j):
            cdf_lower, _ = normal_cdf_bounds(means[j]-means[i])
            ratio_sq *= cdf_lower**(2*B[i]*size_j)
    check(ratio_sq > 10**10)
    print("78 candidates: linearities", linearity(A), linearity(B),
          "and P(B)/P(A) > 100000.")
    print("78 candidates: the rational lower bound itself is %.4g" % float(ratio_sq)**0.5)
    # Isomorphism classes.  In an ordered block tournament every vertex of block j has
    # score (vertices in later blocks) + (b_j - 1)/2; these scores are distinct across
    # blocks here, so every automorphism maps each block onto itself and |Aut| is the
    # product of the block automorphism counts.
    scores_A = [a + (a-1)//2, (a-1)//2]
    scores_B = [sum(B[j+1:]) + (B[j]-1)//2 for j in range(len(B))]
    check(len(set(scores_A)) == 2 and len(set(scores_B)) == len(B))
    aut39 = automorphism_count(39, arcs39)
    aut_circ = {b: circulant_automorphism_count(b) for b in set(B)}
    check(all(automorphism_count(b, circulant(b)) == b for b in (5, 7, 9, 11, 13)))
    aut_A = aut39**2
    aut_B = 1
    for b in B:
        aut_B *= aut_circ[b]
    check(aut39 == 3 and aut_circ == {5: 5, 7: 7, 49: 49})
    check(aut_A == 9 and aut_B == 300125)
    # class probability = (n!/|Aut|) * labelled probability
    class_ratio_sq = ratio_sq * F(aut_A, aut_B)**2
    check(class_ratio_sq > F(33, 10)**2)
    print("78 candidates: |Aut(A)| =", aut_A, "|Aut(B)| =", aut_B,
          "and the isomorphism-class probability ratio exceeds 3.3.")
    print("78 candidates: class-ratio lower bound %.4f" % float(class_ratio_sq)**0.5)


def witness_319():
    A, B = [159, 159, 1], [61, 197, 61]
    check(sum(B) == sum(A) == 319 and linearity(B) < linearity(A))
    check(edges(A)-edges(B) == 2156)
    check(normal_cdf_bounds(F(13, 5))[0] > F(199, 200))
    check(normal_cdf_bounds(F(26, 5))[0] > F(9999, 10000))
    # e < 11/4 < sqrt(8); the first follows by the exponential series.
    check(F(11, 4)**2 < 8 and F(3, 2)*61*F(13, 5)**2 < 619)
    ratio_lo = (F(2)**(2156-619) * F(199, 200)**(2*61*197)
                * F(9999, 10000)**(61*61) / 320**159)
    check(ratio_lo > 2**39)
    print("319 candidates: linearities", linearity(A), linearity(B),
          "and P(B)/P(A) > 2^39.")


if __name__ == "__main__":
    witness_78()
    witness_319()
