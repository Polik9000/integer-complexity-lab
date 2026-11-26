#!/usr/bin/env bash
# EXP-0004: regenerate the table-free certificate for ||2^61-1|| > 126 and check it with BOTH checkers.
# Usage: run_tablefree.sh WORKDIR     (~1 min table, ~6 min generation, ~3 min per check; < 1 GB RAM)
# The 10^8 table is used ONLY to seed the search (as hints); the certificate's header names the
# trivial table [0, 1] (T = 1), and the checkers are run against that 2-byte table.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../.." && pwd)"; WORK="${1:?workdir}"
N=2305843009213693951; TRIV_SHA=b413f47d13ee2fe6c845b2ee141af81de858df4ec549a58b7970bb96645bc8d2
mkdir -p "$WORK"; cd "$ROOT"
gcc -O2 -o "$WORK/complexity_table" algorithms/c/complexity_table.c
"$WORK/complexity_table" 100000000 "$WORK/table_1e8.bin"
echo "34dbc4da4f105ff7cc01942a6d7b491efba5bceee44bbad87fb0540e461b38f6  $WORK/table_1e8.bin" | sha256sum -c -
python3 -c "open('$WORK/trivial_table.bin','wb').write(bytes([0,1]))"
echo "$TRIV_SHA  $WORK/trivial_table.bin" | sha256sum -c -
python3 "$HERE/gen_table_free_cert.py" "$WORK/table_1e8.bin" 61 127 "$WORK/tablefree_k61.jsonl.gz" \
  "$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
out1=$(python3 -I "$HERE/check_lower_strict.py" "$WORK/tablefree_k61.jsonl.gz" "$WORK/trivial_table.bin" $N 126 $TRIV_SHA)
echo "$out1"; [[ "$out1" == "ACCEPTED: ||$N|| > 126"* ]]
# check_lower.py version 2 (EXP-0005, merged in PR #6) must be given the expected statement
out2=$(python3 -I certificates/lower/check_lower.py "$WORK/tablefree_k61.jsonl.gz" "$WORK/trivial_table.bin" \
  --target $N --claim-gt 126 --table-sha256 $TRIV_SHA)
echo "$out2"; [[ "$out2" == "ACCEPTED: ||$N|| > 126  (table sha256 $TRIV_SHA)" ]]
echo "BOTH CHECKERS ACCEPT (table-free)"
