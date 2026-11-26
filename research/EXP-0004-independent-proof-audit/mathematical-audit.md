# EXP-0004 B. Mathematical audit of ‖2^61 − 1‖ ≥ 127

Written 2026-11-25 by Claude Code (primary agent). It merges the primary agent's own reconstruction with the
independent **mathematical proof auditor** (a separate subagent that saw the proof notes and the checker but none
of the primary agent's conclusions; its full report is summarized in [`agent-disagreement-log.md`](agent-disagreement-log.md)).
Statuses follow CLAUDE.md §4.

## 1. The statement and what it rests on

Let N = 2^61 − 1. The claim ‖N‖ = 127 splits into:

| Part | Content | Evidence | Status after this audit |
|------|---------|----------|-------------------------|
| U | ‖N‖ ≤ 127 | two explicit 127-ones expressions, kernel-checked in Lean (`lean/IntegerComplexity/Certificates/M61.lean`, no axioms) | `FORMALLY VERIFIED` (unchanged) |
| L | ‖N‖ > 126 | a certificate of claims "‖m‖ > j" accepted by a checker that applies the rules below | `COMPUTATIONALLY VERIFIED`, with the mathematics behind the rules now partly `FORMALLY VERIFIED` (§6) |

U is not used anywhere in the proof of L. U only turns L into an equality.

## 2. Reconstructed proof of L (all hypotheses numbered)

Definitions. An expression is `1`, `(E + F)` or `(E · F)`; v(E) is its value and ℓ(E) its number of ones.
‖n‖ = min{ℓ(E) : v(E) = n}. G(m, j) means "‖m‖ > j", i.e. every expression for m has more than j ones.
λ(m) := min{j ≥ 0 : m³ ≤ 3^j}.

**Lemma 1 (Selfridge).** For every expression E, v(E)³ ≤ 3^{ℓ(E)}. Hence ‖m‖ ≥ λ(m), and G(m, j) holds whenever j < λ(m).

*Proof.* Define E(1) = 1, E(2) = 2, E(3) = 3, E(4) = 4 and E(k + 3) = 3·E(k). (This agrees with the note's
E(3j) = 3^j, E(3j+1) = 4·3^{j−1}, E(3j+2) = 2·3^j for k ≥ 2.) Show v(E) ≤ E(ℓ(E)) by structural induction, using
E(i)·E(j) ≤ E(i + j) and E(i) + E(j) ≤ E(i + j) for i, j ≥ 1, and then E(k)³ ≤ 3^k. ∎

Audit: both the primary agent and the independent auditor re-derived all six product cases (r, s) ∈ {0,1,2}²,
the cases i = 1 or j = 1 (which reduce to E(k + 1) ≥ E(k) + 1) and k = 1…4. The sum case uses x + y ≤ xy for x, y ≥ 2,
which is valid because E(i) ≥ 2 for i ≥ 2. The auditor checked the inequalities by script for k < 400 and that E(k) is
the true maximum for k ≤ 14 by unfiltered enumeration. **The whole lemma is now kernel-checked in Lean**
(`Expr.selfridge : e.eval ^ 3 ≤ 3 ^ e.ones`, `lean/IntegerComplexity/PoC/Selfridge.lean`, axioms `[propext, Quot.sound]`).
Status: `LITERATURE + FORMALLY VERIFIED`.

**Lemma 2 (decomposition).** Let m ≥ 2 and let E be an expression for m. Then E = F + G with v(F) + v(G) = m, or
E = F · G with v(F)·v(G) = m.

Audit: correct, but the existing note words it as a statement about "optimal expressions" and dismisses factors of 1
informally. The precise version needed for a *lower* bound is:

- (H1) For a sum, order the operands so that x := min(v(F), v(G)) ≤ m/2. Then ℓ(E) ≥ ‖x‖ + ‖m − x‖ with 1 ≤ x ≤ m/2.
- (H2) For a product with both factor values ≥ 2, order them so that d := min ≤ m/d. Then ℓ(E) ≥ ‖d‖ + ‖m/d‖ with
  2 ≤ d ≤ m/d and d | m.
- (H3) For a product with a factor of value 1, the other factor F has v(F) = m and ℓ(F) < ℓ(E). So it is enough to bound
  ℓ(F). This is an induction on ℓ(E) (or on the structure of E), **not** on m.

The Lean proof of Theorem C handles (H3) exactly this way: by structural induction on the expression. So no strong
induction on m is needed for the factor-1 case. This is a wording gap in `research/proof-exact-search.md`, not an error.

**Fact S (sum cut-off).** If ‖x‖ + ‖m − x‖ ≤ j then (x(m − x))³ ≤ 3^j (Lemma 1 twice). The function x ↦ x(m − x) is strictly
increasing on the integers 1 ≤ x ≤ ⌊m/2⌋. So, if the test (x(m − x))³ ≤ 3^j fails at some x, it fails for all larger
x ≤ m/2. The checker's loop "while 2x ≤ m and (x(m − x))³ ≤ 3^j" therefore visits every sum split that could have
‖x‖ + ‖m − x‖ ≤ j. The non-strict `≤` is the correct direction. Status: `PROVEN` (by both agents) and
`FORMALLY VERIFIED` (`mul_sub_mono`, `ones_gt_of_prod_cube`, used inside `sumsFrom_sound`).

**Theorem C (one claim).** Let m ≥ 2 and j ≥ 0. Let LB be a function with LB(v) ≤ ‖v‖ for every v < m. Suppose
(a) LB(x) + LB(m − x) > j for every 1 ≤ x ≤ m/2 with (x(m − x))³ ≤ 3^j, and
(b) LB(d) + LB(m/d) > j for every divisor d of m with 2 ≤ d ≤ m/d.
Then ‖m‖ > j.

*Proof.* Take any expression E for m and induct on its structure. Sums: by Fact S if outside the cut-off, otherwise by
(a), since ℓ(F) ≥ ‖x‖ ≥ LB(x) and likewise for the other part. Products with both factors ≥ 2: by (b). Products with a
factor 1: by the induction hypothesis applied to the other factor (H3). ∎

Kernel-checked as `theoremC` in `lean/IntegerComplexity/PoC/Checker.lean`, with exactly these hypotheses
(`hm : 2 ≤ m`, `hlb : ∀ v, v < m → LowerBound v (lb v)`). Status: `FORMALLY VERIFIED`.

**Certificate induction.** Records are processed in file order. When claim number t is checked, LB(v) is
max(1, λ(v), j' + 1) over already-accepted claims G(v, j') (plus, for the EXP-0003 certificate, the table value for
v ≤ T). Every value it is applied to (x, m − x, d, m/d) is < m. By induction on t, every accepted claim is true, provided
(H4) the table entries satisfy c[v] ≤ ‖v‖, and (H5) the divisor list in (b) is complete. Well-foundedness comes from the
record order, not from any property of the search. Kernel-checked as `checkAll_sound` / `lowerBound_of_check` (for a
checker that enumerates divisors by trial division, see §6).

**Divisor completeness (H5).** The checker generates the divisors from a factorization f = ∏ p_i^{e_i} with strictly
increasing p_i, each p_i verified prime, and checks ∏ p_i^{e_i} = m. By unique factorization, the products
∏ p_i^{a_i} with 0 ≤ a_i ≤ e_i are exactly the divisors of m, each listed once. This is `PROVEN` (textbook), **provided the
arithmetic is integer arithmetic** — see finding F1 below; it is not yet formalized.

**Pratt / Lucas (H6).** If p ≥ 2, a^{p−1} ≡ 1 (mod p), and a^{(p−1)/q} ≢ 1 (mod p) for every prime q | p − 1 (and the q
listed are all the primes of p − 1, as checked by dividing them out to 1), then a has order p − 1 in (ℤ/pℤ)*, so
φ(p) ≥ p − 1 and p is prime. Primes q < 2^16 are verified by trial division; larger q need their own earlier record.
Status: `PROVEN` (Lucas 1876; textbook), not yet formalized here.

## 3. Strict versus non-strict inequalities (all checked)

| Place | Relation | Correct? |
|-------|----------|----------|
| λ(m) | least j with m³ ≤ 3^j | yes; `lam()` computes it with integers only |
| shortcut | accept G(m, j) if j < λ(m) | yes: ‖m‖ ≥ λ(m) > j |
| sum cut-off | loop while (x(m − x))³ ≤ 3^j | yes (Fact S) |
| refutation | LB(p) + LB(q) > j | yes: then ℓ ≥ j + 1 for that split |
| conclusion | proven[target] ≥ claim_gt ⇒ ‖target‖ > claim_gt | yes |
| final | ‖N‖ > 126 and ‖N‖ ≤ 127 ⇒ ‖N‖ = 127 | yes |

## 4. Gaps and errors found

| ID | Where | Kind | Severity | Effect on ‖N‖ = 127 |
|----|-------|------|----------|---------------------|
| M1 | Checker vs Theorem C | Theorem C needs **m ≥ 2**. `check_lower.py` only requires m > T. With a table of length 1 (T = 0) it accepts the false claim ‖1‖ > 50 (demonstrated by the independent auditor). | low | none: the real certificate has T = 10⁸, so every claim has m > 10⁸ |
| M2 | Checker vs (H5) | Divisor completeness assumes **integer** arithmetic. The checker never checks that factor primes are ints; a JSON float such as `267906533327977.0` compares equal to the verified int prime, and the float product can round to m. Then the true divisors are never enumerated. **Demonstrated: a false claim is accepted** (finding F1, see [`adversarial-review.md`](adversarial-review.md)). | critical for the checker as a tool | none: the real certificates contain only integer tokens (checked by two parsers that reject floats) |
| M3 | `proof-exact-search.md`, Lemma 2 | factor-1 products dismissed for "optimal" expressions only; the lower-bound argument needs (H3) | wording | none |
| M4 | `proof-exact-search.md`, procedure step 5 | reads c[x] without saying x ≤ T (the code raises an error if not) | wording | none |
| M5 | `lit-AltmanZelinsky2012.md` | the "n = 1 is the only number with δ = 1" step is unnecessary: δ(N) = 1 would need 3 log₃ N + 1 ∈ ℤ, impossible since 3 log₃ N is irrational. The ≥ 117 result should be labelled `LITERATURE` (relative to a checked citation), not `PROVEN`. | wording / status | none |

No error was found in Lemma 1, Fact S, Theorem C, the certificate induction or the Lucas criterion.

## 5. Mathematical theorems versus computational assumptions

**Mathematical (proved; most now machine-checked):** Lemma 1, Lemma 2 (H1–H3), Fact S, Theorem C, the
certificate induction over record order, unique factorization ⇒ divisor completeness, Lucas' criterion.

**Computational assumptions (trusted, not proved):**
1. The checker program implements the rules exactly (two Python implementations; both written by Claude).
2. CPython's integer arithmetic, `pow(a, b, m)`, `json` and `gzip` are correct.
3. The certificate file contains only JSON integers in numeric fields (verified for both real certificates; it matters only for `check_lower.py`).
4. **For the EXP-0003 certificate only:** c[v] ≤ ‖v‖ for v ≤ 10⁸ (our C table, byte-identical to He's independent table).
   **This assumption is removed by the table-free certificate** built in this audit (see README §3).
5. Someone confirms that the verdict names target 2^61 − 1 and claim 126 (the strict checker enforces this itself).

No step uses the search program, Miller–Rabin, floating point, or He's defect list.

## 6. What is kernel-checked after this audit

`lean/IntegerComplexity/PoC/` (core Lean 4.35.0, no Mathlib, no `sorry`; all axioms ⊆ `[propext, Quot.sound]`):
- `Expr.selfridge`, `lowerBound_of_cube` (Lemma 1 and the shortcut);
- `theoremC` (Theorem C with the m ≥ 2 hypothesis);
- `sumsFrom_sound`, `prodsFrom_sound`, `checkClaim_sound`, `checkAll_sound`, `lowerBound_of_check`: a Bool-valued checker
  over a list of claims is sound. Its product rule uses **trial division** up to √m, so it is complete by construction but
  only usable for small m;
- `PoC.M10.exact : HasComplexity 1023 22`, i.e. ‖2^10 − 1‖ = 22, entirely in the kernel from a table-free certificate.

Not yet formalized: divisor generation from a factorization (H5), Lucas/Pratt (H6), and the run on the 2^61 − 1
certificate. See [`lean-formalization-roadmap.md`](lean-formalization-roadmap.md).

## 7. Verdict

The mathematics behind the lower-bound certificate is **correct**. Every lemma was reconstructed independently by two
agents, the core lemmas are kernel-checked in Lean, and no gap affects the claim. The two soundness holes found are in
the checker's input validation (M1, M2), not in the mathematics, and neither is triggered by the real certificate.
