#!/usr/bin/env python3
"""EXP-0004: estimate the size of a table-free lower-bound certificate for ||2^61-1|| > 126.

The EXP-0003 certificate uses a base table of ||v|| for v <= 10^8. A Lean kernel cannot load that.
`check_lower_strict.py --demand` lists which table entries the checker actually needed above the trivial
bound max(1, lambda(v)), and the value r needed for each.  Here we replace those entries by
sub-certificates: for each needed (v, r) we run the existing budgeted search with a tiny base table
(T0 = 1000) and budget r-1, and count the claims "||m|| > j" with m > T0 that it would emit.
Entries v <= T0 would be certified by T0 trivial claims (all v <= T0 in increasing order).

This is an ESTIMATE of certificate size (it uses the search program, so it proves nothing by itself).
Usage: python3 table_free_estimate.py TABLE_1e8.bin DEMAND.json STRIDE [T0]
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from algorithms.exact_single import ExactSearch

tpath, dpath, stride = sys.argv[1], sys.argv[2], int(sys.argv[3])
T0 = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
big = open(tpath, "rb").read()
small = list(big[:T0 + 1])
need = [(v, r) for v, r in json.load(open(dpath))["need"] if v > T0][::stride]


class Count:
    def __init__(self):
        self.claims = set()

    def claim(self, m, j):
        self.claims.add(m)


em = Count()
s = ExactSearch(small, emit=em)
sys.setrecursionlimit(100000)
t0 = time.time()
bad = 0
for i, (v, r) in enumerate(need):
    got = s.at_most(v, r - 1)
    if got <= r - 1:          # would contradict the table value: report, never hide
        bad += 1
print(json.dumps({"T0": T0, "stride": stride, "entries": len(need), "distinct_claimed_m": len(em.claims),
                  "search_calls": s.calls, "contradictions": bad, "sec": round(time.time() - t0, 1)}))
