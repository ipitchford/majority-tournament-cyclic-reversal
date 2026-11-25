# AI index: When a more cyclic majority tournament is more probable (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [majority.pdf](majority.pdf) (source [majority.tex](majority.tex); Section 1 states the
question, why it matters, what was known, what is new, what is not claimed and a roadmap). DOI 10.5281/zenodo.24526810
(concept 10.5281/zenodo.24526809). Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

Impartial culture: N voters rank n labelled candidates independently and uniformly; N → ∞ through odd integers with n
fixed. p(T) is the limiting probability that the majority tournament equals the labelled tournament T. d_v is the
outdegree (number of wins) of v; linearity lin(T) = Σ_v d_v²; cyclic triples c(T) = C(n,3) − lin(T)/2 + C(n,2)/2 (eq. 1).
Harrison-Trainor's conjecture (Conjecture 6.3 of arXiv:2009.02979; Mathematical Social Sciences 116, 2022,
doi:10.1016/j.mathsocsci.2022.01.002): lin(T) > lin(U) implies p(T) > p(U). Ordered regular block tournament: blocks
of odd sizes b_1, b_2, …, every member of an earlier block beats every member of a later one, each block internally
regular. Part II: latent-type paired-comparison models with win probabilities strictly in (0,1); Bradley–Terry (BT)
case; Makur–Singh = doi:10.1109/TIT.2025.3605846. Reference keys as in [refs.bib](refs.bib).

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| 1 | Two-sided bound for every T: M_T − ((n−1)/2) log(n+1) ≤ log p(T) ≤ M_T; regular tournaments: log p = −C(n,2) log 2 − ((n−1)/2) log n + O(n) | Theorem 3.1, Proposition 3.2 | written proof; Gaussian limit credited to Harrison-Trainor and Hązła–Mossel–Ross–Zheng |
| 2 | Ordered regular block tournaments with k fixed blocks: log p = −m log 2 + O_k(n log(n+1)), m = number of internal pairs (Σ b_j² scale); lin = Σ_{r<n} r² − (1/12) Σ (b_j³ − b_j) | Proposition 4.2 | written proof |
| 3 | The conjecture is false: for every odd t, (7t,7t) versus (t,9t,3t,t) on 14t candidates; the second has 3t³ more cyclic triples and is 2^(3t²+O(t log t)) times as probable; lin difference 6t³ | Theorem 4.3, Remark 4.4 | written proof; new |
| 4 | Explicit 78-candidate pair: A = two 39-blocks (triangle-decomposed), B = circulant blocks (7,7,49,5,5,5); lin 145275 vs 145269; c 4940 vs 4943; p(B)/p(A) > 10^5 (rational lower bound 1.104e5) | Proposition 5.1, Appendix A | exact rational certificate (code/certificate.py) |
| 5 | Isomorphism classes: |Aut A| = 9, |Aut B| = 300125; class ratio > 3.3 (bound 3.3109) | Corollary 5.2 | proof plus exhaustive automorphism count in certificate.py |
| 6 | 319-candidate witness (159,159,1) vs (61,197,61): ratio > 2^39 | Section 5.1 | certificate.py |
| 7 | Small cases: no reversal among the 2, 4, 12, 56, 456 isomorphism types on 3..7 candidates (min ratio 1.29 at n = 7); none among block tournaments n = 8..12 (best 0.91 at 12); reversals at 13 (about 0.6% and 1%) and 14 (2.706; t = 1 family member 1.268) | Section 5.2, Table 1 | Monte Carlo importance sampling, uncertified (code/small_reversals.py) |
| 8 | Transitive tournaments are exactly the most probable labelled tournaments, every n, every exchangeable latent-strength model with strictly increasing win probabilities | Theorem 6.1 | written proof (compression); five-candidate enumeration check; Saile–Suksompong Lemma 6 distinguished |
| 9 | Fixed latent-type model: either win totals determine probabilities (BT case; qualitatively Lauritzen, Iyer) or typical outcomes have same-score neighbours e^{±cn²} times as probable | Theorem 7.1, Corollaries 7.2–7.3 | written proof |
| 10 | Triangle tests (spectral, score-localised scan, targeted e-value) exactly calibrated given the scores; consistent against every fixed non-BT model from one round robin | Proposition 8.1, Corollary 8.2, Section 8.3 | written proof; exact calibration checked exhaustively for n ≤ 6 (33,864 labelled tournaments) |
| 11 | Power study: e.g. 133/256 (52.0%, Wilson 95% 45.8–58.0%) at n = 360; 11.3% with half the spread; little power for leagues of a few dozen | Table 2, Section 8.3 | seeded simulation (results/power.csv) |
| 12 | One observation per pair: Makur–Singh minimax error sum ≥ 1 − exp(−C(n,2)/8) at separation 1/64 (k = 1 impossible at constant separation); round-robin version ≥ 1 − exp(−⌊n/3⌋²/128), n ≥ 6 | Proposition 9.1 | written proof; masking construction credited to Rastogi et al. Prop. 4; whether constant k suffices is open |
| Open | Smallest counterexample (between 8 and 13 on numerical evidence, certified at 78); a correct replacement statistic; constant replication for Makur–Singh; finite-sample power bounds | Section 10 | open |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| 78- and 319-candidate certificates, 39-block construction (247 triangles partition 741 pairs, outdegree 19), automorphism counts, class ratio | [code/certificate.py](code/certificate.py) | [results/certificate.txt](results/certificate.txt) | exact rational arithmetic, standard library |
| Both 78-candidate tournaments as 3003 pair winners; recount of outdegrees and all 76,076 triples (4,940 and 4,943 cyclic) | [code/example78.py](code/example78.py) | [results/counterexample-78.csv](results/counterexample-78.csv) | exact |
| Compression on five candidates: 1024 tournaments, 5920 strict compressions, 120 maximisers | [code/check_compression.py](code/check_compression.py) | printed | exact enumeration |
| Fair-sign symmetry and exact calibration on every score fibre, n = 3..6 | [code/check_cycles.py](code/check_cycles.py) | printed | exhaustive, exact |
| Scan and spectral tests against direct evaluation; positive controls | [code/check_scan.py](code/check_scan.py), [code/check_spectral.py](code/check_spectral.py) | printed | numerical checks |
| Power study (Table 2) | [code/power_study.py](code/power_study.py) | [results/power.csv](results/power.csv) | seeded simulation |
| Small cases (Section 5.2, Table 1) | [code/small_reversals.py](code/small_reversals.py) | [results/small_reversals.json](results/small_reversals.json), [results/small_reversals.log](results/small_reversals.log) | Monte Carlo, uncertified |

Every check exits non-zero on failure without `assert`, also under `python -O`. Negative control: raising the
certificate threshold from 10^10 to 10^11 makes certificate.py exit 1 under -O (release replay and CI).

Numbers quoted on the release page and in the audio: 78 candidates, three more cyclic triples, more than 100,000 times
as likely; class ratio above 3.3; no reversal with seven or fewer candidates; reversals at 13 (about 1%) and 14 (about
2.7) candidates; smallest counterexample between 8 and 13 on numerical evidence. All come from results/certificate.txt
and results/small_reversals.json.

## Limits

Impartial culture is a null model, not real elections. Election results are in the many-voter limit; no finite
electorate size is given. The small-case results are Monte Carlo estimates. Part II results are pointwise for a fixed
model, with modest power at league sizes. Prior-art searches were of limited scope (see
[RESEARCH_GATES.json](RESEARCH_GATES.json)).

## Records

[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) (rating-free internal review record), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md),
[ENVIRONMENT.txt](ENVIRONMENT.txt), [RESEARCH_GATES.json](RESEARCH_GATES.json), [refs.bib](refs.bib),
[CITATION.cff](CITATION.cff), [LICENSE.md](LICENSE.md), [MANIFEST.sha256](MANIFEST.sha256),
[.github/workflows/replay.yml](.github/workflows/replay.yml).
