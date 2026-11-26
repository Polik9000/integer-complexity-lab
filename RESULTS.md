# RESULTS

Current state of knowledge. Every row has an evidence status as defined in
[`CLAUDE.md` §4](CLAUDE.md#4-evidence-statuses). Superseded rows are moved to the
"History" section, never deleted.

Last updated: 2026-11-25 (fifth update: EXP-0004 proof audit, on branch `research/exp-0004-proof-audit`).

## R-0001 … benchmark N = 2^61 − 1 = 2305843009213693951

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0001 | ‖N‖ ≥ 116 | `PROVEN` (`LITERATURE`) | ‖n‖ ≥ 3 log₃ n for all n (Selfridge; see Guy 1986; Iraids et al. 2012, Thm 1). 3 log₃ N = 115.460…, and ‖N‖ is an integer. Not yet formalized. |
| R-0002 | ‖N‖ ≤ 150 | `COMPUTATIONALLY VERIFIED` | Board baseline expression, [`certificates/m61/M61-UB150-BOARD-BASELINE.json`](certificates/m61/M61-UB150-BOARD-BASELINE.json). |
| R-0003 | ‖N‖ ≤ 127 | `COMPUTATIONALLY VERIFIED` + `FORMALLY VERIFIED` | Two independent 127-ones expressions: [third-party board submission](certificates/m61/M61-UB127-BOARD-PR4.json) and [our own search](certificates/m61/M61-UB127-ICL-PEEL.json) ([EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/)). Both are kernel-checked in [`lean/IntegerComplexity/Certificates/M61.lean`](lean/IntegerComplexity/Certificates/M61.lean); `#print axioms` reports no axioms. |
| R-0004 | ‖N‖ = ? | superseded by R-0007 (see History) | |
| R-0006 | ‖N‖ ≥ 117 | `PROVEN` (relative to `LITERATURE`: Altman–Zelinsky 2012, Thm 1.6) | N isn't one of the 7 families with defect < 1, so ‖N‖ > 3 log₃ N + 1 = 116.46. Proof: [`research/lit-AltmanZelinsky2012.md`](research/lit-AltmanZelinsky2012.md). Thm 1.6 itself was cross-checked against our exact table for n ≤ 4·10⁸ (exactly the 420 predicted numbers). |
| R-0007 | **‖N‖ = 127** (so the 127-ones expressions are optimal) | `COMPUTATIONALLY VERIFIED`: two independent implementations **and** an independently checked lower-bound certificate. **Not `PROVEN`**: the checker, spec and proofs have not been externally reviewed (RP-0002), and the Lean check of the lower bound uses `native_decide` (R-0010), not the kernel alone. | (1) Our exhaustive budgeted search. Its correctness rests on a conditional theorem with a written proof that has been self-checked but not independently reviewed ([`research/proof-exact-search.md`](research/proof-exact-search.md)): [EXP-0002](experiments/EXP-0002-exact-mersenne-pilot/), 117 s. (2) Q. He's independent C++ solver (no shared code or data): [EXP-0003](experiments/EXP-0003-independent-verification/), 2.6 s. It gives the same values with its defect-based pruning switched off (Selfridge bound only), 3.6 s. Both use the same mathematical method (exhaustive split search with Selfridge pruning). (3) A lower-bound certificate for ‖N‖ > 126 (1.12M records, 13 MB gzip) is accepted by a separate checker ([`certificates/lower/check_lower.py`](certificates/lower/check_lower.py), [spec](research/2026-11-25-certificate-architecture.md)). The checker does not trust the search; it trusts only Lemmas 1–2, Theorem C, its own ~170 lines, and the table for n ≤ 10⁸, which is byte-identical between our implementation and He's ([EXP-0003](experiments/EXP-0003-independent-verification/) step 2). Quote it as "computationally verified, with a checkable certificate", not as a proof. (4) **EXP-0004 audit:** five independent agents found no error in the mathematics or the real certificate. A **table-free** certificate (only ‖1‖ = 1 assumed; 3.07M records) is accepted by `check_lower.py` and by a second, strict checker, so the 10⁸ table is no longer in the trust base. Selfridge's bound and Theorem C are now kernel-checked (R-0008). `check_lower.py` itself has an input-validation hole (float factor primes, F1) that the real certificates do not trigger. [EXP-0004](research/EXP-0004-independent-proof-audit/). Status unchanged. (5) **EXP-0004 follow-up:** the table-free certificate was regenerated from committed files (body byte-identical) and is accepted by the hardened checker (PR #6) and the strict checker; with the root raised to > 127 both reject it. A Lean checker with a kernel-checked soundness proof accepts it via `native_decide` (R-0009, R-0010). Four further independent reviewers found no error. **Status unchanged** (`COMPUTATIONALLY VERIFIED`). |
| R-0005 | A simple "peel" search (n = d·m + r, d ≤ 100, r ≤ 1, exact table to 4·10⁸) reaches 127 in ≈5 s; the variants tried (r ≤ 8, d ≤ 400) found nothing below 127. | `OBSERVATION` | [EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/). Says nothing about whether < 127 exists. |
| R-0008 | The lemmas behind the lower-bound checker: Selfridge (e.eval³ ≤ 3^e.ones), the sum cut-off, Theorem C, and soundness of an ordered Bool claim checker (divisors by trial division); also ‖1023‖ = 22 end to end | `FORMALLY VERIFIED` (proof of concept, core Lean, no `sorry`, axioms ⊆ [propext, Quot.sound]) | `lean/IntegerComplexity/PoC/`, [EXP-0004 Lean roadmap](research/EXP-0004-independent-proof-audit/lean-formalization-roadmap.md). Not yet formalized: divisors from a factorization, Pratt, the run on 2^61 − 1 (now done in `lean-cert/`, see R-0009, R-0010). |
| R-0009 | Soundness of the factorization-based certificate checker in `lean-cert/` (`checkCert_sound`: acceptance implies `LowerBound N B`, for all N, B and data), divisor completeness from a verified factorization (`mem_divisorsOf`), Pratt/Lucas soundness via Mathlib `lucas_primality` (`prattOK_sound`); and ‖2^20 − 1‖ > 41, ‖2^24 − 1‖ > 49 from real table-free certificates | `FORMALLY VERIFIED` (Lean 4.35 + Mathlib v4.35.0, `decide +kernel`, no `sorry`, axioms [propext, Classical.choice, Quot.sound]) | `lean-cert/` (`ICLCert/Sound.lean`, `ICLCert/Test/Kernel20.lean`, `Kernel24.lean`), [EXP-0004 README §7](research/EXP-0004-independent-proof-audit/README.md). Mathlib oleans from the binary cache, not re-checked with lean4checker. |
| R-0010 | ‖2^61 − 1‖ > 126 (`LowerBound (2^61 - 1) 127`), with the table-free certificate as data | `COMPUTATIONALLY VERIFIED` (**checked in Lean via `native_decide`**). **Not** `FORMALLY VERIFIED`: `native_decide` adds the axiom `ICLCert.M61.check_native._native.native_decide.ax_1_1` and trusts the Lean compiler, interpreter, C compiler and runtime. A kernel-only check is not done (memory: one declaration does not fit in 8 GB already at k = 30). | `lean-cert/ICLCert/M61/Native.lean`; data SHA-256 `a562ff00…f56ce2` (3,068,111 records, regenerated). Built twice independently, ≈ 100 s. Negative: the root raised to > 127 is rejected. [EXP-0004 README §7](research/EXP-0004-independent-proof-audit/README.md). |

## R-0100 … infrastructure validation (exact small values)

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0100 | Our exact table agrees with literature: ‖3^k‖ = 3k, ‖2^k‖ = 2k (2^k ≤ 4·10⁸), ‖1439‖ = 26, Selfridge's maxima E(m), ‖2^8−1‖ = 17, ‖2^16−1‖ = 34. | `COMPUTATIONALLY VERIFIED` | `tests/test_exact_table.py`. The Python and C implementations agree for n ≤ 20000. |
| R-0101 | ‖353942783‖ = ‖353942782‖ = 63. This is consistent with Wang's result that 353942783 is the least prime p with ‖p‖ ≠ ‖p−1‖ + 1. | `COMPUTATIONALLY VERIFIED` (for the two values) | C table to 4·10⁸, 2026-11-25 (RESEARCH_LOG). Minimality is `LITERATURE` (Wang 2012), not re-checked. |

## R-0200 … Mersenne numbers 2^k − 1

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0200 | ‖2^k − 1‖ for 2 ≤ k ≤ 39 agrees with Iraids et al. 2012, Table 3 | `LITERATURE + COMPUTATIONALLY VERIFIED` | `tests/test_exact_single.py` |
| R-0201 | ‖2^k − 1‖ for 40 ≤ k ≤ 61 as tabulated in EXP-0002 (e.g. ‖2^60−1‖ = 124, ‖2^61−1‖ = 127) | `COMPUTATIONALLY VERIFIED` (two independent implementations) | [EXP-0002](experiments/EXP-0002-exact-mersenne-pilot/), [EXP-0003](experiments/EXP-0003-independent-verification/) |
| R-0202 | Iraids' bounds A(k+1) ≤ A(k) + 1 and A(k) ≤ ⌊log₂ k⌋ + H(k) − 3 hold for k ≤ 61; the second is tight at k = 32, 33, 34 | `OBSERVATION` (on R-0201 data) | EXP-0002 |

## History

- 2026-11-25 (night): EXP-0004 follow-up. New R-0009 (`FORMALLY VERIFIED` checker soundness, divisors, Pratt) and R-0010 (‖N‖ > 126 checked in Lean via `native_decide`, labelled `COMPUTATIONALLY VERIFIED`). R-0007 gains evidence item (5); its status is unchanged. The R-0007 status sentence "nothing is in Lean yet" is replaced by the `native_decide` remark, which is the true reason it is still not `FORMALLY VERIFIED`.
- 2026-11-25: EXP-0004 audit. R-0007 gains a table-free certificate and an audit; status unchanged. New R-0008 (Lean lemmas). Recommended, not yet applied: relabel R-0006 as `LITERATURE` (see EXP-0004 disagreement log D3).

- 2026-11-25: R-0007 gains an independently checked lower-bound certificate (EXP-0003 step 2). The status stays `COMPUTATIONALLY VERIFIED`, not `PROVEN`.

- 2026-11-25: R-0007 and R-0201 lose the "provisional: one implementation" tag after the independent replication in EXP-0003 (He's code, 60/60 values agree).

- 2026-11-25: R-0004 ("‖N‖ = ? open, 116 ≤ ‖N‖ ≤ 127") superseded by R-0006 (≥ 117) and R-0007 (= 127, provisional).
