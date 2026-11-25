# lean/: Lean 4 formalization

Core Lean 4 (toolchain in `lean-toolchain`), no Mathlib yet, so it builds in seconds.

```bash
cd lean
lake build                                  # build everything
lake env lean scripts/CheckAxioms.lean      # axiom report for headline theorems
```

| File | Contents |
|------|----------|
| `IntegerComplexity/Basic.lean` | `Expr`, `eval`, `ones`; `UpperBound`, `LowerBound`, `HasComplexity`; basic lemmas (sub-additivity, sub-multiplicativity, ‖n‖ ≤ n) |
| `IntegerComplexity/Certificates/M61.lean` | **Generated** by `scripts/gen_certificates.py`: kernel-checked `UpperBound (2^61-1) 127` (two independent certificates) and `150` |

Roadmap (RQ-5): formalize ‖n‖ ≥ 3 log₃ n in the integer form n³ ≤ 3^‖n‖ (this needs E(k) = max value
with k ones), then decide whether to move to Mathlib.
