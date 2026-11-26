import IntegerComplexity.Basic

/-!
# Selfridge's bound  `e.eval ^ 3 ≤ 3 ^ e.ones`

`emax k` is the largest value of an expression with `k` ones (we only prove it is an upper bound):
`emax 1 = 1, emax 2 = 2, emax 3 = 3, emax 4 = 4`, and `emax (k+3) = 3 * emax k` for `k ≥ 2`.
-/

namespace IntegerComplexity

/-- E(k): 1, 2, 3, 4, 6, 9, 12, 18, 27, 36, ... (`emax 0 = 1` is a dummy value). -/
def emax : Nat → Nat
  | 0 => 1
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | n + 5 => 3 * emax (n + 2)

theorem emax_ge_two : ∀ k, 2 ≤ k → 2 ≤ emax k
  | 0, h => absurd h (by decide)
  | 1, h => absurd h (by decide)
  | 2, _ => by decide
  | 3, _ => by decide
  | 4, _ => by decide
  | n + 5, _ => by
      have := emax_ge_two (n + 2) (by omega)
      simp only [emax]; omega

theorem emax_pos (k : Nat) : 1 ≤ emax k := by
  match k with
  | 0 => decide
  | 1 => decide
  | k + 2 => have := emax_ge_two (k + 2) (by omega); omega

/-- Strict monotonicity: `E(k) + 1 ≤ E(k+1)` for `k ≥ 1`. -/
theorem emax_succ : ∀ k, 1 ≤ k → emax k + 1 ≤ emax (k + 1)
  | 0, h => absurd h (by decide)
  | 1, _ => by decide
  | 2, _ => by decide
  | 3, _ => by decide
  | 4, _ => by decide
  | n + 5, _ => by
      have : emax (n + 2) + 1 ≤ emax (n + 3) := emax_succ (n + 2) (by omega)
      show 3 * emax (n + 2) + 1 ≤ 3 * emax (n + 3)
      omega

/-- `E(i) * E(j) ≤ E(i + j)` for `i, j ≥ 1`. -/
theorem emax_mul : ∀ i j, 1 ≤ i → 1 ≤ j → emax i * emax j ≤ emax (i + j)
  | n + 5, j, _, hj => by
      have ih := emax_mul (n + 2) j (by omega) hj
      have e1 : emax (n + 5) = 3 * emax (n + 2) := rfl
      have e2 : emax (n + 5 + j) = 3 * emax (n + 2 + j) := by
        have : n + 5 + j = (n + j) + 5 := by omega
        rw [this]; show 3 * emax (n + j + 2) = _
        rw [show n + j + 2 = n + 2 + j by omega]
      rw [e1, e2, Nat.mul_assoc]
      exact Nat.mul_le_mul_left 3 ih
  | i, n + 5, hi, _ => by
      have ih := emax_mul i (n + 2) hi (by omega)
      have e1 : emax (n + 5) = 3 * emax (n + 2) := rfl
      have e2 : emax (i + (n + 5)) = 3 * emax (i + (n + 2)) := by
        have : i + (n + 5) = (i + n) + 5 := by omega
        rw [this]; show 3 * emax (i + n + 2) = _
        rw [show i + n + 2 = i + (n + 2) by omega]
      rw [e1, e2, Nat.mul_left_comm]
      exact Nat.mul_le_mul_left 3 ih
  | 0, _, h, _ => absurd h (by decide)
  | _, 0, _, h => absurd h (by decide)
  | 1, 1, _, _ => by decide
  | 1, 2, _, _ => by decide
  | 1, 3, _, _ => by decide
  | 1, 4, _, _ => by decide
  | 2, 1, _, _ => by decide
  | 2, 2, _, _ => by decide
  | 2, 3, _, _ => by decide
  | 2, 4, _, _ => by decide
  | 3, 1, _, _ => by decide
  | 3, 2, _, _ => by decide
  | 3, 3, _, _ => by decide
  | 3, 4, _, _ => by decide
  | 4, 1, _, _ => by decide
  | 4, 2, _, _ => by decide
  | 4, 3, _, _ => by decide
  | 4, 4, _, _ => by decide
termination_by i j => i + j

/-- `x + y ≤ x * y` for `x, y ≥ 2`. -/
theorem add_le_mul_of_two_le {x y : Nat} (hx : 2 ≤ x) (hy : 2 ≤ y) : x + y ≤ x * y := by
  have h1 : 2 * y ≤ x * y := Nat.mul_le_mul_right y hx
  have h2 : 2 * x ≤ y * x := Nat.mul_le_mul_right x hy
  rw [Nat.mul_comm y x] at h2
  omega

/-- `E(i) + E(j) ≤ E(i + j)` for `i, j ≥ 1`. -/
theorem emax_add (i j : Nat) (hi : 1 ≤ i) (hj : 1 ≤ j) : emax i + emax j ≤ emax (i + j) := by
  by_cases h1 : i = 1
  · subst h1
    have := emax_succ j hj
    rw [Nat.add_comm 1 j]; show 1 + emax j ≤ _; omega
  by_cases h2 : j = 1
  · subst h2
    have := emax_succ i hi
    show emax i + 1 ≤ _; omega
  have a := emax_ge_two i (by omega)
  have b := emax_ge_two j (by omega)
  exact Nat.le_trans (add_le_mul_of_two_le a b) (emax_mul i j hi hj)

/-- Every expression with `k` ones has value at most `E(k)`. -/
theorem Expr.eval_le_emax (e : Expr) : e.eval ≤ emax e.ones := by
  induction e with
  | one => decide
  | add a b iha ihb =>
      simp only [Expr.eval, Expr.ones]
      exact Nat.le_trans (Nat.add_le_add iha ihb) (emax_add _ _ a.ones_pos b.ones_pos)
  | mul a b iha ihb =>
      simp only [Expr.eval, Expr.ones]
      exact Nat.le_trans (Nat.mul_le_mul iha ihb) (emax_mul _ _ a.ones_pos b.ones_pos)

/-- `E(k)^3 ≤ 3^k`. -/
theorem emax_cube : ∀ k, emax k ^ 3 ≤ 3 ^ k
  | 0 => by decide
  | 1 => by decide
  | 2 => by decide
  | 3 => by decide
  | 4 => by decide
  | n + 5 => by
      have ih := emax_cube (n + 2)
      show (3 * emax (n + 2)) ^ 3 ≤ 3 ^ (n + 2 + 3)
      rw [Nat.mul_pow, Nat.pow_add, Nat.mul_comm (3 ^ (n + 2))]
      exact Nat.mul_le_mul_left _ ih

/-- **Selfridge's bound** (integer form of `‖n‖ ≥ 3 log₃ n`). -/
theorem Expr.selfridge (e : Expr) : e.eval ^ 3 ≤ 3 ^ e.ones :=
  Nat.le_trans (Nat.pow_le_pow_left e.eval_le_emax 3) (emax_cube _)

/-- If `3^j < m^3` then `‖m‖ > j`. -/
theorem lowerBound_of_cube {m j : Nat} (h : 3 ^ j < m ^ 3) : LowerBound m (j + 1) := by
  intro e he
  apply Nat.lt_of_not_le
  intro hle
  have h1 := e.selfridge
  rw [he] at h1
  have h2 : 3 ^ e.ones ≤ 3 ^ j := Nat.pow_le_pow_right (by decide) hle
  omega

/-- Sum cut-off (Fact S): an expression `a + b` with `(a.eval * b.eval)^3 > 3^j` has more than `j` ones. -/
theorem ones_gt_of_prod_cube (a b : Expr) {j : Nat} (h : 3 ^ j < (a.eval * b.eval) ^ 3) :
    j < a.ones + b.ones := by
  apply Nat.lt_of_not_le
  intro hle
  have h1 : (a.eval * b.eval) ^ 3 ≤ 3 ^ (a.ones + b.ones) := by
    rw [Nat.mul_pow, Nat.pow_add]; exact Nat.mul_le_mul a.selfridge b.selfridge
  have h2 : 3 ^ (a.ones + b.ones) ≤ 3 ^ j := Nat.pow_le_pow_right (by decide) hle
  omega

end IntegerComplexity
