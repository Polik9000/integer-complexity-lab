# RP-0001: Status of the benchmark ‖2^61 − 1‖ and choice of research target

> Review package for an independent reviewer. Self-contained. Repository: integer-complexity-lab.

## 1. Exact claims under review

Let ‖n‖ be the least number of 1s in an expression for n using only `1`, `+`, `*` and
parentheses (Mahler–Popken complexity, OEIS A005245). Let N = 2^61 − 1 = 2305843009213693951.

- **C1.** ‖N‖ ≥ 116. Status: **PROVEN** (from a standard bound, see §4).
- **C2.** ‖N‖ ≤ 127. Status: **COMPUTATIONALLY VERIFIED + FORMALLY VERIFIED (Lean 4)**.
- **C3.** As far as we could determine on 2026-11-25, nothing better than 116 ≤ ‖N‖ ≤ 127 is
  publicly known. Status: **OBSERVATION** (limited search).
- **C4 (recommendation, not a theorem).** "Determine ‖N‖ exactly with checkable certificates,
  using He's single-target algorithm" is a better research target than "find an expression
  with fewer than 127 ones".

## 2. What we ask you to do

1. Check the proof of C1 (§4.1). Is there a standard, easy argument that gives a better lower
   bound for this particular N, e.g. from the defect theory of Altman and Zelinsky?
2. Check that the expression in §5 is a valid certificate for C2. You can verify it independently,
   e.g. with any big-integer calculator, after replacing nothing but the characters shown.
3. Do you know of any published or online value or better bound for ‖2^61 − 1‖, or exact values of
   ‖2^k − 1‖ for k > 39?
4. Critique C4. Is the feasibility estimate in §4.3 reasonable? What would you do instead?

## 3. Definitions and context

- Selfridge's bound: an expression with k ones has value at most 3^{k/3}. Hence ‖n‖ ≥ 3 log₃ n,
  with equality only for powers of 3 (Guy 1986; Iraids et al. 2012, Thm 1–2).
- Exact values are known for all n ≤ 10¹² (Iraids et al. 2012).
- Q. He, "Improved algorithms for integer complexity", SOSA 2024 (arXiv:2308.10301). Thm 8
  computes ‖n‖ for a single n in time O(n^{3/(9−α)+o(1)}) ≤ O(n^0.6154), without computing
  all smaller values. He verified ‖2^i‖ = 2i for all 2^i ≤ 2^126.

## 4. Mathematical reasoning

**4.1 (C1).** 3 log₃ N = 3·61·ln 2 / ln 3 = 115.4601… Since ‖N‖ is an integer and ‖N‖ ≥ 3 log₃ N,
we get ‖N‖ ≥ 116. This is the "floor 116" quoted by the online board. It is generic and uses
nothing about N.

**4.2 (C2).** The expression in §5 is a certificate. It satisfies
N = 1 + 126·(1 + 192·1387·(1 + 2¹⁸·(1 + 2¹⁸))), with 126 = 2·3²·7, 192 = 3·2⁶ and 1387 = 19·73.
The factors come from N − 1 = 2·3²·5²·7·11·13·31·41·61·151·331·1321.

**4.3 (C4).** n^0.6154 at n = 2.3·10¹⁸ is about 2·10¹¹. That is a feasible order of magnitude on
one machine, up to unknown constants and polylog factors. He reports runs on targets near 10³⁸.

## 5. Relevant files and the certificate

| Path | Role |
|------|------|
| `research/2026-11-25-m61-benchmark-brief.md` | Full brief: provenance, analysis, recommendation |
| `certificates/m61/*.json` | Certificates (127, 127, 150) |
| `algorithms/expression.py` | Strict parser (no eval) |
| `lean/IntegerComplexity/Basic.lean`, `.../Certificates/M61.lean` | Lean definitions and kernel-checked bounds |
| `experiments/EXP-0001-m61-benchmark-reproduction/` | Independent rediscovery of 127 |

Our 127-ones expression (`M61-UB127-ICL-PEEL`) is attached in the flattened version of this package.

## 6. Reproducibility

```bash
python3 -m pytest -q                         # 36 tests
python3 certificates/verify.py               # all certificates OK
cd lean && lake build && lake env lean scripts/CheckAxioms.lean   # "does not depend on any axioms"
bash experiments/EXP-0001-m61-benchmark-reproduction/run.sh /tmp/exp1   # ~1 min, rediscover 127
```

## 7. Known uncertainties and weak points

- Provenance of the third-party 127: pull request #4 on GitHub `math-market/integer-complexity-m61`,
  open and unmerged. We couldn't read its CI result.
- Our literature search was limited: a few papers (some read through imperfect PDF extraction)
  and web searches. Altman's defect papers have not been read yet.
- The feasibility estimate in §4.3 ignores constants. We have not implemented He's algorithm.
- We didn't search exhaustively for a Lean/Mathlib formalization of integer complexity.

## 8. Reviewer response

(to be filled in)
