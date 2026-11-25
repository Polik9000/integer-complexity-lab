# lean-cert: Lean 4 + Mathlib checker for integer-complexity lower-bound certificates

Status (2026-11-25): built by the Lean builder agent, then rebuilt independently by the primary agent from a
certificate regenerated from committed files (same data SHA-256, same axioms), and reviewed by an independent Lean
reviewer. Part of EXP-0004 (PR #5, draft).

**Trust level of the headline.** `‖2^61 − 1‖ > 126` is checked here **via `native_decide`** only. That is *not*
`FORMALLY VERIFIED` in the sense of CLAUDE.md §4 under our trust model, which counts only the kernel and the three
standard axioms. The soundness theorems (checker, divisors, Pratt) and the small cases k = 20, 24 are kernel-checked.
CI builds `ICLCert.CI` (soundness + kernel-only k = 20); the full run needs the generated data and is run by hand.

## What is proved

| Theorem | Statement | Trust level | Axioms (`#print axioms`) |
|---|---|---|---|
| `ICLCert.checkCert_sound` | `checkCert N B chunks = true → IntegerComplexity.LowerBound N B`, for **all** `N B chunks` | kernel | `propext, Classical.choice, Quot.sound` |
| `ICLCert.mem_divisorsOf` | if every `p` in `f` is prime, every `d ∣ ∏ p^e` is in `divisorsOf f` | kernel | same |
| `ICLCert.prattOK_sound` | an accepted Pratt record has `p.Prime` (Mathlib `lucas_primality`) | kernel | same |
| `k20_lb` | `LowerBound (2^20 - 1) 42` (real table-free certificate: 1302 records) | **kernel** (`decide +kernel`) | same |
| `k24_lb` | `LowerBound (2^24 - 1) 50` (1962 records) | **kernel** (`decide +kernel`) | same |
| `ICLCert.M61.check_native` | `checkCert (2^61 - 1) 127 M61Data.chunks = true` | **native_decide** | the three above + `ICLCert.M61.check_native._native.native_decide.ax_1_1` |
| `ICLCert.M61.lowerBound_native` | `LowerBound (2 ^ 61 - 1) 127` (i.e. ‖2^61−1‖ > 126) | **native_decide** | same as `check_native` |
| `ICLCert.M61.hasComplexity_native` | `HasComplexity (2 ^ 61 - 1) 127` | upper bound: kernel. Lower bound: **native_decide** | same as `check_native` |

`LowerBound`, `UpperBound` and `HasComplexity` are the repository's definitions, over `Nat`
(`IntegerComplexity/Basic.lean`, copied byte for byte). `2 ^ 61 - 1` is a `Nat`, so it cannot wrap.

**native_decide trust (Lean 4.35):** `native_decide` adds an auxiliary axiom that states the
compiled evaluation's result. Trusting it means trusting:
- the Lean compiler (LCNF→IR→C) and the IR interpreter;
- the C compiler that built `libICLCert_ICLCertCore.so`;
- the runtime, including GMP for `Nat`;
- the `@[extern]` implementations used by the evaluated term (`String.toUTF8`, `ByteArray` access, `Nat` arithmetic).

Our own code uses no `implemented_by`, `extern`, `partial` or `unsafe`, and no `axiom` or `sorry`.

## Design

- `ICLCertCore.lean` imports only `Init` and holds every executable definition:
  - a binary trie in which every node stores its own key (a malformed trie can only fail);
  - `lb v = max(1, λ(v), proven(v)+1)`;
  - the sum rule, with the same cut-off as `PoC.Checker.sumsFrom`;
  - the product rule over `divisorsOf f`, the list of all divisors generated from the factorisation;
  - a Pratt/Lucas check with fuel-based binary `powMod`; primes below 2^16 are checked by trial division;
  - `step`, `run`, `runChunks` and `checkCert`;
  - an *unverified* text parser.

  Recursion is structural on fuel throughout, so the kernel can evaluate it. Too little fuel can
  only make a check fail. The library is built with `precompileModules = true`, so `native_decide` runs native code.
- `ICLCert/Sound.lean` (Mathlib) holds the soundness proofs. The sum rule reduces to the repository's
  `sumsFrom_sound`, and `theoremC` and `lowerBound_of_cube` are reused unchanged. The checker
  invariant has two parts: every stored claim is true, and every stored prime is `Nat.Prime`.
- The target `N` and the bound `B` are in the theorem statement, not in the data. The checker accepts when
  `B ≤ lb(N)` after all records have been processed. The header and end records of the JSONL are checked
  by the generator, which is not trusted, and then dropped.
- The parser, the generator and the data are **not** in the trust base, because soundness holds for any record list.

## Commands (exact) and measured results

Environment: Lean 4.35.0 (`eb6cafb7290e`), Mathlib `v4.35.0` (rev `56a005855ea1`), 4 vCPU, 15 GB RAM, Linux.
`.lake/packages` is a symlink to an existing Mathlib checkout with its downloaded cache. The manifest is identical.

```
export PATH=<lean-4.35.0>/bin:$PATH
# data (not committed; 94 MB): 32 text chunks from the table-free certificate
#   input sha256 (gz) 623887b1a0cf23f9cc8b407005bc4a03d6472f81cd5c7578467e7dd7808d6173
python3 scripts/gen_lean_data.py text tablefree_k61.jsonl.gz data/k61 32
#   -> 3,068,111 records (= end.records), 98,141,241 bytes,
#      sha256(cat data/k61/chunk_*.txt) = a562ff007fb281efcd09baf0e427cdf14b7950836eddc704d5d3b8d8b7f56ce2
#      37.8 s, 2.6 GB RSS (the script loads everything at once)
rm -rf .lake/build && lake build            # default target: Sound + M61.Native
#   122 s wall, 103.5 s user, peak RSS 3.3 GB; native_decide evaluation 108-111 s
lake build ICLCert.M61.Negative             # 180 s, 1.6 GB
#   genuine data with bound 128 -> false (87.5 s); root claim raised to j=127 (‖N‖>127), bound 128 -> false (89 s)
lake build ICLCert.Axioms                   # 67 s, 5.7 GB (includes the kernel runs k20, k24)
lake build ICLCert.Test.Mutants ICLCert.Test.Native40   # 11 s
```

Logs: `logs/build_default_clean.log`, `logs/build_m61_native.log`, `logs/build_m61_negative.log`,
`logs/build_axioms.log`, `logs/kernel_24_30.log`, `logs/mutants.log`, `logs/gen_k61.log`, `logs/sha256.txt`.

### Kernel path (M6)

Small certificates came from `gen_table_free_cert.py table_1e8.bin K U OUT f847df9` (T0 = 1000).
Each was converted with `gen_lean_data.py terms` into explicit `List Rec` terms and checked by `decide +kernel`.

| k | records | claims | sum checks | prod checks | kernel time | peak RSS |
|---|---|---|---|---|---|---|
| 20 | 1,302 | 1,295 | 1,428 | 3,925 | 16.1 s | (not measured separately) |
| 24 | 1,962 | 1,944 | 2,164 | 8,107 | 34.6 s | 5.7 GB |
| 30 | 6,542 | 6,384 | 7,400 | 42,972 | **killed** at 130 s | 11.8 GB, still growing (over the 8 GB budget) |

(The check counts come from `check_lower_strict.py`, which accepts all four small certificates.)

Extrapolation to 2^61−1: the certificate has 2.9 M claims, 4.08 M sum checks, 27.8 M product checks
and 161,681 Pratt records. The marginal cost from k=20 to k=24 is about 3.8 ms per check. That gives about
31.8 M × 3.8 ms ≈ 1.2·10^5 s, roughly 34 CPU-hours, as a *lower* estimate: lookups go deeper and the numbers are larger.
The bigger problem is memory: the kernel keeps its caches for the whole declaration, and even k=30 does
not fit in 8 GB as one declaration. A kernel-only proof therefore needs the certificate **split into many
declarations with explicit checkpoint states**, or a hint-based format with per-claim lemmas. That is not done here.

### Negative tests

All of these pass (`#guard`; the build fails otherwise):
- `ICLCert/Test/Mutants.lean`, for k=20 and k=40:
  - genuine data is accepted at the true bound and rejected at bound+1;
  - rejected: root j+1, root deleted, largest Pratt record deleted, composite p+2 in place of a prime,
    witness a=1, last q missing, bad root factorisation, the claim just before the root moved after it, truncated file.
  - Informational only: a mid claim moved to the end, or a random claim's j raised by one, can still be
    accepted when that claim is not needed or is still provable. This is expected and not a soundness issue.
- `ICLCert/M61/Negative.lean` checks the full certificate with bound 128, and with the root raised to `> 127`. Both are rejected.

## Files

- `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`
- `IntegerComplexity/{Basic,PoC/Selfridge,PoC/Checker,Certificates/M61}.lean`: unchanged copies from
  branch `research/exp-0004-proof-audit` @ `f847df92d978`. The project copies them because the repo's `lean/`
  has no Mathlib; a later `require IntegerComplexity from "../lean"` should work, since it uses the same toolchain.
- `ICLCertCore.lean`: the executable checker. `ICLCert/Sound.lean`: the proofs.
- `ICLCert/M61/{Data,Native,Negative}.lean`: the 2^61−1 run. `ICLCert/Axioms.lean`: `#print axioms`.
- `ICLCert/Test/{Kernel20,Kernel24,Kernel30,Mutants,Native40}.lean`, with `ICLCert/Data/K{20,24,30}.lean` as generated kernel data.
- `scripts/gen_lean_data.py`, `scripts/make_mutants.py`, `scripts/measure.py`
- `data/`: generated. Committed: the small inputs (`certs/`, `k20`, `k24`, `k30`, `k40`, `mut20`, about 1.6 MB).
  Not committed (ignored): `k61/` (94 MB), `k61mut/`, `mut40/`. Regenerate `k61` with the command above from the
  table-free certificate (`research/EXP-0004-independent-proof-audit/tools/run_tablefree.sh`); `mut40` with
  `python3 scripts/make_mutants.py data/k40/chunk_000.txt data/mut40 1099511627775`; `k61mut` with `mkdir -p data/k61mut && sed "s/^C 2305843009213693951 126 /C 2305843009213693951 127 /" data/k61/chunk_031.txt > data/k61mut/chunk_031_root127.txt`.
- `ICLCert/CI.lean`: the CI target.
