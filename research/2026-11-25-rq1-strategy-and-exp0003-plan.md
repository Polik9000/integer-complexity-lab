# RQ-1: strategies and the EXP-0003 plan (verification to an expert standard)

**Situation (2026-11-25).** EXP-0002 computed ‖2^61 − 1‖ = 127 in 2 minutes with a proven
algorithm and a single, well-tested implementation. The lower bound ‖N‖ ≥ 117 has a short
human-readable proof via Altman–Zelinsky Thm 1.6. The remaining job is to turn "our program says
127" into a result that holds up in front of experts.

## What an expert will ask, and how we answer it

| Question | Answer / plan |
|----------|---------------|
| Is the algorithm correct? | Written proof: `research/proof-exact-search.md`. External review: RP-0002 to ChatGPT, and possibly a human expert (needs the lead's approval). |
| Is the implementation correct? | Tests against literature (Iraids Table 3, AZ2012 Thm 1.6, Wang), a second implementation, and an independent author's code (He). |
| Can I check it without trusting your code? | **Proof certificate:** the search writes out its pruned search tree, and a small independent checker verifies it (S2 below). |
| Is the base table right? | Two implementations already agree on small n. Add a comparison with the published database (Iraids, n ≤ 10¹², online calculator), if reachable. |

## Strategies

**S1: replicate the exhaustive search independently (cheap, fastest confidence gain).**
(a) Build He's GPL code (`hqztrue/integer_complexity`, `single.cpp`, `calc_single`) and run it on
2^k − 1 for k ≤ 61. It's the same method written by another author. **This needs your
approval**, because the sandbox's safety policy blocked compiling and running third-party code without an explicit go-ahead.
(b) Write a second implementation of our own in C/C++ with a different structure: iterative deepening on the
budget (like He), a different factorizer, and no shared code. It also makes k > 61 feasible.

**S2: a proof-producing search with an independent checker (the most defensible).**
The search emits a certificate. For every visited node it records "‖m‖ > j" with the list of
splits it considered and why each was rejected. The leaves are table values or Selfridge bounds. A small
checker (~200 lines, written separately and easy to read) verifies the certificate. Then the trust base is
the checker, the base table and the factorizations, and each factorization is checkable by multiplication.
Primality of the factors needs Pratt or ECPP certificates, or deterministic Miller–Rabin. Size: ~10⁶ nodes,
an estimated 100–500 MB of JSON lines, compressible. In the end the checker could be written in **Lean 4**
for a `FORMALLY VERIFIED` lower bound. Kernel checking of 10⁶ nodes is at the edge of feasibility. A
verified checker with `native_decide` is a weaker but common standard.

**S3: defect theory (human-readable lower bounds).** AZ2012 Thm 1.6 already gives ≥ 117.
Extending the classification to defect ~11.5 is not realistic by hand. Best used as an independent
cross-check on small cases, and as the "short proof" part of a write-up.

**S4: implement He's interval DP (Thm 8) as a truly different algorithm.** It's independent in method,
not just in code. It's costlier and more complex (f/f′ bookkeeping, intervals [n/d − cL, n/d]). It
only pays off if S1/S2 leave doubts.

**Recommendation:** S1(b) + S2 now (both cheap, all in our sandbox). S1(a) as soon as you approve it.
S3 for the write-up. S4 only if needed.

## EXP-0003 plan

| Step | Work | CPU | RAM | Wall time | Risk |
|------|------|-----|-----|-----------|------|
| 1 | C/C++ second implementation, tests against the Python one for k ≤ 61 and random n | < 10 min | < 2 GB | ~1 day of work | The two implementations share design assumptions. Mitigated by S2. |
| 2 | Certificate output in the Python search, plus an independent Python checker; run for k = 61 | ~5–10 min | ~2–4 GB | ~1 day | Certificate size (est. 0.1–0.5 GB). Store it compressed, outside git, with SHA-256 in the README. |
| 3 | Run He's code for k ≤ 61 (**approved and done 2026-11-25**: 60/60 agree, k = 61 in 2.6 s, see EXP-0003) | ~5 min | ≤ 4 GB (table 10⁸ bytes + hash maps) | 1 h | Windows-specific code (`%I64d`, `.bat`), so it needs a small Linux driver. GPL, so we don't vendor it. |
| 4 | AZ2012 Thm 1.6 and Iraids Table 3 regression tests (done) | — | — | — | — |
| 5 | Review package RP-0002: claim, proof note, certificates | — | — | ½ day | — |
| 6 | Optional: Lean checker for the certificate (RQ-5) | hours (kernel) | 8–16 GB | 1–2 weeks of work | Kernel performance at 10⁶ nodes is unknown. Pilot on k ≈ 40 first. |

All steps 1–5 are in the "cheap" class (< 30 min CPU each). Nothing needs paid infrastructure.

## Extending the table (RQ-2): cost model from EXP-0002

The Python runtime grows by about ×1.37 per unit of k for k = 50…61 (fitted to the 3.7 s → 117 s range).
Search nodes grow similarly.

| k | est. Python time | est. nodes | Feasible here? |
|---|------------------|------------|----------------|
| 64 | ~5 min | ~2·10⁶ | yes (cheap) |
| 70 | ~30–40 min | ~1.5·10⁷ | yes ("medium", needs approval) |
| 80 | ~13 h | ~3·10⁸ | not in Python (RAM ~50+ GB); C++ maybe 1–2 h, 10–20 GB |
| 100 | months in Python | ~10¹¹ | needs a better algorithm or lower bounds |

These are extrapolations from 12 data points. The slack s_k varies with k, and the cost is very
sensitive to it. Treat them as order-of-magnitude estimates.

## More interesting open problems found along the way

1. **New data: ‖2^k − 1‖ for 40 ≤ k ≤ 61** appear to be unpublished (Iraids et al. stop at 39). A
   verified table, extended to k ≈ 80 with C++, is a concrete contribution. It's OEIS-worthy (a new sequence
   or b-file), and you'd approve any submission.
2. **Iraids' Observation 2:** ‖2^{2^j} − 1‖ = 2^{j+1} + j − 2 is known for j ≤ 5. **j = 6 (2^64 − 1) is
   one ~5-minute computation away** (predicted value 132). A clean, quotable test of a published
   pattern.
3. **Structure of A(k) = ‖2^k − 1‖ − 2k.** Known: A(k) ≤ ⌊log₂ k⌋ + H(k) − 3 (Iraids Cor. 2), and our
   data shows this is tight at k = 32, 33, 34. Is A(k) bounded, or does it grow like log k? Which k
   attain the bound? This is a conjecture-and-prove direction close to Rawsthorne's ‖2^k‖ = 2k problem, and
   our data for k ≤ 61 (soon more) is new evidence.
4. **A general tool:** a certificate-producing exact solver with an independent (eventually
   Lean) checker for ‖n‖ at n ~ 10¹⁸–10²⁵. Nothing like it exists, as far as we know. It turns
   computational claims in this field into verifiable ones.
