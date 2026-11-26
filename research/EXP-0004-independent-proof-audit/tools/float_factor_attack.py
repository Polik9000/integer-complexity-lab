#!/usr/bin/env python3
"""EXP-0004 finding F1: check_lower.py accepts a FALSE claim when a factor prime is a JSON float.

The claim  ||4*3^33|| > 103  is false: 4*3^33 has an expression with 2*2 + 3*33 = 103 ones.
We present a fake factorization m ~ q * p where p is written as a JSON float (p.0). Python's
float multiplication rounds q*p to exactly m, so `prod != m` passes, and the true divisors of m
(2, 3, 4, 6, ...) are never enumerated.  The real EXP-0003 certificate is not affected if it
contains only integer tokens (see scan_cert_tokens.py).

Usage: python3 float_factor_attack.py PATH/TO/check_lower.py PATH/TO/check_lower_strict.py WORKDIR
"""
import gzip, hashlib, json, os, subprocess, sys

checker, strict, work = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(work, exist_ok=True)

# small exact table, own DP (no repository code): c[v] = ||v||, v <= T
T = 50   # attacker-chosen small table; q = 83 > T so q is looked up via lambda
c = [0] * (T + 1)
c[1] = 1
for v in range(2, T + 1):
    b = min(c[x] + c[v - x] for x in range(1, v // 2 + 1))
    d = 2
    while d * d <= v:
        if v % d == 0:
            b = min(b, c[d] + c[v // d])
        d += 1
    c[v] = b
assert c[2] == 2 and c[6] == 5 and c[46] == 12
table = bytes(c)  # c[v] = ||v|| exactly (independent brute-force DP)
tpath = os.path.join(work, "table_1000.bin")
open(tpath, "wb").write(table)
sha = hashlib.sha256(table).hexdigest()


def lam(v):
    j, p = 0, 1
    while p < v ** 3:
        p, j = p * 3, j + 1
    return j


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, REPO)
from algorithms.exact_single import factorize  # used only to BUILD the attack, never to check it


def factor_small(n):
    return sorted(factorize(n))


def pratt(p, recs, seen):
    if p < (1 << 16) or p in seen:
        return
    qs = factor_small(p - 1)
    for q in qs:
        pratt(q, recs, seen)
    a = 2
    while not (pow(a, p - 1, p) == 1 and all(pow(a, (p - 1) // q, p) != 1 for q in qs)):
        a += 1
    recs.append({"type": "prime", "p": p, "a": a, "q": qs})
    seen.add(p)


m = 4 * 3 ** 33            # exactly representable as a float
j = 103                    # FALSE claim: ||m|| <= 2*2 + 3*33 = 103
assert lam(m) == 103 and float(m) == m
# q * p = m - 1 (a semiprime); float(q) * float(p) rounds to exactly m (float spacing at m is 4).
# Found by a search over m = 2^a 3^k (EXP-0004 notes); re-checked here.
q, p = 83, 267906533327977
assert q * p == m - 1 and is_prime(q) and is_prime(p) and float(q) * float(p) == m
assert lam(q) + lam(m // q) > j and 1 + lam(m - 1) > j   # the only splits the checker will look at
found = (q, p)
assert found, "no suitable (q, p) found"
q, p = found
recs, seen = [], set()
pratt(q, recs, seen)
pratt(p, recs, seen)
lines = [json.dumps({"type": "header", "version": 1, "target": str(m), "claim_gt": j,
                     "table": {"T": T, "sha256": sha, "format": "uint8"}})]
lines += [json.dumps(r) for r in recs]
claim = '{"type":"claim","m":%d,"j":%d,"f":[[%d,1],[%d.0,1]]}' % (m, j, q, p)
lines.append(claim)
lines.append(json.dumps({"type": "end", "records": len(recs) + 1}))
cpath = os.path.join(work, "attack_float.jsonl")
open(cpath, "w").write("\n".join(lines) + "\n")
print("q =", q, " p =", p, " q*p - m =", q * p - m)
print("claim line:", claim)
print("--- certificates/lower/check_lower.py:")
r1 = subprocess.run([sys.executable, "-I", checker, cpath, tpath], capture_output=True, text=True)
print(r1.stdout.strip(), "(exit %d)" % r1.returncode)
print("--- EXP-0004 strict checker:")
r2 = subprocess.run([sys.executable, "-I", strict, cpath, tpath, str(m), str(j), sha], capture_output=True, text=True)
print(r2.stdout.strip(), "(exit %d)" % r2.returncode)
print("TRUTH: ||%d|| <= 103 via (1+1)^2*(1+1+1)^33, so the accepted claim is FALSE" % m)
