#!/usr/bin/env bash
# EXP-0002: exact ||2^k - 1|| for k = 20..61. ~6 min single core, ~1 GB RAM.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; WORK="${1:-$(mktemp -d)}"; mkdir -p "$WORK"; cd "$ROOT"
echo "commit: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
gcc -O2 -o "$WORK/complexity_table" algorithms/c/complexity_table.c
"$WORK/complexity_table" 400000000 "$WORK/c4e8.bin"
python3 "$(dirname "$0")/run_pilot.py" "$WORK/c4e8.bin" 20 61 600 | tee "$WORK/results.jsonl"
