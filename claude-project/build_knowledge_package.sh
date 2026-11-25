#!/usr/bin/env bash
# Build the Claude Chat knowledge package and Skill ZIPs from the current repository state.
# Usage (from anywhere):  bash claude-project/build_knowledge_package.sh
# Output: claude-project/dist/  (git-ignored)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/claude-project/dist"
rm -rf "$DIST"
mkdir -p "$DIST/knowledge" "$DIST/skills"
cd "$ROOT"

FILES=(
  README.md CLAUDE.md RESULTS.md RESEARCH_QUESTIONS.md RESEARCH_LOG.md BIBLIOGRAPHY.md
  docs/WORKFLOW.md docs/SKILLS.md
  research/2026-11-25-m61-benchmark-brief.md research/failed-approaches.md
  hypotheses/README.md hypotheses/H-*.md
  experiments/README.md experiments/EXP-*/README.md
  review-packages/TEMPLATE.md
  lean/README.md lean/IntegerComplexity/Basic.lean
  algorithms/README.md
)

COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo uncommitted)"
DIRTY="$(git status --porcelain 2>/dev/null | grep -q . && echo ' (with uncommitted changes)' || true)"
{
  echo "Knowledge snapshot of integer-complexity-lab"
  echo "commit: ${COMMIT}${DIRTY}"
  echo "built:  $(date -u +%Y-%m-%dT%H:%MZ)"
  echo "The GitHub repository is canonical; this snapshot may be outdated."
} > "$DIST/knowledge/KNOWLEDGE_VERSION.txt"

COMBINED="$DIST/ICL_KNOWLEDGE_COMBINED.md"
cat "$DIST/knowledge/KNOWLEDGE_VERSION.txt" > "$COMBINED"
for pattern in "${FILES[@]}"; do
  for f in $pattern; do
    [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
    flat="$(echo "$f" | tr '/' '__')"
    case "$f" in *.lean) cp "$f" "$DIST/knowledge/${flat}.txt" ;; *) cp "$f" "$DIST/knowledge/$flat" ;; esac
    printf '\n\n---\n\n# FILE: %s\n\n' "$f" >> "$COMBINED"
    case "$f" in *.lean) printf '```lean\n' >> "$COMBINED"; cat "$f" >> "$COMBINED"; printf '```\n' >> "$COMBINED" ;;
                 *) cat "$f" >> "$COMBINED" ;; esac
  done
done
(cd "$DIST/knowledge" && zip -q -r "$DIST/icl-knowledge.zip" .)

# Skill ZIPs: each ZIP contains one top-level folder named after the skill.
for s in record-research-result review-package complexity-certificate reproducible-experiment lean-proof paper-lookup citation-management; do
  (cd "$ROOT/.claude/skills" && zip -q -r "$DIST/skills/$s.zip" "$s" -x '*/__pycache__/*')
done

echo "knowledge files: $(ls "$DIST/knowledge" | wc -l), combined: $(wc -c < "$COMBINED") bytes"
ls -1 "$DIST/skills"
