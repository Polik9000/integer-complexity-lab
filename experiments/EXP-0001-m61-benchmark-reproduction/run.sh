#!/usr/bin/env bash
# EXP-0001: reproduce an upper bound ||2^61-1|| <= 127 from scratch.
# Usage (from repo root):  bash experiments/EXP-0001-m61-benchmark-reproduction/run.sh [WORKDIR]
# Needs: gcc, python3 >= 3.10, ~400 MB RAM and disk. Runtime ~1 min on 1 core.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="${1:-$(mktemp -d)}"
mkdir -p "$WORK"
cd "$ROOT"
echo "commit: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
gcc -O2 -o "$WORK/complexity_table" algorithms/c/complexity_table.c
time "$WORK/complexity_table" 400000000 "$WORK/c4e8.bin"
sha256sum "$WORK/c4e8.bin"
for cfg in "-R 4 -D 16" "-R 1 -D 100"; do
  python3 -m algorithms.upper_bound_search '2^61-1' --table "$WORK/c4e8.bin" $cfg \
    --out "$WORK/ub_$(echo "$cfg" | tr -d ' -').json"
done
python3 certificates/verify.py "$WORK/ub_R1D100.json"
