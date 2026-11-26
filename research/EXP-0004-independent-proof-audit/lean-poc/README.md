# EXP-0004 Lean proof-of-concept extras (not built by CI)

Written by the Lean formalization specialist (subagent). The sound PoC itself lives in `lean/IntegerComplexity/PoC/`.
This folder keeps the extra files:

- `Bench.lean`: a **benchmark-only** checker. Each claim carries its own divisor list, which is **not** proven complete, so it is
  not part of any soundness chain. It is used for the kernel-cost table in `../lean-formalization-roadmap.md`. It also has a
  fuel-based binary `powMod`. To build it, copy it into `lean/IntegerComplexity/PoC/`.
- `M20.lean`: ‖2^20 − 1‖ = 42 with the sound trial-division checker (547 claims, ≈ 15 s kernel time).
- `gen.py`, `genbench.py`: generators for the example and benchmark files (set `ICL_TABLE` to the 10⁸ table from `run_cert.sh`).
