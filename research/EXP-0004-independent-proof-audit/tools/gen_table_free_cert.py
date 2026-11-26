#!/usr/bin/env python3
"""EXP-0004: generate a TABLE-FREE lower-bound certificate ||2^k-1|| > U-1.

The certificate's header names the trivial table [0, 1] (T = 1, i.e. only ||1|| = 1), so a checker needs
no precomputed table at all. It starts with claims G(v, ||v||-1) for v = 2..T0 in increasing order (each is
checkable from the earlier ones), then the claims emitted by the existing search run with a base table of
size T0. Nothing here is trusted by the checker: a wrong value only makes the certificate fail.
Usage: python3 gen_table_free_cert.py TABLE.bin K U OUT.jsonl.gz COMMIT [T0]
"""
import hashlib, json, resource, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from algorithms.certificate_emit import CertificateEmitter, open_cert
from algorithms.exact_single import ExactSearch

tpath, k, U, out, commit = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
T0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1000
with open(tpath, "rb") as fh:
    small = list(fh.read(T0 + 1))
trivial = bytes([0, 1])
n = 2 ** k - 1
t0 = time.time()
em = CertificateEmitter(open_cert(out), n, U - 1, 1, hashlib.sha256(trivial).hexdigest(), commit)
for v in range(2, T0 + 1):
    em.claim(v, small[v] - 1)
s = ExactSearch(small, emit=em)
v = s.complexity(n, U)
em.close()
print(json.dumps({"k": k, "n": n, "U": U, "value": v, "T0": T0, "records": em.records,
                  "primes": len(em.primes), "search_calls": s.calls, "sec": round(time.time() - t0, 1),
                  "maxrss_MB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}))
