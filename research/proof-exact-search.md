# Correctness of the budgeted exact search (`algorithms/exact_single.py`)

Status of this note: **PROVEN** (human-readable proof below). It still needs independent review
(planned in RP-0002). The proof covers the *algorithm*. Whether the *implementation* is correct is a
separate question, handled by tests, cross-checks and independent replication (EXP-0003).

## Setting

An *expression* is `1`, `(E + F)` or `(E · F)`. Its value v and its number of ones ℓ are defined
recursively, and ‖n‖ = min{ℓ(E) : v(E) = n}. Let T ≥ 1, and let c[m] = ‖m‖ for all m ≤ T. This is given
by an exact table, and we treat its correctness as a separate, tested fact (R-0100).

**Lemma 1 (Selfridge).** If v(E) = m then m³ ≤ 3^{ℓ(E)}. Hence ‖m‖ ≥ λ(m) := min{j : m³ ≤ 3^j}.

*Source and status.* `LITERATURE` (Selfridge, reported in Guy 1986. Iraids et al. 2012, Thm 1 and
Thm 3). Thm 3 gives the largest value with k ones as E(3j) = 3^j, E(3j+1) = 4·3^{j−1} and
E(3j+2) = 2·3^j. Each of these is ≤ 3^{k/3}, because 4/3 ≤ 3^{1/3} and 2 ≤ 3^{2/3}. The proof of the
E(k) formula is by strong induction on k, using E(i) + E(j) ≤ E(i + j) and E(i)·E(j) ≤ E(i + j)
(Iraids et al. 2012, §2). The naive induction on 3^{ℓ/3} alone does *not* close for sums, because
(3^{1/3} − 1)² < 1, which is why E(k) is needed. We also checked the E(k) formula computationally
for k ≤ 25 (`tests/test_exact_table.py::test_selfridge_maxima`). **TODO:** write out the E(k)
induction in full here, and formalize it in Lean (RQ-5).

**Lemma 2 (top-level decomposition).** For n ≥ 2,
‖n‖ = min( min_{1 ≤ x ≤ n/2} ‖x‖ + ‖n − x‖ , min_{d·e = n, 2 ≤ d ≤ e} ‖d‖ + ‖e‖ ).

*Proof.* An optimal expression for n ≥ 2 is not `1`, so it is a sum or a product of two
sub-expressions. The sub-expressions are themselves optimal for their values, or we could replace them.
Order the operands so the smaller value comes first. Factors of 1 never help, because ‖1·e‖ = 1 + ‖e‖ > ‖e‖. ∎

## The procedure

`at_most(m, k)` is supposed to return R(m, k) := min(‖m‖, k + 1).

1. If k < 1, return k + 1. (Every m needs at least one 1.)
2. If m ≤ T, return min(c[m], k + 1).
3. If m³ > 3^k, return k + 1. (Lemma 1.)
4. Memo: if ‖m‖ = e is stored, return min(e, k + 1). If "‖m‖ > j" is stored with j ≥ k, return k + 1.
5. Set best := k + 1. Invariant: *best − 1 is the largest value still worth finding*.
   - **Sums.** For x = 1, 2, … while 2x ≤ m: let y = m − x. If (xy)³ > 3^{best−1}, stop the loop.
     If c[x] < best − 1, set best := min(best, c[x] + at_most(y, best − 1 − c[x])).
   - **Products.** For each divisor d of m with 2 ≤ d ≤ e := m/d: skip if λ(d) + λ(e) > best − 1.
     Otherwise compute r := at_most(d, best − 1 − λ(e)). Skip if r > best − 1 − λ(e).
     Otherwise set best := min(best, r + at_most(e, best − 1 − r)).
6. If best ≤ k, store "‖m‖ = best". Otherwise store "‖m‖ > k". Return best.

**Theorem.** If the base table is correct, divisors are enumerated completely, and every
recursive call returns R(·,·) (induction on m, then on k), then `at_most(m, k)` returns R(m, k).

*Proof.* Steps 1–4 are immediate from Lemma 1 and the meaning of the memo entries (induction
hypothesis for earlier calls). For step 5, let V be the set of values ‖x‖ + ‖y‖ (sums) and
‖d‖ + ‖e‖ (products) over all splits of Lemma 2. Then ‖m‖ = min V. We show that the final best equals
min(min V, k + 1).

(i) *best only takes honest values.* Whenever best is updated, the new value is either k + 1 or a
sum r₁ + r₂ where r₁ ≥ the true complexity of one part and r₂ ≥ the true complexity of the other.
When r₂ ≤ its budget it is exact; otherwise it exceeds the budget and the sum exceeds the old
best − 1, so best doesn't decrease. In every update that lowers best, both parts are exact (within
budget), so best ∈ V ∪ {k + 1}.

(ii) *No split with value < best is skipped.* Take any split with value v ≤ best − 1, where best is its
value at the moment the split is considered.
- A sum split x + y has v ≥ 3 log₃ x + 3 log₃ y by Lemma 1, so (xy)³ ≤ 3^{v} ≤ 3^{best−1}. The
  loop stop condition fails at this x. Since xy = x(m − x) is increasing on [1, m/2], every x before
  the stopping point is visited and no later x can qualify. Also ‖y‖ ≥ 1, so ‖x‖ = c[x] ≤ v − 1 < best − 1,
  and the split isn't skipped. Then at_most(y, best − 1 − c[x]) returns ‖y‖, because
  ‖y‖ = v − c[x] ≤ best − 1 − c[x], and best becomes ≤ v.
- A product split d·e has ‖d‖ ≥ λ(d) and ‖e‖ ≥ λ(e), so λ(d) + λ(e) ≤ v ≤ best − 1. It isn't skipped.
  Also ‖d‖ = v − ‖e‖ ≤ best − 1 − λ(e), so r = ‖d‖ (exact) and the second skip doesn't apply. Then
  at_most(e, best − 1 − r) returns ‖e‖ = v − r, and best becomes ≤ v.

best only decreases, so these arguments hold at every moment. Hence the final best is
≤ min V whenever min V ≤ k, and by (i) it is never below min V. If min V > k, then by (i) best stays
k + 1. ∎

**Corollary.** If U is a verified upper bound (an expression with U ones), then
`at_most(n, U)` = ‖n‖. The run on n = 2^61 − 1 with U = 127 returned 127, so ‖2^61 − 1‖ = 127,
*conditional on a correct implementation and a correct base table*.

## Trust base of the computational claim

| Component | How it is checked |
|-----------|-------------------|
| Base table c[m], m ≤ 4·10⁸ (C) | Agrees with an independent Python implementation for m ≤ 20000. Agrees with literature values (‖3^k‖, ‖2^k‖, ‖1439‖, Selfridge maxima, Iraids Table 3 for k ≤ 28, Wang's counterexample). The pruning is rigorous (see algorithms/README.md). |
| Factorization | Miller–Rabin with the first 13 prime bases is deterministic below 3.3·10²⁴ (Sorenson–Webster 2015; to be cited and checked). Pollard rho only needs to *find* factors, and every result is checked by multiplication. Tested on 2^60 − 1. |
| Search | Proof above. It agrees with the exact table on 400+ random n (with a 300-entry base table) and with Iraids et al. Table 3 for k = 2…39. |
| Python big integers | Exact arithmetic. No floating point is used in any decision. |

**Not yet done:** an independent implementation by someone else (EXP-0003), and a review of this
proof (RP-0002).
