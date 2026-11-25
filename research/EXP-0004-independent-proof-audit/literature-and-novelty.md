# EXP-0004 F. Literature and novelty

Written 2026-11-25 by Claude Code, from the independent **literature specialist**'s report. The specialist worked from
primary sources: arXiv PDFs downloaded and converted to text, journal pages, a clone of He's repository, the M61 board with
its PR refs, and OEIS. It did not see the primary agent's conclusions. Legend: ✅ read at the cited location; ◐ partial
or metadata only; ○ not read. A recalled fact that nobody checked is `UNVERIFIED`.

## 1. Summary

- **Lower bounds from the literature:** the best is ‖N‖ ≥ 117 (Altman–Zelinsky 2012, Thm 1.6). The stronger Thm 5.1 of
  the same paper, read verbatim this time (13 families with δ < 12δ(2) ≈ 1.2865), also excludes N, but it still gives only 117,
  because 115.46 + 1.287 = 116.75. Getting 118 would need a classification up to δ ≈ 1.54. Altman's later papers give nothing
  more for N.
- **Upper bound 127: not new.** It has been public since board PR #4 (2026-10-02). It also follows from Iraids et al. 2012:
  Thm 8 (Thm 6 in the arXiv version) with their Table 3 and Hypothesis 13 gives 2^61 − 1 = 2·(2^30 − 1)·(2^30 + 1) + 1,
  which costs 2 + 63 + 61 + 1 = 127 ones. Their closed-form Cor. 2 and Cor. 3 give 129 and 130.
- **Exact value 127:** not found in any published or public source.
- **Exact ‖2^k − 1‖ for k ≥ 40:** not found. Iraids' Table 3 stops at k = 39, because 2^40 − 1 is past their 10¹² range.
- **Formalization (corrected 2026-11-25, see §6):** ~~no formalization of integer complexity was found in Lean, Coq or Isabelle.~~
  **Wrong.** An external audit pointed to a prior public Lean 4 + Mathlib formalization, `BrettKnox/open-problems-lab`
  (`OpenProblemsLab/IntegerComplexity.lean`, first commit 2026-08-20), which proves Selfridge's bound, ‖3^k‖ = 3k and
  ‖2^n‖ = 2n for n ≤ 9. Our literature specialist missed it. The Lean OEIS library Sequencelib (about 25.5k sequences)
  does not contain A005245; that part stands.

## 2. Per-source findings

| # | Source | Location | Finding | Status |
|---|--------|----------|---------|--------|
| 1 | H. Altman, J. Zelinsky, *Integers* 12(6) (2012) 1093–1125; arXiv:1207.4841v1 | Def 1.4; Thm 1.6 (pp. 3–4); Thm 5.1 (§5.1, p. 14); Thm 1.7 | Thm 1.6 gives 7 families with δ < 1 and says n = 1 is the only number with δ = 1. Thm 5.1 gives 13 families with δ < 12δ(2). N is odd, 3 ∤ N, and 5 \| N − 1, so N is in no family of either theorem, and ‖N‖ ≥ 117. Thm 1.7: ‖2^a 3^k‖ = 2a + 3k for a ≤ 21. | ✅ |
| 2 | H. Altman, "Integer complexity: the integer defect", *Moscow J. Combin. Number Theory* 8 (2019) 193–217, doi:10.2140/moscow.2019.8.193; arXiv:1804.07446v4 | Defs 1.2–1.3, Thms 1.8, 1.12 | D(n) = ‖n‖ − L(n), with L(N) = 115. The D ≤ 1 classification gives at most ‖N‖ ≥ 117. Nothing on 2^k − 1. | ◐ |
| 3 | H. Altman, *Theoret. Comput. Sci.* 652 (2016) 64–85; arXiv:1603.06122 | abstract, §1 | A truncation method that represents the low-defect sets exactly. No numerical values. | ◐ |
| 4 | H. Altman, "Integer complexity: algorithms and computational results", *Integers* 18 (2018) A45; arXiv:1606.03635v2 | Thm 1.6; §2.1; App. A | Thm 1.6: ‖2^k 3^ℓ‖ = 2k + 3ℓ for k ≤ 48. §2.1 describes a lower-bound certifier for a known upper bound U: an **independent method** we could use. It was never run on N, and it would need defect ≈ 10.54 there; his largest published run (2^48) needed ≈ 4.15. His Haskell implementation is said to be available, with no location given. | ✅ |
| 5 | J. Iraids et al., *Sci. Papers Univ. Latvia* 787 (2012) 153–179; arXiv:1203.6462v1 | Thm 8 (journal) = Thm 6 (arXiv); Cor. 2–3; Table 3; Hyp. 1, 13 | ‖n‖ was computed for all n ≤ 10¹². ‖2^a‖ = 2a for a ≤ 39. Table 3 gives A(n) = ‖2^n − 1‖ − 2n for n ≤ 39. | ✅ |
| 6 | Čerņenoks et al., arXiv:1409.0446v1 (2014) | full text searched | Links ‖2^n‖ = 2n to the ternary digits of 2^n. Computes complexity with subtraction allowed, up to 2·10¹¹. No table of 2^n − 1. | ✅ |
| 7 | Q. He, SOSA 2024; arXiv:2308.10301v2 | §3; App. A.1–A.3 | Searches 2^i ≤ 2^126, 2^i 3^j 5^k ≤ 10³⁶ and 2^i + 1 ≤ 2^121 + 1. No 2^i − 1 values; 2^61 − 1 is not mentioned. | ✅ |
| 8 | GitHub `hqztrue/integer_complexity` @ `742e8c5` | README; grep of the whole tree | No 2^i − 1, Mersenne or M61 code or output. The README cites a 2026 paper, "Integer Complexity: Algorithms Meet Horner's Rule", with an empty arXiv link; it was not found. | ✅ (paper `UNVERIFIED`) |
| 9 | J. Zelinsky, arXiv:2211.02995v1 | abstract | ‖n‖ ≤ (41/ln 55296)·ln n ≈ 3.7544 ln n ≈ 4.1247 log₃ n. | ✅ |
| 10 | S. Konyagin, K. Oganesyan, arXiv:2603.20876v2 | eq. (2), Thms 1–2, Cor. 1 | C_avg = 69451528190836 / (2^15·3^14·5·ln(2^15·3^14·5)) ≈ 3.23606 (recomputed). Nothing on 2^k − 1. | ✅ |
| 11 | J. Arias de Reyna, *Gaceta RSME* 3 (2000); English version arXiv:2111.03345 | pp. 15–16 | ‖2^27 − 1‖ ≤ 56; "I have not found an n > 2 such that ‖2^n − 1‖ < 2n − 1". | ✅ (that passage) |
| 12 | S. Steinerberger, *Contrib. Discrete Math.* 9(1) (2014) | p. 2 | The 3 log₂ n bound is attained only by 2^k − 1. No values. | ✅ (that passage) |
| 13 | C. Shriver, arXiv:1511.07842v2 | abstract | 3.52 log₃ n holds on a set of logarithmic density one. | ✅ (abstract) |
| 14 | Cordwell et al. arXiv:1706.08424; Arias de Reyna–van de Lune arXiv:1404.2183; Altman–Arias de Reyna arXiv:2111.00671; Amano, ISAAC 2022 | abstracts | All-n algorithms; nothing on 2^k − 1. | ◐ |
| 15 | Guy (1986); Rawsthorne (1989) | — | Not retrieved. Any claim that they treat 2^n − 1 is `UNVERIFIED`. | ○ |
| 16 | OEIS A005245, revision #234 (2026-10-27) | entry; the 61 sequences that cite it | oeis.org **was reachable** from this container. No sequence for ‖2^n − 1‖ (two value searches, one keyword search). The entry credits M. N. Fuller (2008) with the counterexample 353942783 and cites V. Wang, *J. Number Theory* 133(2) (2013) 391–397. | ✅ |
| 17 | Board `math-market/integer-complexity-m61` @ `394bec0` | README, TASK | Task: fewer than 150 ones; the "floor" 116 is ⌈3 log₃ N⌉. | ✅ |
| 18 | Board PR #4 (commits `0995202`, 2026-10-02, and `6b79a63`) | PR page; diff | Still open, with no reviews. Our own non-`eval` parser confirms 127 ones. A maintainer comment on 2026-11-01 says CI is green and the task will be reposted as "beat 127". No method is given and no optimality is claimed. | ✅ |
| 19 | Sequencelib (arXiv:2601.11757; `provables/sequencelib` @ `dfb06c18`) | grep of the whole tree | No A005245. | ✅ |
| 20 | Mathlib `LucasLehmer.lean`; `Archive/Examples/MersennePrimes.lean` | docstrings | A kernel-reducible Lucas–Lehmer test; Mersenne primes are certified through M4423. So "2^61 − 1 is prime" is already available in Lean/Mathlib. | ✅ |
| 21 | PrimeCert (Lean, Pocklington); Isabelle AFP `Pratt_Certificate`; Rocq `coq-addition-chains`; Subercaseaux et al., ITP 2024 (arXiv:2403.17370); Clift, *Computing* 91(3) (2011) 265–284 | entry pages, abstracts | Methodological analogues for certified lower bounds of a finite minimization. None is about integer complexity. | ◐ |

## 3. Novelty assessment

| Category | Item |
|----------|------|
| **Previously known** | ‖N‖ ≤ 127 (board PR #4; implicit in Iraids 2012). ‖N‖ ≥ 117 as a consequence of Altman–Zelinsky (not written down for N by them). The method: exhaustive split search with Selfridge pruning (He 2024, Iraids 2012, Altman 2018). |
| **Our independent reproduction** | Iraids Table 3 (k ≤ 39) with two programs; running He's code is a replication, not an independent result. |
| **New computational result** (modest) | Exact ‖2^k − 1‖ for 40 ≤ k ≤ 61, in particular ‖N‖ = 127. Published algorithms make it computable, and a private computation by someone else cannot be ruled out. |
| **New certified result** | A published, checkable lower-bound certificate for ‖N‖ > 126, now including a table-free version. |
| **New formalized result** (prospective, corrected) | ~~No formalization of integer complexity was found at all, so we found no earlier kernel-checked exact value than our ‖1023‖ = 22 PoC.~~ **Corrected:** integer complexity, Selfridge's bound and several exact values (‖3^k‖ = 3k, ‖2^n‖ = 2n for n ≤ 9, ‖6‖ = 5) were formalized before us (§6). What we found no earlier formalization of: Theorem C, a verified sequential lower-bound certificate checker, an exact value that needs more than Selfridge's bound (such as ‖1023‖ = 22, where λ = 19), and any statement about ‖2^61 − 1‖. This is a statement about what we found, not a priority claim. |
| **New mathematical result** | None. There is no human-readable proof and no general theorem. |

**Do not claim priority.** The searches are listed below. "Not found" is not "does not exist". The problem.market site
itself was not searched, and a "beat 127" repost may exist there.

## 4. Search log (specialist)

- **arXiv PDFs.** 18 papers downloaded and converted to text: 1207.4841, 1203.6462, 1409.0446, 2308.10301, 1804.07446,
  1603.06122, 1606.03635, 2211.02995, 2603.20876, 2111.03345, 1404.1850, 1404.2183, 1706.08424, 1511.07842, 1310.2894,
  2111.00671, 2610.10095, 2211.04379. Also the journal version of Iraids (bjmc 787_9), Steinerberger, Arias de Reyna 2000 and
  Amano. All were grepped for "Mersenne", "2n − 1" and "2k − 1".
- **arXiv API.** Abstract search for "integer complexity" (100 newest): no paper on 2^k − 1. Author search for He: no Horner paper.
- **Web searches.** "2305843009213693951" with integer complexity: only the board and a fork. "2^61-1" with "127 ones": only
  PR #4. Searches for Mersenne numbers, Iraids, "beat 127", and Lean/Isabelle/Coq integer complexity found nothing new.
- **OEIS.** Two value searches, a keyword search, and the list of sequences citing A005245.
- **Access limits.** `gh api` is blocked for third-party repositories, but `git clone` over https works. WebFetch was
  rate-limited twice on PR #4. JSTOR was not tried; the Rawsthorne PDF download failed.

## 5. Corrections for `BIBLIOGRAPHY.md` (to apply in a follow-up; not applied on this branch)

1. Wang2012: the author is **Venecia Wang**, *J. Number Theory* 133(2) (2013) 391–397, doi:10.1016/j.jnt.2012.08.003 (◐, via OEIS). OEIS credits M. N. Fuller (2008) with finding 353942783.
2. Altman2019a and Altman2019 are the same paper (arXiv:1804.07446v4). Merge them.
3. AltmanZelinsky2012: add pp. 1093–1125. Thm 5.1 has now been read verbatim; update `research/lit-AltmanZelinsky2012.md`, which says "only in summary".
4. Altman2016TCS: add arXiv:1603.06122.
5. Altman2018: add the §2.1 certifier as a possible independent route (defect ≈ 10.54 needed for N).
6. Iraids2012: arXiv Thm 6 = journal Thm 8. Thm 8 already gives ‖N‖ ≤ 127; Cor. 2 gives 129 and Cor. 3 gives 130.
7. Iraids2014: now read; no 2^n − 1 table.
8. KonyaginOganesyan2026: the C_avg closed form is confirmed.
9. Zelinsky2022: 41/ln 55296 ≈ 3.7544 (natural log) ≈ 4.1247 in log₃.
10. Shriver2015: 3.52 holds on a set of logarithmic density one; 3.5286 belongs to a different algorithm.
11. OEIS-A005245: reachable from this container; the "not reachable" note depends on the container.
12. He2024: record the unlinked 2026 Horner paper as `UNVERIFIED`.
13. Board-M61-PR4: PR page now read. Do not record the submitter's name or e-mail from the commit metadata (CLAUDE.md rule 9).

## 6. Correction after the external audit (2026-11-25, evening)

The lead forwarded an external audit that found a prior public Lean formalization. The primary agent then inspected it
directly: it cloned the repository (HEAD `04ef51fe64bbdd85a40c7105cf0ea46a3bee80af`, Apache-2.0) and read the Lean source,
not only the README. It did **not** build that project. A rebuild would need its own toolchain, `v4.34.0-rc1`, and its
Mathlib pin `d77ef07`.

**Source.** B. Knox (GitHub `BrettKnox`), *open-problems-lab*, file `OpenProblemsLab/IntegerComplexity.lean` (484 lines,
Lean 4 + Mathlib). The repository's first commit `cf02856` is dated 2026-08-19 and adds the problem statements. The
formalization itself is commit `e899b51` of 2026-08-20, "Formalize integer complexity; prove Selfridge bound and
conjecture for n <= 9". Status: ✅ (source read; not built by us).

**What it formalizes** (theorem names from the source; its header says no `sorry`, axioms `propext`,
`Classical.choice`, `Quot.sound`; our grep found no `sorry`, `axiom` or `native_decide`):

| Item | Their Lean | Ours (EXP-0004) | Prior? |
|------|------------|-----------------|--------|
| Expressions over 1, +, ×; value and size | `OnesExpr`, `eval`, `size` | `Expr`, `eval`, `ones` (since 2026-11-25, `Basic.lean`) | **yes, theirs is earlier** |
| ‖n‖ as a function | `complexity n := sInf (sizes n)` (noncomputable) | only the predicates `UpperBound` / `LowerBound` / `HasComplexity` | **yes, theirs is earlier** |
| Selfridge's bound n³ ≤ 3^‖n‖ (and 3 log₃ n ≤ ‖n‖) | `cube_eval_le_three_pow_size`, `cube_le_three_pow_complexity`, `three_logb_le_complexity` | `Expr.selfridge` | **yes, theirs is earlier**; ours is an independent re-proof in core Lean |
| Exact values | ‖1‖, ‖2‖, ‖3‖, ‖6‖ = 5, ‖3^k‖ = 3k, ‖2^n‖ = 2n for n ≤ 9. Every one follows from Selfridge's bound plus an expression; none needs a split search. | ‖1023‖ = 22 by a kernel-checked certificate (λ(1023) = 19, so Selfridge alone gives only ≥ 19) | exact values: **yes, theirs are earlier**. Exact values that need more than Selfridge: none found in theirs. |
| Sub-additivity API, defect δ(n), stability | `complexity_add_le`, `complexity_mul_le`, `defect`, `IsStable`, `conjecture_iff_defect` | not formalized | theirs only |
| Theorem C (soundness of the split rules) | not present | `theoremC` | none found |
| Sequential lower-bound certificate checker with a soundness proof | not present. Their header says a computational route was "measured and rejected" for 2^n with n ≥ 10. | `checkAll_sound`, `lowerBound_of_checkT` | none found |
| ‖2^61 − 1‖ (any bound) | not present | upper bound 127 kernel-checked; lower bound not formally verified | none found |

**Consequences for our claims:**
1. "No formalization of integer complexity exists" is **retracted** wherever it appeared: this file (§1, §3), the EXP-0004
   README, `RESEARCH_LOG.md` and the PR #5 description. The original wording is kept with strike-through for the audit trail.
2. Our Selfridge proof is a **re-formalization**, not a first.
3. We can say only: *we found no earlier formalization* of Theorem C, of a verified certificate checker, or of an exact value
   that needs more than Selfridge's bound. This needs a new search before anyone relies on it (EXP-0004 follow-up literature review).
4. **Process failure:** the literature specialist searched "Lean / Isabelle / Coq integer complexity" and checked Mathlib,
   Sequencelib and formal-conjectures, but missed a GitHub repository whose README names integer complexity. Lesson,
   recorded in `research/failed-approaches.md`: novelty searches for formalizations must include a GitHub code search for
   the defining notion (e.g. `"integer complexity" language:Lean`), not only libraries and web search.
