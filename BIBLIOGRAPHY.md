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
| Iraids2012 | J. Iraids, K. Balodis, J. Čerņenoks, M. Opmanis, R. Opmanis, K. Podnieks, "Integer complexity: experimental and analytical results", *Sci. Papers Univ. Latvia* 787 (2012) 153–179. arXiv:1203.6462. | ◐ (2026-11-25, PDF from bjmc.lu.lv) | Thm 1: 3 log₃ n ≤ ‖n‖ ≤ 3 log₂ n. ‖n‖ computed for all n ≤ 10¹². ‖2^a‖ = 2a for a ≤ 39. Table 3: ‖2^n−1‖ − 2n for n ≤ 39. Thm 8 and Cor. 2–3 give upper bounds on ‖2^n−1‖. **We did not reliably read the exact formula of Cor. 2** (the extraction was garbled), so we don't use it yet. |
| Iraids2014 | Čerņenoks, Iraids, Opmanis, Opmanis, Podnieks, "Integer complexity: experimental and analytical results II", arXiv:1409.0446. | ○ | Follow-up; to read. |
| Altman2014 | H. Altman, *Integer complexity, addition chains, and well-ordering*, PhD thesis, U. Michigan (2014). | ○ | Defect theory. |
| AltmanZelinsky2012 | H. Altman, J. Zelinsky, "Numbers with integer complexity close to the lower bound", *Integers* 12(6) (2012). | ○ | Classification of low-defect numbers. **Possible route to lower bounds > 116 (RQ-3).** |
| Altman2016TCS | H. Altman, "Integer complexity: representing numbers of bounded defect", *Theoret. Comput. Sci.* 652 (2016) 64–85. | ○ | Algorithms for all numbers below a given defect. |
| Altman2018 | H. Altman, "Integer complexity: algorithms and computational results", *Integers* 18 (2018) A45; arXiv:1606.03635. | ◐ (abstract) | Verified ‖2^k 3^ℓ‖ = 2k + 3ℓ for k ≤ 48. Computes stabilization K(n). |
| Altman2019 | H. Altman, "Integer complexity: the integer defect", *Moscow J. Combin. Number Theory* 8(3) (2019) 193–217. | ○ | Defect lower bounds; used by He for pruning. |
| Wang2012 | J. Wang (?), "A counterexample to the prime conjecture of expressing numbers using just ones", *J. Number Theory* 133(2) (2013). | ○ (cited via Wikipedia) | Least prime p with ‖p‖ ≠ ‖p−1‖ + 1 is 353942783. We re-computed the two values (R-0101). Author name to be checked. |
| Shriver2015 | C. Shriver, "Applications of Markov chain analysis to integer complexity", arXiv:1511.07842. | ○ | Almost-all upper bound ≈ 3.52 log₃ n. The exact constant differs between sources (3.52 or 3.529), so check it. |
| Cordwell2019 | K. Cordwell, A. Epstein, A. Hemmady, S. J. Miller, E. Palsson, A. Sharma, S. Steinerberger, Y. N. Truong Vu, "On algorithms to calculate integer complexity", *Integers* 19 (2019) A12; arXiv:1706.08424. | ○ | O(N^1.223) all-n algorithm. |
| AriasDeReyna2014 | J. Arias de Reyna, J. van de Lune, "Algorithms for determining integer complexity", arXiv:1404.2183. | ○ | O(N^1.231) algorithm. |
| Zelinsky2022 | J. Zelinsky, "Upper bounds on integer complexity", arXiv:2211.02995. | ○ | ‖n‖ ≤ α log₃ n with α ≈ 4.125 for all n (per He 2024). |
| He2024 | Q. He, "Improved algorithms for integer complexity", *SOSA 2024*, SIAM, 107–114; arXiv:2308.10301. | ◐ (2026-11-25, arXiv PDF v2) | All n ≤ N in O(N polylog N). **Single n in O(n^0.6154)** (Thm 8), without computing every smaller value. Checked ‖2^i‖ = 2i for 2^i ≤ 2^126 and ‖2^i+1‖ = 2i+1 up to 2^121+1. Found ‖733^6‖ = 119 < 120. **Key for RQ-1.** Whether code was released is unknown. |
| KonyaginOganesyan2026 | S. Konyagin, K. Oganesyan, "Upper and lower estimates for integer complexity", arXiv:2603.20876 (v2, Apr 2026). | ◐ (2026-11-25) | Thm 1: ‖n‖ ≤ C_avg·ln n + C·(ln n)^{2/3}(ln ln n)^{4/3} for all n ≥ 3, C_avg ≈ 3.236; Cor. 1: 2.785 ≤ limsup ‖n‖/ln n ≤ 3.237. The closed form of C_avg was garbled in extraction, so recheck it. Thm 2: for almost all n, ‖n‖ > 3.06 log₃ n. Does not mention 2^61−1. |
| OEIS-A005245 | OEIS Foundation, A005245 "Mahler-Popken complexity of n". | ○ (oeis.org not reachable from our build container) | Reference values. |

## Non-literature sources (benchmark provenance)

| Key | Source | Status | Notes |
|-----|--------|--------|-------|
| Board-M61 | GitHub `math-market/integer-complexity-m61` ("Problem Market" board), main @ `394bec0`, created 2026-08-07. Apache-2.0. | ✅ (cloned 2026-11-25) | Task: an expression for 2^61−1 with < 150 ones. Baseline 150 (Horner, base 32767). "Floor 116" = ⌈3 log₃ N⌉. |
| Board-M61-PR4 | Same repo, pull request #4 by GitHub user `Prev56`, commit `0995202` (2026-10-02), CI re-trigger `6b79a63` (2026-11-01). | ✅ expression re-verified | **Open, not merged** as of 2026-11-25. Gives a 127-ones expression and no method. We couldn't see CI results or review comments (no API access to that repo). |
| Cody-42834 | MathWorks Cody Problem 42834, "Integer complexity (Large numbers)", by Peng Liu. | ◐ | Unrelated scoring-by-runtime challenge. The test cases load through JavaScript and we couldn't read them. No link to 2^61−1 found. |
