# EXP-0004 G. Agents, their conclusions, and how disagreements were resolved

## 1. Set-up and independence

Six agents took part, all instances of Claude (the same model family). That is the main limit on their independence.

| Agent | Brief | Saw the primary agent's conclusions? | Outcome |
|-------|-------|--------------------------------------|---------|
| Primary (Claude Code, this thread) | Run the audit, write a second checker, build the table-free certificate, write the deliverables | — | — |
| Mathematical proof auditor | Reconstruct the proof from the notes; find gaps and counterexamples | No | Finished |
| Implementation auditor | Line-by-line code review, reproduction, statistics, mutation tests | No | Finished |
| Adversarial reviewer | Assume the claim is wrong; craft accepted false certificates; attack the real one | No | Interrupted once by a usage limit, then resumed and finished. Its final report matches the summary drawn from its output files. |
| Lean formalization specialist | Inventory what is kernel-checked; design the route; build a proof of concept; benchmark | No, until it resumed after the usage limit. On resuming it was told one fact: that a table-free certificate exists, with its size. | Finished |
| Literature specialist | Primary sources, novelty | No | Finished |

The briefs named the files to read and told every agent **not** to read EXP-0004 files or other agents' reports. None of
them could write report files (the harness blocks that for subagents). They returned their reports as text, and the
primary agent wrote the deliverables from those texts. Every claim taken from them that carries weight was either
re-run by the primary agent (the strict checker, the float attack, the certificate checks, the Lean build and the axioms)
or is marked as the agent's own result.

## 2. Independent conclusions (one line each)

| Agent | Main conclusion |
|-------|-----------------|
| Primary | The mathematics is sound. `check_lower.py` has a float-factor soundness hole that the real certificate does not trigger. A table-free certificate removes the 10⁸ table from the trust base, and both checkers accept it. |
| Math auditor | The mathematics is correct. There are two checker holes: float primes (medium) and m = 1 (low). Lemma 2 is worded too loosely. The ≥ 117 result should be labelled `LITERATURE`. |
| Implementation auditor | No bug in the search or the C table. The checker has F1 (critical), F2 (major, header binding) and weak tests (nine real surviving mutants). The real certificate is clean. |
| Adversarial reviewer | Seven ways to make `check_lower.py` accept false statements (floats, T ≤ 0 with m = 1, bool m). Every mutation of the real certificate is rejected. No ≤ 126 expression was found; the table spot checks are clean. |
| Lean specialist | Selfridge, Theorem C and sequential checker soundness are now kernel-checked, along with ‖1023‖ = 22. The full proof is feasible: 1–3 CPU-days kernel-only, or minutes with `native_decide`. Divisor completeness and Lucas remain open. |
| Literature specialist | ≥ 117 is the best published lower bound, and 127 as an upper bound is not new. No published exact value exists for any k ≥ 40, and no formalization of integer complexity exists (**refuted later**, see D8). Do not claim priority. |

## 3. Agreements reached independently

- **The float-factor hole (F1)** was found **three times independently**: by the primary agent, the math auditor and the
  implementation auditor. The adversarial reviewer made a fourth, separate exploit. Each used a different m.
- **The m = 1 / T = 0 hole** was found by the math auditor and the adversarial reviewer.
- **The real certificate is clean.** The implementation auditor scanned the token types. The primary agent's strict checker
  and the implementation and adversarial agents' own strict checkers (three separate programs) all accept it.
- **The table-free certificate size** matches across agents: 2,906,430 claims (primary, T₀ = 1000) against 2.905M (Lean
  specialist, T = 1000) and 2.908M (T = 100).
- **Lemma 2 wording** (factors of 1): the math auditor and the implementation auditor (F8) raised it independently.

## 4. Disagreements and their resolution

| # | Disagreement | Resolution (by argument, not vote) |
|---|--------------|------------------------------------|
| D1 | **Severity of F1.** The math auditor said medium; the implementation auditor said critical. | Two different questions. *As a property of the checker*, it is **critical**: the checker's job is to reject every false certificate, and it accepts one even with the genuine table (A1). *For the claim ‖N‖ = 127*, the impact is **none**, because the real certificates contain only integer tokens (three parsers that reject floats accept them). Both labels are recorded with that scope. |
| D2 | **How many table entries are really needed.** The Lean specialist reported ≈ 60k entries needing more than max(1, λ(v)); the primary agent measured 192,882. | The primary agent read the specialist's script. When **both** parts of a split are ≤ T, it recorded "need 1" for both (an approximation), so it undercounts. The primary checker records, for each entry, the value needed given the other part's actual bound. **192,882 is the right count** under that definition. The question is moot for formalization, because the table-free certificate needs no table. |
| D3 | **Status of ‖N‖ ≥ 117.** `RESULTS.md` says "`PROVEN` (`LITERATURE`)"; the math auditor says it should be `LITERATURE`. | Under CLAUDE.md §4, `PROVEN` needs a checked proof in the repo *or a peer-reviewed source checked by us*. Our derivation from AZ2012 Thm 1.6 is checked, but Thm 1.6 itself (its §5–6 proof) has not been checked by us. **`LITERATURE` is the correct label**, with our derivation recorded as a checked consequence. Recommended for `RESULTS.md` R-0006 and R-0001 (follow-up, not applied here). It does not matter for ‖N‖ = 127, which does not use AZ2012. |
| D4 | **Which induction proves Theorem C and the certificate.** The spec says strong induction on m; the math auditor says induction on record order; the Lean proof uses structural induction on expressions plus the record order. | All three are valid, for different steps. Factors of 1 need induction on the expression (or its size), because the value does not drop. Using earlier claims needs the record order. Strong induction on m alone does not handle the factor-1 case without the extra remark. **Adopt the Lean structure**: it is machine-checked. |
| D5 | **Lucas/Pratt: easy or hard to formalize?** The math auditor called it textbook; the Lean specialist estimated 3–5 days in core Lean. | Not a real disagreement. The mathematics is elementary, but core Lean lacks the group theory (orders of units). The estimate stands, and Mathlib would shorten it. This is a decision for the lead. |
| D6 | **Is the C table independent of our Python table?** EXP-0003 presents our table and He's as independent; the implementation auditor notes that our Python and C tables share an algorithm. | Both statements are true. The independent cross-check at 10⁸ is against **He's** table, not our Python one. This audit did not rebuild He's table. It is moot for the table-free certificate. |
| D7 | **Is oeis.org reachable?** Project memory says it is blocked; the literature specialist reached it. | It depends on the container or network policy. Record both. |
| D8 | **Prior formalization (external audit vs literature specialist).** The specialist reported "no formalization of integer complexity in Lean, Coq or Isabelle". An external audit forwarded by the lead pointed to `BrettKnox/open-problems-lab`. | **Resolved against the specialist, by inspecting the source** (primary agent, 2026-11-25 evening). The repository's `IntegerComplexity.lean` (commit `e899b51`, 2026-08-20) formalizes ‖n‖, Selfridge's bound and several exact values. The claim is retracted. The narrower statement, that we found no formalization of Theorem C or of a certificate checker, is kept only as "not found", pending a new search. See [literature §6](literature-and-novelty.md#6-correction-after-the-external-audit-2026-11-25-evening). |

## 5. Points on which no agent could decide

- Whether a human reviewer will accept the checker code. Nobody outside the Claude model family has read it.
- The real kernel cost at k = 61. It is an extrapolation from k ≤ 26.

## 6. Second round: independent adversarial review (2026-11-25, night)

The lead asked for independent mathematical, programming, Lean and security reviewers, briefed to search actively for
errors and not to confirm the primary agent. Four new agents (again all Claude) ran in parallel, plus the Lean builder
whose work they partly reviewed. Each got the files to read and an explicit adversarial brief; none got the primary agent's
conclusions as facts. They could not write into the repository; the primary agent recorded their reports and re-ran the
findings that carry weight.

| Agent | Main conclusion |
|-------|-----------------|
| Math reviewer | No error that threatens ‖N‖ > 126. Checked by brute force for n ≤ 10⁴: λ ≤ ‖n‖, ‖n‖ ≤ 3·bitlen − 2, Fact S, divisor enumeration, and that v2 with the trivial table accepts every G(n, ‖n‖ − 1) and rejects every G(n, ‖n‖). Spec Lemma 2 is false as worded; some `PROVEN` labels in this audit are inflated. |
| Programming/security reviewer | Could not make either checker accept a false certificate (≈ 30 input attacks, ≈ 6,000 random certificates, 262,944 composite Pratt records). Three unsound mutants survived v2's tests; two short inputs cause minutes of CPU or MemoryError; table values are never checked. |
| Lean reviewer | The headline Lean statement is exactly "every expression for 2^61 − 1 has ≥ 127 ones" and is not vacuous (it proved ¬LowerBound N 128). Only gap: the lower bound rests on `native_decide`; Mathlib oleans come from the binary cache unchecked; the definitions are a copy. |
| Lean builder | Soundness of the checker, divisor completeness (M2) and Pratt via Mathlib `lucas_primality` (M3) are kernel-checked; k = 20, 24 kernel-only; k = 61 by `native_decide` (≈ 100 s). Kernel-only k = 30 exceeds 8 GB as one declaration. |
| Literature reviewer | Knox is not the earliest: google-deepmind/formal-conjectures defined ‖n‖ in Lean on 2025-06-30, with the split lemma; facebookresearch/atlas-lean has Selfridge-type bounds and the recursion (2026-10/11). No formal Theorem C, no verified certificate checker, no formal ‖2^61 − 1‖ found. |

### Disagreements, second round

| # | Disagreement | Resolution |
|---|--------------|------------|
| D9 | **Lemma 2 gap: where is it?** The first math auditor (M3, D4) said `proof-exact-search.md` needs an induction on expression structure for factors of 1. The second math reviewer says that note states Lemma 2 for an *optimal* expression and handles factors of 1 correctly; the literally false sentence is in the *spec* §2 ("every expression for m is a sum or a product d·e with 2 ≤ d"), which the first audit did not flag. | **Second reviewer is right on the location**, checked by the primary agent by reading both texts. The spec sentence is corrected (strike-through) on PR #6. Both agree the result is unaffected: the shortest-expression argument suffices. D4 stands as a statement about proof structure. |
| D10 | **Status labels.** This audit's mathematical-audit table labels Fact S, divisor completeness and Lucas `PROVEN` on agents' own checks. The second math reviewer says that is inflated under CLAUDE.md §4. | **Reviewer is right.** Lucas and divisor completeness: `LITERATURE` (textbook) **and** now kernel-checked in Lean (`prattOK_sound`, `mem_divisorsOf`, axioms propext, Classical.choice, Quot.sound): `FORMALLY VERIFIED` for the Lean statements. Fact S and Theorem C: `FORMALLY VERIFIED` (core-Lean `theoremC`, `sumsFrom_sound`); the written proofs stay unlabelled `PROVEN` until RP-0002. The original table is left as written for the trail. |
| D11 | **"Version 2 is sound."** The primary agent's EXP-0005 conclusion said v2 rejects every known false certificate; the programming reviewer disagrees with any blanket soundness claim: unsound mutants survive the tests, and the verdict trusts the table. | **Both partly right.** No false certificate was found (agreement). The tests were weaker than claimed: three mutants survived. Fixed on PR #6 (four mutants added and killed, battery extended). The table is a trusted input by design; v2 now adds necessary sanity checks only, and the spec says the expected SHA must come from an independent source. "Sound" is stated only relative to the trust base. |
| D12 | **"The guard rules avoid very long loops."** Claimed in the EXP-0005 README; refuted by the programming reviewer (divisor blow-up, factor-product blow-up). | **Refuted.** New reject-only resource guards on PR #6; the reviewer's own inputs are now rejected in < 0.1 s. The README wording is corrected. |
| D13 | **T ≥ 1 rationale.** The spec says T ≥ 1 is there so the table holds ‖1‖; the math reviewer says LB ≥ 1 already, and what the table-free certificate really trusts is c[1] ≤ 1. | **Reviewer is right**; the spec now says so. |
| D14 | **Prior art (literature specialist and §6 vs literature reviewer).** §6 called Knox's repository the prior formalization. | **Resolved against §6**, by the primary agent reading formal-conjectures at `798eb17d` (2025-06-30) and atlas-lean at HEAD. See [literature §7](literature-and-novelty.md#7-second-correction-independent-literature-re-search-2026-11-25-night). The first specialist's claim to have checked formal-conjectures was wrong. |
| D15 | **Trust label for the Lean M61 run.** The builder suggests "checked in Lean via native_decide"; the Lean reviewer "FORMALLY VERIFIED modulo native_decide". | Both mean the same. We use **"checked in Lean via `native_decide`"**, and do *not* use the label `FORMALLY VERIFIED` for ‖N‖ > 126, because the lead's trust model is the kernel plus the three standard axioms. R-0007 is unchanged. |
| D16 | **Values in the Lean builder's brief.** The brief (written by the primary agent) gave ‖2^24 − 1‖ = 49, ‖2^30 − 1‖ = 59, ‖2^40 − 1‖ = 83; the builder's runs give 50, 63, 82. | **The brief was wrong**, a primary-agent error from memory. ‖2^24 − 1‖ ≥ 50 is kernel-checked (`k24_lb`), which rules out 49. The repository's EXP-0002 table is the reference; the brief values were never written into the repository. |

### Points still open after round two
- The strict checker (`tools/check_lower_strict.py`) has no j/e guards and lets RecursionError, MemoryError and some gzip
  errors escape as tracebacks (exit 1, so never a false ACCEPT). It allows duplicate keys and extra fields. It is an audit
  tool and is left as it was; "both checkers accept" is an independence argument about the arithmetic, not about the format.
- No reviewer outside the Claude model family has read any of this.
- Mathlib oleans were taken from the binary cache; nobody has run lean4checker on the final environment.
