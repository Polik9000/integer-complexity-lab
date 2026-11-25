import IntegerComplexity.PoC.CheckerTrie  -- copy into lean/IntegerComplexity/PoC/ to build (benchmark only)

/-!
# Benchmark-only checker variant (NOT part of the soundness chain)

Each claim carries its list of divisors `d` with `2 ≤ d ≤ m/d`. The checker checks `d ∣ m` and the
LB condition for each, but does **not** prove that the list is complete. It has the same kernel cost
profile as the factorisation-based product rule (which would generate this list from a verified
factorisation), so it is used only to measure cost per split.
Also: a fuel-based binary modular exponentiation for Pratt/Lucas checks.
-/

namespace IntegerComplexity.Bench
open IntegerComplexity

def prodsList (lb : Nat → Nat) (m j : Nat) : List Nat → Bool
  | [] => true
  | d :: ds => (m % d == 0) && decide (j < lb d + lb (m / d)) && prodsList lb m j ds

def checkClaimH (lb : Nat → Nat) (m j : Nat) (ds : List Nat) : Bool :=
  decide (2 ≤ m) && (decide (3 ^ j < m ^ 3) || (sumsFrom lb m j 200 1 && prodsList lb m j ds))

def checkAllH : Trie → List (Nat × Nat × List Nat) → Bool
  | _, [] => true
  | t, (m, j, ds) :: rest => checkClaimH (lbT t) m j ds && checkAllH (Trie.insert 80 t m j m) rest

/-- `b ^ e % n` by binary exponentiation, structural recursion on `fuel` (number of bits). -/
def powModF (n : Nat) : Nat → Nat → Nat → Nat → Nat
  | 0, _, _, acc => acc
  | fuel + 1, b, e, acc =>
      if e = 0 then acc
      else powModF n fuel (b * b % n) (e / 2) (if e % 2 = 1 then acc * b % n else acc)

/-- Lucas test data `(p, a, qs)`: `a^(p-1) ≡ 1` and `a^((p-1)/q) ≢ 1` for each `q`, and the `q`s
    exhaust `p - 1` (cost model of one Pratt record; primality of the `q`s is checked elsewhere). -/
def divOut (q : Nat) : Nat → Nat → Nat
  | 0, r => r
  | f + 1, r => if r % q = 0 then divOut q f (r / q) else r

def lucasOK (p a : Nat) (qs : List Nat) : Bool :=
  decide (qs.foldl (fun r q => divOut q 64 r) (p - 1) = 1) &&
  powModF p 64 a (p - 1) 1 == 1 && qs.all (fun q => powModF p 64 a ((p - 1) / q) 1 != 1)

def lucasAll : List (Nat × Nat × List Nat) → Bool
  | [] => true
  | (p, a, qs) :: rest => lucasOK p a qs && lucasAll rest

end IntegerComplexity.Bench
