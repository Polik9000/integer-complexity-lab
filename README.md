# Integer Complexity Lab

A long-term, reproducible research project on **integer complexity**: the least number of
`1`s needed to write a positive integer `n` using only `+`, `*` and parentheses, written ‖n‖
(OEIS [A005245](https://oeis.org/A005245)). For example ‖6‖ = 5 because `6 = (1+1)*(1+1+1)`,
and ‖11‖ = 8 because `11 = (1+1+1)*(1+1+1)+1+1` and nothing shorter works.

## Current benchmark

`N = 2^61 − 1 = 2305843009213693951` (the Mersenne prime M61).

| Statement | Status |
|-----------|--------|
| ‖N‖ ≥ 117 | `PROVEN` (via Altman–Zelinsky 2012, Thm 1.6) |
| ‖N‖ ≤ 127 | `COMPUTATIONALLY VERIFIED` and `FORMALLY VERIFIED` (Lean 4, no axioms) |
| **‖N‖ = 127** | `COMPUTATIONALLY VERIFIED` by two independent programs (ours and Q. He's); certificate and external review pending |

Details, provenance and caveats: [`RESULTS.md`](RESULTS.md) and the research brief
[`research/2026-11-25-m61-benchmark-brief.md`](research/2026-11-25-m61-benchmark-brief.md).

## Quick start

```bash
python3 -m pytest -q                     # all tests (Python ≥ 3.10, pytest; gcc optional)
python3 certificates/verify.py           # verify every upper-bound certificate
cd lean && lake build                    # kernel-check the Lean definitions and certificates
```

Reproduce the 127-ones upper bound from scratch (about 1 minute, needs ~400 MB RAM):
see [`experiments/EXP-0001-m61-benchmark-reproduction/`](experiments/EXP-0001-m61-benchmark-reproduction/).

## Repository map

| Path | Contents |
|------|----------|
| [`CLAUDE.md`](CLAUDE.md) | **Rules** for all agents: evidence statuses, reproducibility, what needs human approval |
| [`RESULTS.md`](RESULTS.md) | Current results, each with an explicit evidence status |
| [`RESEARCH_QUESTIONS.md`](RESEARCH_QUESTIONS.md) | Prioritized open questions |
| [`RESEARCH_LOG.md`](RESEARCH_LOG.md) | Append-only dated log of work, decisions and failures |
| [`BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md) | Sources, with what we verified in each |
| `hypotheses/` | One file per hypothesis |
| `research/` | Briefs, literature notes, failed approaches |
| `algorithms/` | Python package: strict expression checker, exact tables, upper-bound search; C table builder |
| `experiments/` | One directory per experiment, each reproducible |
| `certificates/` | Upper-bound certificates (JSON) + independent verifier |
| `tests/` | pytest suite |
| `lean/` | Lean 4 formalization (core Lean, no Mathlib yet) |
| `papers/` | Drafts for eventual publication |
| `review-packages/` | Packages for independent review (ChatGPT) |
| `claude-project/` | Claude Chat project instructions + uploadable knowledge package |
| `docs/` | Workflow, GitHub setup, Skills inventory |
| `.claude/skills/` | Agent Skills used by Claude Code in this repository |

## How we work

GitHub is the canonical record. Claude does research and implementation, the human project lead
directs and approves, and ChatGPT reviews selected results independently.
See [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

## License

Code: MIT (see [`LICENSE`](LICENSE)). Documentation and research notes: CC BY 4.0.
Third-party material keeps its own license (see `.claude/skills/THIRD_PARTY.md` and
the certificate provenance fields).
