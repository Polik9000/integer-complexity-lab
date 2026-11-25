"""Lower-bound certificates: generator + independent checker (EXP-0003 step 2).

Positive tests compare with a full exact table; mutation tests check that the checker rejects
every kind of corruption listed in research/2026-11-25-certificate-architecture.md §6.
"""
import hashlib
import io
import json
import random
import sys
from pathlib import Path

import pytest

from algorithms.certificate_emit import CertificateEmitter
from algorithms.exact_single import ExactSearch
from algorithms.exact_table import complexity_table

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "certificates" / "lower"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_lower import Checker, Reject  # noqa: E402

FULL_N = 300_000
FULL = complexity_table(FULL_N)
T = 2_000
TABLE = bytes(FULL[: T + 1])
SHA = hashlib.sha256(TABLE).hexdigest()


class _Buf(io.StringIO):
    def close(self):  # keep contents readable after the emitter closes it
        pass


def make_cert(n, value, table=TABLE, sha=SHA):
    buf = _Buf()
    em = CertificateEmitter(buf, n, value - 1, len(table) - 1, sha)
    s = ExactSearch(list(table), emit=em)
    assert s.complexity(n, value) == value
    em.close()
    return buf.getvalue().splitlines()


def check(lines, table=TABLE):
    return Checker(table).run(lines, hashlib.sha256(table).hexdigest())


def test_lambda_and_small_primes():
    from check_lower import lam, small_prime
    assert [lam(v) for v in (1, 2, 3, 4, 5, 6, 7)] == [0, 2, 3, 4, 5, 5, 6]
    assert [p for p in range(50) if small_prime(p)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


@pytest.mark.parametrize("seed", range(3))
def test_random_targets_accepted(seed):
    rng = random.Random(seed)
    for n in rng.sample(range(T + 1, FULL_N + 1), 40):
        assert check(make_cert(n, FULL[n])) == (n, FULL[n] - 1)


def test_mersenne_iraids():
    from test_exact_single import IRAIDS_A
    for k in range(12, 27):
        n = 2**k - 1
        v = 2 * k + IRAIDS_A[k]
        if n > T:
            assert check(make_cert(n, v)) == (n, v - 1)


def test_large_target_with_pratt_records():
    n = 2**40 - 1
    from test_exact_single import IRAIDS_A
    lines = make_cert(n, 80 + IRAIDS_A[40] if 40 in IRAIDS_A else 82)
    assert any(json.loads(l)["type"] == "prime" for l in lines)
    assert check(lines)[0] == n


# ------------------------------- mutation tests -------------------------------

def _base():
    n = 2**21 - 1
    return n, make_cert(n, 44)


def _rejects(lines, table=TABLE):
    with pytest.raises(Reject):
        check(lines, table)


def _set(lines, i, **kw):
    r = json.loads(lines[i]); r.update(kw); lines[i] = json.dumps(r)


def test_true_but_unproved_claim_rejected():
    # G(n, ||n||) is false: raising the root claim must fail.
    n, lines = _base()
    h = json.loads(lines[0]); h["claim_gt"] += 1; lines[0] = json.dumps(h)
    _rejects(lines)
    n, lines = _base()
    _set(lines, len(lines) - 2, j=json.loads(lines[-2])["j"] + 1)
    _rejects(lines)


def test_every_single_raised_claim_rejected_or_harmless():
    # Raising j of any one claim by 1 must either be rejected or still be a true statement.
    n, lines = _base()
    claims = [i for i, l in enumerate(lines) if json.loads(l)["type"] == "claim"]
    for i in claims[:60]:
        mut = list(lines); r = json.loads(mut[i])
        m, j = r["m"], r["j"] + 1
        _set(mut, i, j=j)
        try:
            check(mut)
        except Reject:
            continue
        assert m > FULL_N or FULL[m] > j, f"false claim ||{m}|| > {j} accepted"


def test_deleted_claim_rejected():
    n, lines = _base()
    claims = [i for i, l in enumerate(lines) if json.loads(l)["type"] == "claim"]
    del lines[claims[len(claims) // 2]]
    _rejects(lines)  # record count or a dependency fails


def test_reordered_claim_rejected():
    n, lines = _base()
    claims = [i for i, l in enumerate(lines) if json.loads(l)["type"] == "claim"]
    i = claims[0]
    mut = lines[:i] + lines[i + 1:-1] + [lines[i], lines[-1]]  # first claim moved to the end
    _rejects(mut)


def test_bad_factorizations_rejected():
    n, lines = _base()
    i = len(lines) - 2  # root claim, n = 2^21-1 = 7^2 * 127 * 337
    r = json.loads(lines[i])
    for f in ([[7, 2], [127, 1]], [[49, 1], [127, 1], [337, 1]], [[7, 1], [127, 1], [337, 1], [7, 1]]):
        mut = list(lines); _set(mut, i, f=f); _rejects(mut)


def test_fake_prime_and_bad_witness_rejected():
    p_comp = 65537 * 65539  # composite > 2^16
    q = [2, 3, 5, 7]
    base = [json.dumps({"type": "header", "version": 1, "target": "1", "claim_gt": 0,
                        "table": {"T": T, "sha256": SHA}})]
    for rec in ({"type": "prime", "p": p_comp, "a": 2, "q": [2]},
                {"type": "prime", "p": 65537, "a": 2, "q": [2]},     # 2 has order 32 mod 65537
                {"type": "prime", "p": 70001, "a": 3, "q": q},       # 3 does not divide p - 1 = 70000
                {"type": "prime", "p": 30, "a": 1, "q": []}):
        _rejects(base + [json.dumps(rec), json.dumps({"type": "end", "records": 1})])
    ok = base + [json.dumps({"type": "prime", "p": 65537, "a": 3, "q": [2]}),
                 json.dumps({"type": "end", "records": 1})]
    _rejects(ok)  # well-formed prime, but target claim not established
    with pytest.raises(Reject, match="target"):
        check(ok)


def test_table_tampering_and_truncation_rejected():
    n, lines = _base()
    bad = bytearray(TABLE); bad[1999] += 1
    with pytest.raises(Reject, match="table"):
        Checker(bytes(bad)).run(lines, hashlib.sha256(bytes(bad)).hexdigest())
    _rejects(lines, bytes(bad))       # SHA mismatch against header
    _rejects(lines[:-1])              # missing end record
    _rejects(lines[:-2] + lines[-1:]) # root claim dropped
    _rejects(lines + lines[-1:])      # records after end
