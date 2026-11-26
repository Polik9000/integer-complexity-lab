# Failed and abandoned approaches

Kept so nobody repeats them blindly. Newest at the bottom. Each entry gives the date, the approach,
what happened, why we think it failed, and what might still be worth trying.

## 2026-11-25: narrow peel searches stall at 127–129 (EXP-0001)

- **Approach:** n = d·m + r with small d (≤ 12…400) and small r (≤ 1…8), with an exact table to 4·10⁸.
- **Outcome:** best 127 (d ≤ 100, r ≤ 1). Wider r with small d was *worse* (129 with r ≤ 6, d ≤ 12),
  because the memo budget goes into useless branches.
- **Why:** this family only explores "multiply by small factor, add small r" chains, and the
  board's 127 lives in the same family.
- **Still worth trying (bounded):** use all divisors of n − r (factorize), allow two-term sums
  a·b + c·d with medium-size parts, and raise T to 4·10⁹.

## 2026-11-25: environment notes (not mathematical)

- `release.lean-lang.org` and `oeis.org` are blocked by the cloud sandbox's network policy.
  Lean was installed from the GitHub release zip instead, and the OEIS b-files are unavailable there.

## 2026-11-25: EXP-0004 audit (Claude Code and subagents)

- **Cheap upper-bound heuristic for 2^61 − 1 (adversarial reviewer):** a memoized peel search n = d·m + r with its own
  parameters (C = 2, D = 50 and C = 6, D = 300) found 129 ones at best, nothing ≤ 127. Weak evidence only.
- **Lean, data as list literals:** lists of more than about 1,000 items need `set_option maxRecDepth`. Without it, the `def`
  silently becomes noncomputable, and `native_decide` then fails. Plain `Nat.pow` for a^(p−1) mod p is far too slow in the
  kernel; use a binary `powMod` by structural recursion on fuel.
- **Lean, small table computed in the kernel:** not worth it. A table up to 10⁴ saves only ≈ 1% of the claims of a
  table-free certificate (2.87M vs 2.908M).
- **Float-factor exploit, first tries:** semiprimes within ±1…±3 of 2·3^33 did not exist in a small prime range. The working
  construction needed m = 2^a·3^k with a larger float spacing (see `tools/float_factor_attack.py`).
- **Novelty search for formalizations (EXP-0004 literature review):** it searched Mathlib, Sequencelib, formal-conjectures
  and the web, but **missed** a public GitHub Lean repository (BrettKnox/open-problems-lab, 2026-08-20) that formalizes
  integer complexity. An external audit found it. Rule from now on: a formalization novelty search includes a GitHub code
  search for the notion's name and its Lean identifiers, and a check of the "formal conjectures" style monorepos.
- **Novelty search, second miss (EXP-0004 follow-up):** the corrected §6 named Knox's 2026 repository as "the" prior
  formalization. An independent re-search found google-deepmind/formal-conjectures (`Mathoverflow/75792.lean`, 2025-06-30),
  which the first specialist had claimed to check, and facebookresearch/atlas-lean (2026). Rule tightened: search large Lean
  corpora by **file content** (GitHub code search `"integer complexity" language:Lean`, and the defining identifiers), record
  queries and hit counts, and have a second, independent agent repeat the search before any "not found" is written.
- **Checker v2 tests, first version (EXP-0005):** 72 tests and 14 mutants looked complete, but an independent reviewer found
  three unsound one-line mutants that survived (unverified claim factors, LB + 2, small q without trial division) and two
  short DoS inputs. Lesson: mutation lists written by the author of the code miss the author's blind spots; get an
  independent reviewer to propose mutants.
- **Lean, kernel-only full certificate as one declaration:** k = 30 (6,542 records) already used 11.8 GB and was killed.
  A kernel-only proof needs the run split into checkpointed declarations.
