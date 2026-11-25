import pytest

from algorithms.expression import ExpressionError, evaluate, to_lean


@pytest.mark.parametrize(
    "s,value,ones",
    [
        ("1", 1, 1),
        ("1+1", 2, 2),
        ("(1+1)*(1+1+1)", 6, 5),
        ("(1+1+1)*(1+1+1)+1+1", 11, 8),  # the classic ||11|| = 8 example
        (" ( 1 + 1 ) * ( 1 + 1 ) ", 4, 4),
        ("((((1))))", 1, 1),
    ],
)
def test_evaluate(s, value, ones):
    ev = evaluate(s)
    assert (ev.value, ev.ones) == (value, ones)


@pytest.mark.parametrize(
    "s",
    ["", "2", "1-1", "1**1", "1^1", "(1+1", "1+1)", "1+", "*1", "()", "1 1",
     "__import__('os')", "1+1;1", "１"],
)
def test_rejects_outside_grammar(s):
    with pytest.raises(ExpressionError):
        evaluate(s)


def test_precedence_is_standard():
    assert evaluate("1+1*1+1").value == 3
    assert evaluate("(1+1)*(1+1)+1").value == 5


def test_deep_nesting_is_handled():
    s = "(" * 3000 + "1+1" + ")" * 3000
    assert evaluate(s).value == 2


def test_to_lean_shape():
    assert to_lean("(1+1)*1") == "(.mul (.add .one .one) .one)"
