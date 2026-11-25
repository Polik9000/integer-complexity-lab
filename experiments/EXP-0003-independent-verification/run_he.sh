#!/usr/bin/env bash
# EXP-0003 step 3: run He's single-target solver (GPL, not vendored) on 2^k - 1.
# Usage: run_he.sh WORKDIR [K0] [K1] [MODE]
#   MODE=upstream (default): upstream single.cpp, unmodified.
#   MODE=naive: a *copy* of single.cpp with he_naive_lb.patch applied (Selfridge lower bound only).
# The upstream checkout is never modified; the script aborts if its SHA-256 differs.
# ~20 s CPU for k = 2..61 (upstream), < 2 GB RAM.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="${1:?workdir}"; K0="${2:-2}"; K1="${3:-61}"; MODE="${4:-upstream}"
EXPECTED_SHA=8d35c1d68a6c3276238cb848b97b28f8d1a13becca1c4e7520985f55a6fbeb87
mkdir -p "$WORK"; cd "$WORK"
[ -d integer_complexity ] || git clone -q https://github.com/hqztrue/integer_complexity.git
git -C integer_complexity checkout -q 742e8c5
UP=integer_complexity/integer-complexity-128
echo "$EXPECTED_SHA  $UP/single.cpp" | sha256sum -c --quiet - \
  || { echo "ABORT: upstream single.cpp does not match the inspected version" >&2; exit 2; }
BUILD="build-$MODE"; rm -rf "$BUILD"; cp -r "$UP" "$BUILD"
case "$MODE" in
  upstream) ;;
  naive) (cd "$BUILD" && patch -s -p2 < "$HERE/he_naive_lb.patch") ;;
  *) echo "unknown MODE $MODE" >&2; exit 2 ;;
esac
cp "$HERE/he_driver.cpp" "$BUILD/driver.cpp"
g++ -O2 -fpermissive -w "$BUILD/driver.cpp" -o "he_driver_$MODE"
echo "$EXPECTED_SHA  $UP/single.cpp" | sha256sum -c --quiet -   # upstream still untouched
"./he_driver_$MODE" "$K0" "$K1" 2>/dev/null | grep '^{' | tee "results_he_$MODE.jsonl"
python3 -I "$HERE/compare.py" "results_he_$MODE.jsonl"
