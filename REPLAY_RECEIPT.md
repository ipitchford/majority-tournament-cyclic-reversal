# Replay receipt (release 0.1.0-candidate, 25 November 2026)

Input: the approved candidate (18 files: majority.tex, majority.pdf, 11 scripts in code/, 5 recorded outputs in
results/), each SHA-256 checked against the frozen candidate list before use. After the replay only the title-page DOI
line was added to majority.tex and the PDF was rebuilt (pdflatex, three passes, 19 pages; word-level text comparison
with the approved PDF shows only the added DOI line). No script or recorded output changed.

## Runs (fresh copies, cwd = code/, macOS arm64)

| Command | Interpreter | Result |
|---|---|---|
| `python3 -I -B -O certificate.py` | CPython 3.14.7 and 3.12.11 | exit 0; stdout byte-identical to results/certificate.txt |
| `python3 -I -B -O check_compression.py` | 3.14.7 and 3.12.11 | exit 0; 1024 tournaments, 5920 strict compressions, 120 maximisers, total mass exactly 1 |
| `python3 -I -B -O check_cycles.py` | 3.14.7 and 3.12.11 | exit 0; PASS exact calibration on every score fibre (n = 3..6) |
| `python3 -E -s -B -O check_scan.py` | 3.12.11, NumPy 2.3.5, SciPy 1.17.0 | exit 0; six direct-evaluation matches; positive control log p bound −309.034264 |
| `python3 -E -s -B -O check_spectral.py` | same | exit 0; minimum p 0.13809455; positive control log p bound −63.003488 |
| `python3 -E -s -B example78.py` | same | exit 0; output byte-identical to results/counterexample-78.csv; cyclic triples 4,940 and 4,943 |
| `python3 -E -s -B power_study.py` | same | exit 0; output byte-identical to results/power.csv |

`small_reversals.py` (Monte Carlo, about 4 minutes) was not rerun at release: its code and recorded outputs are
byte-identical to the approved candidate, whose outputs it produced; CI reruns it as a non-blocking job with the
declared tolerance.

## Negative control

In a fresh copy, `check(ratio_sq > 10**10)` in certificate.py was changed to `10**11`; under `python3 -I -B -O` the
script printed `CHECK FAILED` and exited 1.

## Comparison policy

As in ENVIRONMENT.txt and README.md: certificate.txt and counterexample-78.csv compare exactly on every platform;
power.csv is byte-identical on the release platform and within one rejection per cell elsewhere; small_reversals.json
log ratios within 0.01 elsewhere; interpreter versions are not compared.
