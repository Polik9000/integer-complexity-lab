# certificates/

Upper-bound certificates for integer complexity. A certificate is a JSON file whose `expression`
uses only `1 + * ( )`, evaluates to `n`, and contains exactly `ones` ones. It proves ‖n‖ ≤ ones.
It is **not** evidence about lower bounds or optimality.

```bash
python3 certificates/verify.py            # verify all
python3 certificates/verify.py FILE.json  # verify one
```

Format and workflow: `.claude/skills/complexity-certificate/SKILL.md`. Headline certificates are
also kernel-checked in Lean (`lean/IntegerComplexity/Certificates/`).

| File | n | ones | Provenance |
|------|---|------|-----------|
| `m61/M61-UB127-ICL-PEEL.json` | 2^61−1 | 127 | This repository, EXP-0001 |
| `m61/M61-UB127-BOARD-PR4.json` | 2^61−1 | 127 | Third party: board PR #4 (open), Apache-2.0 |
| `m61/M61-UB150-BOARD-BASELINE.json` | 2^61−1 | 150 | Third party: board baseline, Apache-2.0 |
