# EXP-0002: Exact ‖2^k − 1‖ for k ≤ 61 by budgeted exhaustive search (pilot)

| Field | Value |
|-------|-------|
| ID | EXP-0002 |
| Date | 2026-11-25 |
| Question | RQ-1 (‖2^61 − 1‖ exactly), RQ-2 (‖2^k − 1‖ table), H-0001, H-0002 |
| Cost class | cheap: ≈ 6 min CPU in total, single core, < 1 GB RAM (not measured precisely) |
| Code | `algorithms/exact_single.py` (search), `algorithms/upper_bound_search.py` (upper bounds), `algorithms/c/complexity_table.c` (base table) |
| Correctness argument | [`research/proof-exact-search.md`](../../research/proof-exact-search.md) |

## Method

For each k, take the peel-search upper bound U_k (an explicit expression). Then run
`ExactSearch.complexity(2^k − 1, U_k)`. This decides exhaustively whether a cheaper expression
exists, with the rigorous pruning described in the proof note. The base table is exact for n ≤ 4·10⁸.

## Reproduce

```bash
bash experiments/EXP-0002-exact-mersenne-pilot/run.sh /tmp/exp2
```

## Environment

Cloud container, Intel Xeon @ 2.10 GHz, one core, 15 GB RAM. Python 3.13, gcc 13.3.
Run on 2026-11-25 at the parent commit of the PR that adds this file.

## Results

Raw output: [`results_k20-61.jsonl`](results_k20-61.jsonl). A(k) = ‖2^k − 1‖ − 2k.

| k | 20–39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 | **61** |
|---|-------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|--------|
| A(k) | = Iraids Table 3 | 2 | 3 | 2 | 3 | 3 | 3 | 4 | 5 | 2 | 3 | 3 | 3 | 3 | 4 | 3 | 4 | 4 | 4 | 5 | 6 | 4 | **5** |
| ‖2^k−1‖ | | 82 | 85 | 86 | 89 | 91 | 93 | 96 | 99 | 98 | 101 | 103 | 105 | 107 | 110 | 111 | 114 | 116 | 118 | 121 | 124 | 124 | **127** |
| seconds | < 1 | 0.5 | 1.1 | 1.0 | 1.5 | 1.8 | 2.8 | 2.9 | 3.9 | 2.2 | 2.9 | 3.7 | 6.8 | 8.0 | 10.0 | 11.5 | 14.3 | 27.8 | 31.7 | 38.3 | 49.9 | 83.7 | **116.8** |

Search nodes for k = 61: 865,738. For several k (35, 42, 43, 48–53) the exact value is below the
peel bound, so the search does find better expressions when they exist.

## Checks against independent data

| Check | Result |
|-------|--------|
| Iraids et al. 2012, Table 3 (A(k), k = 2…39) | **All 38 values agree** (`tests/test_exact_single.py::test_reproduces_iraids_table3`) |
| Exact C table, 314 values (300 random n ≤ 4·10⁸ plus 2^k−1, k ≤ 28), using a tiny base table so the search does the work | 0 mismatches |
| Iraids Thm 8(c): A(k+1) ≤ A(k) + 1 | holds for all new values |
| Iraids Cor. 2: A(k) ≤ ⌊log₂ k⌋ + H(k) − 3 | holds; tight at k = 32, 33, 34 |
| AZ2012 Thm 1.6 (δ < 1 classification) vs exact table, n ≤ 4·10⁸ | exactly the predicted 420 numbers, all with the predicted complexities |

## Conclusions and status

> **Update 2026-11-25:** independently replicated in [EXP-0003](../EXP-0003-independent-verification/) (He's solver, 60/60 agree, also with its defect pruning switched off). The current statuses are in `RESULTS.md` (R-0007, R-0201). The text below is the original record. One correction: "the algorithm is proven" should read "the algorithm has a conditional correctness proof that has been self-checked but not yet reviewed" (see `research/proof-exact-search.md`).

- **‖2^61 − 1‖ = 127.** Status: `COMPUTATIONALLY VERIFIED`, **provisional**. It rests on a single
  implementation. The algorithm is proven and the implementation is extensively tested, but no
  independent replication exists yet (EXP-0003). The 127 upper bound is also `FORMALLY VERIFIED`.
- ‖2^k − 1‖ for 40 ≤ k ≤ 60: same status. We found no published values for k > 39 in the
  sources we checked.
- **Consequence:** the board's 127 is optimal, and no expression with ≤ 126 ones exists (H-0002 → REFUTED, provisional).

**Not shown:** anything independent of our own code. The base table (n ≤ 4·10⁸) comes from our
code too, although it is cross-checked against literature.
