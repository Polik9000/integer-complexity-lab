"""Cross-checks for the exact complexity tables.

Reference facts (each cited in BIBLIOGRAPHY.md):
* ||11|| = 8                                  (standard example)
* ||3^k|| = 3k                                (Selfridge's lower bound is tight at 3^k)
* ||2^k|| = 2k for small k                   (verified for 2^k < 10^12 by Iraids et al. 2012)
* ||1439|| = 26                               (Rawsthorne; Iraids et al. 2012)
* E(3k+2)=2*3^k, E(3k+3)=3^(k+1), E(3k+4)=4*3^k: the largest n with ||n|| = m (Selfridge)
* ||2^(2^j) - 1|| = 2*2^j + j - 2 for j <= 5  (Iraids et al. 2012, Observation 2)
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from algorithms.exact_table import LIM, complexity_table, optimal_expression
from algorithms.expression import evaluate

N = 20000
C = complexity_table(N)


def test_first_values():
    # A005245 begins 1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 8, 7
    assert C[1:13] == [1, 2, 3, 4, 5, 5, 6, 6, 6, 7, 8, 7]
    assert C[11] == 8


def test_literature_values():
    assert all(C[3**k] == 3 * k for k in range(1, 10))
    assert all(C[2**k] == 2 * k for k in range(1, 15))
    assert C[1439] == 26
    assert C[2**8 - 1] == 17 and C[2**4 - 1] == 8


def test_selfridge_maxima():
    for m in range(2, 26):
        E = max(n for n in range(1, N + 1) if C[n] == m) if 3 ** (m / 3) < N else None
        if E is None:
            continue
        k, r = divmod(m - 2, 3)
        expected = [2 * 3**k, 3 ** (k + 1), 4 * 3**k][r]
        assert E == expected, m


def _E(k):
    """Closed form of the Selfridge maxima used in research/proof-exact-search.md, Lemma 1."""
    if k == 1:
        return 1
    j, r = divmod(k, 3)
    return [3**j, 4 * 3 ** (j - 1), 2 * 3**j][r]


def test_lemma1_inequalities():
    # The facts the written proof of Lemma 1 uses, checked for k <= 300 (the proof covers all k).
    for k in range(1, 301):
        assert _E(k) ** 3 <= 3**k                     # E(k) <= 3^(k/3)
        assert _E(k + 1) >= _E(k) + 1                 # strictly increasing
        for i in range(1, k):
            assert _E(i) * _E(k - i) <= _E(k)         # products
            assert _E(i) + _E(k - i) <= _E(k)         # sums


def test_lower_bound_3log3():
    # ||n|| >= 3 log_3 n  <=>  n^3 <= 3^||n||
    assert all(n**3 <= 3 ** C[n] for n in range(1, N + 1))


def test_cube_limits():
    for k, P in enumerate(LIM[:60]):
        assert P**3 <= 3**k < (P + 1) ** 3


def test_reconstruction_is_optimal_and_correct():
    for n in list(range(1, 400)) + [1439, 19999]:
        ev = evaluate(optimal_expression(n, C))
        assert ev.value == n and ev.ones == C[n]


@pytest.mark.skipif(shutil.which("gcc") is None, reason="gcc not available")
def test_c_implementation_matches_python(tmp_path):
    src = Path(__file__).resolve().parents[1] / "algorithms" / "c" / "complexity_table.c"
    exe = tmp_path / "ct"
    subprocess.run(["gcc", "-O2", "-o", str(exe), str(src)], check=True)
    out = tmp_path / "t.bin"
    subprocess.run([str(exe), str(N), str(out)], check=True, capture_output=True)
    data = out.read_bytes()
    assert list(data[1:]) == C[1:]
