# When a more cyclic majority tournament is more probable

**A counterexample to Harrison-Trainor's linearity conjecture, the transitive maximum, and what win totals reveal**

Version 0.1.0-candidate. DOI [10.5281/zenodo.24526810](https://doi.org/10.5281/zenodo.24526810) (all versions:
[10.5281/zenodo.24526809](https://doi.org/10.5281/zenodo.24526809)). Release page:
<https://evidencepress.org/releases/majority-tournament-cyclic-reversal/>. Author: Anonymous. Status: unrefereed
research candidate; internal AI-assisted review only.

## What this is about

Imagine many voters, each ranking the same candidates in a random order, every ranking equally likely and every voter
independent. This "impartial culture" is the standard yardstick of voting theory. For each pair of candidates, look at
who wins the head-to-head majority vote and draw an arrow from the winner to the loser. The result is a
*tournament*. Sometimes three candidates form a rock-paper-scissors loop: A beats B, B beats C and C beats A. That loop
is a *cyclic triple*, the pattern behind Condorcet's paradox.

Harrison-Trainor (Mathematical Social Sciences, 2022) conjectured that, with many voters, an outcome with fewer such
loops is always more likely than one with more loops. He checked this for up to five candidates.

## What the paper shows

1. **The conjecture is false.** Split the candidates into ordered groups ("blocks"): everyone in a stronger block beats
   everyone in a weaker one, and inside a block everyone wins half their games. Making an outcome happen costs about a
   factor of two for every pair of candidates whose strengths must be almost tied, and those pairs sit inside blocks. Loops
   also sit inside blocks. Pairs grow like the square of the block size and loops like its cube, so some block patterns
   have more loops yet need fewer almost-tied pairs. For every odd t there are tournaments on 14t candidates where the
   one with 3t³ more loops is 2^(3t²+o(t²)) times as likely.
2. **A fully checked example on 78 candidates.** An exact rational certificate shows that a tournament with three more
   loops is more than 100,000 times as likely. The reversal survives when outcomes are counted up to relabelling of the
   candidates (ratio above 3.3).
3. **Small cases (computer estimates, not proofs).** Monte Carlo integration finds no reversal with seven or fewer
   candidates, and finds reversals with 13 candidates (by about 1%) and 14 candidates (by a factor of about 2.7).
4. **The half of the conjecture that survives.** The fully ordered (loop-free) outcomes are exactly the most likely
   ones, for every number of candidates and for a wide class of paired-comparison models.
5. **Part II: what win totals reveal.** In any round robin, unless the Bradley–Terry model holds, outcomes with the
   same win totals differ in likelihood by factors exponential in the number of pairs. An exactly calibrated test built
   from directed triangles detects this from a single round robin. With one game per pair, the minimax Bradley–Terry–Luce
   test of Makur and Singh is impossible at constant separation; whether a constant number of games per pair suffices
   remains open.

## Limits

- Impartial culture is a mathematical null model, not a description of real elections.
- All election results are in the limit of many voters; no finite electorate size is given.
- The smallest counterexample is not determined: it is certified at 78 candidates, and the numerical evidence places
  it between 8 and 13.
- The Part II results hold for a fixed model, and the tests have modest power at the sizes of real leagues.

## Credit

The conjecture is Harrison-Trainor's. The Gaussian many-voter limit is due to Harrison-Trainor and to Hązła, Mossel,
Ross and Zheng. The qualitative characterisation of models whose win totals determine probabilities is due to
Lauritzen and to Iyer. The masking construction behind the replication result is due to Rastogi, Balakrishnan, Shah and
Singh, and the replication question to Makur and Singh. Full references: [refs.bib](refs.bib) and the paper.

## Contents

| Path | What it is |
|---|---|
| [majority.pdf](majority.pdf), [majority.tex](majority.tex) | The paper (19 pages) and its LaTeX source (`pdflatex` twice) |
| [code/certificate.py](code/certificate.py) | Exact rational certificate for the 78- and 319-candidate examples and the automorphism counts (standard library) |
| [code/example78.py](code/example78.py) | Writes both 78-candidate tournaments as a table of the 3003 pair winners and recounts outdegrees and all 76,076 triples |
| [code/check_compression.py](code/check_compression.py) | Exact enumeration on five candidates for the compression argument (standard library) |
| [code/check_cycles.py](code/check_cycles.py) | Exhaustive check of the fair-sign symmetry and exact calibration for up to six candidates (standard library) |
| [code/score_test.py](code/score_test.py), [code/kernel_test.py](code/kernel_test.py), [code/probit_test.py](code/probit_test.py) | The scan, spectral and targeted tests of Part II |
| [code/check_scan.py](code/check_scan.py), [code/check_spectral.py](code/check_spectral.py) | Checks of the tests against direct evaluation and on positive controls |
| [code/power_study.py](code/power_study.py) | Seeded power study (Table 2) |
| [code/small_reversals.py](code/small_reversals.py) | Monte Carlo small-case study (Section 5.2, Table 1); estimates, not certificates |
| [results/](results/) | Recorded outputs: certificate.txt, counterexample-78.csv, power.csv, small_reversals.json and .log |
| [AI_INDEX.md](AI_INDEX.md) | Machine-oriented map of claims, evidence and limits |
| [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [ENVIRONMENT.txt](ENVIRONMENT.txt) | Review, replay, prior-art and environment records |
| [MANIFEST.sha256](MANIFEST.sha256) | SHA-256 of every file |

## How to rerun

From `code/`, with the threads of numerical libraries set to one:

```sh
python3 -I -B -O certificate.py         # seconds; output equals results/certificate.txt
python3 -I -B -O check_compression.py
python3 -I -B -O check_cycles.py
python3 -E -s -B -O check_scan.py        # needs numpy and scipy (requirements.txt); -E -s, not -I,
python3 -E -s -B -O check_spectral.py    # because these import sibling modules
python3 -E -s -B example78.py > x.csv    # equals results/counterexample-78.csv
python3 -E -s -B power_study.py > p.csv  # equals results/power.csv
python3 -E -s -B small_reversals.py out.json   # optional, about 4 minutes; Monte Carlo
```

Every check exits with an error on failure, also under `python -O`. Raising the certificate threshold from 10^10 to
10^11 makes `certificate.py` exit 1 (negative control, run in the release replay and in CI).

**Comparison policy** (the same in CI, ENVIRONMENT.txt and REPLAY_RECEIPT.md). Exact outputs compare exactly on every
platform: `results/certificate.txt` and `results/counterexample-78.csv`. `results/power.csv` holds seeded rejection
counts: byte-identical on the release platform; elsewhere each count may differ by at most 1. `small_reversals.py` is a
seeded Monte Carlo study: on another platform its log ratios should agree with `results/small_reversals.json` to within
0.01; CI runs it as a non-blocking job. Interpreter versions are not compared.

## Assurance

Written proofs with an exact rational certificate and exhaustive small-case checks. Internal AI-assisted review only:
five Claude reviewer roles in two calls, the lead's replay of the rational certificate and every check script with a
negative control, one revision round with extensions, then a re-review and proof audit of the changed proofs. No
Astra/Codex review took place. This is not peer review, independent reproduction or formal verification. See
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).

## Licence and citation

Text, the paper, recorded outputs and records: CC0-1.0. Code: MIT. See [LICENSE.md](LICENSE.md) and
[CITATION.cff](CITATION.cff). Cite as: Anonymous (2026), *When a more cyclic majority tournament is more probable*,
version 0.1.0-candidate, Zenodo, doi:10.5281/zenodo.24526810.
