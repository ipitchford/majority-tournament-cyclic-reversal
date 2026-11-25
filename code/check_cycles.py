"""Exhaustively check the conditional directed-cycle sign law and its calibration.

Run with Python 3.8+. Each edge bit orients an unordered pair. The preassigned
triangles are determined only by the labels. The calculation groups tournaments
by the triangles whose orientations remain free, then separately by degrees.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations


def check(condition):
    """Fail loudly (also under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED")


def audit(n):
    edges = list(combinations(range(n), 2))
    edge_index = {pair: i for i, pair in enumerate(edges)}
    m = n // 3
    triangles = [
        (i, m + j, 2 * m + (i + j) % m)
        for i in range(m)
        for j in range(m)
    ]
    orbit_members = defaultdict(list)
    fibres = defaultdict(Counter)
    for graph in range(1 << len(edges)):
        scores = [0] * n
        for index, (i, j) in enumerate(edges):
            winner = i if (graph >> index) & 1 else j
            scores[winner] += 1

        representative = graph
        signs = []
        weights = []
        for a, b, c in triangles:
            ab, bc, ac = (edge_index[pair] for pair in ((a, b), (b, c), (a, c)))
            bits = [(graph >> k) & 1 for k in (ab, bc, ac)]
            if bits not in ([1, 1, 0], [0, 0, 1]):
                continue
            # Set each directed cycle to the orientation a -> b -> c -> a.
            representative = (representative | (1 << ab) | (1 << bc)) & ~(1 << ac)
            signs.append(1 if bits[0] else -1)
            # Nonconstant, degree-dependent weight; common to every orbit member.
            weights.append((scores[a] + 1) * (scores[b] + 2) * (scores[c] + 3))
        tally = abs(sum(sign * weight for sign, weight in zip(signs, weights)))
        orbit_members[representative].append((tuple(scores), tuple(signs), tally))

    sizes = Counter()
    for members in orbit_members.values():
        degree, signs, _ = members[0]
        k = len(signs)
        expected_size = 1 << k
        check(len(members) == expected_size)
        check(len({member[1] for member in members}) == expected_size)
        check(all(member[0] == degree for member in members))
        sizes[expected_size] += 1
        histogram = Counter(member[2] for member in members)
        tail = 0
        for tally, count in sorted(histogram.items(), reverse=True):
            tail += count
            pvalue = Fraction(tail, expected_size)
            fibres[degree][pvalue] += count

    for pvalue_counts in fibres.values():
        size = sum(pvalue_counts.values())
        rejected = 0
        for level, count in sorted(pvalue_counts.items()):
            rejected += count
            # Exact super-uniformity for every attainable cutoff in this fibre.
            check(rejected * level.denominator <= size * level.numerator)

    print(
        f"n={n}, tournaments={1 << len(edges)}, labelled score vectors={len(fibres)}, "
        f"orbits_by_size={dict(sorted(sizes.items()))}"
    )


if __name__ == "__main__":
    for number_of_vertices in (3, 4, 5, 6):
        audit(number_of_vertices)
    print("PASS: complete fair-sign orbits and exact calibration on every score fibre.")
