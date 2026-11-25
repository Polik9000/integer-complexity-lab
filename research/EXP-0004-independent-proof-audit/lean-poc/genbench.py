"""Benchmark certificates with divisor hints: table-free closure for target N (values <= 1e8)."""
import sys, math
sys.setrecursionlimit(100000)
import sys
import os
c = open(os.environ.get('ICL_TABLE', 'table_1e8.bin'), 'rb').read()  # the 10^8 table from run_cert.sh
N = int(sys.argv[1]); out = sys.argv[2]; tactic = sys.argv[3]
def lam(v):
    j, cc, p = 0, v**3, 1
    while p < cc: p *= 3; j += 1
    return j
def base(v): return max(1, lam(v))
def fac(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def divs(m):
    ds = [1]
    for p, e in fac(m).items(): ds = [d * p**i for d in ds for i in range(e + 1)]
    return sorted(d for d in ds if d >= 2 and d * d <= m)
done = {}; order = []; st = {'sums': 0, 'divs': 0}
def need(v, t):
    if t <= base(v) or done.get(v, -1) >= t - 1: return
    prove(v, t - 1)
def prove(m, j):
    ds = []
    if 3**j >= m**3:
        x = 1
        while 2 * x <= m and (x * (m - x))**3 <= 3**j:
            split(x, m - x, j); x += 1; st['sums'] += 1
        ds = divs(m)
        for d in ds: split(d, m // d, j); st['divs'] += 1
    done[m] = max(done.get(m, -1), j); order.append((m, j, ds))
def split(p, q, j):
    tp = max(base(p), j + 1 - c[q]); tq = max(base(q), j + 1 - tp)
    need(p, tp); need(q, tq)
prove(N, c[N] - 1)
with open(out, 'w') as f:
    f.write("import IntegerComplexity.PoC.Bench\nopen IntegerComplexity IntegerComplexity.Bench\n")
    f.write("def certB : List (Nat × Nat × List Nat) := [" +
            ', '.join(f'({m}, {j}, [{", ".join(map(str, ds))}])' for m, j, ds in order) + "]\n")
    f.write(f"set_option maxRecDepth 100000 in\ntheorem certB_ok : checkAllH .leaf certB = true := by {tactic}\n")
print(N, 'claims', len(order), st)
