#!/usr/bin/env python3
"""Make mutated copies of a compact certificate text (from gen_lean_data.py text) for negative tests.

Usage: make_mutants.py CHUNK.txt OUTDIR TARGET
Each mutant must be REJECTED by the Lean checker (checkCert TARGET B [parse mutant] = false for the
genuine bound B, or for B+1 in the 'root_plus_one' case which keeps the data unchanged).
"""
import os, sys, random

src, outdir, target = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = open(src).read().splitlines()
os.makedirs(outdir, exist_ok=True)
rnd = random.Random(20261125)


def write(name, ls):
    with open(os.path.join(outdir, name + ".txt"), "w") as fh:
        fh.write("".join(l + "\n" for l in ls))


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


claims = [i for i, l in enumerate(lines) if l.startswith("C ")]
primes = [i for i, l in enumerate(lines) if l.startswith("P ")]
root = max(i for i in claims if int(lines[i].split()[1]) == target)

# 1. root claim j raised by one (target bound then B+1)
ls = list(lines); f = ls[root].split(); f[2] = str(int(f[2]) + 1); ls[root] = " ".join(f); write("root_j_plus_one", ls)
# 2. root claim deleted
write("root_deleted", lines[:root] + lines[root + 1:])
# 3. a Pratt record deleted (the one for the largest prime used)
big = max(primes, key=lambda i: int(lines[i].split()[1]))
write("prime_deleted", lines[:big] + lines[big + 1:])
# 4. composite presented as prime: p -> p+2 if composite, keep q list
ls = list(lines); f = ls[big].split(); p = int(f[1])
c = p + 2
while is_prime(c) if c < 10**7 else False:
    c += 2
f[1] = str(c); ls[big] = " ".join(f); write("composite_as_prime", ls)
# 5. Pratt witness replaced by 1 (wrong order)
ls = list(lines); f = ls[big].split(); f[2] = "1"; ls[big] = " ".join(f); write("witness_one", ls)
# 6. Pratt q list missing one prime
ls = list(lines); f = ls[big].split()
if len(f) > 4:
    del f[-1]
ls[big] = " ".join(f); write("pratt_q_missing", ls)
# 7. wrong factorisation in the root claim (replace m's factor list by [m-? ...]): drop last factor pair
ls = list(lines); f = ls[root].split()
if len(f) >= 7:
    f = f[:-2]
else:
    f = f[:3] + ["2", "1"] + f[3:]
ls[root] = " ".join(f); write("root_bad_factorisation", ls)
# 8. the last claim before the root moved after the root (after its first use)
mid = max(i for i in claims if i < root)
write("claim_moved_after_root", lines[:mid] + lines[mid + 1:root + 1] + [lines[mid]] + lines[root + 1:])
# 8b. informational: a mid claim moved to the end (may be accepted if that claim is not needed)
mid2 = claims[len(claims) // 2]
write("mid_claim_moved_to_end", lines[:mid2] + lines[mid2 + 1:] + [lines[mid2]])
# 9. truncated file (last 10 records dropped)
write("truncated", lines[:-10])
# 10. random claim's j raised by one (true-but-unproved style mutation); may or may not break
i = rnd.choice(claims[len(claims) // 2:])
ls = list(lines); f = ls[i].split(); f[2] = str(int(f[2]) + 1); ls[i] = " ".join(f); write("random_j_plus_one", ls)
print("root line", root, "big prime line", big, "mid claim", mid, "random", i)
