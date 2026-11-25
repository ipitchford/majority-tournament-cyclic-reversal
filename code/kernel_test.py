"""Score-conditioned kernel test for a single labelled round robin.

Input a square JSON 0/1 matrix. A one in row i, column j means i beat j.
If specifying a seed, choose it independently of the outcomes and use it once.
"""
import argparse
import json
import math

import numpy as np


def _win_matrix(wins):
    edges = np.asarray(wins)
    if edges.ndim != 2 or edges.shape[0] != edges.shape[1] or len(edges) < 2:
        raise ValueError("provide a square win matrix of order at least two")
    if not np.all((edges == 0) | (edges == 1)) or np.any(np.diag(edges) != 0):
        raise ValueError("entries must be 0 or 1, with diagonal zero")
    edges = edges.astype(bool, copy=False)
    if not np.all((edges != edges.T) == ~np.eye(len(edges), dtype=bool)):
        raise ValueError("each distinct pair must have a single winner")
    return edges


def _fitted_probabilities(edges, training):
    signed = np.where(edges, 2.0, -2.0) * training
    left, values, right = np.linalg.svd(signed, full_matrices=False)
    rank = math.isqrt(len(edges))
    fitted = (left[:, :rank] * values[:rank]) @ right[:rank, :]
    skew = (fitted - fitted.T) / 2
    return (1 + np.clip(skew, -1, 1)) / 2


def kernel_test(wins, *, seed=None):
    """Return a one-sided log p-value bound using an independent training mask."""
    edges = _win_matrix(wins)
    n = len(edges)
    rng = np.random.default_rng(seed)
    first, second = np.triu_indices(n, k=1)
    training = np.zeros((n, n), dtype=bool)
    training[first, second] = rng.integers(0, 2, size=len(first), dtype=np.int8)
    training |= training.T
    fitted = _fitted_probabilities(edges, training)

    m = n // 3
    i, j = np.indices((m, m))
    a, b, c = i, m + j, 2 * m + (i + j) % max(1, m)
    heldout = ~(training[a, b] | training[b, c] | training[c, a])
    a, b, c = a[heldout], b[heldout], c[heldout]
    ab, bc, ca = edges[a, b], edges[b, c], edges[c, a]
    cyclic = (ab == bc) & (bc == ca)
    a, b, c = a[cyclic], b[cyclic], c[cyclic]
    p, q, s = fitted[a, b], fitted[b, c], fitted[c, a]
    weights = p * q * s - (1 - p) * (1 - q) * (1 - s)
    signs = np.where(edges[a, b], 1.0, -1.0)
    signed_sum = float(weights @ signs)
    square_sum = float(weights @ weights)
    log_p = -max(signed_sum, 0.0) ** 2 / (2 * square_sum) if square_sum else 0.0
    p_bound = math.exp(log_p)
    return {"vertices": n, "rank": math.isqrt(n), "packed_triangles": m*m,
            "heldout_triangles": int(heldout.sum()), "heldout_cycles": len(signs),
            "log_p_bound": log_p, "p_bound": p_bound if p_bound > 0 else None,
            "p_display_underflow": p_bound == 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", help="JSON file containing the labelled win matrix")
    parser.add_argument("--seed", type=int, help="prespecified training-mask seed")
    args = parser.parse_args()
    with open(args.matrix, encoding="utf-8") as source:
        print(json.dumps(kernel_test(json.load(source), seed=args.seed), indent=2))
