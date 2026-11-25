"""Exact aggregation over binary latent strengths, for all labelled five-vertex tournaments."""
from itertools import combinations, product
from math import prod


def check(condition):
    """Fail loudly (also under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED")

def main():
    n = 5
    pairs = list(combinations(range(n), 2))
    cases = list(product((0, 1), repeat=len(pairs)))
    assignments = list(product((0, 1), repeat=n))
    weights = {}
    for signs in cases:
        wins = tuple((i, j) if s else (j, i) for (i, j), s in zip(pairs, signs))
        # K(high,low)=3/4, K(low,high)=1/4, K(tie)=1/2.
        weights[frozenset(wins)] = sum(prod(2 + x[i]-x[j] for i, j in wins)
                                        for x in assignments)
    checked = 0
    total = (2**n)*(4**len(pairs))
    check(sum(weights.values()) == total)
    for wins, before in weights.items():
        for i, j in wins:
            back = [k for k in range(n) if (j, k) in wins and (k, i) in wins]
            if not back:
                continue
            after = set(wins)
            for k in back:
                after -= {(j, k), (k, i)}
                after |= {(i, k), (k, j)}
            check(weights[frozenset(after)] > before)
            checked += 1
    max_weight = max(weights.values())
    max_count = sum(w == max_weight for w in weights.values())
    check(max_count == 120)
    print(f'{len(weights)} tournaments, {checked} strict compressions, '
          f'{max_count} maximisers, total mass exactly 1.')

if __name__ == '__main__':
    main()
