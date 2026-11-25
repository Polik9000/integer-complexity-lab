# EXP-0005: harden the lower-bound checker after the EXP-0004 audit

| Field | Value |
|-------|-------|
| ID | EXP-0005 |
| Date | 2026-11-25 |
| Question | Does a hardened `certificates/lower/check_lower.py` close the EXP-0004 audit findings (F1, F2, M1, F3/F4, F5–F7), while still accepting the genuine certificates? |
| Cost class | cheap (about 10 min CPU in total) |
| Code | `certificates/lower/check_lower.py` (version 2), `tests/test_check_lower_hardening.py`, `run_corpus.py` |
| Base commit | `b7d85c9` (main), branch `fix/check-lower-hardening` |

The EXP-0004 audit (PR #5, kept as a draft) found that the version-1 checker can be made to accept a
false statement. The audit itself leaves the version-1 checker untouched, so the record of what it
certified stays readable. This experiment is the separate fix.

## Findings addressed

| Finding | Problem in version 1 | Version 2 rule | Test |
|---------|----------------------|----------------|------|
| F1 | JSON floats are accepted. A factor `p.0` equals the int prime `p` in Python, and a float product rounds to `m`. A false factorization then passes, which removes divisors from the product check. Concrete false acceptances: `‖4·3^33‖ > 103` (T = 50 table), `‖2^8·3^32‖ > 112` with the genuine 10^8 table. | Every numeric field must have type exactly `int`. Fraction/exponent number tokens, `NaN` and `Infinity` are rejected while parsing. `bool` is rejected. | `test_f1_float_factor_rejected`, `test_float_and_bool_tokens_rejected_everywhere`, corpus `f1/`, `adv/attack_float_*`, `impl/fake_float_1e8.jsonl` |
| F2 | The verdict is whatever the header says. Target, claim and table hash are not pinned by the caller. | `--target`, `--claim-gt` and `--table-sha256` are required CLI inputs. The header must match them, and the verdict line repeats them. | `test_expected_statement_is_bound`, `test_cli_requires_and_checks_expected_statement` |
| M1 | `m = 1` is allowed. Theorem C needs `m ≥ 2`. With `T = 0` a claim `‖1‖ > 50` passes and cascades. | Claims need `m ≥ 2`. The table needs `T ≥ 1`. | `test_degenerate_tables_and_m_equal_one_rejected`, `test_m_equal_one_rejected_even_with_valid_table` |
| F3/F4 | The old negative tests are rejected for the wrong reason (at `end`), so they do not test the Pratt and split checks. No mutation testing. | New battery: for every required split of a true claim, weakening the table there must cause a rejection. Pratt negatives whose verdict depends on the prime record. 14 source mutants, all must be killed. | `test_battery_passes_on_real_checker`, `test_mutant_is_killed[*]` |
| F5 | Header fields are not validated (types, unknown keys, `claim_gt < 0`, non-canonical target). | Exact field sets; target is a canonical decimal string; `claim_gt` an int ≥ 0; version is int 1. | `test_header_fields_validated`, `test_bad_claim_gt_rejected` |
| F6 | Duplicate JSON keys silently keep the last value. | Duplicate keys are rejected. | `test_duplicate_keys_rejected` |
| F7 | I/O and gzip errors give a traceback, not a verdict. Records may carry extra fields. | Every failure is `REJECTED`, exit 1. Records have exactly the spec fields. The last claim must be the target claim. | `test_records_fields_validated`, `test_last_claim_must_be_target`, CLI truncated-gzip test |

Two guard rules avoid very long loops on hostile input, and neither rejects a true claim:
`j > 3·bitlen(m)` is rejected (then `j ≥ ‖m‖` since `‖m‖ ≤ 3 log2 m`, so the claim is false), and a
factor exponent above `bitlen(m)` is rejected (then `p^e > m`).

## Method

1. Rewrite the checker from the spec (`research/2026-11-25-certificate-architecture.md`, section 5,
   now with a "Version 2 rules" block). The mathematical checks (Pratt/Lucas, the Selfridge sum
   cut-off, divisors from the verified factorization, `LB`) are unchanged.
2. Run the 72 hardening tests: exploits, battery, mutants and the committed corpus.
3. Run the checker in its permissive mode (no expected statement; the attacker writes the header) over
   every false or malformed certificate built during the EXP-0004 audit (`run_corpus.py`).
4. Run the CLI, with the expected statement, on both genuine certificates for `‖2^61−1‖ > 126`, and on
   the table-free certificate with the root raised to `> 127`.

## Reproduce

```bash
python3 -m pytest -q tests/test_check_lower_hardening.py          # 72 tests, ~2 s
python3 -I experiments/EXP-0005-checker-hardening/run_corpus.py \
    --tables experiments/EXP-0005-checker-hardening/corpus/tables/* WORK/table_1e8.bin \
    --certs experiments/EXP-0005-checker-hardening/corpus
# genuine certificates (regenerate them first, see certificates/README.md):
N=2305843009213693951
python3 -I certificates/lower/check_lower.py WORK/orig.jsonl.gz WORK/table_1e8.bin \
    --target $N --claim-gt 126 --table-sha256 34dbc4da4f105ff7cc01942a6d7b491efba5bceee44bbad87fb0540e461b38f6
python3 -I certificates/lower/check_lower.py WORK/tablefree_k61.jsonl.gz WORK/trivial_table.bin \
    --target $N --claim-gt 126 --table-sha256 b413f47d13ee2fe6c845b2ee141af81de858df4ec549a58b7970bb96645bc8d2
# root raised to 127 (must be rejected):
zcat WORK/tablefree_k61.jsonl.gz | sed -e '1s/"claim_gt":126/"claim_gt":127/' \
    -e 's/^{"type":"claim","m":2305843009213693951,"j":126,/{"type":"claim","m":2305843009213693951,"j":127,/' \
    | gzip -1 > WORK/tf_root127.jsonl.gz
python3 -I certificates/lower/check_lower.py WORK/tf_root127.jsonl.gz WORK/trivial_table.bin \
    --target $N --claim-gt 127 --table-sha256 b413f47d13ee2fe6c845b2ee141af81de858df4ec549a58b7970bb96645bc8d2
```

`WORK/table_1e8.bin` comes from `algorithms/c/complexity_table.c` (see EXP-0003). Without it, the two
corpus files that name the 10^8 table are still rejected, but at line 1 (table mismatch) instead of at
the float token.

## Corpus

`corpus/` holds the small false or malformed certificates built by the EXP-0004 agents (616 KB):
`impl/` (35 probes on `‖2^21−1‖ > 43` with the exact table `tables/t2000.bin`, plus one F1 certificate on
the 10^8 table), `adv/` (F1 on T = 1000 and on the 10^8 table, a header with `claim_gt = −1`), `f1/` (F1
on a T = 50 table, `tables/table_T50.bin`) and the degenerate tables `table_T0.bin`, `table_T1.bin`,
`table_empty.bin`. Four files state true facts and are controls: `baseline.jsonl`, `gz_ok.jsonl.gz`,
`header_reserialised.jsonl`, `trivial_claim_ok.jsonl`. The test suite checks that exactly these four
are accepted.

Three large mutants of the genuine certificate (79 MB each: a deleted middle claim with the count
fixed, a bumped exponent, the root raised to 127) are not committed. They were checked in the run below
and are rebuilt by small edits to the genuine certificate.

## Environment

Cloud container, Intel Xeon @ 2.10 GHz, 4 cores (each run single-threaded), 15 GB RAM, Linux,
Python 3.13.18.

## Results

| Run | Verdict | Time |
|-----|---------|------|
| `pytest -q` (whole suite) | 126 passed | 10 s |
| Corpus, permissive mode: 39 committed files + 3 large mutants | 4 controls accepted, all 38 others rejected, each for the intended reason (float token, `m ≥ 2`, record count, split not refuted, …) | ~2 min |
| EXP-0003 certificate (`4f286d15…46135752`), 10^8 table, expect `> 126` | `ACCEPTED: ‖2305843009213693951‖ > 126  (table sha256 34dbc4da…38f6)` | 1 min 12 s |
| Table-free certificate (`623887b1…7dd7808d6173`, 3,068,111 records), table `[0,1]`, expect `> 126` | `ACCEPTED: ‖2305843009213693951‖ > 126  (table sha256 b413f47d…8d2)` | 3 min 41 s |
| Same, root raised to `> 127`, expect `> 127` | `REJECTED: line 3068112: sum split 1 + 2305843009213693950 not refuted` | 3 min 32 s |
| Genuine table-free certificate, expect `> 127` | `REJECTED: line 1: header claim_gt 126 is not the expected 127` | < 1 s |
| All 14 mutants of the checker | all killed by the battery | in pytest |

The math agent's `exploit.py` P2 probe (F1 on `8·3^33`) found no prime pair in its search range, so it
built no certificate. F1 is covered by the three other F1 certificates above, which version 1 accepts
and version 2 rejects.

## Conclusions

- `COMPUTATIONALLY VERIFIED`: version 2 rejects every false or malformed certificate built in the
  EXP-0004 audit, and kills all 14 listed mutants.
- `COMPUTATIONALLY VERIFIED`: version 2 accepts both genuine certificates for `‖2^61−1‖ > 126`, with the
  expected statement pinned, and rejects the table-free certificate with the root raised to `> 127`.
- The status of R-0007 is not changed by this experiment.

**Not shown:** that no other false certificate is accepted. Tests and a corpus can only show that the
known attacks fail. The soundness argument is the spec plus the checker's code; an independent review of
version 2 is still due (EXP-0004 follow-up).
