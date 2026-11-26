# BIBLIOGRAPHY

Each entry records **what we actually checked** in it, when, and how. "Checked" means we read
the stated location in the primary source. Anything we only know from a secondary
summary is marked as such. BibTeX for papers goes in `papers/references.bib` once we need it.

Legend: ✅ checked at the cited location · ◐ read partially or through a machine
extraction that garbled some formulas · ○ not read yet (cited by others).

## Core literature

| Key | Reference | Status | What we use / verified |
|-----|-----------|--------|------------------------|
| Guy1986 | R. K. Guy, "Some suspiciously simple sequences", *Amer. Math. Monthly* 93(3) (1986) 186–190. | ○ | Origin of the problem in print. Selfridge's lower bound 3 log₃ n. |
| MahlerPopken1953 | K. Mahler, J. Popken, "On a maximum problem in arithmetic", *Nieuw Arch. Wisk.* 1 (1953) 1–15. | ○ | Original source of the notion. |
| Iraids2012 | J. Iraids, K. Balodis, J. Čerņenoks, M. Opmanis, R. Opmanis, K. Podnieks, "Integer complexity: experimental and analytical results", *Sci. Papers Univ. Latvia* 787 (2012) 153–179. arXiv:1203.6462. | ◐ (2026-11-25, PDF from bjmc.lu.lv; Table 3, Thm 8, Cor. 2–3 read verbatim) | Thm 1: 3 log₃ n ≤ ‖n‖ ≤ 3 log₂ n. ‖n‖ computed for all n ≤ 10¹². ‖2^a‖ = 2a for a ≤ 39. Table 3: ‖2^n−1‖ − 2n for n ≤ 39. Thm 8 and Cor. 2–3 give upper bounds on ‖2^n−1‖. Cor. 2: ‖2^n−1‖ ≤ 2n + ⌊log₂ n⌋ + H(n) − 3; Cor. 3: ≤ 2n + 2⌊log₂ n⌋ − 2 (n > 1). Table 3 values are used as regression tests. |
| Iraids2014 | Čerņenoks, Iraids, Opmanis, Opmanis, Podnieks, "Integer complexity: experimental and analytical results II", arXiv:1409.0446. | ○ | Follow-up; to read. |
| Altman2014 | H. Altman, *Integer complexity, addition chains, and well-ordering*, PhD thesis, U. Michigan (2014). | ○ | Defect theory. |
| AltmanZelinsky2012 | H. Altman, J. Zelinsky, "Numbers with integer complexity close to the lower bound", *Integers* 12(6) (2012); arXiv:1207.4841. | ◐ (2026-11-25; Thm 1.6 read verbatim twice, §5–6 not read) | **Thm 1.6** (all n with δ(n) < 1) gives ‖2^61−1‖ ≥ 117 (R-0006). We cross-checked it against our table for n ≤ 4·10⁸. Note: `research/lit-AltmanZelinsky2012.md`. |
| Altman2019a | H. Altman, "Integer complexity: the integer defect", arXiv:1804.07446. | ◐ (partial) | Integer defect D(n) = ‖n‖ − L(n). Gives nothing beyond 117 for N. |
| Altman2016TCS | H. Altman, "Integer complexity: representing numbers of bounded defect", *Theoret. Comput. Sci.* 652 (2016) 64–85. | ○ | Algorithms for all numbers below a given defect. |
| Altman2018 | H. Altman, "Integer complexity: algorithms and computational results", *Integers* 18 (2018) A45; arXiv:1606.03635. | ◐ (abstract) | Verified ‖2^k 3^ℓ‖ = 2k + 3ℓ for k ≤ 48. Computes stabilization K(n). |
| Altman2019 | H. Altman, "Integer complexity: the integer defect", *Moscow J. Combin. Number Theory* 8(3) (2019) 193–217. | ○ | Defect lower bounds; used by He for pruning. |
| Wang2012 | J. Wang (?), "A counterexample to the prime conjecture of expressing numbers using just ones", *J. Number Theory* 133(2) (2013). | ○ (cited via Wikipedia) | Least prime p with ‖p‖ ≠ ‖p−1‖ + 1 is 353942783. We re-computed the two values (R-0101). Author name to be checked. |
| Shriver2015 | C. Shriver, "Applications of Markov chain analysis to integer complexity", arXiv:1511.07842. | ○ | Almost-all upper bound ≈ 3.52 log₃ n. The exact constant differs between sources (3.52 or 3.529), so check it. |
| Cordwell2019 | K. Cordwell, A. Epstein, A. Hemmady, S. J. Miller, E. Palsson, A. Sharma, S. Steinerberger, Y. N. Truong Vu, "On algorithms to calculate integer complexity", *Integers* 19 (2019) A12; arXiv:1706.08424. | ○ | O(N^1.223) all-n algorithm. |
| AriasDeReyna2014 | J. Arias de Reyna, J. van de Lune, "Algorithms for determining integer complexity", arXiv:1404.2183. | ○ | O(N^1.231) algorithm. |
| Zelinsky2022 | J. Zelinsky, "Upper bounds on integer complexity", arXiv:2211.02995. | ○ | ‖n‖ ≤ α log₃ n with α ≈ 4.125 for all n (per He 2024). |
| He2024 | Q. He, "Improved algorithms for integer complexity", *SOSA 2024*, SIAM, 107–114; arXiv:2308.10301. | ✅ (2026-11-25, full arXiv v2 text; formulas partly garbled) | Thms 6–8, Alg. 2, App. A. Code: GitHub `hqztrue/integer_complexity` (GPL), inspected at `742e8c5`; built and run with the lead's approval on 2026-11-25 (EXP-0003: reproduces Iraids Table 3 and our k ≤ 61 values). Note: `research/lit-He2024.md`. |
| KonyaginOganesyan2026 | S. Konyagin, K. Oganesyan, "Upper and lower estimates for integer complexity", arXiv:2603.20876 (v2, Apr 2026). | ◐ (2026-11-25) | Thm 1: ‖n‖ ≤ C_avg·ln n + C·(ln n)^{2/3}(ln ln n)^{4/3} for all n ≥ 3, C_avg ≈ 3.236; Cor. 1: 2.785 ≤ limsup ‖n‖/ln n ≤ 3.237. The closed form of C_avg was garbled in extraction, so recheck it. Thm 2: for almost all n, ‖n‖ > 3.06 log₃ n. Does not mention 2^61−1. |
| Knox2026-OPL | B. Knox (GitHub `BrettKnox`), *open-problems-lab*, `OpenProblemsLab/IntegerComplexity.lean`, commit `e899b51` (2026-08-20); inspected at HEAD `04ef51f`. Apache-2.0. Lean 4 + Mathlib. | ✅ (source read 2026-11-25; not built by us) | **Prior Lean formalization of integer complexity**: `complexity`, Selfridge `n³ ≤ 3^‖n‖`, ‖3^k‖ = 3k, ‖2^n‖ = 2n for n ≤ 9, ‖6‖ = 5, defect and stability. No Theorem C or certificate checker. See EXP-0004 literature §6. |
| DeepMind-FC-75792 | google-deepmind/formal-conjectures, `FormalConjectures/Mathoverflow/75792.lean`, created by PR #269, commit `798eb17d` (2025-06-30, Kenny Lau); inspected at HEAD `9097e2f9`. Apache-2.0. | ✅ (source read 2026-11-25 at both commits; not built) | **Earliest Lean formalization of integer complexity we know of**: `Reachable`, `complexity` (`Nat.find`), split lemma `reachable_iff_of_two_le`, decidable exhaustive procedure; ‖1‖ = 1, ‖2‖ = 2. `complexity_three_pow` is `sorry`. EXP-0004 literature §7. |
| Atlas-Lean-IC | facebookresearch/atlas-lean, `MathlibExt/NumberTheory/IntegerComplexity*.lean`, first commit `b0cf10508` (2026-10-05); inspected at HEAD `58909c41`. Licence forbids use for ML training. | ✅ (theorem names, commits and `sorry` grep checked 2026-11-25; not built) | `complexity`, `complexityLowerBoundG_le` (integer Selfridge-type bound), `complexity_lt_of_gt_extremal`, `complexity_eq_min` (recursion), log₂ bound. EXP-0004 literature §7. |
| PS-powers-cert | GitHub `patternscientist/integer-complexity-powers-certificate`, commits `23f6985`–`be74752` (2026-06-02/03). | ○ (reported by the EXP-0004 literature reviewer; not checked by the primary agent) | Hash-pinned low-defect certificate for ‖2^m − b‖ ≥ 2m − 1, 49 ≤ m ≤ 56; not peer reviewed. |
| Altman-lowdefect-code | H. Altman, low-defect implementation, https://hjaltman.github.io/lowdefect.tar.gz; github.com/hjaltman/lowdefect `9e21cf4` (2020-11-28). | ○ (located by the literature reviewer) | Code for the AZ/Altman algorithms. |
| OEIS-A005245 | OEIS Foundation, A005245 "Mahler-Popken complexity of n". | ○ (reachability depends on the container's network policy: blocked in some sessions, reachable in EXP-0004; see its disagreement log D7) | Reference values. |

## Non-literature sources (benchmark provenance)

| Key | Source | Status | Notes |
|-----|--------|--------|-------|
| Board-M61 | GitHub `math-market/integer-complexity-m61` ("Problem Market" board), main @ `394bec0`, created 2026-08-07. Apache-2.0. | ✅ (cloned 2026-11-25) | Task: an expression for 2^61−1 with < 150 ones. Baseline 150 (Horner, base 32767). "Floor 116" = ⌈3 log₃ N⌉. |
| Board-M61-PR4 | Same repo, pull request #4 by GitHub user `Prev56`, commit `0995202` (2026-10-02), CI re-trigger `6b79a63` (2026-11-01). | ✅ expression re-verified | **Open, not merged** as of 2026-11-25. Gives a 127-ones expression and no method. We couldn't see CI results or review comments (no API access to that repo). |
| Cody-42834 | MathWorks Cody Problem 42834, "Integer complexity (Large numbers)", by Peng Liu. | ◐ | Unrelated scoring-by-runtime challenge. The test cases load through JavaScript and we couldn't read them. No link to 2^61−1 found. |
