# Experiments

One directory per experiment: `EXP-NNNN-short-name/`. Number them sequentially and never reuse a number.

## Required contents of `EXP-NNNN-*/README.md`

1. **Header table:** ID, date, question (link the RQ/H), cost class, code paths, commit.
2. **Method:** enough detail to re-implement without reading the code.
3. **Reproduce:** the exact command(s). Prefer a `run.sh` that takes a work directory.
4. **Environment** of the recorded run: CPU, cores used, RAM, OS/container, compiler and Python versions.
5. **Results:** a table of raw outcomes with runtimes. Large output files are *not* committed.
   Record their size, SHA-256 and how to regenerate them.
6. **Conclusions with evidence statuses** (CLAUDE.md §4), and a "Not shown" line.
7. **Follow-ups.**

## Cost classes

| Class | Budget | Approval |
|-------|--------|----------|
| cheap | ≤ 30 min CPU, ≤ 2 GB RAM/disk | none, just record it |
| medium | ≤ 1 day CPU on one machine, ≤ 20 GB | written plan in the experiment README, and the human lead says go |
| large | anything bigger, paid or cloud infrastructure | plan + explicit approval, including cost |

Failed or inconclusive experiments are kept and recorded the same way.

## Index

| ID | Question | Result | Status |
|----|----------|--------|--------|
| [EXP-0001](EXP-0001-m61-benchmark-reproduction/) | Reproduce ‖2^61−1‖ ≤ 127 independently | 127 found in 5 s by peel search | done |
| [EXP-0002](EXP-0002-exact-mersenne-pilot/) | Exact ‖2^k−1‖, k ≤ 61 | ‖2^61−1‖ = 127 (provisional) | done |
| [EXP-0003](EXP-0003-independent-verification/) | Independent verification (replication + certificate) | Step 3: He's code agrees on all 60 values k = 2..61 (‖2^61−1‖ = 127) | step 3 done; steps 1, 2, 5, 6 planned |
