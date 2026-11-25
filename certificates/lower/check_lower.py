#!/usr/bin/env python3
"""Independent checker for lower-bound certificates  ||target|| > claim_gt.

Written from research/2026-11-25-certificate-architecture.md (section 5) only.
Standard library only; deliberately imports nothing from algorithms/.
Usage:  python3 -I check_lower.py CERT.jsonl[.gz] TABLE.bin
Exit 0 and prints the verdict if every record checks; exit 1 with the failing line otherwise.
"""
import gzip
import hashlib
import json
import sys

SMALL = 1 << 16


class Reject(Exception):
    pass


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

    def is_known_prime(self, p):
        return p in self.primes or (p < SMALL and small_prime(p))

    def LB(self, v):
        if v <= self.T:
            return self.c[v]
        return max(1, lam(v), self.proven.get(v, -1) + 1)

    def prime(self, r):
        p, a, qs = r["p"], r["a"], r["q"]
        if not (isinstance(p, int) and p >= 2):
            raise Reject("bad p")
        if p < SMALL:
            if not small_prime(p):
                raise Reject(f"{p} is not prime")
        else:
            if not qs:
                raise Reject("Pratt record without factors of p-1")
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
        m, j, f = r["m"], r["j"], r["f"]
        if not (isinstance(m, int) and isinstance(j, int)) or m <= self.T or j < 0:
            raise Reject("claim must have m > T and j >= 0")
        prod, prev = 1, 1
        for p, e in f:
            if p <= prev:
                raise Reject("factor primes must be strictly increasing")
            prev = p
            if not (isinstance(e, int) and e >= 1) or not self.is_known_prime(p):
                raise Reject(f"factor {p}^{e} not a verified prime power")
            prod *= p ** e
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

    def run(self, lines, table_sha):
        verdict = None
        for no, line in enumerate(lines, 1):
            try:
                r = json.loads(line)
                t = r.get("type")
                if no == 1:
                    if t != "header" or r.get("version") != 1:
                        raise Reject("first record must be a version-1 header")
                    if r["table"]["T"] != self.T or r["table"]["sha256"] != table_sha:
                        raise Reject("table does not match header (T or SHA-256)")
                    self.header = r
                elif verdict is not None:
                    raise Reject("records after end")
                elif t == "prime":
                    self.prime(r)
                elif t == "claim":
                    self.claim(r)
                elif t == "end":
                    if r.get("records") != self.records:
                        raise Reject("record count mismatch (truncated or padded)")
                    tgt, g = int(self.header["target"]), self.header["claim_gt"]
                    if self.proven.get(tgt, -1) < g:
                        raise Reject(f"target claim ||{tgt}|| > {g} not established")
                    verdict = (tgt, g)
                else:
                    raise Reject(f"unknown record type {t!r}")
                if no > 1 and t != "end":
                    self.records += 1
            except Reject as e:
                raise Reject(f"line {no}: {e}") from None
            except (KeyError, TypeError, ValueError) as e:
                raise Reject(f"line {no}: malformed record ({e})") from None
        if verdict is None:
            raise Reject("missing end record (truncated file)")
        return verdict


def main(cert_path, table_path):
    data = open(table_path, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    opener = gzip.open if cert_path.endswith(".gz") else open
    with opener(cert_path, "rt") as fh:
        try:
            tgt, g = Checker(data).run(fh, sha)
        except Reject as e:
            print(f"REJECTED: {e}")
            return 1
    print(f"ACCEPTED: ||{tgt}|| > {g}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
