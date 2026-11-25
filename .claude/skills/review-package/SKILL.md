---
name: review-package
description: Use in the Integer Complexity Lab when a result, proof, or plan should be sent to the independent reviewer (ChatGPT) or another external reviewer. Builds review-packages/RP-NNNN-*/ from the template, self-contained and with honest uncertainties.
---

# Prepare a review package

The reviewer sees only the package, not our chats. It must stand alone.

1. Copy `review-packages/TEMPLATE.md` to `review-packages/RP-NNNN-short-name/README.md`
   (next free number).
2. Fill in every section:
   - **Exact claim**: one precise statement, with its current evidence status.
   - **What we ask the reviewer**: specific questions (e.g. "find a gap in step 3", "check
     the pruning argument", "is this already known?").
   - **Relevant files**: repository paths *and* inline copies of the essential short
     excerpts. The reviewer may not have repository access.
   - **Mathematical reasoning**: the argument, in full, at the level of detail of a referee report.
   - **Reproducibility**: commands, expected outputs and checksums.
   - **Known uncertainties and weak points**: list them first-hand. Don't hide them.
3. Stick to verifiable content. Leave out credentials, personal data and local paths.
4. If the package should be uploaded or pasted, also produce `RP-NNNN.md` as a single
   flattened file: `python3 review-packages/flatten.py review-packages/RP-NNNN-short-name`.
5. When the review comes back, save it verbatim as `review-packages/RP-NNNN-*/review-<date>.md`,
   then write `response.md`: each point accepted / rejected (with reason) / follow-up.
   Update statuses with the `record-research-result` skill. A reviewer's agreement never
   upgrades a status by itself. Only evidence does.
