"""Conditional evidence against Bradley-Terry, targeted to the Gaussian majority law."""
import numpy as np
from scipy.special import log_ndtr, ndtri


def probit_log_e(wins):
    """Return the natural log of an e-value for one labelled round robin."""
    edges = np.asarray(wins)
    if edges.ndim != 2 or edges.shape[0] != edges.shape[1] or len(edges) < 2:
        raise ValueError("provide a square win matrix of order at least two")
    binary = (edges == 0) | (edges == 1)
    if not np.all(binary) or np.any(np.diag(edges) != 0):
        raise ValueError("entries must be 0 or 1, with diagonal zero")
    edges = edges.astype(bool, copy=False)
    if np.any((edges == edges.T) & ~np.eye(len(edges), dtype=bool)):
        raise ValueError("each distinct pair must have a single winner")
    n = len(edges)
    m = n // 3
    estimate = np.sqrt(2) * ndtri((edges.sum(axis=1) + 0.5) / n)
    if m == 0:
        return 0.0
    a, j = np.indices((m, m))
    b, c = m + j, 2*m + (a+j) % m
    ab, bc, ca = edges[a, b], edges[b, c], edges[c, a]
    cyclic = (ab == bc) & (bc == ca)
    if not np.any(cyclic):
        return 0.0
    a, b, c = a[cyclic], b[cyclic], c[cyclic]
    log_odds = np.zeros(len(a))
    for first, second in ((a,b), (b,c), (c,a)):
        gap = estimate[first] - estimate[second]
        log_odds += log_ndtr(gap) - log_ndtr(-gap)
    # Bounded predictions ensure the consistency proof also covers extreme scores.
    log_odds = np.clip(log_odds, -4.0, 4.0)
    direction = np.where(edges[a,b], 1, -1)
    return float(np.sum(np.log(2) - np.logaddexp(0, -direction * log_odds)))
