---
name: reproducible-experiment
description: Use in the Integer Complexity Lab before running any computation whose output supports a claim. Scaffolds experiments/EXP-NNNN-*/ with method, exact commands, environment, cost class, results and evidence statuses.
---

# Run a reproducible experiment

Follow `experiments/README.md`. In short:

1. **Number it.** Take the next free `EXP-NNNN` from the index in `experiments/README.md`.
2. **Classify the cost** *before* running it. `cheap` (≤ 30 min CPU, ≤ 2 GB) can run straight
   away. `medium` and `large` need a written plan in the README and the human lead's go-ahead
   (CLAUDE.md rule 11). Estimate from a small pilot run, not from intuition.
3. **Write the README skeleton first:** question (link RQ/H), method, and the exact commands.
4. **Prefer a `run.sh WORKDIR`** that rebuilds everything from the repository. Work in a
   directory outside the repo. Never commit large outputs. Record their size and SHA-256 instead.
5. **Record the environment:** `lscpu | grep 'Model name'`, cores used, RAM,
   `gcc --version`, `python3 --version`, and the git commit (`git rev-parse --short HEAD`).
6. **Results table:** raw outputs with runtimes, including failures and dead ends.
7. **Conclusions:** each with an evidence status, plus an explicit "Not shown:" line.
8. **Record** with the `record-research-result` skill (RESULTS.md, RESEARCH_LOG.md).

## Validation habits for this project

- New exact algorithms must reproduce `algorithms/exact_table.py` / `complexity_table.c` on
  the overlapping range before their new outputs are trusted.
- Every claimed upper bound must come with an expression that `certificates/verify.py`
  accepts. Headline bounds also go into Lean (`lean/scripts/gen_certificates.py`, then `lake build`).
- Use fixed seeds for anything randomized, and record them.
