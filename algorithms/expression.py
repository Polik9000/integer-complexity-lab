"""Safe parsing, evaluation and one-counting for integer-complexity expressions.

Grammar (no `eval`, no other digits, no subtraction or powers):

    expr   := term ('+' term)*
    term   := factor ('*' factor)*
    factor := '1' | '(' expr ')'

Whitespace is ignored. The parser is iterative over '+' / '*' chains and
recursive only over parentheses, so the recursion depth equals the nesting
depth of the input.

An expression that evaluates to n using k ones is a *certificate* that
||n|| <= k. It says nothing about lower bounds.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

ALLOWED = frozenset("1+*() \t\n\r")


class ExpressionError(ValueError):
    """Raised for any input outside the grammar."""


@dataclass(frozen=True)
class Evaluation:
    value: int
    ones: int
    max_depth: int


class _Parser:
    def __init__(self, s: str) -> None:
        self.s = s
        self.i = 0
        self.depth = 0
        self.max_depth = 0

    def _peek(self) -> str:
        s, i = self.s, self.i
        while i < len(s) and s[i] in " \t\n\r":
            i += 1
        self.i = i
        return s[i] if i < len(s) else ""

    def expr(self) -> int:
        v = self.term()
        while self._peek() == "+":
            self.i += 1
            v += self.term()
        return v

    def term(self) -> int:
        v = self.factor()
        while self._peek() == "*":
            self.i += 1
            v *= self.factor()
        return v

    def factor(self) -> int:
        c = self._peek()
        if c == "1":
            self.i += 1
            return 1
        if c == "(":
            self.i += 1
            self.depth += 1
            self.max_depth = max(self.max_depth, self.depth)
            v = self.expr()
            if self._peek() != ")":
                raise ExpressionError(f"expected ')' at position {self.i}")
            self.i += 1
            self.depth -= 1
            return v
        if c == "":
            raise ExpressionError("expression ended unexpectedly")
        raise ExpressionError(f"unexpected {c!r} at position {self.i}")


def evaluate(s: str) -> Evaluation:
    """Parse ``s`` strictly and return its value, number of ones and nesting depth."""
    if not isinstance(s, str):
        raise ExpressionError("expression must be a string")
    bad = set(s) - ALLOWED
    if bad:
        raise ExpressionError(f"disallowed characters: {sorted(bad)!r}")
    # Each '(' costs a few Python frames; make room for deep but legitimate inputs.
    need = 4 * s.count("(") + 100
    old = sys.getrecursionlimit()
    if need > old:
        sys.setrecursionlimit(need)
    try:
        p = _Parser(s)
        value = p.expr()
        if p._peek():
            raise ExpressionError(f"trailing input at position {p.i}")
    except RecursionError as e:  # pragma: no cover - defensive
        raise ExpressionError("expression nests too deeply") from e
    finally:
        sys.setrecursionlimit(old)
    return Evaluation(value=value, ones=s.count("1"), max_depth=p.max_depth)


# ---------------------------------------------------------------------------
# Building expressions
# ---------------------------------------------------------------------------

def ones_sum(k: int) -> str:
    """'1+1+...+1' with k ones (k >= 1)."""
    if k < 1:
        raise ValueError("k must be >= 1")
    return "+".join("1" * k)


def add(a: str, b: str) -> str:
    return f"{a}+{b}"


def mul(a: str, b: str) -> str:
    return f"({a})*({b})"


# ---------------------------------------------------------------------------
# Export to Lean 4 (used to generate formal certificates in lean/)
# ---------------------------------------------------------------------------

class _LeanBuilder(_Parser):
    """Same grammar as _Parser, but builds a Lean term of type IntegerComplexity.Expr."""

    def expr(self) -> str:  # type: ignore[override]
        v = self.term()
        while self._peek() == "+":
            self.i += 1
            v = f"(.add {v} {self.term()})"
        return v

    def term(self) -> str:  # type: ignore[override]
        v = self.factor()
        while self._peek() == "*":
            self.i += 1
            v = f"(.mul {v} {self.factor()})"
        return v

    def factor(self) -> str:  # type: ignore[override]
        c = self._peek()
        if c == "1":
            self.i += 1
            return ".one"
        if c == "(":
            self.i += 1
            v = self.expr()
            if self._peek() != ")":
                raise ExpressionError(f"expected ')' at position {self.i}")
            self.i += 1
            return v
        raise ExpressionError(f"unexpected {c!r} at position {self.i}")


def to_lean(s: str) -> str:
    """Translate a checked expression string into a Lean `IntegerComplexity.Expr` term."""
    evaluate(s)  # validates characters and grammar first
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 4 * s.count("(") + 100))
    try:
        p = _LeanBuilder(s)
        out = p.expr()
    finally:
        sys.setrecursionlimit(old)
    return out
