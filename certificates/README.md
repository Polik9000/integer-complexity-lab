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

## Lower-bound certificates (`lower/`)

`lower/check_lower.py` checks certificates of the form ‖n‖ > j (spec:
[`research/2026-11-25-certificate-architecture.md`](../research/2026-11-25-certificate-architecture.md)).
It uses the standard library only and imports nothing from `algorithms/`. It needs the base table file, and you must state the
statement you expect it to prove (version 2, after the EXP-0004 audit):

```bash
python3 -I certificates/lower/check_lower.py CERT.jsonl.gz TABLE.bin \
    --target 2305843009213693951 --claim-gt 126 --table-sha256 <SHA-256 of TABLE.bin>
```

The verdict line is `ACCEPTED: ||target|| > claim_gt  (table sha256 …)`. Anything else, or exit code ≠ 0, means rejected.
Hardening record: [`experiments/EXP-0005-checker-hardening/`](../experiments/EXP-0005-checker-hardening/).

| Certificate | Claim | Size | SHA-256 (gzip) | How to get it |
|-------------|-------|------|----------------|---------------|
| M61-LB126-cert-v1 | ‖2^61−1‖ > 126 | 13.17 MB gzip, 1,121,887 records | `4f286d15…46135752` | Not committed (size). Regenerate with `experiments/EXP-0003-independent-verification/run_cert.sh` (~5 min). |

Together with `m61/M61-UB127-*.json`, this gives ‖2^61−1‖ = 127, `COMPUTATIONALLY VERIFIED` with a checkable
certificate. It is not `PROVEN` (see RESULTS R-0007).
