#!/usr/bin/env python3
"""EXP-0003 step 2: write a lower-bound certificate ||n|| > U-1 for n = 2^k - 1.
Usage: python3 gen_cert.py TABLE.bin K U OUT.jsonl.gz COMMIT
U must be a verified upper bound (an expression with U ones); the run then also proves ||n|| = U.
"""
import hashlib, json, resource, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from algorithms.certificate_emit import CertificateEmitter, open_cert
from algorithms.exact_single import ExactSearch
from algorithms.exact_table import ByteTable

table_path, k, U, out, commit = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
sha = hashlib.sha256(Path(table_path).read_bytes()).hexdigest()
tab = ByteTable(table_path)
n = 2**k - 1
t0 = time.time()
em = CertificateEmitter(open_cert(out), n, U - 1, tab.N, sha, commit)
s = ExactSearch(tab, emit=em)
v = s.complexity(n, U)
em.close()
print(json.dumps({"k": k, "n": n, "U": U, "value": v, "T": tab.N, "table_sha256": sha,
                  "records": em.records, "primes": len(em.primes), "search_calls": s.calls,
                  "sec": round(time.time() - t0, 1),
                  "maxrss_MB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}))
