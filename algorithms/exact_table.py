"""Exact integer complexity for small n, plus optimal-expression reconstruction.

Two independent implementations exist in this repository:

* ``complexity_table`` below (pure Python, for n up to ~10^5; used by tests), and
* ``algorithms/c/complexity_table.c`` (C, for n up to ~4*10^9 bytes of RAM).

Both use the same recurrence and the same rigorous pruning of additive splits:
a value built from k ones is at most 3^(k/3), so ||a|| + ||n-a|| >= 3 log_3(a(n-a)).
The tests cross-check the two implementations against each other and against
facts published in the literature (see tests/test_exact_table.py).
"""
from __future__ import annotations

import mmap
import os
from functools import lru_cache
from typing import Sequence


def _cube_limits(kmax: int = 120) -> list[int]:
    """lim[k] = largest P with P**3 <= 3**k (exact integer arithmetic)."""
    out = []
    for k in range(kmax + 1):
        t = 3**k
        lo, hi = 0, 1
        while hi**3 <= t:
            hi *= 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if mid**3 <= t:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)
    return out


LIM = _cube_limits()


def complexity_table(N: int) -> list[int]:
    """Return c with c[n] = ||n|| for 1 <= n <= N (c[0] = 0)."""
    if N < 1:
        raise ValueError("N must be >= 1")
    INF = 10**9
    c = [INF] * (N + 1)
    c[0] = 0
    c[1] = 1
    for n in range(1, N + 1):
        if n >= 2:
            best = min(c[n], c[n - 1] + 1)
            a = 2
            while 2 * a <= n and a * (n - a) <= LIM[best - 1]:
                v = c[a] + c[n - a]
                if v < best:
                    best = v
                a += 1
            c[n] = best
        cn = c[n]
        d = 2
        while d <= n and d * n <= N:
            v = c[d] + cn
            if v < c[d * n]:
                c[d * n] = v
            d += 1
    return c


class ByteTable(Sequence[int]):
    """Read-only view of a table file written by complexity_table.c."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._f = open(path, "rb")
        self._m = mmap.mmap(self._f.fileno(), 0, access=mmap.ACCESS_READ)
        self.N = len(self._m) - 1

    def __len__(self) -> int:
        return len(self._m)

    def __getitem__(self, i):  # type: ignore[override]
        return self._m[i]

    def close(self) -> None:
        self._m.close()
        self._f.close()


def optimal_expression(n: int, c: Sequence[int]) -> str:
    """Reconstruct an expression for n with exactly c[n] ones (requires c exact up to n)."""

    @lru_cache(maxsize=None)
    def build(m: int) -> str:
        if m <= 5:
            return "+".join("1" * m) if m > 1 else "1"
        target = c[m]
        d = 2
        while d * d <= m:
            if m % d == 0 and c[d] + c[m // d] == target:
                return f"({build(d)})*({build(m // d)})"
            d += 1
        a = 1
        while 2 * a <= m:
            if c[a] + c[m - a] == target:
                return f"{build(a)}+{build(m - a)}"
            if a * (m - a) > LIM[target]:
                break
            a += 1
        raise AssertionError(f"table inconsistent at {m}")

    return build(n)
