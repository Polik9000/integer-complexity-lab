# Literature note: Altman & Zelinsky (2012) and Altman's defect papers

- H. Altman, J. Zelinsky, "Numbers with integer complexity close to the lower bound",
  arXiv:1207.4841 (v1, 2012-07-20), *Integers* 12(6) (2012). Read on 2026-11-25 through two independent
  full-text extractions. Theorem 1.6 was read verbatim (twice, consistently).
- H. Altman, "Integer complexity: the integer defect", arXiv:1804.07446; *Moscow J. Combin.
  Number Theory* 8(3) (2019). Read partially.
- H. Altman, "Integer complexity: representing numbers of bounded defect", arXiv:1603.06122;
  *Theoret. Comput. Sci.* 652 (2016). Read partially (summary only).

## Definitions

Defect δ(n) = ‖n‖ − 3 log₃ n ≥ 0, with δ(n) = 0 iff n = 3^k (AZ2012 Def. 1.4, Prop. 2.1).

## Theorem 1.6 (AZ2012): all n with δ(n) < 1

The numbers with 0 ≤ δ(n) < 1 are exactly:
1. 3^k (k ≥ 1), with complexity 3k;
2. 2^a 3^k, a ≤ 9 (a, k not both 0), with complexity 2a + 3k;
3. 5·2^a 3^k, a ≤ 3, with complexity 5 + 2a + 3k;
4. 7·2^a 3^k, a ≤ 2, with complexity 6 + 2a + 3k;
5. 19·3^k, with complexity 9 + 3k;
6. 13·3^k, with complexity 8 + 3k;
7. (3^n + 1)·3^k, n ≠ 0, with complexity 1 + 3n + 3k.

Also, n = 1 is the only number with δ = 1. The paper says it is proven in §6.2, based on Thm 5.1
(δ < 12δ(2) ≈ 1.286). We haven't read §5–6 and haven't checked whether the pruning there is by hand.

## Consequence for N = 2^61 − 1: ‖N‖ ≥ 117

N is prime, odd, and N ≡ 1 (mod 3), so 3 ∤ N, and N > 19.
- Families 1–6 with 3 ∤ N force k = 0. That leaves N ∈ {2^a : a ≤ 9} ∪ {5·2^a : a ≤ 3} ∪ {7·2^a : a ≤ 2}
  ∪ {13, 19}. All of these are ≤ 512, so none equals N.
- Family 7 with k = 0 needs 3^n = N − 1 = 2^61 − 2, which is even. That's impossible.
- N ≠ 1, so δ(N) ≠ 1.

Hence δ(N) > 1, i.e. ‖N‖ > 3 log₃ N + 1 = 116.46…, so **‖N‖ ≥ 117**.

Status: `PROVEN` relative to AZ2012 Thm 1.6 (`LITERATURE`). Our own computation in EXP-0002
independently gives the stronger ‖N‖ = 127, which is consistent with this.

**Independent sanity check (cheap, planned for EXP-0003):** use the exact table to list every n ≤ 4·10⁸ with
δ(n) < 1, and compare with families 1–7.

## Further lower bounds from defect theory (RQ-3)

- Getting ‖N‖ ≥ 118 would need the classification of δ < 1.54. The paper only states δ < 1.286
  explicitly (Thm 5.1, which we've only read in summary). Altman (2016) gives a general method for any
  bound r, but that doesn't yield a human-checkable proof of ≥ 127.
- **Assessment:** defect theory gives a short, human-readable proof of ≥ 117, a useful second
  route. It can't realistically certify 127, which is 11.5 above the floor. The exhaustive search
  (with an independent replication and, ideally, a Lean-checked certificate) remains the main route.
