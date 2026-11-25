"""Tests for the budgeted exact search (algorithms/exact_single.py)."""
import random

import pytest

from algorithms.exact_single import ExactSearch, divisors, factorize, is_prime, min_ones_lower
from algorithms.exact_table import complexity_table

C = complexity_table(30000)

# Iraids et al. 2012, Table 3: A(n) = ||2^n - 1|| - 2n, n = 2..39 (read 2026-11-25, BJMC PDF).
IRAIDS_A = {2: -1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 1, 8: 1, 9: 1, 10: 2, 11: 3, 12: 1, 13: 2, 14: 2,
            15: 2, 16: 2, 17: 3, 18: 1, 19: 2, 20: 2, 21: 2, 22: 3, 23: 4, 24: 2, 25: 3, 26: 3,
            27: 2, 28: 3, 29: 4, 30: 3, 31: 4, 32: 3, 33: 4, 34: 4, 35: 4, 36: 2, 37: 2, 38: 2,
            39: 3}


def test_number_theory_helpers():
    assert is_prime(2**61 - 1) and not is_prime(2**61 + 1)
    assert factorize(2**60 - 1) == {3: 2, 5: 2, 7: 1, 11: 1, 13: 1, 31: 1, 41: 1, 61: 1,
                                    151: 1, 331: 1, 1321: 1}
    assert divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]
    for m in range(1, 3000):
        j = min_ones_lower(m)
        assert m**3 <= 3**j and (j == 0 or m**3 > 3 ** (j - 1))


def test_matches_exact_table_with_small_base_table():
    # Use only a 300-entry table so the search does real work on n <= 30000.
    s = ExactSearch(C[:301])
    rng = random.Random(7)
    for n in [rng.randrange(301, 30001) for _ in range(400)] + [2**14 - 1, 29999]:
        assert s.complexity(n, C[n] + 2) == C[n], n


def test_budget_semantics():
    s = ExactSearch(C[:301])
    n = 1439  # ||1439|| = 26
    assert s.at_most(n, 25) == 26  # "more than 25"
    assert s.at_most(n, 26) == 26
    assert s.at_most(n, 40) == 26
    with pytest.raises(ValueError):
        ExactSearch(C[:301]).complexity(n, 25)


def test_reproduces_iraids_table3():
    s = ExactSearch(C)
    for k, A in IRAIDS_A.items():
        n = 2**k - 1
        assert s.complexity(n, 2 * k + 2 * k.bit_length()) - 2 * k == A, k
