"""Hardening tests for certificates/lower/check_lower.py (EXP-0004 findings F1, F2, M1, F3-F7).

Three groups:
1. Every exploit found in the EXP-0004 audit, as a concrete certificate that must be REJECTED.
2. A "battery" that checks every split the spec requires is really checked: for a true claim
   G(m, ||m|| - 1), weakening the (still valid) lower-bound table at the two parts of any one
   required split must make the checker reject. Plus Pratt negatives whose verdict depends on the
   prime record (the old Pratt tests were rejected at `end` whatever the prime record said).
3. Mutation testing as a standing check: each listed source mutation of the checker must make at
   least one battery check fail. If you change the checker, keep the mutants in sync (the test
   fails loudly if a mutant's source pattern disappears).
"""
import gzip
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from algorithms.exact_table import complexity_table

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "certificates" / "lower" / "check_lower.py"
SRC = CHECKER.read_text()

EXACT_N = 3000
EXACT = complexity_table(EXACT_N)          # exact ||v|| for v <= 3000


def load(source=SRC, name="check_lower_under_test"):
    spec = importlib.util.spec_from_loader(name, loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(source, str(CHECKER), "exec"), mod.__dict__)
    return mod


CL = load()


def lam(v):
    j, p = 0, 1
    while p < v ** 3:
        p, j = p * 3, j + 1
    return j


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return [[p, e] for p, e in sorted(f.items())]


def sha(table):
    return hashlib.sha256(bytes(table)).hexdigest()


def header(target, gt, table, **extra):
    h = {"type": "header", "version": 1, "target": str(target), "claim_gt": gt,
         "table": {"T": len(table) - 1, "sha256": sha(table)}}
    h.update(extra)
    return json.dumps(h)


def claim(m, j, f=None):
    return json.dumps({"type": "claim", "m": m, "j": j, "f": factor(m) if f is None else f})


def end(n):
    return json.dumps({"type": "end", "records": n})


def cert(target, gt, table, body):
    return [header(target, gt, table)] + body + [end(len(body))]


def run(mod, lines, table, target=None, gt=None):
    """True if accepted, False if rejected (any other exception is a test failure)."""
    try:
        mod.Checker(bytes(table)).run(lines, sha(table), target, gt)
        return True
    except mod.Reject:
        return False


def pratt_records(p, seen=None):
    """Pratt records (in dependency order) for a prime p, factoring p - 1 by trial division."""
    seen = set() if seen is None else seen
    out = []
    if p < 1 << 16 or p in seen:
        return out
    qs = [q for q, _ in factor(p - 1)]
    for q in qs:
        out += pratt_records(q, seen)
    a = 2
    while not (pow(a, p - 1, p) == 1 and all(pow(a, (p - 1) // q, p) != 1 for q in qs)):
        a += 1
    out.append(json.dumps({"type": "prime", "p": p, "a": a, "q": qs}))
    seen.add(p)
    return out


# ------------------------------------------------------------------------------------------
# 1. Known exploits (EXP-0004 adversarial review A1-A7, F2, F5-F7). All must be rejected.
# ------------------------------------------------------------------------------------------

SMALL50 = EXACT[:51]


def f1_float_cert():
    """F1: ||4*3^33|| > 103 is false; 83 * 267906533327977 = m - 1 rounds to m in floats."""
    m, j, q, p = 4 * 3 ** 33, 103, 83, 267906533327977
    assert q * p == m - 1 and float(q) * float(p) == m
    body = pratt_records(p) + ['{"type":"claim","m":%d,"j":%d,"f":[[%d,1],[%d.0,1]]}' % (m, j, q, p)]
    return cert(m, j, SMALL50, body), SMALL50, m, j


def test_f1_float_factor_rejected():
    lines, table, m, j = f1_float_cert()
    assert not run(CL, lines, table)
    assert not run(CL, lines, table, m, j)


def test_float_and_bool_tokens_rejected_everywhere():
    table = SMALL50
    base = cert(1009, 0, table, [claim(1009, 0)])           # a true, trivially checkable claim
    assert run(CL, base, table, 1009, 0)
    variants = [
        base[1].replace('"j": 0', '"j": 0.0'),
        base[1].replace('"m": 1009', '"m": 1009.0'),
        base[1].replace('[[1009, 1]]', '[[1009, true]]'),
        base[1].replace('[[1009, 1]]', '[[1009, 1.0]]'),
        base[1].replace('[[1009, 1]]', '[[1009.0, 1]]'),
        base[1].replace('[[1009, 1]]', '[[1009, 1e0]]'),
        base[1].replace('"j": 0', '"j": NaN'),
        base[1].replace('"j": 0', '"j": false'),
    ]
    for v in variants:
        assert v != base[1]
        assert not run(CL, [base[0], v, base[2]], table), v


@pytest.mark.parametrize("T", [0, -1])
def test_degenerate_tables_and_m_equal_one_rejected(T):
    """A4-A7: with T <= 0 the old checker accepted ||1|| > 100 and cascades from it."""
    table = [0, 1][: T + 1]
    for body in ([claim(1, 100, [])],
                 [claim(1, 11, []), claim(2, 11)],
                 ['{"type":"claim","m":true,"j":5,"f":[]}']):
        lines = [json.dumps({"type": "header", "version": 1, "target": "2", "claim_gt": 11,
                             "table": {"T": T, "sha256": sha(table)}})] + body + [end(len(body))]
        assert not run(CL, lines, table)


def test_m_equal_one_rejected_even_with_valid_table():
    table = [0, 1]
    assert not run(CL, cert(1, 0, table, [claim(1, 0, [])]), table)


@pytest.mark.parametrize("gt", ["NaN", "-Infinity", "-1", "126.5", '"126"', "true"])
def test_bad_claim_gt_rejected(gt):
    table = SMALL50
    h = header(1009, 0, table).replace('"claim_gt": 0', '"claim_gt": ' + gt)
    assert not run(CL, [h, claim(1009, 0), end(1)], table)


def test_duplicate_keys_rejected():
    table = SMALL50
    h = header(1009, 0, table)[:-1] + ', "claim_gt": 0}'
    assert not run(CL, [h, claim(1009, 0), end(1)], table)
    c = claim(1009, 0)[:-1] + ', "j": 0}'
    assert not run(CL, [header(1009, 0, table), c, end(1)], table)


def test_header_fields_validated():
    table = SMALL50
    good = cert(1009, 0, table, [claim(1009, 0)])
    assert run(CL, good, table)
    h = json.loads(good[0])
    for mut in ({"version": True}, {"version": 2}, {"target": 1009}, {"target": "01009"},
                {"target": "1009.0"}, {"target": " 1009"}, {"table": {"T": 50.0, "sha256": sha(table)}},
                {"table": {"T": 50, "sha256": "0" * 64}}, {"table": {"T": 49, "sha256": sha(table)}},
                {"extra": 1}):
        hh = dict(h); hh.update(mut)
        assert not run(CL, [json.dumps(hh)] + good[1:], table), mut


def test_expected_statement_is_bound():
    table = SMALL50
    good = cert(1009, 0, table, [claim(1009, 0)])
    assert run(CL, good, table, 1009, 0)
    assert not run(CL, good, table, 1013, 0)        # wrong expected target
    assert not run(CL, good, table, 1009, 1)        # wrong expected claim


def test_records_fields_validated():
    table = SMALL50
    good = cert(1009, 0, table, [claim(1009, 0)])
    r = json.loads(good[1]); r["note"] = "x"
    assert not run(CL, [good[0], json.dumps(r), good[2]], table)
    e = json.loads(good[2]); e["records"] = True
    assert not run(CL, good[:2] + [json.dumps(e)], table)
    assert not run(CL, [good[0], "[1, 2]", good[2]], table)                       # not an object
    assert not run(CL, good[:2] + [json.dumps({"type": "end", "records": 1, "x": 0})], table)


def test_last_claim_must_be_target():
    table = SMALL50
    body = [claim(1009, 0), claim(1013, 0)]
    assert not run(CL, cert(1009, 0, table, body), table)
    assert run(CL, cert(1013, 0, table, body), table)


def test_huge_j_and_exponent_rejected_quickly():
    table = SMALL50
    assert not run(CL, cert(1009, 10 ** 6, table, [claim(1009, 10 ** 6)]), table)
    assert not run(CL, cert(1024, 0, table, [claim(1024, 0, [[2, 10 ** 9]])]), table)


def test_cli_requires_and_checks_expected_statement(tmp_path):
    lines, table, m, j = f1_float_cert()
    good = cert(1009, 0, SMALL50, [claim(1009, 0)])
    tp = tmp_path / "t.bin"; tp.write_bytes(bytes(SMALL50))
    cp = tmp_path / "c.jsonl"; cp.write_text("\n".join(good) + "\n")
    gz = tmp_path / "c.jsonl.gz"
    with gzip.open(gz, "wt") as fh:
        fh.write("\n".join(good) + "\n")
    trunc = tmp_path / "trunc.jsonl.gz"; trunc.write_bytes(gz.read_bytes()[:-12])
    fp = tmp_path / "f1.jsonl"; fp.write_text("\n".join(lines) + "\n")

    def cli(*args):
        r = subprocess.run([sys.executable, "-I", str(CHECKER), *map(str, args)], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    s = sha(SMALL50)
    code, out = cli(cp, tp, "--target", 1009, "--claim-gt", 0, "--table-sha256", s)
    assert code == 0 and out.startswith("ACCEPTED: ||1009|| > 0") and s in out
    assert cli(gz, tp, "--target", 1009, "--claim-gt", 0, "--table-sha256", s)[0] == 0
    assert cli(cp, tp)[0] != 0                                                     # expected values required
    assert cli(cp, tp, "--target", 1013, "--claim-gt", 0, "--table-sha256", s)[0] == 1
    assert cli(cp, tp, "--target", 1009, "--claim-gt", 1, "--table-sha256", s)[0] == 1
    assert cli(cp, tp, "--target", 1009, "--claim-gt", 0, "--table-sha256", "0" * 64)[0] == 1
    code, out = cli(trunc, tp, "--target", 1009, "--claim-gt", 0, "--table-sha256", s)
    assert code == 1 and out.startswith("REJECTED") and "Traceback" not in out
    code, out = cli(fp, tp, "--target", m, "--claim-gt", j, "--table-sha256", s)
    assert code == 1 and out.startswith("REJECTED")


# ------------------------------------------------------------------------------------------
# 2. Battery: every required split is checked; Pratt records really matter.
# ------------------------------------------------------------------------------------------

def required_splits(m, j):
    out = []
    x = 1
    while 2 * x <= m and (x * (m - x)) ** 3 <= 3 ** j:
        out.append((x, m - x))
        x += 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            out.append((d, m // d))
        d += 1
    return out


BATTERY_M = [1439, 1458, 1849, 2048, 2187, 2310, 2401, 2999]   # prime, 2*3^6, 43^2, 2^11, 3^7, 2*3*5*7*11, 7^4, prime


def battery(mod):
    """Return a list of failure descriptions (empty means the checker passed every check)."""
    fails = []
    for m in BATTERY_M:
        j = EXACT[m] - 1
        exact = list(EXACT[:m])                     # T = m - 1: every part of every split is in the table
        if not run(mod, cert(m, j, exact, [claim(m, j)]), exact):
            fails.append(f"true claim ||{m}|| > {j} rejected")
        if run(mod, cert(m, j + 1, exact, [claim(m, j + 1)]), exact):
            fails.append(f"false claim ||{m}|| > {j + 1} accepted")
        if j < lam(m):
            continue                                # Selfridge alone proves it; no split is checked
        for a, b in required_splits(m, j):
            # weaken the table at this split's parts, keeping it a valid lower bound, so that
            # LB(a) + LB(b) == j exactly (boundary case) and, separately, == 2 (deep)
            for target_sum in (j, 2):
                weak = list(exact)
                if a == b:
                    weak[a] = max(1, min(EXACT[a], target_sum // 2))
                else:
                    weak[b] = 1
                    weak[a] = max(1, min(EXACT[a], target_sum - 1))
                if weak[a] + weak[b] > j:
                    continue
                if run(mod, cert(m, j, weak, [claim(m, j)]), weak):
                    fails.append(f"split {a}+{b} or {a}*{b} of {m} not checked (sum {weak[a] + weak[b]})")
    # a composite m given as its own "prime" factor: the product splits would be skipped
    for m in BATTERY_M:
        if factor(m) == [[m, 1]]:
            continue                                # m is prime
        exact = list(EXACT[:m])
        if run(mod, cert(m, EXACT[m], exact, [claim(m, EXACT[m], [[m, 1]])]), exact):
            fails.append(f"composite {m} accepted as its own prime factor")
    # chained claims with the trivial table [0, 1]: LB must use proven(v) + 1 and lambda(v) exactly
    triv = [0, 1]
    for top in (53, 81, 162, 200):
        chain = [claim(v, EXACT[v] - 1) for v in range(2, top + 1)]
        if not run(mod, cert(top, EXACT[top] - 1, triv, chain), triv):
            fails.append(f"true chain up to {top} rejected")
        bad = chain[:-1] + [claim(top, EXACT[top])]
        if run(mod, cert(top, EXACT[top], triv, bad), triv):
            fails.append(f"false claim ||{top}|| > {EXACT[top]} accepted after a true chain")
    for k in (2, 3, 4):                             # lambda(3^k) = 3k exactly: off-by-one shows here
        v = 3 ** k
        if run(mod, cert(v, 3 * k, triv, [claim(v, 3 * k)]), triv):
            fails.append(f"false claim ||3^{k}|| > {3 * k} accepted")
    # record count: dropping a redundant claim without fixing the count must be rejected
    exact = list(EXACT[:1439])
    lines = cert(1439, EXACT[1439] - 1, exact, [claim(1439, 0), claim(1439, EXACT[1439] - 1)])
    if not run(mod, lines, exact):
        fails.append("redundant-claim certificate rejected")
    if run(mod, [lines[0], lines[2], lines[3]], exact):
        fails.append("record count not checked")
    # a wrong factorization of a trivially true claim
    small = list(EXACT[:51])
    if run(mod, cert(2048, 0, small, [claim(2048, 0, [[2, 10]])]), small):
        fails.append("wrong factorization accepted")
    # Pratt: target claims that are trivially true *given* the prime, so the verdict depends on it
    small = list(EXACT[:51])
    p = 1000003                                     # prime > 2^16; p - 1 = 2 * 3 * 166667
    good = pratt_records(p)
    if not run(mod, cert(p, 0, small, good + [claim(p, 0)]), small):
        fails.append("valid Pratt record rejected")
    rec = json.loads(good[-1])
    carm = 3215031751                               # Carmichael number = 151 * 751 * 28351
    bad_records = [
        dict(rec, a=1),                                             # witness of order 1
        dict(rec, q=rec["q"][:-1]),                                 # p - 1 not fully factored
        dict(rec, q=[3, 2, 166667]),                                # not strictly increasing
        {"type": "prime", "p": carm, "a": 2, "q": [2, 3, 5, 7, 37, 613]},  # Fermat holds, order check fails
        {"type": "prime", "p": carm, "a": 2, "q": [carm - 1]},      # composite "q"
        {"type": "prime", "p": carm, "a": 3, "q": [2]},             # incomplete factorization of p - 1
        {"type": "prime", "p": 1000001, "a": 2, "q": [2, 5]},       # composite p, Fermat fails
        {"type": "prime", "p": 69751, "a": 16, "q": [2, 9, 31, 125]},  # composite (11*17*373); small q not prime
    ]
    for br in bad_records:
        tp = br["p"]
        prefix = good[:-1] if tp == p else []      # Pratt records for the large factors of p - 1
        lines = cert(tp, 0, small, prefix + [json.dumps(br), claim(tp, 0, [[tp, 1]])])
        if run(mod, lines, small):
            fails.append(f"bad Pratt record accepted: {br}")
    return fails


def test_battery_passes_on_real_checker():
    assert battery(CL) == []


# ------------------------------------------------------------------------------------------
# 3. Mutation testing (standing check).
# ------------------------------------------------------------------------------------------

MUTANTS = {
    "no p-1 factorization check": ("            if rest != 1:\n                raise Reject(\"p-1 not fully factored\")\n", ""),
    "no witness-order check": ("                if pow(a, (p - 1) // q, p) == 1:", "                if False:"),
    "no Fermat check": ("            if pow(a, p - 1, p) != 1:", "            if False:"),
    "q need not be prime": ("                if not self.is_known_prime(q):", "                if False:"),
    "q need not be increasing": ("            if any(x >= y for x, y in zip(qs, qs[1:])):", "            if False:"),
    "sum test < j": ("if self.LB(x) + self.LB(m - x) <= j:", "if self.LB(x) + self.LB(m - x) < j:"),
    "sum x = 1 only": ("                x += 1\n", "                break\n"),
    "skip d = sqrt(m)": ("if d >= 2 and d * d <= m and", "if d >= 2 and d * d < m and"),
    "cut-off 3^(j-1)": ("x, lim = 1, 3 ** j", "x, lim = 1, 3 ** (j - 1)"),
    "no record count": ("or r[\"records\"] != self.records:", ":"),
    "product test < j": ("self.LB(d) + self.LB(m // d) <= j:", "self.LB(d) + self.LB(m // d) < j:"),
    "lambda shortcut off by one": ("if j >= lam(m):", "if j > lam(m):"),
    "no product check": ("            for d in ds:\n", "            for d in []:\n"),
    "no factorization product check": ("        if prod != m:", "        if False:"),
    # found by the EXP-0005 independent review (they survived the first version of the battery)
    "claim factor need not be known prime": ("e > m.bit_length() or not self.is_known_prime(p):",
                                             "e > m.bit_length():"),
    "LB uses proven + 2": ("self.proven.get(v, -1) + 1)", "self.proven.get(v, -1) + 2)"),
    "small q not trial-divided": ("(p < SMALL and small_prime(p))", "(p < SMALL)"),
    "lambda off by one": ("    while p < c:", "    while p <= c:"),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_mutant_is_killed(name):
    old, new = MUTANTS[name]
    assert SRC.count(old) == 1, f"mutant pattern for {name!r} no longer matches the checker source"
    mod = load(SRC.replace(old, new), "mutant")
    assert battery(mod), f"mutant {name!r} survives the battery"


# --- 4. The committed corpus of false certificates found during the EXP-0004 audit ----------------
CORPUS = ROOT / "experiments" / "EXP-0005-checker-hardening" / "corpus"
# True statements in the corpus (controls); every other file states something false or is malformed.
CORPUS_TRUE = {"baseline.jsonl", "gz_ok.jsonl.gz", "header_reserialised.jsonl", "trivial_claim_ok.jsonl"}


def corpus_files():
    return sorted(p for p in CORPUS.rglob("*") if p.is_file() and ".jsonl" in p.name)


@pytest.mark.parametrize("path", corpus_files(), ids=lambda p: p.name)
def test_committed_corpus(path):
    tables = {}
    for t in (CORPUS / "tables").iterdir():
        d = t.read_bytes()
        tables[hashlib.sha256(d).hexdigest()] = d
    opener = gzip.open if path.name.endswith(".gz") else open
    try:
        with opener(path, "rt", encoding="utf-8") as fh:
            h = json.loads(fh.readline())
        table = tables.get(h["table"]["sha256"], b"\x00\x01")
    except Exception:
        table = b"\x00\x01"
    try:
        with opener(path, "rt", encoding="utf-8") as fh:
            CL.Checker(table).run(fh, sha(table))
        accepted = True
    except CL.Reject:
        accepted = False
    assert accepted == (path.name in CORPUS_TRUE)


# --- 5. Resource guards and table sanity (EXP-0005 review) -----------------------------------------

def test_factor_product_blowup_rejected_quickly():
    """A ~3800-digit m with many large prime powers must be rejected before computing the product."""
    import time
    m = 3 ** 8000 + 2
    primes = [p for p in range(2, 2000) if CL.small_prime(p)][:300]
    f = [[p, m.bit_length() // 2] for p in primes]
    t = time.time()
    assert not run(CL, cert(m, 1, SMALL50, [claim(m, 1, f)]), SMALL50)
    assert time.time() - t < 2


def test_divisor_blowup_rejected_quickly():
    """m = product of the first 26 primes would give 2^26 divisors: rejected (resource limit)."""
    import time
    primes = [p for p in range(2, 200) if CL.small_prime(p)][:26]
    m = 1
    for p in primes:
        m *= p
    t = time.time()
    assert not run(CL, cert(m, lam(m), SMALL50, [claim(m, lam(m), [[p, 1] for p in primes])]), SMALL50)
    assert time.time() - t < 2


@pytest.mark.parametrize("bad", ["c1_zero", "c1_two", "c5_inflated"])
def test_table_sanity(bad):
    table = list(EXACT[:51])
    if bad == "c1_zero":
        table[1] = 0
    elif bad == "c1_two":
        table[1] = 2
    else:
        table[5] = 3 * 3 - 1                         # 5 has 3 bits; the bound is 3*3 - 2 = 7
    assert not run(CL, cert(60, 0, table, [claim(60, 0)]), table)
    assert run(CL, cert(60, 0, SMALL50, [claim(60, 0)]), SMALL50)
