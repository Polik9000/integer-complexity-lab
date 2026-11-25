# EXP-0001: Independent reproduction of the 127-ones benchmark for 2^61 − 1

| Field | Value |
|-------|-------|
| ID | EXP-0001 |
| Date | 2026-11-25 |
| Question | Can the claimed upper bound ‖2^61 − 1‖ ≤ 127 be verified and reproduced without the third-party expression? (RQ-4, brief §3) |
| Cost class | cheap (≈ 1 min CPU, 400 MB RAM) |
| Code | `algorithms/c/complexity_table.c`, `algorithms/upper_bound_search.py`, `algorithms/expression.py` |
| Commit | the commit that adds this file. `run.sh` prints the commit it ran at |

## Method

1. Build an exact table of ‖n‖ for all n ≤ T = 4·10⁸ (`complexity_table.c`). The
   additive-split pruning is rigorous (see the file header). The table is cross-checked against the
   independent Python implementation and literature values in `tests/test_exact_table.py`.
2. "Peel" search. Recursively write n = d·m + r with 2 ≤ d ≤ D and 0 ≤ r ≤ R, using exact
   values for d, r and for any m ≤ T, with memoization. Every candidate is an explicit
   expression, so whatever the search finds is a valid upper bound.
3. Verify the expression with the strict parser, store it as a certificate, and kernel-check it in Lean.

## Reproduce

```bash
bash experiments/EXP-0001-m61-benchmark-reproduction/run.sh /tmp/exp1
```

## Environment of the recorded run

Cloud container. Intel Xeon @ 2.10 GHz, 1 core used, 15 GB RAM. gcc 13.3.0, Python 3.13.

## Results

| Step | Output | Time |
|------|--------|------|
| Table n ≤ 4·10⁸ | `N=400000000 max=65 fnv1a=4c3e0497732259af`; SHA-256 of the table file `939a78d3ddf819c042cbbb386b7f46f1dd4177639947d5708e9f41e42ef7bc6f` | 36 s |
| Peel R=4, D=16 | 128 | 1 s |
| Peel R=1, D=100 | **127** | 5 s |
| Peel R=2, D=80 (manual run) | 127 | 25 s |
| Peel R=1, D=400 (manual run) | 127 | 29 s |
| Peel R=6, D=12 / R=3, D=30 (manual runs) | 129 / 128 | 1 s / 6 s |
| With T = 10⁷ instead: R=4, D=16 | 128 | 2 s |

The R=1, D=100 expression is committed as
[`certificates/m61/M61-UB127-ICL-PEEL.json`](../../certificates/m61/M61-UB127-ICL-PEEL.json). A re-run of
`run.sh` reproduced it byte for byte. The third-party expression (board PR #4) re-verifies with
our parser: 127 ones, value N.

Side check (same table): ‖353942783‖ = ‖353942782‖ = 63, consistent with Wang's counterexample.

## Conclusions and their status

- ‖2^61 − 1‖ ≤ 127: `COMPUTATIONALLY VERIFIED` (two independent expressions) and `FORMALLY VERIFIED`
  (Lean kernel, no axioms).
- 127 is reachable by a generic, seconds-long search: `OBSERVATION`. It suggests the board
  result is not a hard-won record.
- **Not shown:** anything about whether fewer than 127 ones suffice. The plateau at 127 under
  these settings is weak evidence at most. This search space is narrow.

## Follow-ups

Bounded variations: larger T, factor sets beyond d ≤ D (e.g. all divisors of n − r), and
mixed "+r" positions. These feed RQ-4 only. RQ-1 (the exact value) needs a different, exact algorithm.
