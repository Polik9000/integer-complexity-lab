#!/usr/bin/env python3
"""EXP-0004: a second, stricter checker for lower-bound certificates ||target|| > claim_gt.

Written for the EXP-0004 audit from the mathematics (Lemma 1, Lemma 2, Theorem C in
research/2026-11-25-certificate-architecture.md), NOT by editing certificates/lower/check_lower.py.
Differences from the first checker (each closes a gap found in the audit):
  * every numeric field must have Python type exactly int (no bool, no float);
  * claims need m >= 2 (Lemma 2 / Theorem C only hold for m >= 2);
  * the expected target, claim_gt and table SHA-256 are given on the command line and must match;
  * the table must satisfy table[1] == 1 and 1 <= table[v] for v >= 1 (sanity only);
  * optional --demand OUT.json: records which table entries were *needed* above the trivial
    bound max(1, lambda(v)), to size a table-free (Lean-friendly) certificate.
Standard library only; imports nothing from the repository.

Usage: python3 -I check_lower_strict.py CERT.jsonl[.gz] TABLE.bin TARGET CLAIM_GT TABLE_SHA256 [--demand OUT.json]
"""
import gzip, hashlib, json, sys

SMALL = 1 << 16


class Bad(Exception):
    pass


def is_int(v):
    return type(v) is int


def lam(v):
    # least j >= 0 with v**3 <= 3**j  (exact integers)
    j, p, c = 0, 1, v ** 3
    while p < c:
        p, j = p * 3, j + 1
    return j


def trial_prime(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def no_float(s):
    raise Bad("non-integer number token %r" % s)


def main(argv):
    cert, tpath, target, gt, sha = argv[1], argv[2], int(argv[3]), int(argv[4]), argv[5]
    demand_out = argv[7] if len(argv) > 7 and argv[6] == "--demand" else None
    data = open(tpath, "rb").read()
    if hashlib.sha256(data).hexdigest() != sha:
        raise Bad("table SHA-256 differs from the pinned value")
    T = len(data) - 1
    if T < 1 or data[1] != 1 or min(data[1:]) < 1:
        raise Bad("table fails sanity checks")
    primes, proven = set(), {}
    need = {}  # table index -> largest value the checker needed from it (only when > trivial)
    stats = {"claims": 0, "primes": 0, "lambda_shortcut": 0, "sum_checks": 0, "prod_checks": 0,
             "max_sum_loop": 0, "max_slack": 0}

    def known_prime(p):
        return p in primes or (p < SMALL and trial_prime(p))

    def LB(v):
        if v <= T:
            return data[v]
        return max(1, lam(v), proven.get(v, -1) + 1)

    def refute(a, b, j):
        la, lb = LB(a), LB(b)
        if la + lb <= j:
            return False
        if demand_out is not None:
            for v, lv, lo in ((a, la, lb), (b, lb, la)):
                if v <= T:
                    req = j + 1 - lo
                    if req > max(1, lam(v)):
                        if req > need.get(v, 0):
                            need[v] = req
        return True

    opener = gzip.open if cert.endswith(".gz") else open
    n_rec, done = 0, False
    with opener(cert, "rt") as fh:
        for no, line in enumerate(fh, 1):
            try:
                r = json.loads(line, parse_float=no_float, parse_constant=no_float)
                if type(r) is not dict:
                    raise Bad("record is not an object")
                t = r.get("type")
                if done:
                    raise Bad("record after end")
                if no == 1:
                    tb = r.get("table", {})
                    if (t != "header" or r.get("version") != 1 or r.get("target") != str(target)
                            or r.get("claim_gt") != gt or tb.get("T") != T or tb.get("sha256") != sha):
                        raise Bad("header does not match the pinned target / claim / table")
                    continue
                if t == "prime":
                    p, a, qs = r["p"], r["a"], r["q"]
                    if not (is_int(p) and is_int(a) and type(qs) is list and all(is_int(q) for q in qs)):
                        raise Bad("prime record fields must be ints")
                    if p < SMALL:
                        if not trial_prime(p):
                            raise Bad("small p not prime")
                    else:
                        rest = p - 1
                        for q in qs:
                            if not known_prime(q) or rest % q:
                                raise Bad("bad factor of p-1")
                            while rest % q == 0:
                                rest //= q
                        if rest != 1 or not qs:
                            raise Bad("p-1 not completely factored")
                        if pow(a, p - 1, p) != 1 or any(pow(a, (p - 1) // q, p) == 1 for q in qs):
                            raise Bad("Lucas condition fails")
                    primes.add(p)
                    stats["primes"] += 1
                elif t == "claim":
                    m, j, f = r["m"], r["j"], r["f"]
                    if not (is_int(m) and is_int(j) and type(f) is list):
                        raise Bad("claim fields must be ints / list")
                    if m < 2 or m <= T or j < 0:
                        raise Bad("claim needs m >= 2, m > T, j >= 0")
                    prod, last = 1, 1
                    for pe in f:
                        if not (type(pe) is list and len(pe) == 2 and is_int(pe[0]) and is_int(pe[1])):
                            raise Bad("factor entry must be [int, int]")
                        p, e = pe
                        if p <= last or e < 1 or not known_prime(p):
                            raise Bad("factorization entry invalid")
                        last = p
                        prod *= p ** e
                    if prod != m:
                        raise Bad("factorization product != m")
                    stats["claims"] += 1
                    L = lam(m)
                    if j < L:
                        stats["lambda_shortcut"] += 1
                    else:
                        stats["max_slack"] = max(stats["max_slack"], j - L)
                        bound, x = 3 ** j, 1
                        while 2 * x <= m and (x * (m - x)) ** 3 <= bound:
                            if not refute(x, m - x, j):
                                raise Bad("sum split %d + %d not refuted" % (x, m - x))
                            x += 1
                        stats["sum_checks"] += x - 1
                        stats["max_sum_loop"] = max(stats["max_sum_loop"], x - 1)
                        divs = [1]
                        for p, e in f:
                            divs = [d * p ** i for d in divs for i in range(e + 1)]
                        for d in divs:
                            if 2 <= d and d * d <= m:
                                stats["prod_checks"] += 1
                                if not refute(d, m // d, j):
                                    raise Bad("product split %d * %d not refuted" % (d, m // d))
                    if j > proven.get(m, -1):
                        proven[m] = j
                elif t == "end":
                    if r.get("records") != n_rec or not is_int(r.get("records")):
                        raise Bad("record count mismatch")
                    if proven.get(target, -1) < gt:
                        raise Bad("target claim not established")
                    done = True
                    continue
                else:
                    raise Bad("unknown record type")
                n_rec += 1
            except Bad as e:
                print("REJECTED line %d: %s" % (no, e))
                return 1
            except (KeyError, TypeError, ValueError, AttributeError) as e:
                print("REJECTED line %d: malformed (%s)" % (no, e))
                return 1
    if not done:
        print("REJECTED: no end record")
        return 1
    print("ACCEPTED: ||%d|| > %d   stats=%s" % (target, gt, json.dumps(stats)))
    if demand_out is not None:
        vals = sorted(need.items())
        with open(demand_out, "w") as fo:
            json.dump({"count": len(vals), "max_index": vals[-1][0] if vals else 0,
                       "max_required": max((v for _, v in vals), default=0),
                       "need": vals}, fo)
        print("demand: %d table entries needed above max(1, lambda); written to %s" % (len(vals), demand_out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Bad as e:
        print("REJECTED: %s" % e)
        sys.exit(1)
