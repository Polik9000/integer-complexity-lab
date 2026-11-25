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
