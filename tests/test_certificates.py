import json
from pathlib import Path

from certificates.verify import verify

ROOT = Path(__file__).resolve().parents[1]
CERTS = sorted((ROOT / "certificates").rglob("*.json"))


def test_there_are_certificates():
    assert CERTS


def test_all_certificates_verify():
    for p in CERTS:
        ok, msg = verify(p)
        assert ok, f"{p}: {msg}"


def test_m61_benchmark_bound():
    best = min(json.loads(p.read_text())["ones"] for p in CERTS
               if json.loads(p.read_text())["n"] == str(2**61 - 1))
    assert best == 127  # update together with RESULTS.md if this ever improves


def test_tampered_certificate_fails(tmp_path):
    c = json.loads(CERTS[0].read_text())
    c["ones"] = c["ones"] - 1
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(c))
    ok, _ = verify(p)
    assert not ok
