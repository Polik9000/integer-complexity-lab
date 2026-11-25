# RESEARCH QUESTIONS

Prioritized. Each question links to hypotheses (`hypotheses/`) and experiments (`experiments/`)
once they exist. Status: `open`, `active`, `answered` (see RESULTS), `parked`, `dropped` (with reason).

| ID | Question | Priority | Status | Notes |
|----|----------|----------|--------|-------|
| RQ-1 | What is ‖2^61 − 1‖ exactly? | **P1** | **computationally answered: 127** (not a proof), verified by two independent programs (EXP-0002, EXP-0003 step 3); certificate pending | Known: 116 ≤ ‖N‖ ≤ 127. Route: implement He's (2023/24) single-target exact algorithm (Thm 8, O(n^0.6154)). Validate it against our exact tables and published data, then run it under an approved plan. See the [brief](research/2026-11-25-m61-benchmark-brief.md) §6-B. |
| RQ-2 | Exact ‖2^k − 1‖ for 40 ≤ k ≤ ~100? How do they compare with the upper bounds of Iraids et al. (2012, Thm 8 / Cor. 2–3)? | P2 | active: k ≤ 61 done (two independent programs, EXP-0002/0003) | Extends Iraids et al. Table 3 (k ≤ 39). Next: k = 64 (Iraids Observation 2, predicted 132), then k ≤ ~80. **On hold** (lead, 2026-11-25) until the certificate architecture is specified. See the [plan](research/2026-11-25-rq1-strategy-and-exp0003-plan.md). |
| RQ-3 | Can defect theory (Altman–Zelinsky 2012; Altman 2016, 2019) prove ‖2^61 − 1‖ ≥ 117 or more, rigorously and cheaply? | P3 | partly answered: ≥ 117 via AZ2012 Thm 1.6 | Defect theory can't realistically reach 127. Kept as a short human-readable proof component. |
| RQ-4 | Is there an expression for 2^61 − 1 with fewer than 127 ones? | P3 | open | Bounded heuristic side experiments only. Answered as a byproduct if RQ-1 succeeds. |
| RQ-5 | Formalize in Lean 4: ‖n‖ ≥ 3 log₃ n (as n³ ≤ 3^‖n‖), and a verified checker for certificates. | **P1** | active: Selfridge, Theorem C and a sound claim checker done (EXP-0004 PoC); next M2 divisors from a factorization, M3 Pratt (see EXP-0004 roadmap) | Core Lean only for now. Consider Mathlib when we need real analysis or `Nat.find`. |
| RQ-6 | Has ‖2^61 − 1‖ or ‖2^k − 1‖ for k > 39 been computed anywhere (He's code, OEIS b-files, forums)? | P2 | checked again in EXP-0004 (18 papers, He's repo, OEIS reachable this time, web): nothing found. Not a proof of absence. | Must be settled before RQ-1 compute. We may also need to contact authors, which requires the human lead's approval. |
| RQ-7 | What is the CI/review outcome of board PR #4, and does the board accept further submissions? | P3 | open | Informational. Any submission by us needs the human lead's approval. |
| RQ-8 | Can the exact search emit a compact certificate that a small independent checker (eventually Lean) verifies? | **P1** | answered for k = 61 (EXP-0003; table-free version in EXP-0004). Open: harden `check_lower.py` (EXP-0004 F1/F2) | Makes R-0007 checkable without trusting our search code (strategy S2). |
| RQ-9 | Is A(k) = ‖2^k−1‖ − 2k bounded? Which k attain Iraids' bound ⌊log₂ k⌋ + H(k) − 3? | P3 | open | Our data so far: tight at k = 32, 33, 34 only (k ≤ 61). |
