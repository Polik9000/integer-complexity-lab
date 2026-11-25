# Certificate architecture for lower bounds ‖n‖ > j (EXP-0003 step 2)

**Status of this document:** design specification, written 2026-11-25. It has not been reviewed yet. **Implemented the same day** (EXP-0003 step 2). Two small additions were made during implementation and are part of the spec: the primes in `f` must be strictly increasing, and the header `table.format` field is informational.
**Goal:** turn "two programs say ‖2^61 − 1‖ = 127" into a claim that anyone can check without trusting either
search program. The trust base should be small, explicit and readable.
**Gate:** the lead asked us not to extend the ‖2^k − 1‖ table to larger k until this architecture is
sufficiently specified. This document is that specification.

## 1. What is certified

The upper bound ‖N‖ ≤ 127 already has certificates: explicit expressions, checked by
`certificates/verify.py` and kernel-checked in Lean. The certificate specified here proves the
**lower bound** ‖N‖ > 126. Together they give ‖N‖ = 127.

A *claim* is a pair (m, j) meaning **G(m, j): ‖m‖ > j**, i.e. no expression for m uses ≤ j ones.

## 2. Mathematical basis

We use the following, all stated and proved in [`proof-exact-search.md`](proof-exact-search.md):
- **Lemma 1 (Selfridge).** ‖m‖ ≥ λ(m) := min{ j : m³ ≤ 3^j }, and ‖m‖ ≥ 1.
- **Lemma 2 (decomposition).** For m ≥ 2, every expression for m is a sum x + y (1 ≤ x ≤ m/2) or a product
  d·e (2 ≤ d ≤ e, de = m) of two expressions. So ‖m‖ = min over these splits of ‖·‖ + ‖·‖.
- **Fact S (sum cut-off).** If ‖x‖ + ‖y‖ ≤ j then (xy)³ ≤ 3^j, by Lemma 1. On 1 ≤ x ≤ m/2 the product
  x(m − x) is increasing. So only the x before the first failure of (x(m − x))³ ≤ 3^j can matter.

**Theorem C (soundness of the checker rules).** Let LB be any function with LB(v) ≤ ‖v‖ for all v. Suppose
that for m ≥ 2:
(a) for every x with 1 ≤ x ≤ m/2 and (x(m − x))³ ≤ 3^j: LB(x) + LB(m − x) > j; and
(b) for every divisor d of m with 2 ≤ d ≤ m/d: LB(d) + LB(m/d) > j.
Then ‖m‖ > j.

*Proof.* Take any split in Lemma 2. A sum split with (x(m − x))³ > 3^j has ‖x‖ + ‖m − x‖ > j by Fact S.
Every other sum split, and every product split, has ‖p‖ + ‖q‖ ≥ LB(p) + LB(q) > j by (a) or (b).
So every expression for m has more than j ones. ∎

The checker builds LB incrementally. Each accepted claim G(m, j) raises LB(m) to j + 1. Children
always have **smaller values** than their parent: x, m − x < m, and d, m/d < m. So we can argue by strong
induction on m: if every claim the checker used for smaller values is true, then the new claim is true.
Cycles are impossible. Only the *order of the records* matters for streaming, and the format requires
it (§4).

## 3. Trust base

| Component | Role | How it is made trustworthy |
|-----------|------|----------------------------|
| Lemmas 1, 2, Theorem C | the mathematics | written proofs (self-checked; review in RP-0002); later Lean (§7) |
| The checker program | applies Theorem C to each record | ~150 lines of Python, standard library only, **no imports from `algorithms/`**. Written from this spec, not from the search code. Negative tests (§6). |
| Base table c[v], v ≤ T | LB(v) for small v | **Only used as a lower bound**, so it only needs c[v] ≤ ‖v‖. T = 10⁸ for the certificate: every entry is then cross-checked against **He's independent table** (Fuller's algorithm, run with the lead's approval) for all v ≤ 10⁸, not just a sample. The file is identified by its SHA-256. |
| Primality of the factors | completeness of the divisor list in (b) | **Pratt certificates** inside the certificate, checked by modular exponentiation. No Miller–Rabin and no cited bases in the trust base. |
| Python big integers | arithmetic | exact; no floating point anywhere in the checker |

**Not in the trust base:** the search program, its factorizer, its memo logic and its pruning heuristics.
A bug there can only make the certificate *fail to check*. It cannot make a false claim check.

## 4. Format (`.jsonl`, one JSON object per line, gzip-compressed)

```
{"type":"header","version":1,"target":"2305843009213693951","claim_gt":126,
 "table":{"T":100000000,"sha256":"…","format":"uint8, index v = ||v||, v=0 unused"},
 "generator":{"code":"algorithms/exact_single.py","commit":"…"}}
{"type":"prime","p":P,"a":A,"q":[Q1,Q2,…]}          # Pratt: P prime, A a witness, Qi = distinct primes of P-1
{"type":"claim","m":M,"j":J,"f":[[P1,E1],[P2,E2],…]} # G(M,J); f = full prime factorization of M
…
{"type":"end","records":R}
```

- Numbers are JSON integers (Python reads them exactly). The `m` field is a decimal string only if a JSON
  tool needs it. Version 1 uses plain integers.
- **Order:** every prime record comes before any record that uses it. Every claim that a later record
  relies on comes before it. The search emits claims in post-order (a node is finished after its
  children), which gives this order for free.
- Several claims for the same m are allowed. The checker keeps the largest accepted j.
- The last claim must be G(target, claim_gt). The `end` record guards against truncation.

## 5. Checker algorithm (normative)

**Version 2 rules (added 2026-11-25 after the EXP-0004 audit, findings F1, F2, M1, F5–F7).** These apply on top of the rules below.
- **Integers only.** Every numeric field must be a JSON integer token. Floats (`1.0`, `1e0`), `NaN`, `Infinity` and booleans are
  rejected. The cause was F1: a float factor prime equals the verified int prime in Python, and the float product can round a wrong
  factorization to m, so true divisors were never enumerated and a false claim was accepted.
- **Strict JSON.** Duplicate keys are rejected. Every line must be an object. Records must have exactly the fields of §4; the header
  may also carry `generator`, and `table` may also carry `format`.
- **Header.** `version` is the integer 1. `target` is a canonical decimal string (no sign, no leading zero). `claim_gt` is an integer
  ≥ 0. `table.T` is an integer equal to the table length − 1. T must be ≥ 1, so the table holds at least ‖1‖ = 1.
- **Claims.** m ≥ 2, which Lemma 2 and Theorem C require (M1). Claims with j > 3·bitlen(m) are rejected early: such claims are false,
  since ‖m‖ ≤ 3 log₂ m, and rejecting them only avoids a long loop. Exponents satisfy 1 ≤ e ≤ bitlen(m).
- **Prime records.** For p ≥ 2^16 the q list is strictly increasing.
- **End.** The last claim must be the target claim, with j ≥ claim_gt.
- **Binding (F2).** The checker takes the *expected* target, claim_gt and table SHA-256 as inputs. It rejects the certificate unless the
  header matches them, and it prints the SHA-256 in the verdict. Every error, including I/O and gzip errors, gives `REJECTED` and exit 1.

State: `table` (bytes, length T + 1), `primes` (a set of verified primes), `proven` (a dict m → largest
accepted j).

`LB(v) = c[v]` if v ≤ T, otherwise `max(1, λ(v), proven.get(v, -1) + 1)`, where λ(v) = min{j : v³ ≤ 3^j}
is computed in integers.

- **header:** check the version, and check that the table file's SHA-256 equals the header's.
- **prime (p, a, q):** require 2 ≤ p. If p < 2^16, check primality by trial division (and q may be empty).
  Otherwise require:
  - every Qi to be in `primes` or < 2^16 and trial-division prime;
  - p − 1 to be divisible by the Qi only (divide them all out repeatedly and reach 1);
  - a^(p−1) ≡ 1 (mod p) and a^((p−1)/Qi) ≢ 1 (mod p) for every i.

  Then add p to `primes`. (This is Lucas's theorem: a has order p − 1, so p is prime.)
- **claim (m, j, f):** require m > T, j ≥ 0, ∏ Pi^Ei = m, and every Pi ∈ `primes` (or < 2^16 and checked).
  If j < λ(m) the claim holds by Lemma 1. Accept it and stop here. Otherwise:
  - **Sums:** for x = 1, 2, …, while 2x ≤ m and (x(m − x))³ ≤ 3^j, require LB(x) + LB(m − x) > j.
  - **Products:** for every divisor d of m (generated from f) with 2 ≤ d ≤ m/d, require
    LB(d) + LB(m/d) > j.

  If both pass, set proven[m] = max(proven.get(m, −1), j).
- **end:** require the record count to match, and require proven[target] ≥ claim_gt.

If any check fails, the checker reports the line number and exits non-zero. The verdict is **"‖target‖ > claim_gt"**.

The checker needs no hints. It recomputes every split, and it only needs the claims to *exist*. So a
certificate cannot leave out a split by mistake.

## 6. Validation of the checker

1. **Positive:** small targets with a brute-force check against the full table. For example, generate certificates
   for random n ≤ 10⁸ with a small artificial T (say 10³), and check that G(n, ‖n‖ − 1) is accepted.
   Also check the Iraids Table 3 values k ≤ 26.
2. **Negative (mutation tests):** each must be rejected.
   - j raised by one at the root;
   - one claim deleted;
   - a claim moved after its first use;
   - a wrong factor or a missing prime factor;
   - a composite presented as prime;
   - a Pratt witness of the wrong order;
   - a table entry *increased* by one (so the SHA-256 differs);
   - a truncated file.
3. **Claim G(n, ‖n‖) must fail** for every small test n (the checker must not accept true-but-unproved claims).
4. Review: the checker goes into RP-0002 together with this spec.

## 7. Path to `FORMALLY VERIFIED` (later, RQ-5)

The checker rules are simple enough to write in Lean as a `Bool` function, `check : Cert → Bool`, with a
proof `check c = true → ‖target‖ > j` (from Theorem C and Lemma 1). The obstacle is the base table: 10⁸
entries cannot go through the kernel. Two options:
1. Make certificates with a small T, say 10⁴, and a table computed inside Lean. This means many more claims, and
   we would need to measure it on a pilot (k ≈ 30–40).
2. Use `native_decide` on the full certificate. This is a weaker standard: it trusts the compiler. If we did this,
   we would label it as such.

## 8. Cost estimate for N = 2^61 − 1 (cheap class)

| Item | Estimate | Basis |
|------|----------|-------|
| Generation (Python search + emitter, T = 10⁸) | 3–10 min CPU, ≤ 4 GB RAM | EXP-0002: 117 s and 866k nodes at T = 4·10⁸. A smaller T means more nodes; we will measure this. |
| Certificate size | ~1–3·10⁶ claims, ~100–300 MB raw, ~30–100 MB gzip | ~80–100 bytes per claim, plus Pratt records |
| Checking (Python) | 5–15 min CPU, ~1–2 GB RAM | ≤ ~100 sum splits and a few divisor pairs per claim; the table is 100 MB |
| Table cross-check against He's dump (v ≤ 10⁸) | < 1 min | byte comparison; needs one more run of He's code (driver change only) |

If generation or checking exceeds 30 min CPU, we stop and report back before going on (CLAUDE.md rule 11).
The certificate itself is **not committed**. We record its SHA-256 and size, keep a copy in project files, and
document how to regenerate it.

## 9. Implementation plan

1. `certificates/lower/check_lower.py`: the checker, written from §5 only.
2. `algorithms/exact_single.py`: an optional emitter hook. When a memo entry is stored, it writes the claim
   (exact e → G(m, e − 1); gt → G(m, k)), plus Pratt records for any new primes.
3. Tests: §6 (1)–(3), plus a test that the search's results are unchanged when the emitter is on.
4. EXP-0003 step 2: generate and check for 2^61 − 1, and record runtimes, sizes and hashes.
5. Table cross-check against He's table for v ≤ 10⁸.
6. Update RESULTS: R-0007 would become "`COMPUTATIONALLY VERIFIED`, with an independently checked certificate". It
   stays **not `PROVEN`** until the checker and the mathematics have been reviewed. A Lean checker (§7) would
   be the route to `FORMALLY VERIFIED`.
