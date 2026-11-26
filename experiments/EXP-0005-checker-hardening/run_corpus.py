#!/usr/bin/env python3
"""EXP-0005: run the hardened checker over a corpus of certificate files.

For every certificate file in the corpus directories, find the table whose SHA-256 the header names
(among the given table files), and run certificates/lower/check_lower.py's Checker on it in its most
permissive mode (no expected target/claim given: the attacker controls the header). Print one line per
file: ACCEPT/REJECT and the reason. Files are classified by the caller (see README).
Usage: python3 run_corpus.py --tables T1.bin T2.bin ... --certs FILE_OR_DIR ...
"""
import argparse, gzip, hashlib, importlib.util, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_lower", ROOT / "certificates/lower/check_lower.py")
CL = importlib.util.module_from_spec(spec); spec.loader.exec_module(CL)

ap = argparse.ArgumentParser()
ap.add_argument("--tables", nargs="+", required=True)
ap.add_argument("--certs", nargs="+", required=True)
a = ap.parse_args()
tables = {}
for t in a.tables:
    d = open(t, "rb").read()
    tables[hashlib.sha256(d).hexdigest()] = (t, d)
files = []
for c in a.certs:
    p = Path(c)
    files += sorted(x for x in p.rglob("*") if x.is_file() and ".jsonl" in x.name) if p.is_dir() else [p]
for f in files:
    opener = gzip.open if f.name.endswith(".gz") else open
    try:
        with opener(f, "rt", encoding="utf-8", errors="strict") as fh:
            first = fh.readline()
        h = json.loads(first)
        sha = h.get("table", {}).get("sha256") if isinstance(h, dict) and isinstance(h.get("table"), dict) else None
    except Exception as e:  # unreadable header: use any table, the checker must still reject
        sha = None
    t = tables.get(sha) or next(iter(tables.values()))
    try:
        with opener(f, "rt", encoding="utf-8") as fh:
            v = CL.Checker(t[1]).run(fh, hashlib.sha256(t[1]).hexdigest())
        print(f"ACCEPT  {f}  ||{v[0]}|| > {v[1]}  table={os.path.basename(t[0])}")
    except CL.Reject as e:
        print(f"REJECT  {f}  {str(e)[:110]}")
