# Setting up the Claude Chat project (about 5 minutes)

1. **Build the package** (Claude Code does this; you can also run it yourself):
   ```bash
   bash claude-project/build_knowledge_package.sh
   ```
   Output in `claude-project/dist/`:
   - `knowledge/`: the files to upload as project knowledge, plus `KNOWLEDGE_VERSION.txt`
   - `icl-knowledge.zip`: the same files zipped, for download and transfer
   - `ICL_KNOWLEDGE_COMBINED.md`: everything in one file, if you'd rather upload a single file
   - `skills/*.zip`: Skills packaged for upload to Claude Chat

2. **Create the project** in Claude (claude.ai → Projects → New project).
   - Name: `Integer Complexity Lab – Mathematical Research`
   - Description: "Research planning, literature and mathematics for the integer-complexity-lab repository."

3. **Instructions:** paste the part of `claude-project/PROJECT_INSTRUCTIONS.md` below the line.

4. **Knowledge:** upload either all files from `dist/knowledge/` or the single
   `ICL_KNOWLEDGE_COMBINED.md`. Don't upload both, because duplicates waste context.
   If GitHub integration is available in your plan, you can instead add the repository
   (after it's published) as a knowledge source and select the same files. That keeps them in sync.

5. **Skills** (optional; Settings → Capabilities → Skills → upload ZIP). Recommended:
   `record-research-result.zip`, `review-package.zip`, `complexity-certificate.zip`,
   `lean-proof.zip`, `paper-lookup.zip`. Skills are account-wide, not per project.

6. **Refresh** the knowledge after significant repository changes: rebuild, delete the old files in
   the project, and upload the new ones. Check `KNOWLEDGE_VERSION.txt`.

## First prompt to try

> Read RESULTS.md and the research brief. Summarize what is known about ‖2^61−1‖ with evidence
> statuses, then propose a reading plan for He (2024) and Altman (2016, 2019) aimed at RQ-1 and RQ-3.
