# EXP-0003: Independent verification of ‖2^k − 1‖ for k ≤ 61

| Field | Value |
|-------|-------|
| ID | EXP-0003 |
| Date | 2026-11-25 |
| Question | RQ-1 (‖2^61 − 1‖ exactly): independent check of R-0007 / R-0201 |
| Plan | [`research/2026-11-25-rq1-strategy-and-exp0003-plan.md`](../../research/2026-11-25-rq1-strategy-and-exp0003-plan.md) |
| Cost class | cheap (step 3: ≈ 20 s CPU, < 2 GB RAM) |
| Approval | Step 3 (building and running third-party GPL code) was approved by the project lead on 2026-11-25 by a decision card. |
| Code | `run_he.sh`, `he_driver.cpp`, `compare.py`. He's code is fetched at a pinned commit and is not vendored (GPL). |
| Repo commit | on top of `819e6c9` (branch `exp/EXP-0002-exact-mersenne`) |

## Steps

| Step | Work | State |
|------|------|-------|
| 1 | Our own second implementation (C/C++, different structure) | planned |
| 2 | Certificate-emitting search plus an independent checker | planned |
| **3** | **Run He's solver (`hqztrue/integer_complexity`, `single.cpp`, `calc_single`) on 2^k − 1, k ≤ 61** | **done (this record)** |
| 5 | Review package RP-0002 | planned |
| 6 | Optional Lean checker | planned |

## Step 3: method

He's `calc_single(n)` (Q. He, SOSA 2024; code at `742e8c5`, `integer-complexity-128/single.cpp`,
SHA-256 `8d35c1d6…fbeb87`) uses iterative deepening on the budget t, starting at a lower bound for n.
For each t it runs a memoized DFS `dfs128(n, t)` over:
- additive splits n = (n − i) + i with i ≤ g[k] (g = Selfridge maxima E(·)), and
- all factor pairs (g, n/g) from its own factorizer (Pollard rho / quadratic sieve).

It uses a precomputed table of ‖m‖ for m ≤ 10⁸ (Fuller's all-n algorithm). We read the source before running it
(CLAUDE.md rule 12). Our driver only renames `main` and `_init` (a Linux linker clash), calls
`init(1e8, 1e38)`, and loops `calc_single(2^k − 1)` for k = 2..61.

**How independent is it from EXP-0002?**

| Aspect | EXP-0002 (ours) | He's code |
|--------|-----------------|-----------|
| Author, language | us, Python | Q. He, C++ |
| Base table | our C table, n ≤ 4·10⁸ | Fuller's algorithm, n ≤ 10⁸ |
| Factorization | Miller–Rabin + Pollard rho (ours) | own rho/QS library |
| Search control | one budgeted search from a known upper bound | iterative deepening from a lower bound |
| Lower-bound pruning | Selfridge only | Selfridge **plus** a hard-coded list of defect < 1 numbers: numbers not in the list get a bound one higher |

The two share the **mathematical method**: exhaustive split search with Selfridge-type pruning.
A flaw in that method would affect both. Our written proof covers the method
(`research/proof-exact-search.md`; a conditional theorem, self-checked, not yet independently reviewed).
He's paper also argues for it, but we have not checked his argument line by line for this finite use. The two share
**no code and no data**.

One caveat about He's extra pruning: it is valid only if the hard-coded list contains every number
of defect < 1 (Altman–Zelinsky 2012, Thm 1.6). If the list missed one, He's code could over-prune and
report a value that is **too large**, never too small. Our search uses only Selfridge, and every value agrees,
so this caveat does not affect the comparison. The sensitivity run below also removes it directly.

## Sensitivity run: He's code with the defect pruning switched off (lead's request, 2026-11-25)

[`he_naive_lb.patch`](he_naive_lb.patch) (SHA-256 `70c58de2…a6aea651`) changes **one line** of a *copy*
of `single.cpp`. It enables He's own commented-out `return complexity_LB_naive(n);` in `complexity_LB`.
After the patch every pruning and the starting depth use only the Selfridge bound λ(n) = min{i : E(i) ≥ n}.
The hard-coded defect < 1 list (`M_lb`) is then never read. We checked that `complexity_LB` is the only reader of `M_lb`.
The upstream checkout is not modified: `run_he.sh` copies it to `build-naive/`, patches the copy, and
re-asserts the upstream SHA-256 after the build.

One more dependency remains in both modes, and we did not change it: the base-table routine (`calc_all`, credited to Fuller) sizes a
buffer with He's upper bound ‖n‖ ≤ 4.125·log₃ n (`complexity_UB`). It affects only the table for n ≤ 10⁸, and
it is cross-checked by the agreement with our independently built table on every value we compare.

## Reproduce

```bash
bash experiments/EXP-0003-independent-verification/run_he.sh /tmp/exp3 2 61            # upstream, unmodified
bash experiments/EXP-0003-independent-verification/run_he.sh /tmp/exp3 2 61 naive      # sensitivity run
```

The script **aborts (exit 2)** if the upstream `single.cpp` does not match the SHA-256 of the inspected
version (`8d35c1d6…fbeb87`). We tested this by appending a line to a copy: it aborted.

The script clones the upstream repo and checks out `742e8c5`. It then compiles with g++ -O2, runs, and
compares the output with EXP-0002 and with Iraids et al. 2012, Table 3. The exit code is non-zero on any mismatch.

## Environment

Intel Xeon @ 2.10 GHz (container, 4 vCPU, 1 core used), 15 GB RAM, Ubuntu 24.04, g++ 13.3.0, Python 3.

## Results

| Run | k | Wall time | Output |
|-----|---|-----------|--------|
| full | 2..61 | 17.3 s in total, about 10 s of it initialization (the 10⁸ table); k = 61 itself took 2.6 s | [`results_he_k2-61.jsonl`](results_he_k2-61.jsonl), SHA-256 `25dbb402…dec6095` |
| script check | 55..61 | 22.9 s, including the compile | identical values |
| **naive (Selfridge only)** | 2..61 | 26.9 s in total, including the compile; k = 61 itself took 3.58 s | [`results_he_naive_k2-61.jsonl`](results_he_naive_k2-61.jsonl), SHA-256 `cdada982…b39fd681e` |

`compare.py` output: **60 values. All 42 overlaps with EXP-0002 (k = 20..61) agree, and all 38 overlaps
with Iraids Table 3 (k = 2..39) agree. There are 0 mismatches.** In particular, He's code gives ‖2^61 − 1‖ = 127.
The **naive** run gives the same 60 values. 0 differ from the upstream run, so the result does not depend on He's
defect list. Search time rises by about 50% (k = 60: 1.52 → 2.53 s; k = 61: 2.61 → 3.58 s).

He's code is ≈ 45× faster than our Python search on k = 61 (2.6 s vs 117 s). This changes the
cost model in the plan: k ≈ 64–70 is seconds to minutes, not minutes to hours.

## Conclusions

- ‖2^k − 1‖ for 40 ≤ k ≤ 61 (R-0201), including **‖2^61 − 1‖ = 127** (R-0007): `COMPUTATIONALLY
  VERIFIED` by **two independent implementations**, which share no code or data.
- He's implementation reproduces Iraids et al. Table 3 exactly: `LITERATURE + COMPUTATIONALLY VERIFIED`.
- Sensitivity: the values do not depend on He's defect < 1 pruning (`COMPUTATIONALLY VERIFIED`, naive run).

**Not shown.**
- The value is not checkable without trusting one of the two programs. That needs the certificate in step 2.
- The common method has not been reviewed externally (that is RP-0002).
- Nothing here is `PROVEN` in the CLAUDE.md sense.

## Follow-ups

- Steps 1, 2, 5 and 6 above.
- k = 62..64 is cheap, but it is **on hold** at the lead's request (2026-11-25) until the certificate architecture is specified.
