"""Exact integer complexity of a single large n by budgeted branch-and-bound.

``complexity_at_most(n, k)`` returns min(||n||, k + 1): the exact value if ||n|| <= k,
otherwise k + 1 (meaning "||n|| > k").  Calling it with k = a known upper bound
(e.g. from a certificate) therefore yields the exact value of ||n||.

Correctness (every step is exhaustive except for rigorous pruning):

* The top operation of any expression for n > 1 is n = x + y or n = x * y with x, y >= 1
  (for *, x, y >= 2).  So ||n|| = min over these splits of ||x|| + ||y||.
* Selfridge: a value made from j ones is at most 3^(j/3), so ||m|| >= 3 log_3 m, i.e.
  ||m|| <= j is impossible when m^3 > 3^j.  (Exact integer test, no floating point.)
* Sum n = x + y with x <= y: ||x|| + ||y|| <= b requires (x*y)^3 <= 3^b.  Since x*y is
  increasing in x on [1, n/2], the scan over x stops at the first violation.  For our
  targets this leaves only x <= 2 * 3^(s/3), where s = b - 3 log_3 n is the "slack".
* Product n = d * e with 2 <= d <= e: all divisor pairs are enumerated from a full
  factorization (deterministic Miller-Rabin for n < 3.3*10^24, Pollard rho).
* Values with n <= T come from an exact table (``exact_table`` / ``complexity_table.c``).
* Memoization stores either an exact value or a proven strict lower bound (||m|| > j).

The search is exhaustive within the budget, so the result is exact.  Its cost grows
with the slack between the budget and 3 log_3 n.
"""
from __future__ import annotations

import math
import random
import sys
from typing import Sequence

# ---------------------------------------------------------------------------
# Factorization (64-bit and somewhat beyond)
# ---------------------------------------------------------------------------

_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)  # deterministic < 3.3e24


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
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


def _pollard_rho(n: int, rng: random.Random) -> int:
    if n % 2 == 0:
        return 2
    while True:
        c = rng.randrange(1, n)
        f = lambda x: (x * x + c) % n  # noqa: E731
        x = y = rng.randrange(2, n)
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def factorize(n: int, _rng: random.Random = random.Random(12345)) -> dict[int, int]:
    """Prime factorization {p: e}.  Deterministic result (randomness affects speed only)."""
    out: dict[int, int] = {}
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            out[m] = out.get(m, 0) + 1
            continue
        d = _pollard_rho(m, _rng)
        stack += [d, m // d]
    return out


def divisors(n: int) -> list[int]:
    ds = [1]
    for p, e in factorize(n).items():
        ds = [d * p**i for d in ds for i in range(e + 1)]
    return sorted(ds)


# ---------------------------------------------------------------------------
# Budgeted exact search
# ---------------------------------------------------------------------------

def min_ones_lower(m: int) -> int:
    """Least j with m^3 <= 3^j (so ||m|| >= this, by Selfridge)."""
    j = max(0, int(3 * math.log(m, 3)) - 2) if m > 1 else 0
    while m**3 > 3**j:
        j += 1
    while j > 0 and m**3 <= 3 ** (j - 1):
        j -= 1
    return j


class ExactSearch:
    def __init__(self, table: Sequence[int], T: int | None = None, emit=None) -> None:
        """``emit``: optional object with ``claim(m, j)``, called whenever a lower bound
        ||m|| > j is established (used to write certificates; see algorithms/certificate_emit.py)."""
        self.emit = emit
        self.c = table
        self.T = len(table) - 1 if T is None else T
        self.exact: dict[int, int] = {}
        self.gt: dict[int, int] = {}  # gt[m] = j  means proven ||m|| > j
        self.calls = 0

    def at_most(self, m: int, k: int) -> int:
        """min(||m||, k+1)."""
        if k < 1:
            return k + 1
        if m <= self.T:
            return min(self.c[m], k + 1)
        if m**3 > 3**k:
            return k + 1
        e = self.exact.get(m)
        if e is not None:
            return min(e, k + 1)
        if self.gt.get(m, -1) >= k:
            return k + 1
        self.calls += 1
        best = k + 1
        c = self.c
        # sums m = x + y, x <= y
        x = 1
        while 2 * x <= m:
            y = m - x
            if (x * y) ** 3 > 3 ** (best - 1):
                break
            if x > self.T:
                raise RuntimeError(f"additive part {x} exceeds table size; increase T")
            cx = c[x]
            if cx < best - 1:
                v = cx + self.at_most(y, best - 1 - cx)
                if v < best:
                    best = v
            x += 1
        # products m = d * e, 2 <= d <= e
        if best > 1:
            for d in divisors(m):
                if d < 2:
                    continue
                e_ = m // d
                if d > e_:
                    break
                lo_e = min_ones_lower(e_)
                if lo_e + min_ones_lower(d) > best - 1:
                    continue
                cd = self.at_most(d, best - 1 - lo_e)
                if cd > best - 1 - lo_e:
                    continue
                ce = self.at_most(e_, best - 1 - cd)
                if cd + ce < best:
                    best = cd + ce
        if best <= k:
            self.exact[m] = best
            if self.emit is not None:
                self.emit.claim(m, best - 1)
        else:
            self.gt[m] = max(self.gt.get(m, -1), k)
            if self.emit is not None:
                self.emit.claim(m, k)
        return best

    def complexity(self, n: int, upper: int) -> int:
        """Exact ||n||, given any valid upper bound ``upper`` (e.g. from a certificate)."""
        sys.setrecursionlimit(max(sys.getrecursionlimit(), 100000))
        v = self.at_most(n, upper)
        if v > upper:
            raise ValueError(f"upper bound {upper} is invalid: ||{n}|| > {upper}")
        return v
