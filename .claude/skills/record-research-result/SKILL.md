---
name: record-research-result
description: Use in the Integer Complexity Lab whenever a mathematical claim, result, decision, or failed approach should be recorded, or a claim's evidence status changes. Updates RESULTS.md, RESEARCH_LOG.md, hypotheses and the bibliography consistently.
---

# Record a research result

The repository is the canonical record (CLAUDE.md §3). A result that is not written down in it
does not exist. Do this in the same session in which the result appears.

## 1. Classify the claim

Pick exactly one status (two if both apply) from CLAUDE.md §4:
`PROVEN`, `FORMALLY VERIFIED`, `COMPUTATIONALLY VERIFIED`, `LITERATURE`, `CONJECTURE`,
`OBSERVATION`, `UNVERIFIED`, `REFUTED`.

Decision rules:
- An expression or other witness proves only an **upper bound** (`COMPUTATIONALLY VERIFIED`).
- "A search found nothing better" is an `OBSERVATION`, never a lower bound.
- A computation over a finite range is `COMPUTATIONALLY VERIFIED` only with an experiment
  record and preferably two independent implementations.
- A literature statement is `LITERATURE` until we have checked it ourselves, and only after the
  source has been read at the stated location (record that in BIBLIOGRAPHY.md).
- Anything from a chat, a web page, or memory, if not checked, is `UNVERIFIED`.
- When unsure, use the weaker status and say why.

## 2. Write it down

1. `RESULTS.md`: add a row `R-NNNN | statement | status | evidence link`. Never delete a row.
   If you supersede one, move the old row to "History" with the date and reason.
2. `RESEARCH_LOG.md`: append a dated entry. Say what was done, what was found, what failed,
   and which decisions were taken and by whom.
3. If the claim came from a hypothesis, update `hypotheses/H-NNNN-*.md` (status, evidence).
4. If a source was used, update `BIBLIOGRAPHY.md` with what exactly was verified, and where.
5. If an approach failed, add it to `research/failed-approaches.md` with enough detail that
   nobody repeats it blindly.

## 3. Check before committing

- The statement is precise. Quantifiers, ranges and the exact n are explicit.
- The evidence link resolves to a file in the repository.
- `python3 -m pytest -q` passes. If a certificate changed, run `python3 certificates/verify.py`.
- The commit message names the R-/H-/EXP- IDs.

Publicizing a result (posting, submitting to a board, contacting authors) needs the human
lead's explicit approval.
