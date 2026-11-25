# Hypotheses

One file per hypothesis: `H-NNNN-short-name.md`. Never delete one. Change its status instead.

Template:

```markdown
# H-NNNN: <title>
- **Status:** CONJECTURE | OBSERVATION | UNVERIFIED | COMPUTATIONALLY VERIFIED (finite range) | PROVEN | REFUTED
- **Related:** RQ-…, EXP-…, R-…
- **Statement:** <precise>
- **Motivation / evidence so far:**
- **What would refute it:**
- **Planned test:**
- **History:** <dated status changes>
```

| ID | Statement (short) | Status |
|----|-------------------|--------|
| [H-0001](H-0001-m61-exact-computation-feasible.md) | ‖2^61−1‖ can be computed exactly on a single machine | COMPUTATIONALLY VERIFIED (117 s, EXP-0002) |
| [H-0002](H-0002-m61-below-127.md) | ‖2^61−1‖ < 127 | REFUTED (provisional, EXP-0002) |
