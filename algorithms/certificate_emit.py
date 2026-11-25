"""Emit lower-bound certificates while ExactSearch runs (format: research/2026-11-25-certificate-architecture.md §4).

The checker (certificates/lower/check_lower.py) does not trust anything computed here: a bug in this
module or in the search can only produce a certificate that fails to check.
"""
from __future__ import annotations

import gzip
import json
from typing import IO

from .exact_single import factorize

SMALL = 1 << 16


class CertificateEmitter:
    def __init__(self, fh: IO[str], target: int, claim_gt: int, T: int, table_sha256: str,
                 commit: str = "unknown") -> None:
        self.fh = fh
        self.records = 0
        self.primes: set[int] = set()
        self._write({"type": "header", "version": 1, "target": str(target), "claim_gt": claim_gt,
                     "table": {"T": T, "sha256": table_sha256,
                               "format": "uint8, index v = ||v||, v=0 unused"},
                     "generator": {"code": "algorithms/exact_single.py", "commit": commit}},
                    count=False)

    def _write(self, rec: dict, count: bool = True) -> None:
        self.fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
        if count:
            self.records += 1

    def _prime(self, p: int) -> None:
        """Write a Pratt record for p (and, first, for the primes of p-1)."""
        if p < SMALL or p in self.primes:
            return
        qs = sorted(factorize(p - 1))
        for q in qs:
            self._prime(q)
        a = 2
        while not (pow(a, p - 1, p) == 1 and all(pow(a, (p - 1) // q, p) != 1 for q in qs)):
            a += 1
        self._write({"type": "prime", "p": p, "a": a, "q": qs})
        self.primes.add(p)

    def claim(self, m: int, j: int) -> None:
        """Record G(m, j): ||m|| > j."""
        f = sorted(factorize(m).items())
        for p, _ in f:
            self._prime(p)
        self._write({"type": "claim", "m": m, "j": j, "f": [[p, e] for p, e in f]})

    def close(self) -> None:
        self._write({"type": "end", "records": self.records}, count=False)
        self.fh.close()


def open_cert(path: str) -> IO[str]:
    return gzip.open(path, "wt", compresslevel=6) if path.endswith(".gz") else open(path, "w")
