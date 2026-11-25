#!/usr/bin/env python3
"""Verify every upper-bound certificate under certificates/.

A certificate is a JSON file with at least: id, n (decimal string), ones, expression.
Verification = the expression is in the strict grammar {1, +, *, (, )}, evaluates
exactly to n, and contains exactly `ones` ones. This proves ||n|| <= ones and
nothing more.

Usage:  python3 certificates/verify.py [FILE ...]     (default: all *.json here)
Exit code 0 iff every certificate verifies.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from algorithms.expression import ExpressionError, evaluate  # noqa: E402

REQUIRED = ("id", "n", "ones", "expression")


def verify(path: Path) -> tuple[bool, str]:
    try:
        c = json.loads(path.read_text())
    except Exception as e:  # noqa: BLE001
        return False, f"unreadable JSON: {e}"
    missing = [k for k in REQUIRED if k not in c]
    if missing:
        return False, f"missing keys {missing}"
    try:
        ev = evaluate(c["expression"])
    except ExpressionError as e:
        return False, f"bad expression: {e}"
    n = int(c["n"])
    if ev.value != n:
        return False, f"evaluates to {ev.value}, not {n}"
    if ev.ones != int(c["ones"]):
        return False, f"has {ev.ones} ones, certificate says {c['ones']}"
    return True, f"||{c.get('n_form', n)}|| <= {ev.ones}"


def main(argv: list[str]) -> int:
    files = [Path(a).resolve() for a in argv] or sorted(Path(__file__).parent.rglob("*.json"))
    ok_all = True
    for f in files:
        ok, msg = verify(f)
        ok_all &= ok
        shown = f.relative_to(ROOT) if f.resolve().is_relative_to(ROOT) else f
        print(f"{'OK  ' if ok else 'FAIL'} {shown}: {msg}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
