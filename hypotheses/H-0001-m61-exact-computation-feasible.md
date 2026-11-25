# H-0001: Exact ‖2^61 − 1‖ is computable on one machine

- **Status:** COMPUTATIONALLY VERIFIED. The budgeted exact search (not He's interval DP) took 117 s on one core (EXP-0002).
- **Related:** RQ-1, RQ-6; brief §6-B
- **Statement:** A correct implementation of He's single-target algorithm (SOSA 2024, Thm 8)
  determines ‖2^61 − 1‖ in under ~1 CPU-week on a 4-core, 16 GB machine.
- **Motivation:** The asymptotic cost is n^0.6154 ≈ 2·10¹¹ basic steps at n ≈ 2.3·10¹⁸. He reports
  runs for targets up to ~10³⁸ (powers of 2, where heavy pruning applies).
- **What would refute it:** a pilot on 2^k − 1 for k = 30…45 whose runtime extrapolates far beyond
  that budget, or memory needs over 16 GB.
- **Planned test:** EXP-0002 (to be planned). Implement the algorithm, validate it against exact
  tables (n ≤ 4·10⁸ here, ≤ 10¹² published), then run pilots on 2^k − 1 for growing k.
- **History:** 2026-11-25 created. 2026-11-25 confirmed by EXP-0002. The slack-based pruning makes the worst-case n^0.6154 bound irrelevant here.
