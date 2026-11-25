# Literature note: He (2024), "Improved Algorithms for Integer Complexity"

Q. He, SOSA 2024 (SIAM), 107–114. arXiv:2308.10301 (v2, 2023-09-13). Code: GitHub
`hqztrue/integer_complexity` (GPL), inspected at commit `742e8c5` (2026-06-21).
Read on 2026-11-25 through a full-text extraction of the arXiv PDF (some formulas garbled; flagged below).

## Results

| Item | Statement in the paper | Our assessment |
|------|------------------------|----------------|
| Thm 6 | ‖n‖ for **all** n ≤ N in Õ(N) time | Rigorous within the paper (induction / LCA argument). Not needed for RQ-1. |
| Thm 7 | single n in O(n^{α/6+o(1)}) ≤ O(n^0.6875) | Rigorous asymptotically, given α. |
| Thm 8 | single n in O(n^{3/(9−α)+o(1)}) ≤ O(n^0.6154) | Same. The printed pseudocode (Alg. 2) mixes up f and f′ (f′ = complexity when the last operation is ·) and ignores rounding of n/d. The main-text interval argument carries the proof. |
| α | sup_{n>1} ‖n‖ / log₃ n ≤ 4.125 (Zelinsky, arXiv:2211.02995, cited as Lemma 1) | `LITERATURE`, not re-checked by us. It is only used to bound the additive part. |

## The key structural lemma, made rigorous for finite n

He uses (after Vivek–Shankar): if ‖n‖ = ‖i‖ + ‖n − i‖ with i ≤ n − i, then i ≤ L(n) = n^ℓ with
ℓ = α/3 − 1 ≈ 0.375. The paper derives this asymptotically from
3 log₃ i + 3 log₃(n − i) ≤ ‖n‖ ≤ α log₃ n.

**For a single target with a known good upper bound U, the same inequality is far stronger.**
i(n − i) ≤ 3^{U/3} gives i ≲ 2·3^{s/3}, where s = U − 3 log₃ n is the slack. For n = 2^61 − 1 and
U = 127, s ≈ 11.5, so i ≤ ~94. That is tiny, compared with n^{0.375} ≈ 10⁷. This is the basis of our
search (`research/proof-exact-search.md`). He's own implementation uses the same idea: it picks L(n)
per instance and prunes with defect-based lower bounds, rather than the worst-case n^ℓ from the theorem.

## Complexity: theory vs practice for our target

- Worst-case bound: n^0.6154 ≈ 2·10¹¹ basic steps at n ≈ 2.3·10¹⁸ (before n^{o(1)} factors).
- In practice: the worst case is driven by α (the *worst* n). Our n has slack ≈ 11.5 instead of the worst-case
  (4.125 − 3)·log₃ n ≈ 43. The budgeted search visited 8.7·10⁵ nodes and finished in 117 s (EXP-0002).
  **So the asymptotic bound is irrelevant for this target. The effective cost is set by the slack.**
- He reports no runtimes or memory figures. Appendix A runs targets up to ~10³⁸ (powers of 2,
  2^i 3^j 5^k, 2^i + 1, prime powers).

## The code (`hqztrue/integer_complexity`), inspected but not run

- `integer-complexity-128/single.cpp`: `dfs128(x, t)` "decides whether f(x) ≤ t" and
  returns the optimum if so. Additive parts i ≤ g[k], where g[k] is the largest value with k ones. Divisors come from
  factorization (C-RHO, quadratic sieve). Memo in hash maps. Lower bounds `complexity_LB` use a
  precomputed table of low-defect numbers (`gen_low_defect`). Their correctness depends on that table.
  `calc_single(n)` uses iterative deepening on t.
- It's structurally the same method as ours, written independently by a different author: a
  valuable **independent replication** (EXP-0003). Building and running it in our sandbox was blocked
  by the sandbox's safety policy for third-party code, so it awaits the lead's approval.
- `old/single64.cpp` restricts additive parts to i ≤ 36 with an additive budget D = 10. That is a
  *heuristic* restriction, valid only as an upper bound. Don't use it as evidence of exactness.
- License: GPL. We don't vendor or copy it. If we ever run it, we only cite it.

## Open points

- He's claim that α can be replaced by α₀ = limsup "for all but finitely many n" is given without proof.
  It doesn't matter for us.
- Recheck Zelinsky's α ≤ 4.125 if we ever rely on the worst-case bound. Currently we don't.
