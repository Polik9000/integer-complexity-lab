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
