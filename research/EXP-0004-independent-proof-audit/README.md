# EXP-0004: Independent proof audit of ‖2^61 − 1‖ = 127, and a Lean roadmap

| Field | Value |
|-------|-------|
| ID | EXP-0004 |
| Date | 2026-11-25 |
| Requested by | the project lead (task: "EXP-0004: Independent Proof Audit and Lean Formalization Roadmap") |
| Branch | `research/exp-0004-proof-audit`, based on `main` at `b7d85c9`. That is the merge of PR #4, so `main` contains the EXP-0003 certificate, checker and spec. The audited tree is identical to `8aba2e8`, the PR #3/#4 head. |
| Question | RQ-1, RQ-5, RQ-8: is ‖2^61 − 1‖ = 127 correct, is its lower-bound certificate sound and complete, and can it be formalized? |
| Cost class | cheap. Every run was under 7 min CPU and under 1 GB RAM (total ≈ 30 min CPU, spread over several runs). No larger k was computed. |
| Agents | the primary agent plus five independent specialist subagents. See [`agent-disagreement-log.md`](agent-disagreement-log.md). |

Deliverables: [mathematical audit](mathematical-audit.md) · [implementation audit](implementation-audit.md) ·
[adversarial review](adversarial-review.md) · [Lean roadmap](lean-formalization-roadmap.md) ·
[literature and novelty](literature-and-novelty.md) · [agent disagreement log](agent-disagreement-log.md).

## 1. Executive summary

- **The result stands.** No agent found an error in the mathematics or in the real certificate. ‖2^61 − 1‖ = 127 is
  `COMPUTATIONALLY VERIFIED` with a checkable certificate. The upper bound is `FORMALLY VERIFIED`. The mathematical lemmas
  behind the lower bound are **now kernel-checked in Lean**. The status is still **not `PROVEN`/`FORMALLY VERIFIED` as a
  whole**: the run of the checker on the certificate is a Python computation, and no human has reviewed the checker.
- **One serious checker bug was found (F1), with no effect on the result.** `certificates/lower/check_lower.py`
  accepts a *false* claim if a factor prime is written as a JSON float such as `p.0`. Python's float multiplication then
  rounds a wrong factorization to m, and the real divisors are never checked. Three agents found this independently, and it
  works even with the genuine 10⁸ table. The real certificates contain only integers, so they are unaffected. The checker is
  left unchanged here, as instructed; the hole is documented by a strict xfail test.
- **New: a table-free certificate.** The 10⁸-entry base table is no longer needed. A certificate whose only table entry is
  ‖1‖ = 1 (3,068,111 records) is accepted by **both** checkers. That removes the largest trusted computational component
  (the table, and the He cross-check behind it) from the trust base. It also makes a Lean check possible in principle.
- **Lean.** A sorry-free proof of concept proves the following, with axioms `[propext, Quot.sound]` only:
  - Selfridge's bound e.eval³ ≤ 3^e.ones;
  - Theorem C;
  - the soundness of a Bool-valued claim checker;
  - ‖1023‖ = 22, end to end in the kernel.

  What is left: divisor completeness from a factorization (M2), Lucas/Pratt (M3), and the data pipeline (M4). Kernel-only
  checking of the full certificate is estimated at 1–3 CPU-days (an extrapolation); `native_decide` would take minutes but
  trusts the compiler.
- **Novelty.** The upper bound 127 was already public (board PR #4) and follows from Iraids et al. 2012. We found no
  published exact value of ‖2^k − 1‖ for any k ≥ 40. ~~and no formalization of integer complexity.~~ **Corrected:** a prior
  Lean formalization exists (BrettKnox/open-problems-lab, 2026-08-20: Selfridge, ‖3^k‖ = 3k, ‖2^n‖ = 2n for n ≤ 9); see
  [literature §6](literature-and-novelty.md#6-correction-after-the-external-audit-2026-11-25-evening). We found no earlier
  formalization of Theorem C or of a certificate checker. The exact values are new computational and certified results.
  They are not new mathematics, and we claim no priority.

## 2. Answers to the six questions

**1. Is ‖2^61 − 1‖ = 127 mathematically justified?**
Yes, to the standard of a computer-assisted proof with an explicit trust base. U: two 127-ones expressions are
kernel-checked. L: Lemma 1, Lemma 2, Fact S and Theorem C were reconstructed independently by two agents, and Lemma 1, Fact S
and Theorem C are kernel-checked in Lean. A certificate that applies them is accepted by two separately written checkers,
and the table-free version needs no table. The remaining trust is in the Python checker code and CPython. Evidence status:
`COMPUTATIONALLY VERIFIED`, **not** `PROVEN` (CLAUDE.md §4: no human-checked proof of the finite case analysis, and no
complete Lean check).

**2. Is the lower-bound certificate sound and complete?**
*The certificate* is complete for the claim. Its last claim is G(2^61 − 1, 126), every split the rules demand is refuted,
and every mutation tried is rejected. *The checker* is sound **on well-typed input**, but not on arbitrary input:
- F1 (float factor primes) is a critical soundness hole;
- M1 (m = 1 with T ≤ 0) is a low-severity hole;
- F2 means the verdict line is not bound to the expected statement.

None of these is triggered by the real certificates. The strict checker in [`tools/`](tools/) closes all three.

**3. Which parts are independently verified?**

| Part | How |
|------|-----|
| ‖N‖ ≤ 127 | Lean kernel (two expressions), plus our parser |
| Selfridge (Lemma 1) | two agents by hand, plus Lean (`Expr.selfridge`) |
| Lemma 2, Fact S, Theorem C | two agents by hand, plus Lean (`theoremC`, `checkAll_sound`) |
| Lucas criterion, divisor completeness | two agents by hand (textbook); not formalized |
| EXP-0003 certificate | regenerated byte-identically (except the commit field) and accepted by `check_lower.py` and by three separately written strict checkers |
| Table-free certificate | accepted by `check_lower.py` and `check_lower_strict.py` against the 2-byte table [0, 1] |
| Table ≤ 10⁸ (old certificate only) | He's table byte-identical (EXP-0003); an independent DP for v ≤ 2·10⁶; invariants on the whole table |
| ‖2^k − 1‖ for k ≤ 61 | two programs (ours and He's), EXP-0002/0003; not re-run here |

**4. Which parts still depend on trusted software or unformalized arguments?**
- The two Python checkers and CPython (`int`, `pow`, `json`, `gzip`). Both checkers were written by Claude; **no human has reviewed
  them**.
- Divisor completeness from a factorization and Lucas/Pratt: proved by hand, not in Lean.
- For the EXP-0003 certificate only: the 10⁸ table (c[v] ≤ ‖v‖). The table-free certificate avoids this.
- The written proofs in `research/proof-exact-search.md` and the spec have had no human or external review (RP-0002 is still open).

**5. Can the complete result realistically be formalized in Lean?**
Yes. Everything needed is elementary, and the hardest conceptual parts are already kernel-checked. The route is M2
(factorization-based product rule) → M3 (Pratt) → M4 (chunked certificate data) → M5 (`native_decide`, minutes) and/or M6
(kernel only, ≈ 1–3 CPU-days, which needs a plan and approval). The estimate is 1–2 weeks of work in core Lean, less with
Mathlib. See the [roadmap](lean-formalization-roadmap.md).

**6. What is the smallest next task that would materially strengthen the result?**
**Harden `check_lower.py`.** Apply the F1/M1/F2 fixes (exact int types, m ≥ 2, pinned target/claim/SHA, verdict comparison in
`run_cert.sh`) and the mutant-killing tests. Then re-run it on both certificates and adopt the table-free certificate as the
reference. This takes about half a day, needs no new mathematics, and closes the only soundness defect found. The next
step after that, and the one that changes the evidence status, is Lean milestone M2+M3 followed by a `native_decide` run (M5).

## 3. The table-free certificate (new result of this audit)

**Why.** The EXP-0003 certificate relies on c[v] ≤ ‖v‖ for all v ≤ 10⁸. That table cannot be kernel-checked, and it is the
largest trusted computational input.

**How.** [`tools/gen_table_free_cert.py`](tools/gen_table_free_cert.py) first writes claims G(v, ‖v‖ − 1) for v = 2…1000
in increasing order. Each of these can be checked from the earlier ones. It then runs the existing search with a 1000-entry
base table and emits its claims. The header names the trivial table [0, 1] (T = 1). The 10⁸ table is used **only as a source
of hints**: a wrong hint would only make the certificate fail to check.

| Item | Value |
|------|-------|
| Generation | 365.5 s CPU, 192 MB peak RSS, 2,905,431 search nodes |
| Records | 3,068,111: 2,906,430 claims (999 small plus the search's) and 161,681 Pratt records |
| Size | 205,316,702 bytes raw; 31,187,687 bytes gzip |
| SHA-256 (gzip) | `623887b1a0cf23f9cc8b407005bc4a03d6472f81cd5c7578467e7dd7808d6173` |
| SHA-256 (raw) | `7758ee2608ee108e1abc5912d58ef116d144cb9d84fc1dbe245ec3cd3d609a1f` |
| Table | `[0, 1]`, SHA-256 `b413f47d13ee2fe6c845b2ee141af81de858df4ec549a58b7970bb96645bc8d2` |
| `check_lower_strict.py` (pinned target, claim, SHA) | **ACCEPTED ‖2305843009213693951‖ > 126**, 2 m 51 s; 4,079,045 sum checks, 27,764,482 product checks, longest sum loop 47, largest slack 10, 204 λ shortcuts |
| `check_lower.py` (unchanged) | **ACCEPTED ‖2305843009213693951‖ > 126**, 2 m 38 s |
| Root raised to > 127 | REJECTED at the split 1 + 2305843009213693950 |

The certificate is not committed (31 MB). A copy is in the project files as
`integer-complexity-lab/certificates/M61-LB126-tablefree-v1.jsonl.gz`. Its header records the generator commit as `b7d85c9` (the branch base; the scripts were not yet committed). **Reproduced from the EXP-0004 commit `2ba7a9e`** with `run_tablefree.sh`: the body (all lines after the header) is byte-identical, and both checkers accept it (9 min 52 s in total, 290 s of it generation). Regenerate and check it with:

```bash
bash research/EXP-0004-independent-proof-audit/tools/run_tablefree.sh /tmp/exp4
```

## 4. What was run (exact commands; environment: Xeon 2.1 GHz container, 1 core used, 15 GB RAM, Python 3.13.18, Lean 4.35.0)

```bash
python3 -m pytest -q                                   # before: 54 passed; after: 60 passed, 1 xfailed
python3 certificates/verify.py                         # 3 OK
bash experiments/EXP-0003-independent-verification/run_cert.sh WORK
#   table SHA OK; 1,121,887 records; ACCEPTED ||2305843009213693951|| > 126; 4m13s
cmp <(zcat project-copy | tail -n +2) <(zcat WORK/cert_k61.jsonl.gz | tail -n +2)   # identical
T=research/EXP-0004-independent-proof-audit/tools
python3 -I $T/check_lower_strict.py CERT TABLE 2305843009213693951 126 34dbc4da…38f6 --demand demand.json
#   ACCEPTED, 98 s; 192,882 table entries needed above max(1, lambda)
python3 $T/table_free_estimate.py TABLE demand.json 1      # 759,912 extra claimed m, 0 contradictions, 37 s
python3 $T/gen_table_free_cert.py TABLE 61 127 OUT.jsonl.gz b7d85c9
python3 -I $T/check_lower_strict.py OUT.jsonl.gz trivial.bin 2305843009213693951 126 b413…c8d2   # ACCEPTED
python3 -I certificates/lower/check_lower.py OUT.jsonl.gz trivial.bin                             # ACCEPTED
python3 -I $T/float_factor_attack.py certificates/lower/check_lower.py $T/check_lower_strict.py WORK
#   check_lower.py: ACCEPTED ||22236242266222092|| > 103  (FALSE);  strict: REJECTED
cd lean && rm -rf .lake && lake build && lake env lean scripts/CheckAxioms.lean   # builds; axioms ⊆ [propext, Quot.sound]
```

## 5. Files added on this branch

| Path | What |
|------|------|
| `research/EXP-0004-independent-proof-audit/*.md` | the seven deliverables |
| `tools/check_lower_strict.py` | second, strict checker (stdlib only), with table-demand analysis |
| `tools/float_factor_attack.py` | reproducer for F1 |
| `tools/table_free_estimate.py`, `tools/gen_table_free_cert.py`, `tools/run_tablefree.sh` | table-free certificate |
| `lean-poc/` | the Lean specialist's benchmark-only files and generators (not built by CI) |
| `lean/IntegerComplexity/PoC/` | Selfridge, Checker, CheckerTrie, Examples/M10 (built by `lake build`; axioms in `lean/scripts/CheckAxioms.lean`) |
| `tests/test_exp0004_strict_checker.py` | 7 tests for the strict checker; 1 strict xfail documenting F1 in `check_lower.py` |

Nothing in `algorithms/`, `certificates/` or the existing tests was changed.

## 6. Recommended next steps (in order)

1. Harden `check_lower.py` (F1, M1, F2), add the mutant-killing tests, and make the table-free certificate the reference
   (§2, Q6). This is a separate PR and needs the lead's go-ahead, because it changes the certified checker.
2. RP-0002: give the spec, both checkers and the mathematical audit to the external reviewer (ChatGPT) and, ideally, a human.
3. Lean M2 (divisors from a factorization) and M3 (Pratt). First decide whether to use Mathlib.
4. Lean M4 + M5 (`native_decide`), labelled as such. Then a written plan for M6 (kernel only, ≈ 1–3 CPU-days).
5. Apply the bibliography corrections in [literature-and-novelty.md](literature-and-novelty.md) §5. Relabel R-0006 as
   `LITERATURE` (disagreement log, D3).
6. Optional independent route: Altman 2018 §2.1 lower-bound certifier (needs defect ≈ 10.54 for N; probably expensive).
