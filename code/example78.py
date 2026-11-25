"""Emit the two labelled outcomes from the 78-candidate certificate as CSV."""
import csv
import hashlib
import io
import sys
from itertools import combinations

LABELS = range(1, 79)
PAIRS = tuple(combinations(LABELS, 2))


def add_edge(winners, winner, loser):
    pair = tuple(sorted((winner, loser)))
    if winner == loser or pair in winners:
        raise ValueError(f"Repeated or invalid edge {pair}")
    winners[pair] = winner


def outcome_a():
    winners = {}
    for offset in (0, 39):
        def label(x, layer):
            return offset + 1 + 3 * x + layer

        def cycle(a, b, c):
            add_edge(winners, a, b)
            add_edge(winners, b, c)
            add_edge(winners, c, a)

        for x in range(13):
            cycle(label(x, 0), label(x, 1), label(x, 2))
        for x, y in combinations(range(13), 2):
            midpoint = 7 * (x + y) % 13
            for layer in range(3):
                cycle(label(x, layer), label(y, layer),
                      label(midpoint, (layer + 1) % 3))
    for stronger in range(40, 79):
        for weaker in range(1, 40):
            add_edge(winners, stronger, weaker)
    return winners


def outcome_b():
    winners = {}
    first = 1
    for size in (7, 7, 49, 5, 5, 5):
        block = range(first, first + size)
        for candidate in block:
            for earlier in range(1, first):
                add_edge(winners, candidate, earlier)
        for left, right in combinations(block, 2):
            if right - left <= (size - 1) // 2:
                add_edge(winners, left, right)
            else:
                add_edge(winners, right, left)
        first += size
    return winners


def audit(winners, expected_scores, expected_linearity, expected_cycles):
    if set(winners) != set(PAIRS) or len(PAIRS) != 3003:
        raise ValueError("Expected exactly one record for every unordered pair")
    scores = [0] * len(LABELS)
    for pair, winner in winners.items():
        if winner not in pair:
            raise ValueError(f"Invalid winner {winner} on {pair}")
        scores[winner - 1] += 1
    if scores != expected_scores or sum(d*d for d in scores) != expected_linearity:
        raise ValueError("Observed labelled scores or linearity differ from the certificate")

    cycles = 0
    triples = 0
    for a, b, c in combinations(LABELS, 3):
        # The three winners are all distinct exactly when the triple is cyclic.
        wins = (winners[a, b], winners[b, c], winners[a, c])
        cycles += len(set(wins)) == 3
        triples += 1
    if triples != 76076 or cycles != expected_cycles:
        raise ValueError(f"Unexpected triple enumeration: {triples} triples, {cycles} cycles")
    return scores


def main():
    a = outcome_a()
    b = outcome_b()
    scores_a = audit(a, [19]*39 + [58]*39, 145275, 4940)
    scores_b = audit(b, [3]*7 + [10]*7 + [38]*49 + [65]*5 + [70]*5 + [75]*5,
                     145269, 4943)
    data = io.StringIO(newline="")
    writer = csv.writer(data, lineterminator="\n")
    writer.writerow(("first_candidate", "second_candidate", "winner_in_A", "winner_in_B"))
    writer.writerows((i, j, a[i, j], b[i, j]) for i, j in PAIRS)
    result = data.getvalue().encode("ascii")
    sys.stdout.buffer.write(result)
    print("Verified 3,003 candidate pairs and 76,076 triples per tournament.", file=sys.stderr)
    print("Cyclic triples (A,B): 4,940 and 4,943. Linearities: 145,275 and 145,269.", file=sys.stderr)
    print(f"Outdegrees A in label order: {scores_a}", file=sys.stderr)
    print(f"Outdegrees B in label order: {scores_b}", file=sys.stderr)
    print(f"CSV SHA-256: {hashlib.sha256(result).hexdigest()}", file=sys.stderr)


if __name__ == "__main__":
    main()
