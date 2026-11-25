# RESULTS

Current state of knowledge. Every row has an evidence status as defined in
[`CLAUDE.md` §4](CLAUDE.md#4-evidence-statuses). Superseded rows are moved to the
"History" section, never deleted.

Last updated: 2026-11-25 (fourth update: EXP-0003 step 2, certificate).

## R-0001 … benchmark N = 2^61 − 1 = 2305843009213693951

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0001 | ‖N‖ ≥ 116 | `PROVEN` (`LITERATURE`) | ‖n‖ ≥ 3 log₃ n for all n (Selfridge; see Guy 1986; Iraids et al. 2012, Thm 1). 3 log₃ N = 115.460…, and ‖N‖ is an integer. Not yet formalized. |
| R-0002 | ‖N‖ ≤ 150 | `COMPUTATIONALLY VERIFIED` | Board baseline expression, [`certificates/m61/M61-UB150-BOARD-BASELINE.json`](certificates/m61/M61-UB150-BOARD-BASELINE.json). |
| R-0003 | ‖N‖ ≤ 127 | `COMPUTATIONALLY VERIFIED` + `FORMALLY VERIFIED` | Two independent 127-ones expressions: [third-party board submission](certificates/m61/M61-UB127-BOARD-PR4.json) and [our own search](certificates/m61/M61-UB127-ICL-PEEL.json) ([EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/)). Both are kernel-checked in [`lean/IntegerComplexity/Certificates/M61.lean`](lean/IntegerComplexity/Certificates/M61.lean); `#print axioms` reports no axioms. |
| R-0004 | ‖N‖ = ? | superseded by R-0007 (see History) | |
| R-0006 | ‖N‖ ≥ 117 | `PROVEN` (relative to `LITERATURE`: Altman–Zelinsky 2012, Thm 1.6) | N isn't one of the 7 families with defect < 1, so ‖N‖ > 3 log₃ N + 1 = 116.46. Proof: [`research/lit-AltmanZelinsky2012.md`](research/lit-AltmanZelinsky2012.md). Thm 1.6 itself was cross-checked against our exact table for n ≤ 4·10⁸ (exactly the 420 predicted numbers). |
| R-0007 | **‖N‖ = 127** (so the 127-ones expressions are optimal) | `COMPUTATIONALLY VERIFIED`: two independent implementations **and** an independently checked lower-bound certificate. **Not `PROVEN`**: the checker, spec and proofs have not been externally reviewed (RP-0002), and nothing is in Lean yet. | (1) Our exhaustive budgeted search. Its correctness rests on a conditional theorem with a written proof that has been self-checked but not independently reviewed ([`research/proof-exact-search.md`](research/proof-exact-search.md)): [EXP-0002](experiments/EXP-0002-exact-mersenne-pilot/), 117 s. (2) Q. He's independent C++ solver (no shared code or data): [EXP-0003](experiments/EXP-0003-independent-verification/), 2.6 s. It gives the same values with its defect-based pruning switched off (Selfridge bound only), 3.6 s. Both use the same mathematical method (exhaustive split search with Selfridge pruning). (3) A lower-bound certificate for ‖N‖ > 126 (1.12M records, 13 MB gzip) is accepted by a separate checker ([`certificates/lower/check_lower.py`](certificates/lower/check_lower.py), [spec](research/2026-11-25-certificate-architecture.md)). The checker does not trust the search; it trusts only Lemmas 1–2, Theorem C, its own ~170 lines, and the table for n ≤ 10⁸, which is byte-identical between our implementation and He's ([EXP-0003](experiments/EXP-0003-independent-verification/) step 2). Quote it as "computationally verified, with a checkable certificate", not as a proof. |
| R-0005 | A simple "peel" search (n = d·m + r, d ≤ 100, r ≤ 1, exact table to 4·10⁸) reaches 127 in ≈5 s; the variants tried (r ≤ 8, d ≤ 400) found nothing below 127. | `OBSERVATION` | [EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/). Says nothing about whether < 127 exists. |

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

- 2026-11-25: R-0007 gains an independently checked lower-bound certificate (EXP-0003 step 2). The status stays `COMPUTATIONALLY VERIFIED`, not `PROVEN`.

- 2026-11-25: R-0007 and R-0201 lose the "provisional: one implementation" tag after the independent replication in EXP-0003 (He's code, 60/60 values agree).

- 2026-11-25: R-0004 ("‖N‖ = ? open, 116 ≤ ‖N‖ ≤ 127") superseded by R-0006 (≥ 117) and R-0007 (= 127, provisional).
