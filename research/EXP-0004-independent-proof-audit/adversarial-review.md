# EXP-0004 D. Adversarial review

Written 2026-11-25 by Claude Code. Sources: the independent **adversarial reviewer** (a subagent told to assume the claim
is wrong and to break the checker; its run was interrupted once by a usage limit, then resumed and completed; its final
report agrees with everything below), plus the primary agent's own attacks. The reviewer's scripts stayed in session scratch space; the attacks that matter are reproduced by
committed tools and tests.

## 1. Summary

- **The real certificate survived every attack.** Every mutation of it was rejected: root raised to 127, a mid-file claim
  deleted, an exponent bumped. It contains nothing that any successful attack needs.
- **The checker `check_lower.py` can be made to accept false statements** with crafted input. Two families of attacks work:
  float factor primes (F1, critical) and degenerate tables, T ≤ 0, with m = 1 (M1, low). Header games (F2) also produce a
  misleading `ACCEPTED` line. None of these can be produced by our emitter, and none occurs in the real certificate.
- **No expression with ≤ 126 ones was found** by a cheap independent heuristic. This is weak evidence, as expected.
- **Table spot checks:** an independent DP agrees with the 10⁸ table on every v ≤ 2·10⁶, and structural invariants hold on
  the whole table.

## 2. Successful attacks (false statements accepted by `check_lower.py`)

| # | Attack | Accepted statement | Why it works | Reproducer |
|---|--------|--------------------|--------------|------------|
| A1 | Float factor primes, genuine 10⁸ table | ‖2^8·3^32‖ > 112 (false: 2^8·3^32 has a 112-ones expression) | `f` = [[578528833.0,1],[819964609.0,1]]; their true product is m + 1, but the float product rounds to m. The true divisors 2, 3, … are never tried. | reviewer's `attack_float_factor.py` (scratch) |
| A2 | Same, T = 1000 | ‖2^8·3^33‖ > 115 (false) | Product of the true primes is m − 97 | same |
| A3 | Same, T = 50, one float prime | ‖4·3^33‖ > 103 (false) | 83 · 267906533327977 = m − 1 | [`tools/float_factor_attack.py`](tools/float_factor_attack.py), `tests/test_exp0004_strict_checker.py::test_orig_rejects_float_factor` (strict xfail) |
| A4 | Table of length 1 (T = 0), claim m = 1 | ‖1‖ > 100 | m = 1 has no splits, and Theorem C's m ≥ 2 is not checked | reviewer's battery |
| A5 | T = 0, then cascade | ‖2‖ > 11, ‖3‖ > 60 | A4 makes LB(1) huge, so the splits of 2 and 3 are "refuted" | reviewer's battery |
| A6 | Empty table (T = −1) | ‖1‖ > 5 | as A4 | reviewer's battery |
| A7 | T = 0, `"m": true` | ‖1‖ > 5 | `bool` is an `int` in Python, and then A4 applies | reviewer's battery |

**Misleading verdicts (not false mathematics, but a false-looking `ACCEPTED`):** `claim_gt` = NaN, −Infinity or −1 with no
claims at all; a duplicate `claim_gt` key (126, then −1; a reader of the first key sees 126); `"version": true`;
`"T": 1000.0`. All exit 0. They matter because `run_cert.sh` checks only the exit code.

**Also accepted, harmless:** exponent `e: true` (treated as 1).

All of A1–A7 are **rejected by the strict checker** written in this audit, which requires exact ints, m ≥ 2, and an expected
target, claim and table SHA given on the command line.

## 3. Failed attacks (correctly rejected)

- Wrong table SHA-256; claim m ≤ T; j < 0, j = 1e3, j = NaN; m given as a string; `f` given as a dict or nested wrongly;
  float `q` in a Pratt record (fails at `pow`); a composite p, a wrong-order witness, a q that does not divide p − 1, a small
  composite, the Carmichael number 3215031751 presented as prime (each tested alone with a trivially true target, by the
  implementation auditor); m = 0; a correct table with the false claim ‖2‖ > 2; `claim_gt` 126.5 or "126"; target string
  "2305843009213693951.0".
- **Mutations of the real certificate:**
  - root raised to > 127: rejected at the split 1 + (N − 1), because ‖N − 1‖ ≤ 2 + ‖2^60 − 1‖ = 126. This was checked for both
    the EXP-0003 certificate and the table-free one.
  - a claim in the middle deleted (m = 246035318951): rejected at the product split 2 · 246035318951.
  - an exponent bumped: rejected ("factorization does not multiply to m").
  - a deleted claim with the record count fixed, a claim moved after the root, the root dropped with the count fixed: all
    rejected (implementation auditor).

## 4. Attempts to refute the claim itself

- **Upper-bound heuristic** (independent of our search): a memoized "peel" search n = d·m + r with different parameters
  found 129 ones at best (C = 2, D = 50 and C = 6, D = 300; 0.3 s and 3.2 s). It found nothing ≤ 126, and nothing ≤ 127 either.
  This is a weak test, since a heuristic failing to find something proves nothing.
- **Table consistency:**
  - an independent naive DP agrees with the 10⁸ table for every v ≤ 2·10⁶ (0 mismatches), and with OEIS A005245 for n ≤ 30;
  - spot values agree: ‖1439‖ = 26, ‖3^16‖ = 48, ‖2^26‖ = 52, ‖2·3^16‖ = 50;
  - on the whole table, λ(v) ≤ c[v] ≤ c[v − 1] + 1, c[2v] ≤ c[v] + 2 and c[3v] ≤ c[v] + 3 hold everywhere.
  These checks cannot detect a value that is too large but self-consistent beyond 2·10⁶. That gap is closed differently, by
  the table-free certificate (§5).

## 5. Circularity and hidden trust

| Question | Answer |
|----------|--------|
| Does the checker trust the search? | No. It recomputes every split; a search bug can only make the certificate fail. |
| Does the checker trust the table? | **Yes, for the EXP-0003 certificate**: c[v] ≤ ‖v‖ for v ≤ 10⁸. That table came from our C program and was cross-checked byte-for-byte against He's table. But the comparison was made by the same agent, and its value rests on He's code being independent. **No, for the table-free certificate**: its only table entry is ‖1‖ = 1. All 999 values v ≤ 1000 and every larger value it uses are re-proved by claims. |
| Same author everywhere? | Yes. The search, emitter, both checkers, the spec and the proofs were all written by Claude (same model family). The mathematical lemmas are now kernel-checked in Lean, which removes that dependence for Selfridge and Theorem C. **The checker code itself has had no human review.** |
| Does the verdict bind to the right statement? | With `check_lower.py`, only if a human reads the printed target and claim. With the strict checker, yes: they are command-line inputs. |
| Is any branch of the proof omitted? | No. Sum splits up to the cut-off, all divisor pairs including d = √m, the λ shortcut and the ordering are all covered (and the Lean `theoremC` has exactly these cases). |

## 6. Unresolved concerns

1. No **human** has reviewed the checker code or the proofs. The planned RP-0002 review is still needed, and the Lean PoC
   covers only the mathematics, not the Python code.
2. `check_lower.py` remains unfixed on this branch, by instruction. The F1 hole stays documented by a strict xfail test.
3. Python, `json` and `gzip` are trusted. A Lean-checked run would remove this (roadmap M4–M6).
4. A kernel-only Lean run of the full certificate is estimated, not measured.
5. The reviewer did not try to forge a false claim about N itself with the float trick. That would need a
   float-representable number above 2^53 in the derivation tree. It is irrelevant to our certificates, which contain no
   floats, but it is the reason F1 must be fixed before `check_lower.py` is used on third-party certificates.
6. Independent table comparison covers v ≤ 2·10⁶ only. Above that, only invariants and He's byte comparison (EXP-0003, not
   re-run) support the table. This matters only for the EXP-0003 certificate, not the table-free one.
