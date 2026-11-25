"""Heuristic UPPER-bound search for ||n|| when n is far beyond any exact table.

This produces certificates (explicit expressions), never lower bounds and
never proofs of optimality.

Search space ("peel" recursion):

    ub(n) = c[n]                                         if n <= T (exact table)
    ub(n) = min over 0 <= r <= R, and d | (n - r) with 2 <= d <= D:
                c[r] + c[d] + ub((n - r) / d)            (c[0] = 0)

i.e. n = d * m + r with small d, r. Every candidate is an honest expression,
so the result is a valid upper bound whatever R, D, T are.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Sequence

from algorithms.exact_table import ByteTable, optimal_expression
from algorithms.expression import evaluate


class PeelSearch:
    def __init__(self, c: Sequence[int], T: int, R: int, D: int) -> None:
        self.c, self.T, self.R, self.D = c, T, R, D
        self.memo: dict[int, tuple[int, tuple | None]] = {}

    def ub(self, n: int) -> int:
        if n <= self.T:
            return self.c[n]
        hit = self.memo.get(n)
        if hit is not None:
            return hit[0]
        c = self.c
        best, how = 10**9, None
        for r in range(0, self.R + 1):
            m = n - r
            cr = c[r] if r else 0
            if cr >= best:
                continue
            for d in range(2, self.D + 1):
                if m % d:
                    continue
                base = cr + c[d]
                if base >= best:
                    continue
                v = base + self.ub(m // d)
                if v < best:
                    best, how = v, (r, d)
        self.memo[n] = (best, how)
        return best

    def expression(self, n: int) -> str:
        if n <= self.T:
            return optimal_expression(n, self.c)
        _, how = self.memo[n]
        assert how is not None
        r, d = how
        inner = f"({optimal_expression(d, self.c)})*({self.expression((n - r) // d)})"
        return f"{inner}+{optimal_expression(r, self.c)}" if r else inner


def parse_int(text: str) -> int:
    """Parse a decimal integer or a small arithmetic form such as '2^61-1' (no eval)."""
    import ast
    import operator as op
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Pow: op.pow}

    def ev(node: ast.AST) -> int:
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError(f"unsupported integer expression: {text!r}")

    return ev(ast.parse(text.replace("^", "**"), mode="eval").body)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("n", help="target, e.g. 2305843009213693951 or 2**61-1")
    ap.add_argument("--table", required=True, help="byte table from complexity_table.c")
    ap.add_argument("-R", type=int, default=6)
    ap.add_argument("-D", type=int, default=64)
    ap.add_argument("--out", help="write a certificate JSON here")
    args = ap.parse_args(argv)

    n = parse_int(args.n)
    table = ByteTable(args.table)
    t0 = time.time()
    s = PeelSearch(table, table.N, args.R, args.D)
    sys.setrecursionlimit(100000)
    k = s.ub(n)
    expr = s.expression(n)
    ev = evaluate(expr)
    assert ev.value == n and ev.ones == k, (ev, k)
    print(f"n={n} upper_bound={k} T={table.N} R={args.R} D={args.D} "
          f"nodes={len(s.memo)} seconds={time.time() - t0:.1f}")
    if args.out:
        with open(args.out, "w") as f:
            json.dump({"id": f"UB{k}-PEEL-R{args.R}-D{args.D}", "n": str(n), "ones": k, "expression": expr,
                       "method": f"peel search T={table.N} R={args.R} D={args.D}"}, f)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
