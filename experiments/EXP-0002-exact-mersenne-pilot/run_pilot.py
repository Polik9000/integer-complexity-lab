#!/usr/bin/env python3
"""EXP-0002 pilot: exact ||2^k-1|| by budgeted exhaustive search.
Usage: python3 run_pilot.py TABLE.bin K_FROM K_TO TIMEOUT_SEC
Upper bound per k comes from the peel search; the exact search then proves optimality.
"""
import sys, time, math, json, signal
from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from algorithms.exact_table import ByteTable
from algorithms.exact_single import ExactSearch
from algorithms.upper_bound_search import PeelSearch
tab = ByteTable(sys.argv[1]); ks = range(int(sys.argv[2]), int(sys.argv[3])+1)
sys.setrecursionlimit(100000)
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
for k in ks:
    n = 2**k - 1
    p = PeelSearch(tab, tab.N, 1, 100); ub = p.ub(n)
    s = ExactSearch(tab)
    t = time.time(); signal.alarm(int(sys.argv[4]))
    try:
        v = s.complexity(n, ub); signal.alarm(0)
        print(json.dumps({"k":k,"ub_peel":ub,"exact":v,"A=v-2k":v-2*k,"slack":round(ub-3*math.log(n,3),2),"calls":s.calls,"sec":round(time.time()-t,2)}), flush=True)
    except TO:
        print(json.dumps({"k":k,"ub_peel":ub,"timeout":int(sys.argv[4]),"calls":s.calls}), flush=True); break
