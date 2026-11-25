# EXP-0004 C. Implementation audit

Written 2026-11-25 by Claude Code. It combines the independent **implementation auditor** (a subagent that read the code
without the primary agent's conclusions) with the primary agent's own checks. The auditor's scripts were kept in the
session scratch space and are not committed. Their results are quoted here. The soundness findings (F1, M1) and the certificate
checks are reproduced by committed tools in [`tools/`](tools/) and tests. The mutation-testing counts in F3/F4 are the
auditor's and were **not** re-run by a committed tool.

Code audited: `main` at `b7d85c9`. Its tree is identical to `8aba2e8`, the PR #3/#4 head.

## 1. Verdict

- **Search (`algorithms/exact_single.py`):** no bug found. Every split is enumerated. Budget and memo semantics are correct
  (an exact value versus "‖m‖ > j"). `min_ones_lower` starts from a float guess but then corrects it with exact integer
  loops. Miller–Rabin with the first 13 prime bases is deterministic for the range used. The search is **not** in the
  trust base of the certificate anyway.
- **C table (`algorithms/c/complexity_table.c`):** the DP and its pruning are rigorous. Integer widths are adequate: uint8
  sums do not wrap, and u128 cubes stay below 2^128. ASan/UBSan at N = 3·10⁶ is clean. Minor issues: `strtoull` input is not
  validated ("1e8" gives N = 1), and `fclose` is unchecked.
- **Checker (`certificates/lower/check_lower.py`):** it implements spec §5 for well-typed input, and it accepts the real
  certificate. But it has **one critical and one major input-validation hole** (F1, F2), and its tests miss nine
  weakened-checker mutants (F3, F4).
- **Real certificate:** not affected by any finding. It contains only JSON integers, no duplicate keys and exactly the
  spec's fields.

## 2. Findings

| ID | File:line | Severity | Description | Affects the real certificate? |
|----|-----------|----------|-------------|-------------------------------|
| F1 | `check_lower.py:89-98` | **critical** | The factor primes `p` in `f` are never type-checked. The float `p.0` equals the verified int prime (`in` set, `<`), and `prod *= p ** e` is computed in floating point, so `prod == m` can hold for a wrong factorization. The true divisors are then never enumerated, and **a false claim is accepted.** Found independently three times: by the primary agent (‖4·3^33‖ > 103 accepted with T = 50), the math auditor (‖2^7·3^30‖ > 104, T = 1) and the implementation auditor (‖2^8·3^32‖ > 112, with the genuine 10⁸ table). Reproducer: [`tools/float_factor_attack.py`](tools/float_factor_attack.py) and the strict xfail test in `tests/test_exp0004_strict_checker.py`. | **no**: 0 float/bool/null/NaN tokens, by two parsers that reject them |
| F2 | `check_lower.py:137-140,164`; `run_cert.sh` | major | The verdict is printed from header fields that are not type-checked. `claim_gt` set to NaN, −1 or 42.5, or given twice, still gives `ACCEPTED`. `target` goes through `int()`. The checker never takes the *expected* target, claim or table SHA, and `run_cert.sh` checks only the exit code. A certificate for another statement would also give exit 0. | no: header is `target "2305843009213693951"`, `claim_gt 126`, table SHA `34dbc4da…` |
| M1 | `check_lower.py:87` | low | Claims with m = 1 are allowed if T = 0; Theorem C needs m ≥ 2 (see the mathematical audit). | no (T = 10⁸) |
| F3 | `tests/test_certificate_lower.py:142-156` | major (tests) | The Pratt negative tests use target `"1"` with claim 0, which can never be established, so they are rejected at `end` whatever the prime record says. Mutants that remove the p − 1 factorization check, the witness-order check, the Fermat check, or the "q is prime" check all survive the test suite. | n/a |
| F4 | tests (whole file) | major (tests) | 11 of 23 weakened checkers still pass the suite; 9 of them are real holes. Surviving mutants include: sum test `< j`, sum check of x = 1 only, skipping d = √m, cut-off 3^(j−1), and no record count. There is no equality-boundary case, no case that needs x ≥ 2 or a square divisor, and no type tests. | n/a |
| F5 | `check_lower.py:118-148` | minor | A non-object line, a truncated gzip or a read error gives a traceback rather than `REJECTED`. The exit code is still 1, so this never produces a false accept. A huge j or exponent can make the checker hang (denial of service only). | no |
| F6 | `check_lower.py` | minor | `true` is accepted as 1; extra fields and duplicate keys are silently ignored. Harmless except through F1 and F2. | no |
| F7 | spec §4/§5 | minor | "The last claim must be the target" is not enforced (the checker's rule is weaker but sound). The spec allows string `m`, the checker rejects it. The spec has no "integers only" rule, which is the root cause of F1. | no |
| F9 | `certificates/verify.py:41-43` | minor | It prints the untrusted `n_form` label (a probe with n = 6 printed `OK ||2^61-1|| <= 5`) and accepts `ones` = 5.9 via `int()`. The m61 certificates themselves are fine, and their Lean versions are independent of this. | no |
| F10 | `complexity_table.c:25,39,73` | info | Unvalidated `strtoull`, unchecked `fclose`. | no |
| F12 | `.github/workflows/ci.yml` | info | Actions pinned by tag, not SHA; pytest unpinned; no smoke run of the lower-bound checker. | n/a |
| F13 | table independence | info | Our Python and C tables use the same algorithm (identical for n ≤ 10⁶). Independence at 10⁸ rests on He's table (EXP-0003), which this audit did not rebuild. **Moot for the table-free certificate.** | n/a |

## 3. Reproduction (commands actually run in this audit)

Environment: Intel Xeon @ 2.10 GHz container, 4 vCPU (1 used), 15 GB RAM, Python 3.13.18, gcc (Ubuntu 24.04), Lean 4.35.0.

| Command | Result |
|---------|--------|
| `python3 -m pytest -q` (before EXP-0004 changes) | 54 passed |
| `python3 certificates/verify.py` | 3 × OK |
| `bash experiments/EXP-0003-independent-verification/run_cert.sh WORK` | table SHA `34dbc4da…` OK; generation 191.6 s, 1,121,887 records, 120,212 primes; `ACCEPTED: ‖2305843009213693951‖ > 126`; wall time 4 m 13 s |
| Byte comparison, regenerated vs project-file certificate | **identical except the `generator.commit` header field** (`8aba2e8` vs `771b7a6`). The project copy matches the EXP-0003 SHA-256 (gzip `4f286d15…`, raw `b6d16f8f…`) |
| `tools/check_lower_strict.py` on the EXP-0003 certificate (pinned target, claim and table SHA) | `ACCEPTED`, 98 s; 1,001,675 claims, 120,212 primes, 1,417,031 sum checks, 15,291,147 product checks, longest sum loop 47, largest slack j − λ(m) = 10 |
| `tools/float_factor_attack.py` | `check_lower.py`: **ACCEPTED ‖22236242266222092‖ > 103** (false); strict checker: REJECTED (non-integer token) |
| `python3 -m pytest -q` (after) | 60 passed, 1 xfailed (the documented F1 hole) |

## 4. Certificate statistics (EXP-0003 certificate)

Measured by the implementation auditor and confirmed by the strict checker's counters:
- 1 header, 120,212 prime records, 1,001,675 claims, 1 end. 374,081 claims repeat an earlier m with a larger j.
- No claim uses the λ shortcut. The largest j is 126 (the root); the largest exponent is 31.
- Sum-loop lengths: 1 → 788,039 claims, 2 → 128,368, 3 → 40,961, …; the longest is 47, at the root.
- 2 to 9,216 divisors per claim. No prime record is below 2^16, every prime record is used, and the largest p is N itself.
- The table is read at 930,206 distinct indices. **192,882** of them are needed above the trivial bound max(1, λ(v)); the largest
  value needed is 58 (`check_lower_strict.py --demand`).

## 5. The second checker written in this audit

[`tools/check_lower_strict.py`](tools/check_lower_strict.py) (stdlib only, no repository imports) was written from the
mathematics rather than by editing `check_lower.py`. Compared with the first checker it:
- rejects every non-int numeric field, using `parse_float` / `parse_constant` hooks and `type(x) is int`;
- requires m ≥ 2;
- takes the expected target, claim and table SHA-256 on the command line and requires the header to match;
- sanity-checks the table (c[1] = 1, all entries ≥ 1);
- can report the table demand (§4).

It accepts both real certificates and rejects the F1 attack. The implementation auditor also wrote a separate strict
checker of its own (not committed) and got the same verdict. All three checkers come from the same model family, so they
are **implementations, not an independent human review**.

## 6. Recommendations (not applied: the existing checker is left unchanged, as instructed)

1. Fix F1/M1 in `check_lower.py`: `type(x) is int` for every numeric field, parse hooks that reject floats and NaN,
   m ≥ 2, and an "integers only" rule in spec §5.
2. Fix F2: take the expected target, claim and table SHA as arguments, print the SHA in the verdict, and compare the
   verdict line in `run_cert.sh`.
3. Report every exception as `REJECTED <line>`; cap j and exponents.
4. Strengthen the tests to kill the surviving mutants: Pratt negatives with a trivially true target, an equality-boundary
   case, cases that need x ≥ 2 and d = √m, deletion with the record count fixed, the F1 reproducer, NaN `claim_gt`, and
   CLI exit codes. Run mutation testing as a standing check.
5. In `verify.py`, print the evaluated n and require an int `ones`.
6. Validate `strtoull` and check `fclose` in the C program.
