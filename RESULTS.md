# RESULTS

Current state of knowledge. Every row has an evidence status as defined in
[`CLAUDE.md` §4](CLAUDE.md#4-evidence-statuses). Superseded rows are moved to the
"History" section, never deleted.

Last updated: 2026-11-25.

## R-0001 … benchmark N = 2^61 − 1 = 2305843009213693951

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0001 | ‖N‖ ≥ 116 | `PROVEN` (`LITERATURE`) | ‖n‖ ≥ 3 log₃ n for all n (Selfridge; see Guy 1986; Iraids et al. 2012, Thm 1). 3 log₃ N = 115.460…, and ‖N‖ is an integer. Not yet formalized. |
| R-0002 | ‖N‖ ≤ 150 | `COMPUTATIONALLY VERIFIED` | Board baseline expression, [`certificates/m61/M61-UB150-BOARD-BASELINE.json`](certificates/m61/M61-UB150-BOARD-BASELINE.json). |
| R-0003 | ‖N‖ ≤ 127 | `COMPUTATIONALLY VERIFIED` + `FORMALLY VERIFIED` | Two independent 127-ones expressions: [third-party board submission](certificates/m61/M61-UB127-BOARD-PR4.json) and [our own search](certificates/m61/M61-UB127-ICL-PEEL.json) ([EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/)). Both are kernel-checked in [`lean/IntegerComplexity/Certificates/M61.lean`](lean/IntegerComplexity/Certificates/M61.lean); `#print axioms` reports no axioms. |
| R-0004 | ‖N‖ = ? | **open** | 116 ≤ ‖N‖ ≤ 127. No better expression and no better lower bound found in any source we checked (2026-11-25). |
| R-0005 | A simple "peel" search (n = d·m + r, d ≤ 100, r ≤ 1, exact table to 4·10⁸) reaches 127 in ≈5 s; the variants tried (r ≤ 8, d ≤ 400) found nothing below 127. | `OBSERVATION` | [EXP-0001](experiments/EXP-0001-m61-benchmark-reproduction/). Says nothing about whether < 127 exists. |

## R-0100 … infrastructure validation (exact small values)

| ID | Statement | Status | Evidence |
|----|-----------|--------|----------|
| R-0100 | Our exact table agrees with literature: ‖3^k‖ = 3k, ‖2^k‖ = 2k (2^k ≤ 4·10⁸), ‖1439‖ = 26, Selfridge's maxima E(m), ‖2^8−1‖ = 17, ‖2^16−1‖ = 34. | `COMPUTATIONALLY VERIFIED` | `tests/test_exact_table.py`. The Python and C implementations agree for n ≤ 20000. |
| R-0101 | ‖353942783‖ = ‖353942782‖ = 63. This is consistent with Wang's result that 353942783 is the least prime p with ‖p‖ ≠ ‖p−1‖ + 1. | `COMPUTATIONALLY VERIFIED` (for the two values) | C table to 4·10⁸, 2026-11-25 (RESEARCH_LOG). Minimality is `LITERATURE` (Wang 2012), not re-checked. |

## History

(none yet)
