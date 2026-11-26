# EXP-0004 E. Lean formalization roadmap for ‖2^61 − 1‖ ≥ 127

Written 2026-11-25 by Claude Code, from the independent **Lean formalization specialist**'s report and the primary
agent's own rebuild of its proof of concept. Toolchain: Lean 4.35.0 (installed from the GitHub release zip), core Lean
only, no Mathlib.

## 1. What is kernel-checked

**Before EXP-0004:** only upper bounds. `upperBound_c_m61_ub127_board_pr4` and `upperBound_c_m61_ub127_icl_peel`
(‖N‖ ≤ 127, by `rfl`, no axioms) and the ≤ 150 baseline. No lower bound of any kind.

**Added on this branch** (`lean/IntegerComplexity/PoC/`, built by `lake build`, 0 `sorry`, listed in
`lean/scripts/CheckAxioms.lean`):

| Theorem | File | Content | Axioms |
|---------|------|---------|--------|
| `Expr.selfridge` | `Selfridge.lean` | e.eval³ ≤ 3^e.ones for every expression (via E(k), `emax_mul`, `emax_add`, `emax_cube`) | propext, Quot.sound |
| `lowerBound_of_cube` | `Selfridge.lean` | 3^j < m³ → ‖m‖ > j | propext, Quot.sound |
| `theoremC` | `Checker.lean` | Theorem C, with hypothesis 2 ≤ m and a lower-bound function sound below m | propext, Quot.sound |
| `checkAll_sound`, `lowerBound_of_check` | `Checker.lean` | a Bool checker over an ordered claim list is sound: `checkAll … cert = true`, `(n, j) ∈ cert` ⟹ `LowerBound n (j+1)` | propext, Quot.sound |
| `lowerBound_of_checkT` | `CheckerTrie.lean` | the same with earlier claims stored in a binary trie (O(log m) lookups). Soundness only needs "every stored entry is true", not a well-formed trie. | propext, Quot.sound |
| `PoC.M10.exact` | `Examples/M10.lean` | `HasComplexity 1023 22`: ‖2^10 − 1‖ = 22, from a 19-claim table-free certificate, by `decide +kernel` | propext, Quot.sound |

Commands (run by the primary agent after copying the specialist's files):

```bash
cd lean && rm -rf .lake && lake build          # Build completed successfully (9 jobs), about 3 s
lake env lean scripts/CheckAxioms.lean          # output as in the table above
```

The specialist also checked ‖2^15 − 1‖ = 32 (70 claims, 2 s) and ‖2^20 − 1‖ = 42 (547 claims, 15 s) in the kernel with the
same checker. The ‖2^20 − 1‖ file and the benchmark files are in [`lean-poc/`](lean-poc/) (not built by CI).

**Limitation of the PoC checker:** its product rule enumerates divisors by **trial division** up to √m. That is complete by
construction and needs no number theory, but it costs √m steps, so it cannot be used for m ≈ 2.3·10¹⁸.

## 2. Architecture

```
Basic.lean           Expr, eval, ones, UpperBound, LowerBound            (exists)
PoC/Selfridge.lean   E(k), Selfridge, λ-shortcut, sum cut-off            (done)
PoC/Checker.lean     theoremC, Bool rules, sequential checker soundness  (done; trial-division products)
PoC/CheckerTrie.lean trie-backed checker soundness                       (done)
Factor.lean          divisors from a verified factorization: complete    (M2)
Pratt.lean           Lucas criterion + binary powMod by fuel             (M3)
CertM61/*.lean       chunked certificate data + chunk theorems           (M4)
M61Exact.lean        HasComplexity (2^61-1) 127 := ⟨UB, LB⟩              (M5/M6)
```

The certificate to use is the **table-free** one built in this audit (3,068,111 records: 2,906,430 claims plus 161,681
Pratt records; 205 MB raw, 31 MB gzip). It needs no base table, so the 10⁸-entry table, which no kernel can load, is no
longer needed. The specialist measured the claim count against the base-table size: 1.00M claims at T = 10⁸, 1.87M at 10⁶,
2.87M at 10⁴, 2.905M at 10³, 2.908M at 100. A small table computed in Lean therefore saves almost nothing.

## 3. Options and trust levels

| Option | What is trusted | Estimated cost for N |
|--------|-----------------|----------------------|
| (a) reflective checker, `decide +kernel`, table-free certificate | **the Lean kernel only** (plus the two standard axioms) | ≈ 20 ms per claim measured (2.5–3 ms per split, linear in k = 20…26). 2.9M claims ≈ 16 h, times 1.5–2.5 for 61-bit keys and deeper tries, plus 161k Pratt records and ≈ 5 h of elaboration: **≈ 1–3 CPU-days**. Needs a plan and the lead's go-ahead (CLAUDE.md rule 11). |
| (b) small table computed in Lean | kernel only | no benefit (≈ 1% fewer claims at T = 10⁴) |
| (c) `native_decide` / `Lean.ofReduceBool` | the Lean compiler, the C toolchain and the GMP runtime in addition | minutes. Label it "formally verified modulo `native_decide`". |
| (d) (a) split into chunk theorems | kernel only | same total CPU, but lake builds modules in parallel (4+ cores) |

Micro-benchmark (specialist, `lean-poc/Bench.lean`, a cost model whose divisor lists are not proven complete):

| k | claims | splits | elaboration | `decide +kernel` | `native_decide` |
|---|--------|--------|-------------|------------------|-----------------|
| 20 | 547 | 2,679 | 3 s | ≈ 10 s | — |
| 24 | 1,506 | 8,801 | 8 s | ≈ 25 s | ≈ 6 s total |
| 26 | 3,053 | 22,414 | 19 s | ≈ 64 s | ≈ 18 s total |

Kernel notes from the specialist: Nat `+ − * / % gcd pow log2` and comparisons use GMP in the kernel, so 3^j is cheap.
Modular exponentiation must be a binary `powMod` by structural recursion on fuel; plain `Nat.pow` would compute a^(p−1) in
full, and well-founded recursion reduces badly in the kernel. List literals over ≈ 1,000 items need
`set_option maxRecDepth`; without it, the `def` silently becomes noncomputable.

The ≈ 1–3 CPU-day figure is an **extrapolation** from k ≤ 26 to k = 61. It has not been measured at that size.

## 4. Milestones

| ID | Work | Depends on | Effort (estimate) | Result |
|----|------|-----------|-------------------|--------|
| M1 | Selfridge, Theorem C, sequential checker, ‖1023‖ = 22 | — | done | `FORMALLY VERIFIED` lemmas |
| M2 | Product rule from a factorization, with a proof that the generated divisors are complete (needs Euclid's lemma / unique factorization; core Lean has `Nat.gcd`, `Nat.Coprime` but no unique factorization) | M1 | 3–6 days core Lean; less with Mathlib's `Nat.factorization` / `Nat.divisors` | sound checker usable for large m |
| M3 | Pratt/Lucas checker with a soundness proof (needs the order of a unit divides p − 1 and φ(p) = p − 1 ⇒ prime) | M2 (gcd facts) | 3–5 days core Lean; much less with Mathlib's `lucas_primality` (named from memory by the specialist, `UNVERIFIED`) | primes verified in the kernel |
| M4 | Converter: certificate JSONL → chunked Lean data files, plus a linking theorem across chunks | M2, M3 | ≈ 2 days | Lean certificate for N |
| M5 | Run with `native_decide`, labelled as such | M4 | minutes of CPU | "formally verified modulo native_decide" |
| M6 | Kernel-only run (`decide +kernel`, chunked, parallel) | M4, written plan, lead's approval | ≈ 1–3 CPU-days | `FORMALLY VERIFIED` (kernel only) |

**Decision for the lead:** M2 and M3 are much cheaper with Mathlib. Adding Mathlib means a far larger build and trust base
(still only the kernel and standard axioms, but much more library code). Staying in core Lean keeps the development small
and self-contained but costs about a week more.

## 5. Can the result realistically be fully formalized?

Yes. Nothing in the argument goes beyond elementary number theory. The heavy part (Selfridge, Theorem C, sequential
soundness) is already kernel-checked. The remaining proofs (M2, M3) are standard. The remaining risk is cost: a kernel-only
check is estimated at 1–3 CPU-days, which is feasible but needs approval. A `native_decide` run is cheap but trusts the
compiler. Until M2–M4 are done, **we must not claim `FORMALLY VERIFIED` for the lower bound.**
