#!/usr/bin/env bash
# EXP-0003 step 3: run He's single-target solver (GPL, not vendored) on 2^k - 1.
# Usage: run_he.sh WORKDIR [K0] [K1].  ~20 s CPU for k = 2..61, < 2 GB RAM.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="${1:?workdir}"; K0="${2:-2}"; K1="${3:-61}"
mkdir -p "$WORK"; cd "$WORK"
[ -d integer_complexity ] || git clone -q https://github.com/hqztrue/integer_complexity.git
git -C integer_complexity checkout -q 742e8c5
SRC=integer_complexity/integer-complexity-128
echo "single.cpp sha256: $(sha256sum $SRC/single.cpp | cut -d' ' -f1)"   # expect 8d35c1d6...
cp "$HERE/he_driver.cpp" "$SRC/driver.cpp"
g++ -O2 -fpermissive -w "$SRC/driver.cpp" -o he_driver
./he_driver "$K0" "$K1" 2>/dev/null | grep '^{' | tee results_he.jsonl
python3 -I "$HERE/compare.py" results_he.jsonl
