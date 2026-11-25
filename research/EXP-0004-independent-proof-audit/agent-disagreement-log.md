# EXP-0004 G. Agents, their conclusions, and how disagreements were resolved

## 1. Set-up and independence

Six agents took part, all instances of Claude (the same model family). That is the main limit on their independence.

| Agent | Brief | Saw the primary agent's conclusions? | Outcome |
|-------|-------|--------------------------------------|---------|
| Primary (Claude Code, this thread) | Run the audit, write a second checker, build the table-free certificate, write the deliverables | — | — |
| Mathematical proof auditor | Reconstruct the proof from the notes; find gaps and counterexamples | No | Finished |
| Implementation auditor | Line-by-line code review, reproduction, statistics, mutation tests | No | Finished |
| Adversarial reviewer | Assume the claim is wrong; craft accepted false certificates; attack the real one | No | Interrupted once by a usage limit, then resumed. Its own report text is summarized from its output files and partial results. |
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
| Literature specialist | ≥ 117 is the best published lower bound, and 127 as an upper bound is not new. No published exact value exists for any k ≥ 40, and no formalization of integer complexity exists. Do not claim priority. |

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

## 5. Points on which no agent could decide

- Whether a human reviewer will accept the checker code. Nobody outside the Claude model family has read it.
- The real kernel cost at k = 61. It is an extrapolation from k ≤ 26.
