"""Numerical (uncertified) search for small linearity reversals.

p(T) = E exp(sum_{i->j} log Phi(X_i - X_j)), X ~ N(0, I_n)  (the impartial-culture
large-electorate limit, eq. (3) of the manuscript).  Each p(T) is estimated by
importance sampling from a multivariate Student t (8 d.f.) centred at the mode of
H_T(x) = L_T(x) - |x|^2/2 with the inverse negative Hessian as scale.
Outputs are Monte Carlo estimates with standard errors; they are NOT certificates.
"""
import itertools, json, math, sys
import numpy as np
from scipy.special import log_ndtr, gammaln

LOG2PI = math.log(2 * math.pi)

def edges(T):
    i, j = np.nonzero(T)
    return i, j

def mode(T):
    n = len(T); i, j = edges(T); x = np.zeros(n)
    for _ in range(100):
        d = x[i] - x[j]
        r = np.exp(-0.5 * d * d - 0.5 * LOG2PI - log_ndtr(d))      # phi/Phi
        g = -x.copy(); np.add.at(g, i, r); np.add.at(g, j, -r)
        l2 = -r * (d + r)                                           # l''(d)
        Hs = -np.eye(n)
        np.add.at(Hs, (i, i), l2); np.add.at(Hs, (j, j), l2)
        np.add.at(Hs, (i, j), -l2); np.add.at(Hs, (j, i), -l2)
        step = np.linalg.solve(Hs, -g); x = x + step
        if np.abs(step).max() < 1e-12:
            break
    return x, -Hs

def logp(T, nsamp, seed, df=8.0, chunk=50000):
    n = len(T); i, j = edges(T); x0, P = mode(T)
    C = np.linalg.cholesky(np.linalg.inv(P)); logdetC = np.log(np.diag(C)).sum()
    rng = np.random.default_rng(seed); logw = []
    for s in range(0, nsamp, chunk):
        m = min(chunk, nsamp - s)
        z = rng.standard_normal((m, n)); u = rng.chisquare(df, m)
        y = z / np.sqrt(u / df)[:, None]
        x = x0 + y @ C.T
        H = log_ndtr(x[:, i] - x[:, j]).sum(1) - 0.5 * (x * x).sum(1) - 0.5 * n * LOG2PI
        q2 = (y * y).sum(1)
        logq = (gammaln((df + n) / 2) - gammaln(df / 2) - 0.5 * n * math.log(df * math.pi)
                - logdetC - 0.5 * (df + n) * np.log1p(q2 / df))
        logw.append(H - logq)
    lw = np.concatenate(logw); mx = lw.max(); w = np.exp(lw - mx)
    mean = w.mean(); se = w.std(ddof=1) / math.sqrt(len(w))
    return math.log(mean) + mx, se / mean

def lin(T):
    return int((T.sum(1) ** 2).sum())

def cyc(T):
    n = len(T); return math.comb(n, 3) - sum(math.comb(int(d), 2) for d in T.sum(1))

def odd_compositions(n):
    """All ordered compositions of n into odd positive parts."""
    if n == 0:
        yield ()
        return
    for first in range(1, n + 1, 2):
        for rest in odd_compositions(n - first):
            yield (first,) + rest

def block_tournament(sizes):
    """Blocks listed from strongest to weakest; earlier blocks beat later blocks;
    regular circulant tournament inside each (odd) block."""
    n = sum(sizes); T = np.zeros((n, n), dtype=np.int8); start = 0; starts = []
    for b in sizes:
        starts.append(start)
        for u in range(b):
            for k in range(1, (b - 1) // 2 + 1):
                T[start + u, start + (u + k) % b] = 1
        start += b
    for a, (sa, ba) in enumerate(zip(starts, sizes)):
        for sb, bb in zip(starts[a + 1:], sizes[a + 1:]):
            T[sa:sa + ba, sb:sb + bb] = 1
    return T

def canon(T, perms):
    n = len(T); best = None
    for p in perms:
        key = T[np.ix_(p, p)].tobytes()
        if best is None or key < best:
            best = key
    return best

def iso_classes(nmax):
    """Isomorphism classes of tournaments on n<=nmax vertices, by vertex extension."""
    classes = {1: [np.zeros((1, 1), dtype=np.int8)]}
    for n in range(2, nmax + 1):
        perms = [list(p) for p in itertools.permutations(range(n))]
        # canonicalise only within score-sorted orderings for speed: sort perms
        seen = {}
        for R in classes[n - 1]:
            for mask in range(2 ** (n - 1)):
                T = np.zeros((n, n), dtype=np.int8); T[:n - 1, :n - 1] = R
                for v in range(n - 1):
                    if mask >> v & 1:
                        T[n - 1, v] = 1
                    else:
                        T[v, n - 1] = 1
                sc = T.sum(1); order = np.argsort(-sc, kind="stable")
                T = T[np.ix_(order, order)]; sc = T.sum(1)
                ps = [p for p in perms if all(sc[p[k]] == sc[k] for k in range(n))]
                key = canon(T, ps)
                if key not in seen:
                    seen[key] = T
        classes[n] = list(seen.values())
    return classes

def main():
    out = {"note": "Monte Carlo importance-sampling estimates; uncertified", "small_n": {}, "blocks": {}, "pairs": []}
    # (a) every isomorphism class for n = 3..7
    cls = iso_classes(7)
    for n in range(3, 8):
        rows = []
        for k, T in enumerate(cls[n]):
            lp, rse = logp(T, 200000, 1000 * n + k)
            aut = sum(1 for p in itertools.permutations(range(n)) if (T[np.ix_(p, p)] == T).all()) if n <= 6 else None
            rows.append((lin(T), lp, rse, T))
        # labelled class sizes for total-mass check (n<=6 only)
        viol = []; minratio = math.inf
        for a in rows:
            for b in rows:
                if a[0] > b[0]:
                    r = a[1] - b[1]
                    minratio = min(minratio, r)
                    if r < 0:
                        viol.append((a[0], b[0], r))
        out["small_n"][n] = {"classes": len(rows), "reversals": len(viol),
                             "min_log_ratio_higher_lin_over_lower_lin": minratio,
                             "max_rel_se": max(x[2] for x in rows)}
        print(n, out["small_n"][n], flush=True)
    # (b) all ordered compositions into odd blocks, n = 8..14
    for n in range(8, 15):
        comps = list(odd_compositions(n))
        est = []
        for k, c in enumerate(comps):
            T = block_tournament(c); lp, rse = logp(T, 40000, 7 * n + 100000 + k)
            est.append((lin(T), lp, rse, c))
        best = None
        for a in est:
            for b in est:
                if a[0] < b[0]:      # a has LOWER linearity (more cyclic)
                    r = a[1] - b[1]
                    if best is None or r > best[0]:
                        best = (r, a[3], b[3], a[0], b[0])
        out["blocks"][n] = {"compositions": len(comps), "best_log_ratio_more_cyclic_over_less": best[0],
                            "more_cyclic": best[1], "less_cyclic": best[2], "lins": [best[3], best[4]]}
        print(n, out["blocks"][n], flush=True)
    # (c) high-precision confirmation of selected pairs
    for A, B in [((7, 7), (1, 1, 1, 9, 1, 1)), ((7, 7), (1, 9, 3, 1)),
                 ((7, 1, 1, 1, 3), (3, 7, 3)), ((7, 1, 1, 1, 1, 1, 1), (1, 1, 7, 3, 1))]:
        TA, TB = block_tournament(A), block_tournament(B)
        reps = []
        for s in range(4):
            la, ea = logp(TA, 1000000, 500 + s); lb, eb = logp(TB, 1000000, 600 + s)
            reps.append({"logp_less_cyclic": la, "logp_more_cyclic": lb, "relse": [ea, eb], "log_ratio": lb - la})
        lr = [r["log_ratio"] for r in reps]
        rec = {"less_cyclic_blocks": A, "more_cyclic_blocks": B, "lin": [lin(TA), lin(TB)], "cyclic_triples": [cyc(TA), cyc(TB)],
               "log_ratio_mean": float(np.mean(lr)), "log_ratio_sd_between_seeds": float(np.std(lr, ddof=1)),
               "ratio": math.exp(float(np.mean(lr))), "replicates": reps}
        out["pairs"].append(rec); print(json.dumps({k: rec[k] for k in rec if k != "replicates"}), flush=True)
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)

if __name__ == "__main__":
    main()
