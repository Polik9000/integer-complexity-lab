"""EXP-0004: tests for the second (strict) lower-bound checker and for the float-factor finding F1.

The strict checker lives in research/EXP-0004-independent-proof-audit/tools/. These tests do not change
or weaken any existing test. The former xfail test documented hole F1 in certificates/lower/check_lower.py version 1 (fixed in version 2);
after PR #6 merged it was turned into a normal test, as planned.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "research" / "EXP-0004-independent-proof-audit" / "tools"
STRICT = TOOLS / "check_lower_strict.py"
ORIG = ROOT / "certificates" / "lower" / "check_lower.py"


def brute_table(T):
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
    return c


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return sorted(f.items())


def write(tmp, name, table, lines):
    tp = tmp / (name + ".bin")
    tp.write_bytes(bytes(table))
    cp = tmp / (name + ".jsonl")
    cp.write_text("\n".join(lines) + "\n")
    return cp, tp, hashlib.sha256(bytes(table)).hexdigest()


def header(target, gt, T, sha):
    return json.dumps({"type": "header", "version": 1, "target": str(target), "claim_gt": gt,
                       "table": {"T": T, "sha256": sha, "format": "uint8"}})


def run(checker, *args):
    r = subprocess.run([sys.executable, "-I", str(checker), *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout


def table_free_cert(n, c):
    """Claims G(v, ||v||-1) for v = 2..n in increasing order, trivial table [0, 1]."""
    return [json.dumps({"type": "claim", "m": v, "j": c[v] - 1, "f": [[p, e] for p, e in factor(v)]})
            for v in range(2, n + 1)]


def test_strict_accepts_table_free_small(tmp_path):
    c = brute_table(300)
    sha = hashlib.sha256(bytes([0, 1])).hexdigest()
    body = table_free_cert(300, c)
    cp, tp, sha = write(tmp_path, "tf", [0, 1], [header(300, c[300] - 1, 1, sha)] + body +
                        [json.dumps({"type": "end", "records": len(body)})])
    assert run(STRICT, cp, tp, 300, c[300] - 1, sha)[0] == 0
    assert run(ORIG, cp, tp, "--target", 300, "--claim-gt", c[300] - 1, "--table-sha256", sha)[0] == 0


def test_strict_rejects_overclaim_table_free(tmp_path):
    c = brute_table(200)
    sha = hashlib.sha256(bytes([0, 1])).hexdigest()
    body = table_free_cert(200, c)
    body[-1] = json.dumps({"type": "claim", "m": 200, "j": c[200], "f": [[2, 3], [5, 2]]})  # false: ||200|| > ||200||
    cp, tp, sha = write(tmp_path, "tf", [0, 1], [header(200, c[200], 1, sha)] + body +
                        [json.dumps({"type": "end", "records": len(body)})])
    assert run(STRICT, cp, tp, 200, c[200], sha)[0] == 1
    assert run(ORIG, cp, tp, "--target", 200, "--claim-gt", c[200], "--table-sha256", sha)[0] == 1


# F1: m = 4*3^33 has ||m|| <= 103; q*p = m - 1 with q = 83, p = 267906533327977 (both prime),
# and float(q) * float(p) == m. Writing p as a JSON float hides the true divisors of m.
F1_M, F1_J, F1_Q, F1_P = 4 * 3 ** 33, 103, 83, 267906533327977


def f1_cert(tmp_path):
    T = 50
    c = brute_table(T)
    pre, seen = [], set()

    def pratt(n):                      # recursive Pratt records, factors of n - 1 by trial division
        if n < 1 << 16 or n in seen:
            return
        qs = [q for q, _ in factor(n - 1)]
        for q in qs:
            pratt(q)
        w = 2
        while not (pow(w, n - 1, n) == 1 and all(pow(w, (n - 1) // q, n) != 1 for q in qs)):
            w += 1
        pre.append(json.dumps({"type": "prime", "p": n, "a": w, "q": qs}))
        seen.add(n)

    pratt(F1_P)
    lines = pre + ['{"type":"claim","m":%d,"j":%d,"f":[[%d,1],[%d.0,1]]}' % (F1_M, F1_J, F1_Q, F1_P)]
    sha = hashlib.sha256(bytes(c)).hexdigest()
    cp, tp, sha = write(tmp_path, "f1", c, [header(F1_M, F1_J, T, sha)] + lines +
                        [json.dumps({"type": "end", "records": len(lines)})])
    return cp, tp, sha


def test_f1_facts():
    assert F1_Q * F1_P == F1_M - 1 and float(F1_Q) * float(F1_P) == F1_M
    # the claim is false: (1+1)*(1+1) * (1+1+1)^33 uses 4 + 99 = 103 ones
    assert 2 * 2 + 3 * 33 == F1_J


def test_strict_rejects_float_factor(tmp_path):
    cp, tp, sha = f1_cert(tmp_path)
    code, out = run(STRICT, cp, tp, F1_M, F1_J, sha)
    assert code == 1 and "non-integer" in out


# Was a strict xfail documenting F1 in check_lower.py version 1. Version 2 (EXP-0005, PR #6, merged) fixes F1,
# so the test now passes and the xfail marker is removed.
def test_orig_rejects_float_factor(tmp_path):
    cp, tp, sha = f1_cert(tmp_path)
    code, out = run(ORIG, cp, tp, "--target", F1_M, "--claim-gt", F1_J, "--table-sha256", sha)
    assert code == 1 and "non-integer" in out


def test_strict_rejects_m_equal_one(tmp_path):
    # with a 1-byte table (T = 0) a claim ||1|| > 5 has no splits at all; Lemma 2 needs m >= 2
    sha = hashlib.sha256(bytes([0])).hexdigest()
    lines = [json.dumps({"type": "claim", "m": 1, "j": 5, "f": []})]
    cp, tp, sha = write(tmp_path, "m1", [0], [header(1, 5, 0, sha)] + lines +
                        [json.dumps({"type": "end", "records": 1})])
    assert run(STRICT, cp, tp, 1, 5, sha)[0] == 1


def test_strict_pins_header(tmp_path):
    c = brute_table(100)
    sha = hashlib.sha256(bytes([0, 1])).hexdigest()
    body = table_free_cert(100, c)
    cp, tp, sha = write(tmp_path, "pin", [0, 1], [header(100, c[100] - 1, 1, sha)] + body +
                        [json.dumps({"type": "end", "records": len(body)})])
    assert run(STRICT, cp, tp, 100, c[100] - 1, sha)[0] == 0
    assert run(STRICT, cp, tp, 99, c[100] - 1, sha)[0] == 1      # wrong expected target
    assert run(STRICT, cp, tp, 100, c[100] - 2, sha)[0] == 1     # wrong expected claim
    assert run(STRICT, cp, tp, 100, c[100] - 1, "0" * 64)[0] == 1  # wrong expected table hash
