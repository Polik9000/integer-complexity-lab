# RESEARCH LOG

Append-only. Newest entry at the bottom. Each entry: date, who (human lead / Claude Chat /
Claude Code / reviewer), what was done, findings with statuses, decisions, failures, next steps.

---

## 2026-11-25: Project bootstrap (Claude Code)

**Done**
- Inspected the environment: cloud container, Python 3.13, gcc 13, 4 cores, 15 GB RAM. GitHub
  is reachable through the connector as the lead's account; the `gh` CLI token there is invalid.
  Lean 4 v4.35.0 was installed from the GitHub release (the official Lean release host is blocked).
- Created the repository structure, CLAUDE.md (rules, evidence statuses), README, RESULTS,
  RESEARCH_QUESTIONS, BIBLIOGRAPHY, docs (workflow, GitHub plan, skills), templates.
- Implemented and tested: a strict expression parser, an exact ‖n‖ table (Python + C,
  cross-checked), a peel upper-bound search, a certificate format and verifier, and a Lean core with
  kernel-checked certificates (36 pytest tests pass, `lake build` OK).
- Vetted skills from 4 sources. Installed 3 third-party skills and wrote 4 project skills (docs/SKILLS.md).
- Wrote the Claude Chat project instructions and knowledge package (`claude-project/`).

**Benchmark re-validation** (details: research/2026-11-25-m61-benchmark-brief.md)
- The 127-ones claim comes from PR #4 on the GitHub board `math-market/integer-complexity-m61`
  (opened 2026-10-02, **open, not merged**). The board's baseline is 150. The "116" is
  ⌈3 log₃ N⌉, the generic lower bound.
- The PR #4 expression is valid: 127 ones, value 2^61 − 1. It was checked with our own parser and in the
  Lean kernel (no axioms). `COMPUTATIONALLY VERIFIED` + `FORMALLY VERIFIED` (R-0003).
- EXP-0001: our own peel search found an independent 127-ones expression in ~5 s (R-0005).
- No better bound found anywhere we looked. Status of ‖N‖: open in [116, 127].
- Sanity checks of the exact table against the literature all pass (R-0100, R-0101).

**Failures / notes**
- Peel searches with wider r but small d got worse (128–129). Recorded in research/failed-approaches.md.
- `oeis.org` and `release.lean-lang.org` are blocked from the cloud container.

**Proposed decision (awaiting the human lead)**
- Reframe the primary target from "beat 127" to **RQ-1: determine ‖2^61 − 1‖ exactly** (He's
  single-target algorithm), with RQ-3 (defect-based lower bounds) and RQ-2 (‖2^k − 1‖ table) as
  companions. The next step is reading He 2024 in full and Altman 2016/2019, then planning EXP-0002.
  No expensive computation until the plan is approved.

## 2026-11-25: Decision: primary research target (human lead)

**Decision:** The human lead approved reframing the primary target from "beat 127" to
**RQ-1: determine ‖2^61 − 1‖ exactly**. RQ-3 (defect-based lower bounds) and RQ-2 (a table of
exact ‖2^k − 1‖) are companions. RQ-4 ("fewer than 127 ones") is kept only as bounded side
experiments.
**Alternatives considered:** keep "beat 127" as the main goal (rejected: heuristic results only,
no endpoint; see brief §6).
**Also:** the lead approved publishing the repository as public `Polik9000/integer-complexity-lab`.
It was created and `main` was pushed on 2026-11-25.
**Next step:** a literature step: read He 2024 §3–4 in full and Altman 2016/2019, then write an
EXP-0002 plan (implementation and validation of He's single-target algorithm) for approval.

## 2026-11-25 (afternoon): RQ-1 literature step and exact pilot (Claude Code)

The lead asked for: He's algorithm and proofs studied in full, assumptions and costs verified,
alternatives explored, independent checks against literature, ≥ 2 alternative strategies, and an EXP plan
with CPU/RAM/risk estimates. No long or paid computation.

**Literature** (notes in `research/lit-He2024.md`, `research/lit-AltmanZelinsky2012.md`)
- He 2024: the single-target O(n^0.6154) bound is worst-case and driven by α ≤ 4.125. The finite-n use of
  the additive-part lemma needs the explicit inequality, which the paper leaves asymptotic. The code is public
  (GPL), uses the same budgeted-DFS idea, and reports no runtimes.
- Altman–Zelinsky 2012 Thm 1.6 (classification of δ < 1) gives **‖2^61−1‖ ≥ 117** with a short proof.
  We checked Thm 1.6 against our exact table for n ≤ 4·10⁸: exactly the 420 predicted numbers.

**Key insight.** With a verified upper bound U, any additive split x + y of n needs x·y ≤ 3^{(U−1)/3}.
For N with U = 127 that means x ≤ ~94. So an exhaustive budgeted search is tiny compared with
He's worst case.

**EXP-0002 (cheap, ~6 min CPU in total).** Implemented `algorithms/exact_single.py` with a written
correctness proof (`research/proof-exact-search.md`). Results:
- Matches the exact table on 314 values, and **all 38 published values of Iraids Table 3** (k ≤ 39).
- **‖2^61 − 1‖ = 127** (117 s), plus new values ‖2^k − 1‖ for 40 ≤ k ≤ 60.
- Status: `COMPUTATIONALLY VERIFIED`, **provisional**, because there is only one implementation.

**Blocked:** compiling and running He's GPL code as an independent replication was refused by the
sandbox's safety policy. We'll ask the lead for explicit approval. Not worked around.

**Plan:** `research/2026-11-25-rq1-strategy-and-exp0003-plan.md`. Four strategies (S1 independent
replication, S2 certificate plus independent checker, possibly in Lean, S3 defect theory, S4 He's interval
DP). EXP-0003 steps with cost and risk estimates. Interesting follow-ups: ‖2^64 − 1‖ (tests Iraids'
Observation 2, predicted 132), and the A(k) structure (RQ-9).

## 2026-11-25 (afternoon, cont.): EXP-0003 step 3, independent replication with He's code (Claude Code)

The lead approved building and running Q. He's GPL solver in the sandbox, by a decision card. We
built `hqztrue/integer_complexity@742e8c5` (`single.cpp`, unmodified) with a small Linux driver
(renames `main` and `_init`), and ran `calc_single(2^k − 1)` for k = 2..61.
**Result: 60/60 values agree with EXP-0002 (42 overlaps) and Iraids Table 3 (38 overlaps). ‖2^61 − 1‖ = 127.**
That took 17 s in total, 2.6 s for k = 61, about 45× faster than our Python search.

Reading the source showed that He's lower bound is stronger than Selfridge. It hard-codes the families of
defect < 1 and gives every other number one more. If that list were incomplete, the error could only make
values too large, so the agreement with our Selfridge-only search is still meaningful.

R-0007 and R-0201 move from "provisional: one implementation" to "two independent implementations". They are
not `PROVEN`. The certificate (step 2) and external review (RP-0002) remain.

## 2026-11-25 (afternoon, cont.): Lead's review of PR #2 and follow-up fixes (Claude Code)

The lead reviewed PR #2 and agrees with the conclusion: "strongly supported by two independent implementations".
The lead asked for four fixes, then for the certificate work. Done:
1. `run_he.sh` now **asserts** the upstream SHA-256, aborting with exit 2 on a mismatch (tested with a modified copy). It
   asserts again after the build.
2. PR description: removed the stale "provisional" wording.
3. `research/proof-exact-search.md`: a new status table. The Theorem is a *conditional* correctness theorem, and
   its proof is self-checked only. Nothing in the note is labeled `PROVEN` until RP-0002. We also wrote out
   the missing E(k) induction for Lemma 1 (previously TODO), with a new test of its inequalities for k ≤ 300.
4. Sensitivity run: He's code with the defect < 1 pruning switched off by a one-line patch to a copy
   (`he_naive_lb.patch`; upstream untouched). It gives the **same 60 values**, k = 61 in 3.58 s.

Decision recorded (lead): **don't extend the table to larger k** until the certificate architecture is specified.
Next: specify the certificate format and an independently implemented checker for 2^61 − 1.

## 2026-11-25 (afternoon, cont.): certificate architecture and the first lower-bound certificate (Claude Code)

The lead asked us to prioritize a certificate-producing search with an independent checker, and to keep larger k
on hold until the architecture is specified.
- **Spec:** `research/2026-11-25-certificate-architecture.md`. The claims are G(m, j) "‖m‖ > j", each with its full
  factorization and Pratt primality records. The checker recomputes every split itself, so no hints are needed (Theorem C).
  Trust base: Lemmas 1–2, Theorem C, the checker, and the table as a *lower* bound.
- **Table cross-check:** our C table and He's independent table (Fuller's algorithm, dumped via our driver) are
  byte-identical for n ≤ 10⁸ (SHA-256 34dbc4da…).
- **Implementation:** `certificates/lower/check_lower.py` (169 lines, stdlib only) and `algorithms/certificate_emit.py`.
  13 tests, including mutation tests.
- **Result:** the certificate for ‖2^61 − 1‖ > 126 has 1.12M records and is 13 MB gzip. It took 220 s to generate. The checker
  **accepted** it in 56 s. The same certificate with its root raised to > 127 is rejected.
- Status of R-0007: `COMPUTATIONALLY VERIFIED` with a checkable certificate. It is still **not `PROVEN`**, because there has been no
  external review of the checker and the proofs (RP-0002 is next) and no Lean version.
- We did not run anything for larger k.

## 2026-11-25 (evening): EXP-0004 independent proof audit (Claude Code + five subagents)

The lead asked for an independent, skeptical audit of ‖2^61 − 1‖ = 127 and a Lean roadmap, with independent agents
(math, implementation, adversarial, Lean, literature). The branch is `research/exp-0004-proof-audit`, based on `main`
`b7d85c9` (PR #4 merged). Record: `research/EXP-0004-independent-proof-audit/`.
- **Reproduction:** 54 tests pass. The EXP-0003 certificate regenerates byte-identically (except the header commit) and is
  accepted (4 min 13 s).
- **Mathematics:** no error found. Lemma 1, Fact S and Theorem C are now kernel-checked in Lean (PoC, no `sorry`), along with
  ‖1023‖ = 22 end to end (R-0008, `FORMALLY VERIFIED`). Lemma 2 is worded loosely about factors of 1 (fixed in the audit's
  write-up).
- **Checker bug F1 (critical for the tool, no effect on the result):** `check_lower.py` accepts false claims when a factor prime
  is a JSON float (demonstrated: ‖4·3^33‖ > 103). Three agents found it independently. The real certificates contain only
  integers. The checker was left unchanged as instructed; a strict xfail test documents the hole. Also found: m = 1 with T ≤ 0
  (M1), unbound verdict header fields (F2), and weak tests (mutants survive).
- **New:** a second, strict checker, and a **table-free certificate** (3,068,111 records, 31 MB gzip, only ‖1‖ = 1 assumed). Both
  checkers accept it. The 10⁸ table is no longer in the trust base.
- **Literature:** no published exact ‖2^k − 1‖ for k ≥ 40 and ~~no formalization of integer complexity~~ found (the formalization part is **corrected** in the next entry). The upper bound 127
  is not new (board PR #4; Iraids 2012 Thm 8). No priority claimed.
- **Status:** R-0007 stays `COMPUTATIONALLY VERIFIED`, not `PROVEN`.
- **Next (recommended):** harden `check_lower.py` (separate PR, needs the lead's OK); RP-0002; Lean M2/M3 (decide whether to use
  Mathlib); then `native_decide` (M5) and a plan for a kernel-only run (M6, ≈ 1–3 CPU-days, estimated).

## 2026-11-25 (late evening): EXP-0004 correction, prior Lean formalization (Claude Code)

An external audit forwarded by the lead found a prior public Lean formalization of integer complexity:
`BrettKnox/open-problems-lab`, `OpenProblemsLab/IntegerComplexity.lean`, commit `e899b51` (2026-08-20). It covers ‖n‖,
Selfridge's bound, ‖3^k‖ = 3k and ‖2^n‖ = 2n for n ≤ 9, plus defect and stability. We inspected its source (we did not build it).
Our claim "no formalization of integer complexity exists" is **retracted** in EXP-0004 (literature §6, README, disagreement
log D8). What remains, as "not found" only: Theorem C, a verified certificate checker, exact values that need more than
Selfridge's bound, and anything about 2^61 − 1. Process lesson recorded in `research/failed-approaches.md`.

## 2026-11-25 (night): EXP-0004 follow-up: reproduction, Lean with Mathlib, second independent review (Claude Code)

The lead asked for the follow-ups to the external audit (PR #5 stays a draft; nothing merged).
- **Novelty, corrected again.** An independent literature reviewer found google-deepmind/formal-conjectures (Lean definition of
  ‖n‖ and the split lemma, 2025-06-30) and facebookresearch/atlas-lean (Selfridge-type bounds, recursion, 2026). The primary agent
  read both at the stated commits. Literature §7; no priority is claimed for anything.
- **Checker hardening** is in a separate PR (#6, EXP-0005). This branch's certified checker is unchanged.
- **Reproduction.** `tools/run_tablefree.sh` from a clean checkout: 3,068,111 records, body byte-identical to the first run (only the
  header's commit field and gzip metadata differ); accepted by the version-1 checker, the strict checker and v2; the root raised
  to > 127 is rejected by the strict checker and v2.
- **Lean (`lean-cert/`, Mathlib v4.35.0).** Kernel-checked: checker soundness, divisor completeness, Pratt via `lucas_primality`,
  and ‖2^20 − 1‖ > 41, ‖2^24 − 1‖ > 49. ‖2^61 − 1‖ > 126 is checked **via `native_decide`** (≈ 100 s), rebuilt independently from
  the reproduced certificate. New R-0009 (`FORMALLY VERIFIED`) and R-0010 (`COMPUTATIONALLY VERIFIED`, native_decide).
- **Second review round** (math, programming/security, Lean, literature): no false certificate accepted, no mathematical error.
  Disagreements D9–D16 recorded. The brief given to the Lean builder had wrong values for ‖2^24 − 1‖, ‖2^30 − 1‖ and ‖2^40 − 1‖
  (from memory; D16); the repository's EXP-0002 values (50, 63, 82) were confirmed.
- R-0007 status unchanged (`COMPUTATIONALLY VERIFIED`); it gains evidence item (5).
