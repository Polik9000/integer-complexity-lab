# Collaboration workflow

Four environments, one record. GitHub is the record. Everything else is a workspace.

```
           ┌──────────────────────────┐
           │   Human project lead     │  decides, approves, publishes
           └──────┬─────────┬─────────┘
                  │         │
     plans, asks  │         │  forwards review packages / brings back reviews
                  ▼         ▼
 ┌────────────────────┐   ┌───────────────────────┐
 │ Claude Chat project│   │ ChatGPT (independent  │
 │ planning, theory,  │   │ reviewer & critic)    │
 │ literature, drafts │   └──────────▲────────────┘
 └─────────┬──────────┘              │ review-packages/RP-NNNN.md
           │ decisions & drafts      │
           ▼                         │
 ┌────────────────────┐   PRs   ┌────┴───────────────────┐
 │ Claude Code        │ ──────▶ │ GitHub repository      │
 │ code, experiments, │ ◀────── │ (canonical record)     │
 │ Lean, tests, docs  │  clone  └────────────────────────┘
 └────────────────────┘
```

## Who does what

| Environment | Used for | Writes to GitHub? |
|-------------|----------|-------------------|
| **Claude Chat project** ("Integer Complexity Lab – Mathematical Research") | Planning, reading papers, proofs on paper, hypothesis design, strategy | Not directly. Its outputs are pasted or uploaded into a Claude Code session, or committed by the lead. Anything decided there gets recorded in `RESEARCH_LOG.md`. |
| **Claude Code** | Implementation, experiments, Lean, tests, repository upkeep, review packages | Yes, through branches and PRs. It may commit small doc fixes to `main`. |
| **GitHub** | The single source of truth: code, data pointers, results, logs, decisions | (is the record) |
| **ChatGPT** | Independent critique of selected results | No. Its reviews are saved verbatim by Claude Code into `review-packages/`. |

## The research loop

1. **Question.** Add or refresh an entry in `RESEARCH_QUESTIONS.md` (Chat or Code).
2. **Hypothesis.** Write `hypotheses/H-NNNN-*.md`: the statement, the motivation, what
   would confirm or refute it, and the planned experiment.
3. **Plan.** Write `experiments/EXP-NNNN-*/README.md` with the method and a cost class. Medium or large
   cost waits for the lead's go-ahead.
4. **Run** (Code). Follow the `reproducible-experiment` skill.
5. **Record** (Code). Use the `record-research-result` skill: RESULTS.md, RESEARCH_LOG.md,
   hypothesis status. Failures are recorded too.
6. **Review** (selected results). Use the `review-package` skill. The lead sends the
   package to ChatGPT and returns the review. Claude records the review and a point-by-point response.
7. **Formalize** (headline results). Put certificates and theorems in Lean (`lean/`).
8. **Publish** (lead only). Papers, posts or board submissions happen only with explicit approval.

## Syncing Claude Chat with the repository

- The Chat project's knowledge is a **snapshot** of the repository, built by
  `claude-project/build_knowledge_package.sh`. Re-upload it after significant changes. The file
  `KNOWLEDGE_VERSION.txt` inside the snapshot says which commit it came from.
- If Chat and the repository disagree, the repository wins (CLAUDE.md §1). Chat should say
  so instead of guessing.
- To bring a Chat result into the repository, ask Chat for a "repository-ready note"
  (Markdown with statuses and sources). Then paste it into a Claude Code session with
  "record this".

## Branches and pull requests

- `main` is always green: tests pass, Lean builds, certificates verify.
- Use one branch per piece of work: `exp/EXP-0002-he-algorithm`, `docs/...`, `lean/...`.
- Open a PR for every significant change. The PR says which claims changed status and links the evidence.
- No force-push to shared branches. No history rewriting after a push.
- CI (`.github/workflows/ci.yml`) runs the pytest suite, the certificate check and the Lean build.

## Decision records

Strategic decisions (e.g. "primary target is RQ-1") are logged in `RESEARCH_LOG.md` under a
**Decision** heading: what was decided, the alternatives, who decided, and why.
