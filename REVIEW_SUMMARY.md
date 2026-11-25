# Review summary (internal, AI-assisted)

This file records the internal checking of this candidate before release, without any ratings. It is not peer review,
independent reproduction or formal verification. All review steps were carried out by AI systems (Claude) under the
Evidence Press publication protocol; no external referee has seen the paper.

## What was done (24–25 November 2026)

1. **Five reviewer roles** (editor, domain, perspective, methodology and devil's advocate), run as two Claude subagent
   calls. The methodology and devil's-advocate roles audited every proof line by line and recomputed the load-bearing
   numbers (including the block identities for t = 1, 3, 5, 7). No role found a mathematical error; the objections
   concerned the framing of the replication result, credit to earlier work, the labelled-versus-isomorphism-class
   question, the size of the smallest counterexample, the certificate margin, the checks under `python -O` and
   readability.
2. **Replay** of every script by the lead from a fresh copy, which found that the pass/fail checks relied on `assert`
   (and so would be skipped under `python -O`). All checks were converted to explicit failures; a negative control
   (raising the certificate threshold from 10^10 to 10^11) makes `certificate.py` exit 1 under `-O`.
3. **One revision round** with extensions (listed below).
4. **Re-review and proof audit** of the changed material, including an independent recomputation of the certificate
   constants and the automorphism counts. No error in a proved statement was found; one wording item in the abstract
   and six minor items were applied.
5. No Astra/Codex review took place for this candidate.

## Main objections and how they were resolved

- **Replication result (Makur and Singh).** Makur and Singh's upper bound needs k ≥ max{2, c d_max h log n / ξ⁴}
  observations per ordered pair, and they remark that the necessity of k ≥ 2 is unclear. The paper now states exactly
  what it proves: k = 1 is impossible at constant separation (Proposition 9.1), and whether a constant number of
  observations per pair suffices remains open. The masking construction is credited to Rastogi et al. (Proposition 4
  there), and the explicit error bounds are stated.
- **Credit.** The Gaussian many-voter limit is credited to Harrison-Trainor and to Hązła, Mossel, Ross and Zheng; the
  cyclic-triple count is tied to the classical circular-triad count via Singh and Davidov (2026); Mossel's
  exp(−Θ(n^{5/3})) bound for the transitive probability is added; Saile and Suksompong's Lemma 6 is cited and
  distinguished from the compression theorem; Lauritzen's characterisation is credited through Lauritzen (2008,
  Section 2.4), and the paper reproves the converse independently.
- **Labelled outcomes versus isomorphism classes.** Corollary 5.2 counts the automorphisms of the 78-candidate pair
  exactly (9 and 300125) and shows the reversal persists for isomorphism classes (ratio above 3.3).
- **How small can a counterexample be?** A Monte Carlo study (`code/small_reversals.py`) was added: no reversal among
  all isomorphism types on three to seven candidates, none among block tournaments on 8 to 12, and reversals on 13 and
  14 candidates. These are labelled as uncertified estimates; certification at 13 or 14 candidates is stated as open.
- **Certificate margin.** The rational lower bound (about 1.104 × 10⁵, roughly 10% above the stated 10⁵) is reported.
- **Readability.** Context-first abstract and introduction, purpose sentences for every section, a Part I / Part II
  split with a bridging paragraph, a discussion of scope, uses and open problems, and the certificate arithmetic moved to
  an appendix.

## Verification-round changes

- The abstract no longer implies that reversals are known for every size from 14 onwards.
- Minor wording, a definition added, a section heading changed, the certificate now checks the class ratio bound 3.3
  directly, and the difference from Singh and Davidov's lack-of-fit tests (cardinal or replicated data) is stated.

## What remains open or unchecked

- The smallest number of candidates admitting a reversal (between 8 and 13 on numerical evidence; certified at 78).
- A correct replacement for the conjecture; finite-sample power bounds for the tests; constant replication for the
  Makur–Singh guarantee.
- The small-case results are Monte Carlo estimates, not certificates.
- Prior-art searches were of limited scope; this is not a proof of priority.
- No external specialist has checked the proofs.
