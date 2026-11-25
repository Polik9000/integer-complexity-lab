#!/usr/bin/env bash
# EXP-0003 step 2: certificate for ||2^61-1|| > 126, checked by the independent checker.
# Usage: run_cert.sh WORKDIR [K] [U]     (default K=61, U=127). ~4 min generate + ~1 min check, < 1 GB RAM.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; WORK="${1:?workdir}"; K="${2:-61}"; U="${3:-127}"
mkdir -p "$WORK"; cd "$ROOT"
gcc -O2 -o "$WORK/complexity_table" algorithms/c/complexity_table.c
"$WORK/complexity_table" 100000000 "$WORK/table_1e8.bin"
echo "34dbc4da4f105ff7cc01942a6d7b491efba5bceee44bbad87fb0540e461b38f6  $WORK/table_1e8.bin" | sha256sum -c -
python3 "$(dirname "$0")/gen_cert.py" "$WORK/table_1e8.bin" "$K" "$U" "$WORK/cert_k$K.jsonl.gz" \
  "$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
python3 -I certificates/lower/check_lower.py "$WORK/cert_k$K.jsonl.gz" "$WORK/table_1e8.bin"
# Optional table cross-check with He's independent table (needs run_he.sh, see README):
#   bash experiments/EXP-0003-independent-verification/run_he.sh "$WORK/he" dump "$WORK/he_table_1e8.bin"
#   cmp "$WORK/table_1e8.bin" "$WORK/he_table_1e8.bin"
