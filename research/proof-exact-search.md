# Correctness of the budgeted exact search (`algorithms/exact_single.py`)

## Status of this note (revised 2026-11-25 after the lead's review of PR #2)

| Part | What it is | Status |
|------|------------|--------|
| Lemma 1 (Selfridge bound) | Classical result. Full proof written below in this revision (it was a TODO before). | `LITERATURE`. Our write-up has been **self-checked only**. Its arithmetic facts are tested for k ≤ 300 (`tests/test_exact_table.py::test_lemma1_inequalities`). |
| Lemma 2, Theorem | Correctness of the *algorithm*, given its inputs | A complete written proof, **self-checked only**. It is a *conditional* theorem: it assumes a correct base table, complete divisor enumeration and a correct implementation. |
| Corollary (‖2^61 − 1‖ = 127) | Applies the theorem to one run | `COMPUTATIONALLY VERIFIED` (EXP-0002, replicated in EXP-0003). **Not** `PROVEN`. |

Under CLAUDE.md §4, `PROVEN` needs a proof that "has been checked". We do not count our own reading as that
check. So **no part of this note is labeled `PROVEN` until the independent review (RP-0002) is done.**
The proof covers the *algorithm*. The *implementation* is a separate question, handled by tests,
cross-checks, replication (EXP-0003) and, eventually, a certificate plus an independent checker.

## Setting

An *expression* is `1`, `(E + F)` or `(E · F)`. Its value v and its number of ones ℓ are defined
recursively, and ‖n‖ = min{ℓ(E) : v(E) = n}. Let T ≥ 1, and let c[m] = ‖m‖ for all m ≤ T. This is given
by an exact table, and we treat its correctness as a separate, tested fact (R-0100).

**Lemma 1 (Selfridge).** If v(E) = m then m³ ≤ 3^{ℓ(E)}. Hence ‖m‖ ≥ λ(m) := min{j : m³ ≤ 3^j}.

*Source.* `LITERATURE` (Selfridge, reported in Guy 1986; Iraids et al. 2012, Thm 1 and Thm 3).

*Proof (written by us 2026-11-25, self-checked, not yet reviewed).* Define E(1) = 1 and, for k ≥ 2,
E(3j) = 3^j, E(3j+1) = 4·3^{j−1}, E(3j+2) = 2·3^j. We show that **v(E) ≤ E(ℓ(E))** for every
expression E. We then show **E(k)³ ≤ 3^k**. Together they give the lemma. We only need the upper bound,
not that E(k) is attained.

(a) *E(k)³ ≤ 3^k.* E(1)³ = 1 ≤ 3. E(3j)³ = 3^{3j}. E(3j+1)³ = 64·3^{3j−3} ≤ 81·3^{3j−3} = 3^{3j+1}.
E(3j+2)³ = 8·3^{3j} ≤ 9·3^{3j} = 3^{3j+2}.

(b) *E is strictly increasing, so E(k+1) ≥ E(k) + 1.* The successive ratios are E(2)/E(1) = 2,
E(3j+1)/E(3j) = 4/3, E(3j+2)/E(3j+1) = 3/2 and E(3j+3)/E(3j+2) = 3/2. All are > 1, and the values are integers.

(c) *Products: E(i)·E(j) ≤ E(i+j) for i, j ≥ 1.* If i = 1 or j = 1, this is (b). Otherwise write
i = 3a + r and j = 3b + s with i, j ≥ 2. The cases are symmetric in (r, s):
- (0,0): 3^{a+b} = E(i+j).
- (0,1): 3^a·4·3^{b−1} = E(i+j).
- (0,2): 3^a·2·3^b = E(i+j).
- (1,1): 16·3^{a+b−2} ≤ 18·3^{a+b−2} = E(3(a+b)+2).
- (1,2): 8·3^{a+b−1} ≤ 9·3^{a+b−1} = E(3(a+b+1)).
- (2,2): 4·3^{a+b} = E(3(a+b+1)+1).

(d) *Sums: E(i) + E(j) ≤ E(i+j) for i, j ≥ 1.* If i = 1 or j = 1, this is (b). Otherwise
E(i), E(j) ≥ 2, so E(i) + E(j) ≤ E(i)·E(j) ≤ E(i+j) by (c), using x + y ≤ xy for x, y ≥ 2.

(e) *Induction on ℓ(E).* If E = `1`, then v = 1 = E(1). If E = F ∘ G with ∘ ∈ {+, ·}, then
ℓ(F), ℓ(G) ≥ 1 and ℓ(E) = ℓ(F) + ℓ(G). By induction v(F) ≤ E(ℓ(F)) and v(G) ≤ E(ℓ(G)), and + and · are
monotone on positive integers. So (c) or (d) gives v(E) ≤ E(ℓ(E)). ∎

A note on why E(k) is needed: induction on 3^{ℓ/3} alone does *not* close for sums, because
3^{1/3} + 3^{1/3} > 3^{2/3}. The same facts are checked by computer for k ≤ 300
(`test_lemma1_inequalities`), and E(k) is checked to be the exact maximum for k ≤ 25 against the table
(`test_selfridge_maxima`). **Still to do:** formalize this in Lean (RQ-5).

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

**Theorem (conditional).** If the base table is correct, divisors are enumerated completely, and every
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
| Factorization | Miller–Rabin with the first 13 prime bases is deterministic below 3.3·10²⁴ (Sorenson–Webster 2015; `UNVERIFIED` until we check the source). Pollard rho only needs to *find* factors, and every result is checked by multiplication. Tested on 2^60 − 1. |
| Search | Proof above. It agrees with the exact table on 400+ random n (with a 300-entry base table) and with Iraids et al. Table 3 for k = 2…39. |
| Python big integers | Exact arithmetic. No floating point is used in any decision. |

**Done:** independent replication by another author's program (EXP-0003, 60/60 agree, also with He's
defect pruning switched off). **Not yet done:** an independent review of this note (RP-0002), and a certificate
that can be checked without trusting either search program (EXP-0003 step 2).
