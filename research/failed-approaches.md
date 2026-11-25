# Failed and abandoned approaches

Kept so nobody repeats them blindly. Newest at the bottom. Each entry gives the date, the approach,
what happened, why we think it failed, and what might still be worth trying.

## 2026-11-25: narrow peel searches stall at 127–129 (EXP-0001)

- **Approach:** n = d·m + r with small d (≤ 12…400) and small r (≤ 1…8), with an exact table to 4·10⁸.
- **Outcome:** best 127 (d ≤ 100, r ≤ 1). Wider r with small d was *worse* (129 with r ≤ 6, d ≤ 12),
  because the memo budget goes into useless branches.
- **Why:** this family only explores "multiply by small factor, add small r" chains, and the
  board's 127 lives in the same family.
- **Still worth trying (bounded):** use all divisors of n − r (factorize), allow two-term sums
  a·b + c·d with medium-size parts, and raise T to 4·10⁹.

## 2026-11-25: environment notes (not mathematical)

- `release.lean-lang.org` and `oeis.org` are blocked by the cloud sandbox's network policy.
  Lean was installed from the GitHub release zip instead, and the OEIS b-files are unavailable there.
