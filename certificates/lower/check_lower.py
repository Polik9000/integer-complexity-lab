#!/usr/bin/env python3
"""Independent checker for lower-bound certificates  ||target|| > claim_gt.

Written from research/2026-11-25-certificate-architecture.md (section 5) only.
Standard library only; deliberately imports nothing from algorithms/.

Version 2 (hardened after the EXP-0004 audit, findings F1, F2, M1, F5-F7, and the EXP-0005 review):
  * every numeric field must have Python type exactly ``int`` (bools, floats, NaN and
    Infinity are rejected; JSON number tokens with a fraction or exponent are rejected while
    parsing), and duplicate JSON keys are rejected;
  * records must have exactly the fields of the spec;
  * claims need m >= 2 (Theorem C) and the table must have T >= 1;
  * the expected target, claim_gt and table SHA-256 are command-line inputs, and the header must
    match them, so the verdict is bound to the intended statement;
  * the last claim must be the target claim (spec section 4);
  * every failure, including I/O and gzip errors, is reported as REJECTED with exit code 1.
  * resource guards (reject only): a factor p^e or a partial product above m, more than 2^20 divisors;
  * table sanity (necessary conditions only): c[1] = 1 and c[v] <= 3*bitlen(v) - 2.

Usage:
  python3 -I check_lower.py CERT.jsonl[.gz] TABLE.bin --target N --claim-gt J --table-sha256 HEX
Exit 0 and print the verdict if every record checks; exit 1 with the failing line otherwise.
"""
import argparse
import gzip
import hashlib
import json
import re
import sys

SMALL = 1 << 16
MAX_DIVISORS = 1 << 20   # resource limit only: a claim over the limit is rejected, never accepted
HEX64 = re.compile(r"[0-9a-f]{64}")
DECIMAL = re.compile(r"[1-9][0-9]*")

HEADER_KEYS = {"type", "version", "target", "claim_gt", "table"}   # "generator" is optional
PRIME_KEYS = {"type", "p", "a", "q"}
CLAIM_KEYS = {"type", "m", "j", "f"}
END_KEYS = {"type", "records"}


class Reject(Exception):
    pass


def is_int(v):
    """Exactly int: excludes bool (a subclass of int) and float."""
    return type(v) is int


def _no_float(token):
    raise Reject(f"non-integer number {token!r}")


def _no_dupes(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Reject(f"duplicate key {k!r}")
        out[k] = v
    return out


def parse(line):
    """Strict JSON: integers only, no NaN/Infinity, no duplicate keys, top level must be an object."""
    r = json.loads(line, parse_float=_no_float, parse_constant=_no_float, object_pairs_hook=_no_dupes)
    if type(r) is not dict:
        raise Reject("record is not a JSON object")
    return r


def lam(v):
    """Least j with v^3 <= 3^j (integers only)."""
    j, c, p = 0, v ** 3, 1
    while p < c:
        p *= 3
        j += 1
    return j


def small_prime(p):
    if p < 2:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i += 1
    return True


class Checker:
    def __init__(self, table):
        self.c = table
        self.T = len(table) - 1
        self.primes = set()
        self.proven = {}
        self.header = None
        self.records = 0
        self.last_claim = None

    def is_known_prime(self, p):
        return is_int(p) and (p in self.primes or (p < SMALL and small_prime(p)))

    def LB(self, v):
        if v <= self.T:
            return self.c[v]
        return max(1, lam(v), self.proven.get(v, -1) + 1)

    def check_table_sanity(self):
        """Cheap necessary conditions on the table (it is still a trusted input, see the spec).

        c[1] must be 1, and c[v] <= 3*bitlen(v) - 2 for every v (writing v in binary by Horner's rule
        with 2 = 1+1 uses at most that many ones), so no entry exceeds a known upper bound on ||v||."""
        if self.c[1] != 1:
            raise Reject("table entry c[1] must be 1")
        b = 1
        while (1 << (b - 1)) <= self.T:
            lo, hi = 1 << (b - 1), min(1 << b, self.T + 1)
            if max(self.c[lo:hi]) > 3 * b - 2:
                raise Reject(f"table entry for a {b}-bit number exceeds the upper bound 3*{b}-2")
            b += 1

    def check_header(self, r, table_sha, target, claim_gt):
        keys = set(r)
        if not (HEADER_KEYS <= keys <= HEADER_KEYS | {"generator"}):
            raise Reject("header fields differ from the spec")
        if r["type"] != "header" or not is_int(r["version"]) or r["version"] != 1:
            raise Reject("first record must be a version-1 header")
        t, g, tb = r["target"], r["claim_gt"], r["table"]
        if type(t) is not str or not DECIMAL.fullmatch(t):
            raise Reject("header target must be a canonical decimal string")
        if not is_int(g) or g < 0:
            raise Reject("header claim_gt must be a non-negative integer")
        if type(tb) is not dict or not is_int(tb.get("T")) or type(tb.get("sha256")) is not str:
            raise Reject("header table must give integer T and string sha256")
        if not (set(tb) <= {"T", "sha256", "format"}):
            raise Reject("header table fields differ from the spec")
        if self.T < 1:
            raise Reject("table must contain at least ||1|| (T >= 1)")
        self.check_table_sanity()
        if tb["T"] != self.T or tb["sha256"] != table_sha:
            raise Reject("table does not match header (T or SHA-256)")
        if target is not None and int(t) != target:
            raise Reject(f"header target {t} is not the expected target {target}")
        if claim_gt is not None and g != claim_gt:
            raise Reject(f"header claim_gt {g} is not the expected {claim_gt}")
        self.header = r

    def prime(self, r):
        if set(r) != PRIME_KEYS:
            raise Reject("prime record fields differ from the spec")
        p, a, qs = r["p"], r["a"], r["q"]
        if not (is_int(p) and p >= 2 and is_int(a) and type(qs) is list and all(is_int(q) for q in qs)):
            raise Reject("prime record needs integer p >= 2, integer a and a list of integers q")
        if p < SMALL:
            if not small_prime(p):
                raise Reject(f"{p} is not prime")
        else:
            if not qs:
                raise Reject("Pratt record without factors of p-1")
            if any(x >= y for x, y in zip(qs, qs[1:])):
                raise Reject("factors of p-1 must be strictly increasing")
            rest = p - 1
            for q in qs:
                if not self.is_known_prime(q):
                    raise Reject(f"factor {q} of p-1 not known prime")
                if rest % q:
                    raise Reject(f"{q} does not divide p-1")
                while rest % q == 0:
                    rest //= q
            if rest != 1:
                raise Reject("p-1 not fully factored")
            if pow(a, p - 1, p) != 1:
                raise Reject("Fermat condition fails")
            for q in qs:
                if pow(a, (p - 1) // q, p) == 1:
                    raise Reject(f"witness order divides (p-1)/{q}")
        self.primes.add(p)

    def claim(self, r):
        if set(r) != CLAIM_KEYS:
            raise Reject("claim record fields differ from the spec")
        m, j, f = r["m"], r["j"], r["f"]
        if not (is_int(m) and is_int(j) and type(f) is list):
            raise Reject("claim needs integer m, integer j and a list f")
        if m < 2 or m <= self.T or j < 0:
            raise Reject("claim must have m >= 2, m > T and j >= 0")
        if j > 3 * m.bit_length():
            # ||m|| <= 3 log2 m < 3 * bitlen(m) for m >= 2, so such a claim is false anyway;
            # rejecting it early only avoids a very long sum loop.
            raise Reject("j exceeds the trivial upper bound 3*bitlen(m)")
        prod, prev, nd = 1, 1, 1
        for pe in f:
            if not (type(pe) is list and len(pe) == 2 and is_int(pe[0]) and is_int(pe[1])):
                raise Reject("factor entry must be a pair of integers [p, e]")
            p, e = pe
            if p <= prev:
                raise Reject("factor primes must be strictly increasing")
            prev = p
            if e < 1 or e > m.bit_length() or not self.is_known_prime(p):
                raise Reject(f"factor {p}^{e} not a verified prime power")
            if (p.bit_length() - 1) * e >= m.bit_length():
                # p^e >= 2^((bitlen(p)-1)*e) >= 2^bitlen(m) > m: cannot divide m (checked before the power)
                raise Reject(f"factor {p}^{e} exceeds m")
            prod *= p ** e
            if prod > m:
                raise Reject("factorization exceeds m")
            nd *= e + 1
            if nd > MAX_DIVISORS:
                raise Reject(f"more than {MAX_DIVISORS} divisors (resource limit)")
        if prod != m:
            raise Reject("factorization does not multiply to m")
        if j >= lam(m):
            # sums m = x + (m - x), Selfridge cut-off (Fact S)
            x, lim = 1, 3 ** j
            while 2 * x <= m and (x * (m - x)) ** 3 <= lim:
                if self.LB(x) + self.LB(m - x) <= j:
                    raise Reject(f"sum split {x} + {m - x} not refuted")
                x += 1
            # products m = d * (m/d), all divisors from the verified factorization
            ds = [1]
            for p, e in f:
                ds = [d * p ** i for d in ds for i in range(e + 1)]
            for d in ds:
                if d >= 2 and d * d <= m and self.LB(d) + self.LB(m // d) <= j:
                    raise Reject(f"product split {d} * {m // d} not refuted")
        if j > self.proven.get(m, -1):
            self.proven[m] = j
        self.last_claim = (m, j)

    def run(self, lines, table_sha, target=None, claim_gt=None):
        """Check all records. ``target`` / ``claim_gt``, if given, must match the header."""
        verdict = None
        no = 0
        try:
            for no, line in enumerate(lines, 1):
                try:
                    r = parse(line)
                    t = r.get("type")
                    if no == 1:
                        self.check_header(r, table_sha, target, claim_gt)
                    elif verdict is not None:
                        raise Reject("records after end")
                    elif t == "prime":
                        self.prime(r)
                    elif t == "claim":
                        self.claim(r)
                    elif t == "end":
                        if set(r) != END_KEYS or not is_int(r["records"]) or r["records"] != self.records:
                            raise Reject("record count mismatch (truncated or padded)")
                        tgt, g = int(self.header["target"]), self.header["claim_gt"]
                        if self.proven.get(tgt, -1) < g:
                            raise Reject(f"target claim ||{tgt}|| > {g} not established")
                        if self.last_claim is None or self.last_claim[0] != tgt or self.last_claim[1] < g:
                            raise Reject("the last claim must be the target claim")
                        verdict = (tgt, g)
                    else:
                        raise Reject(f"unknown record type {t!r}")
                    if no > 1 and t != "end":
                        self.records += 1
                except Reject as e:
                    raise Reject(f"line {no}: {e}") from None
                except (KeyError, TypeError, ValueError, AttributeError, RecursionError, MemoryError) as e:
                    raise Reject(f"line {no}: malformed record ({type(e).__name__}: {e})") from None
        except (OSError, EOFError, UnicodeDecodeError) as e:
            raise Reject(f"after line {no}: cannot read certificate ({type(e).__name__}: {e})") from None
        if verdict is None:
            raise Reject("missing end record (truncated file)")
        return verdict


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a lower-bound certificate ||target|| > claim_gt.")
    ap.add_argument("cert")
    ap.add_argument("table")
    ap.add_argument("--target", required=True, type=int, help="expected target n (decimal)")
    ap.add_argument("--claim-gt", required=True, type=int, help="expected claim: ||n|| > CLAIM_GT")
    ap.add_argument("--table-sha256", required=True, help="expected SHA-256 of the table file")
    a = ap.parse_args(argv)
    try:
        data = open(a.table, "rb").read()
        sha = hashlib.sha256(data).hexdigest()
        if not HEX64.fullmatch(a.table_sha256) or sha != a.table_sha256:
            raise Reject(f"table SHA-256 {sha} is not the expected {a.table_sha256}")
        opener = gzip.open if a.cert.endswith(".gz") else open
        with opener(a.cert, "rt", encoding="utf-8") as fh:
            tgt, g = Checker(data).run(fh, sha, a.target, a.claim_gt)
    except Reject as e:
        print(f"REJECTED: {e}")
        return 1
    except (OSError, EOFError, UnicodeDecodeError) as e:
        print(f"REJECTED: cannot read input ({type(e).__name__}: {e})")
        return 1
    print(f"ACCEPTED: ||{tgt}|| > {g}  (table sha256 {sha})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
