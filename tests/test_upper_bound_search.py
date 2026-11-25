from algorithms.exact_table import complexity_table
from algorithms.expression import evaluate
from algorithms.upper_bound_search import PeelSearch, parse_int

C = complexity_table(3000)


def test_parse_int():
    assert parse_int("2^61-1") == 2**61 - 1
    assert parse_int("12345") == 12345


def test_search_gives_valid_upper_bounds():
    s = PeelSearch(C, T=200, R=3, D=12)
    for n in [1439, 2047, 2999]:
        k = s.ub(n)
        ev = evaluate(s.expression(n))
        assert ev.value == n and ev.ones == k
        assert k >= C[n]  # never below the true complexity
