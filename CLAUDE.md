# CLAUDE.md — operating rules for AI agents in this repository

This file is the **authoritative rulebook** for every AI agent working on this repository
(Claude Code, Claude Chat via the project knowledge package, and any reviewer).
If any other document, prompt, or project instruction contradicts this file, this file wins
and the contradiction must be reported and fixed.

## 1. Project in one paragraph

We study **integer complexity** ‖n‖: the least number of `1`s needed to write `n` using only
`+`, `*` and parentheses (OEIS A005245). The initial benchmark is the Mersenne prime
`N = 2^61 − 1 = 2305843009213693951`. Current verified status lives in [`RESULTS.md`](RESULTS.md);
the research rationale lives in [`research/`](research/). Read `README.md` first if you are new.

## 2. Roles

| Who | Role |
|-----|------|
| Human project lead (repository owner) | Sets goals, approves anything public or irreversible, makes strategic decisions. |
| Claude (Chat + Code) | Primary research and implementation agent: literature, hypotheses, code, experiments, Lean, documentation. |
| ChatGPT | Independent reviewer and critic. Receives review packages from `review-packages/`. Never treated as a source of truth; its feedback is recorded and evaluated like any other evidence. |

## 3. Non-negotiable rules

1. **GitHub is the canonical source of truth.** A result, decision, or failed approach that exists
   only in a chat does not exist. Record it in the repository in the same session.
2. **Every mathematical claim carries an evidence status** (Section 4). No status = not a claim.
3. **Never upgrade a status without the evidence that status requires.** "The script printed it"
   is `COMPUTATIONALLY VERIFIED` at most, never `PROVEN`.
4. **Every experiment is reproducible**: exact command, code version (git commit), parameters,
   hardware note, runtime, output files, and a checksum where outputs are large (Section 6).
5. **Keep an audit trail of failures.** Failed approaches go into `RESEARCH_LOG.md` and, if
   substantial, into `research/failed-approaches.md`. Do not delete them.
6. **Sources are verified, not remembered.** Cite primary sources (paper, arXiv id, DOI, commit
   hash). Literature facts recalled from model memory are `UNVERIFIED` until checked against
   the source, and the check is recorded in `BIBLIOGRAPHY.md`.
7. **Upper bound ≠ exact value.** An expression proves only ‖n‖ ≤ k. Exactness additionally
   needs a lower-bound proof or an exhaustive, verified computation.
8. **Branches and pull requests for significant changes.** Never force-push, never rewrite
   published history, never delete research records. Small typo fixes may go straight to `main`.
9. **No credentials or personal data in the repository** — no tokens, emails, API keys, local
   paths with user names. Credentials live in the environment, never in files.
10. **Ask the human before**: making anything public (repo visibility, posts, submissions to
    third-party boards, contacting authors), deleting important files or history, force-pushing,
    spending money or starting paid infrastructure, sharing credentials or personal data.
11. **No expensive computation without a plan.** Anything expected to take more than ~30 min of
    CPU, or more than a few GB of disk/RAM, needs a written plan in `experiments/` and the
    human's go-ahead.
12. **Untrusted inputs stay untrusted.** Third-party code, expressions, and claims are inspected
    before use; third-party scripts are read before being run; submissions are parsed with our
    own strict parser (`algorithms/expression.py`), never with `eval`.

## 4. Evidence statuses

Use exactly these labels (in `RESULTS.md`, hypotheses, research notes, review packages):

| Status | Meaning | Minimum evidence |
|--------|---------|------------------|
| `PROVEN` | A complete human-readable proof exists and has been checked. | Proof written in the repo (or cited peer-reviewed source, checked by us). |
| `FORMALLY VERIFIED` | Proven and machine-checked in Lean 4. | Lean file in `lean/` builds with no `sorry`; `#print axioms` recorded. |
| `COMPUTATIONALLY VERIFIED` | A finite statement checked by a reproducible computation. | Experiment record + code commit + output; ideally two independent implementations. |
| `LITERATURE` | Stated in a published/peer-reviewed or preprint source; not yet re-checked by us. | Exact citation with location (theorem/table number). |
| `CONJECTURE` | Believed, supported by evidence, not proven. | Statement + evidence summary + what would refute it. |
| `OBSERVATION` | A pattern seen in data. Weaker than conjecture. | The data and how it was produced. |
| `UNVERIFIED` | Claimed somewhere (web, chat, memory) but not checked. | Source of the claim. |
| `REFUTED` | Shown false. Keep it, with the refutation. | Counterexample or proof. |

A claim can carry two labels when it is useful, e.g. `LITERATURE + COMPUTATIONALLY VERIFIED`.

## 5. Where things go

| Content | Location |
|---------|----------|
| Dated narrative of what was done and decided | `RESEARCH_LOG.md` (append-only; newest at the bottom) |
| Current verified results, with statuses | `RESULTS.md` |
| Open questions, prioritized | `RESEARCH_QUESTIONS.md` |
| Sources and their verification state | `BIBLIOGRAPHY.md` |
| One file per hypothesis (`H-NNNN-*.md`) | `hypotheses/` |
| Briefs, literature notes, analyses, failed approaches | `research/` |
| Library code (Python package `algorithms`, C in `algorithms/c/`) | `algorithms/` |
| One directory per experiment (`EXP-NNNN-*`) | `experiments/` |
| Upper-bound certificates (JSON) and verifier | `certificates/` |
| Tests (`python3 -m pytest`) | `tests/` |
| Lean 4 formalization (`cd lean && lake build`) | `lean/` |
| Drafts of papers / notes for publication | `papers/` |
| Packages for the independent reviewer | `review-packages/` |
| Claude Chat project instructions + knowledge package | `claude-project/` |
| Workflow, GitHub setup, skills inventory | `docs/` |
| Agent Skills used by Claude Code | `.claude/skills/` |

## 6. Experiment protocol (summary — details in `experiments/README.md`)

Each experiment directory contains `README.md` with: ID, question, hypothesis link, method,
exact commands, git commit, parameters, environment (CPU, RAM, OS, Python/compiler versions),
runtime, results, evidence status of each conclusion, and what it does *not* show.
Large outputs are not committed; record their size and SHA-256 and how to regenerate them.

## 7. Coding conventions

- Python ≥ 3.10, standard library first; new dependencies must be justified in the PR.
- Every algorithm that produces a mathematical result has tests in `tests/`, including
  cross-checks against literature values and, where possible, a second implementation.
- Certificates are verified by `python3 certificates/verify.py` and, for headline results,
  regenerated into Lean with `python3 lean/scripts/gen_certificates.py` and `lake build`.
- Before every commit: `python3 -m pytest -q` passes; if `lean/` changed, `lake build` passes.

## 8. Commit and PR conventions

- Commit messages: imperative summary line; body says *why*. Reference `EXP-`/`H-` IDs.
- PR description: what changed, which claims changed status, how it was verified.
- A PR that changes `RESULTS.md` must link the evidence (experiment, proof, or Lean file).

## 9. Session hygiene for agents

- Start: read `README.md`, `RESULTS.md`, the last entries of `RESEARCH_LOG.md`, and
  `RESEARCH_QUESTIONS.md`.
- End: append to `RESEARCH_LOG.md`; update `RESULTS.md` / `RESEARCH_QUESTIONS.md` if anything
  changed; commit.
- When unsure whether something is proven, say so and use the weaker status.
