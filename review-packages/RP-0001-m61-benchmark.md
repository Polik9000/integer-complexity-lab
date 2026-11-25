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


---
### `certificates/m61/M61-UB127-ICL-PEEL.json`

```json
{
  "id": "M61-UB127-ICL-PEEL",
  "n": "2305843009213693951",
  "n_form": "2^61-1",
  "claim": "||2^61-1|| <= 127",
  "ones": 127,
  "evidence_status": "COMPUTATIONALLY VERIFIED (upper bound only)",
  "provenance": {
    "source": "this repository",
    "experiment": "experiments/EXP-0001-m61-benchmark-reproduction",
    "date": "2026-11-25"
  },
  "method": "peel search n = d*m + r, exact table T=4e8, R=1, D=100 (algorithms/upper_bound_search.py)",
  "notes": "Found independently in ~5 s. Structurally different search from the board submission; same count.",
  "expression": "(1+1)*((1+1+1)*((1+1+1)*((1+(1+1)*(1+1+1))*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1+1)*((1+(1+1)*((1+1+1)*(1+1+1)))*((1+(1+1)*((1+1)*((1+1)*((1+1+1)*(1+1+1)))))*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*(1+(1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*((1+1)*(1+1+1+1))))))))))))))))))))))))))))))))))+1)))))))))+1))))+1"
}
```


---
### `research/2026-11-25-m61-benchmark-brief.md`

```
# Research brief: the benchmark ‖2^61 − 1‖ (verified 2026-11-25)

**Purpose.** Re-validate the original research target before any expensive work: where the
numbers 127 and 116 come from, what they are worth, and whether this is the right question.

**Bottom line.**

1. **127 is a verified upper bound, not a known minimum.** The 127-ones expression is a
   third-party submission to a GitHub "Problem Market" board. The pull request is still open
   and unmerged. We re-verified it with our own parser and in the Lean 4 kernel. Our own generic
   search found a *different* 127-ones expression in about 5 seconds, so 127 is not a hard-won
   record.
2. **116 is not a computed lower bound.** It is the general bound ‖n‖ ≥ 3 log₃ n (≈ 115.46
   here), rounded up. It holds for every n and uses nothing specific to 2^61 − 1.
3. **The true value is open: 116 ≤ ‖2^61 − 1‖ ≤ 127.** We found no better expression and no
   better lower bound in any source we checked.
4. **Recommendation: reframe the target.** "Find an expression with fewer than 127 ones"
   gives only heuristic results and no endpoint. A better-defined goal is to **determine ‖2^61 − 1‖ exactly**
   with checkable certificates. The literature suggests this is feasible: He (2023/24) gives an
   exact single-target algorithm in O(n^0.6154), about 2·10¹¹ basic steps here before
   constants. A natural extension is **exact values of ‖2^k − 1‖ for k up to ~100**. The
   published table stops at k = 39.

---

## 1. The target

N = 2^61 − 1 = 2305843009213693951, the Mersenne prime M61.

- N − 1 = 2 · 3² · 5² · 7 · 11 · 13 · 31 · 41 · 61 · 151 · 331 · 1321 (computed; trial division).
  This highly composite N − 1 is what makes expressions of the form N = 1 + d·m cheap.
- N + 1 = 2^61, and ‖2^61‖ ≤ 122. Subtraction is not allowed, so this doesn't help directly.

## 2. Provenance of "127" and "116"

| Item | Finding | Status |
|------|---------|--------|
| Original challenge | GitHub repo `math-market/integer-complexity-m61`, first commit 2026-08-07. Task: an expression for N using **fewer than 150** ones. Container-verified checker (`check.py`, recursive-descent parser, no `eval`). Apache-2.0. | ✅ read in full (clone at `394bec0`) |
| Board's numbers | "Baseline 150" is the board's own Horner-style expansion in base 32767. "Floor 116" is ⌈3 log₃ N⌉, explicitly called "a floor nobody can go below". | ✅ |
| The 127 expression | Pull request #4 by GitHub user `Prev56`, commit `0995202` dated 2026-10-02. Title: "Expression for 2^61-1 using 127 ones (baseline 150)". The PR adds a single file `my_expression.json` and describes no method. A later commit (2026-11-01) re-triggered CI. | ✅ |
| Status of the submission | **Open, not merged** into `main` as of 2026-11-25. We couldn't read its CI result or review comments because this session has no GitHub API access to that repository. | ✅ open / ○ CI outcome unknown |
| Other submissions | PRs #1–#3 are the maintainers' own infrastructure changes. #4 is the only submission. | ✅ (git refs `refs/pull/*`) |
| Literature mention of 2^61 − 1 | None of He 2024, Konyagin–Oganesyan 2026 or Iraids et al. 2012 mentions it. A web search for the number with "integer complexity" finds only the board. | ◐ (searches on 2026-11-25) |
| MathWorks Cody 42834 ("Integer complexity, large numbers") | An unrelated speed challenge. We couldn't read its test cases (JavaScript-rendered) and found no link to M61. | ◐ |

## 3. Reproducibility of 127

- **Independent verification.** `algorithms/expression.py` is our own strict parser, written
  without looking at the board's. It confirms the PR #4 expression evaluates to N with exactly
  127 ones (671 characters, nesting depth 81).
- **Formal verification.** `lean/IntegerComplexity/Certificates/M61.lean` turns both 127-ones
  expressions into `Expr` terms. The Lean kernel proves `UpperBound (2^61 - 1) 127`, and
  `#print axioms` reports *no axioms*.
- **Independent rediscovery.** [EXP-0001](../experiments/EXP-0001-m61-benchmark-reproduction/):
  exact table ‖n‖ for n ≤ 4·10⁸ (C, 34 s), then a memoized search over N = d·m + r with
  d ≤ 100 and r ≤ 1. Result: 127 in ~5 s. Wider settings (d ≤ 400, or r ≤ 2 with d ≤ 80)
  also give 127. Smaller d gives 128–129.
- **Structure of the PR #4 expression.** Following its largest branch:
  **N = 1 + 126·(1 + 192·1387·(1 + 2¹⁸·(1 + 2¹⁸)))**, with 126 = 2·3²·7, 192 = 3·2⁶ and
  1387 = 19·73 (identity checked in Python). It chains small factors of N − 1, then long runs
  of ×2, with "+1" steps in between. This is exactly the family our search explores.

## 4. Upper bound vs proven minimum

- An expression with k ones proves ‖N‖ ≤ k. It cannot show that k is optimal.
- Optimality needs either (a) a lower-bound proof showing no expression with fewer ones exists,
  or (b) an exact, verified computation of ‖N‖.
- The only lower bound we know of for N is the generic 116. No N-specific lower bound appears
  in any source we checked.

## 5. Has a better expression appeared?

No evidence of one. Checked on 2026-11-25: the board's PR list (only #4) and web searches. The papers listed
in BIBLIOGRAPHY.md don't treat this number. **Caveat:** results posted in places we didn't search
(forums, private boards) can't be ruled out.

## 6. Novelty and feasibility of our research directions

| Direction | Novelty | Feasibility | Comment |
|-----------|---------|-------------|---------|
| A. Beat 127 by heuristic search | Low. It's a puzzle result, and anything found is just a new upper bound. | Unclear. Our cheap search plateaus at 127. | Worth a *bounded* effort as a byproduct, but not as the main goal. |
| B. **Exact ‖2^61 − 1‖** | Moderate. No published value, though experts with He's algorithm could probably compute it quickly. | **Plausible.** He's Thm 8 costs ~n^0.6154 ≈ 2·10¹¹ basic steps before constants. He ran targets up to ~10³⁸ on a laptop. | Needs a careful reimplementation, tests against the 10¹²-range data, and an auditable lower-bound argument. **Recommended primary target.** |
| C. Exact ‖2^k − 1‖ for 40 ≤ k ≤ ~100 | Moderate to good. It extends Iraids et al.'s Table 3 (k ≤ 39) and tests their upper bounds on ‖2^n − 1‖. | Plausible once B works. | Natural paper-sized contribution: a table plus certificates. |
| D. Better N-specific lower bound via defect theory (Altman–Zelinsky) | Moderate | Unclear until we read Altman 2016/2019. | Could lift 116 cheaply and rigorously. It would also be useful for pruning in B. |
| E. Lean formalization of the basic theory (‖n‖ ≥ 3 log₃ n, certificates) | Moderate. We found no Lean/Mathlib formalization of integer complexity, but we haven't searched thoroughly. | Feasible | Gives `FORMALLY VERIFIED` status to our foundations. Basic definitions and certificates are already done. |

**Recommendation.** Make B the primary target, with D as its lower-bound companion and C as the
follow-up. Run A only in bounded side experiments. The first step is a literature step, not a
computation: read He 2024 §3–4 in full and Altman 2016/2019, then write an implementation
plan in `experiments/` for the human lead to approve.

## 7. Known uncertainties

- CI outcome and review status of board PR #4 (we couldn't read them).
- Whether He's code is public, and whether ‖M61‖ has been computed privately.
- Exact formulas in Iraids et al. 2012 Cor. 2 and Konyagin–Oganesyan C_avg (the extractions were garbled).
- Real constants in He's O(n^0.6154). The feasibility estimate is order-of-magnitude only.
```
