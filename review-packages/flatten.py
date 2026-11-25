#!/usr/bin/env python3
"""Flatten a review package directory into one Markdown file for upload or pasting.

Usage: python3 review-packages/flatten.py review-packages/RP-NNNN-name [--include PATH ...]

Writes review-packages/RP-NNNN-name.md: the package README, then each --include file
(repository-relative) in a fenced block. Files over 200 kB are skipped with a note.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("--include", nargs="*", default=[])
    a = ap.parse_args()
    pkg = Path(a.package).resolve()
    parts = [(pkg / "README.md").read_text()]
    for rel in a.include:
        p = (ROOT / rel).resolve()
        if not p.is_relative_to(ROOT):
            raise SystemExit(f"refusing to include a file outside the repository: {rel}")
        body = p.read_text()
        if len(body) > 200_000:
            parts.append(f"\n---\n### `{rel}`\n\n(skipped: {len(body)} bytes)\n")
            continue
        lang = {".py": "python", ".lean": "lean", ".c": "c", ".json": "json", ".sh": "bash"}.get(p.suffix, "")
        parts.append(f"\n---\n### `{rel}`\n\n```{lang}\n{body.rstrip()}\n```\n")
    out = pkg.with_suffix(".md")
    out.write_text("\n".join(parts))
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
