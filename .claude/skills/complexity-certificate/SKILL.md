---
name: complexity-certificate
description: Use in the Integer Complexity Lab when checking, storing, or formalizing an expression that claims an upper bound on integer complexity ||n|| (e.g. "this uses k ones"). Covers the strict parser, the certificate JSON format, and the Lean kernel check.
---

# Check and store an integer-complexity certificate

An expression in `1`, `+`, `*` and parentheses that evaluates to n with k ones proves
‖n‖ ≤ k. Nothing more.

## Check (never with `eval`)

```bash
python3 -c "from algorithms.expression import evaluate; print(evaluate(open('expr.txt').read().strip()))"
```

`evaluate` rejects every character outside `1+*() ` and every malformed input, and it returns
`value`, `ones` and `max_depth`. Third-party expressions are untrusted input. Check them only
this way.

## Store

Create `certificates/<family>/<ID>.json`:

```json
{
  "id": "M61-UB127-ICL-PEEL",
  "n": "2305843009213693951",
  "n_form": "2^61-1",
  "claim": "||2^61-1|| <= 127",
  "ones": 127,
  "evidence_status": "COMPUTATIONALLY VERIFIED (upper bound only)",
  "provenance": {"source": "...", "url": "...", "commit": "...", "date": "YYYY-MM-DD", "license": "..."},
  "method": "...",
  "notes": "...",
  "expression": "..."
}
```

Use public handles only for third-party authors, never e-mail addresses. Then run
`python3 certificates/verify.py` and `python3 -m pytest -q`.

## Formalize (headline results)

```bash
python3 lean/scripts/gen_certificates.py      # regenerates lean/IntegerComplexity/Certificates/M61.lean
cd lean && lake build && lake env lean scripts/CheckAxioms.lean
```

A theorem `UpperBound n k` with "does not depend on any axioms" may be labelled
`FORMALLY VERIFIED`. For other families, extend the generator rather than hand-writing Lean terms.

## Improving a bound

If a new certificate beats the best known one, also update `RESULTS.md`, the test
`tests/test_certificates.py::test_m61_benchmark_bound`, and `RESEARCH_LOG.md`. Use
`record-research-result` for this. Don't announce it outside the repository without the
human lead's approval.
