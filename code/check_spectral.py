"""Check a fair-sign orbit and an alternative for the held-out kernel test."""
from itertools import product

import numpy as np

from kernel_test import kernel_test


def check(condition):
    """Fail loudly (also under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED")


def audit_orbit():
    n = 27
    m = n // 3
    first, second = np.triu_indices(n, k=1)
    mask = np.zeros((n, n), dtype=bool)
    mask_seed = 17
    rng = np.random.default_rng(mask_seed)
    mask[first, second] = rng.integers(0, 2, size=len(first), dtype=np.int8)
    mask |= mask.T
    rng = np.random.default_rng(6)
    edges = np.zeros_like(mask)
    edges[first, second] = rng.integers(0, 2, size=len(first))
    edges |= np.tril(~edges.T, -1)
    degrees = edges.sum(axis=1)

    triangles = []
    for i, j in product(range(m), repeat=2):
        a, b, c = i, m + j, 2*m + (i + j) % m
        if mask[a, b] or mask[b, c] or mask[c, a]:
            continue
        if edges[a, b] == edges[b, c] == edges[c, a]:
            triangles.append(((a, b), (b, c), (c, a)))
    check(len(triangles) == 5)
    p_values = []
    for choices in product((False, True), repeat=len(triangles)):
        sample = edges.copy()
        for choice, triangle in zip(choices, triangles):
            if choice:
                for u, v in triangle:
                    sample[u, v], sample[v, u] = sample[v, u], sample[u, v]
        check(np.array_equal(degrees, sample.sum(axis=1)))
        p_values.append(kernel_test(sample, seed=mask_seed)["p_bound"])
    p_values = np.array(p_values)
    for alpha in np.unique(p_values):
        check(np.mean(p_values <= alpha) <= alpha + 1e-12)
    print(f"n={n}, {len(triangles)} held-out cyclic signs, "
          f"{len(p_values)} assignments, {len(np.unique(p_values))} p-values; "
          f"all attainable levels passed (minimum p={min(p_values):.8f}).")


def audit_alternative():
    # A regular three-type kernel with directional cycle bias on distinct types.
    # Keep the generator stream in the order used for the initial smoke check.
    rng = np.random.default_rng(3)
    for n in (2, 4, 48, 240):
        types = rng.integers(0, 3, n)
        win_prob = np.take([0.5, 0.95, 0.05], (types[:, None] - types[None, :]) % 3)
        edges = np.triu(rng.random((n, n)) < win_prob, 1)
        edges |= np.tril(~edges.T, -1)
        result = kernel_test(edges, seed=27)
        check(result["log_p_bound"] <= 0)
        if n == 2:
            check(result["p_bound"] == 1)
    check(result["log_p_bound"] < -20)
    print(f"Three-type kernel at n={n}: {result['heldout_triangles']} retained "
          f"triangles, {result['heldout_cycles']} cycles, "
          f"log p bound = {result['log_p_bound']:.6f}.")


if __name__ == "__main__":
    audit_orbit()
    audit_alternative()
