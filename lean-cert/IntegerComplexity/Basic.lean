/-!
# Integer complexity: core definitions

`‖n‖` is the least number of `1`s in an expression for `n` built from `1`, `+`, `*`
and parentheses. This file uses only core Lean (no Mathlib) so that it builds fast
and its trust base is small.

* `Expr`             — syntax of such expressions.
* `Expr.eval`, `Expr.ones` — value and number of ones.
* `UpperBound n k`   — some expression for `n` uses at most `k` ones (`‖n‖ ≤ k`).
* `LowerBound n k`   — every expression for `n` uses at least `k` ones (`k ≤ ‖n‖`).
* `HasComplexity n k` — both, i.e. `‖n‖ = k`.
-/

namespace IntegerComplexity

/-- Expressions built from `1` with `+` and `*`. -/
inductive Expr where
  | one : Expr
  | add : Expr → Expr → Expr
  | mul : Expr → Expr → Expr
  deriving Repr

namespace Expr

/-- The value of an expression. -/
def eval : Expr → Nat
  | one => 1
  | add a b => a.eval + b.eval
  | mul a b => a.eval * b.eval

/-- The number of `1`s in an expression. -/
def ones : Expr → Nat
  | one => 1
  | add a b => a.ones + b.ones
  | mul a b => a.ones + b.ones

theorem eval_pos (e : Expr) : 0 < e.eval := by
  induction e with
  | one => decide
  | add a b iha _ => simp only [eval]; omega
  | mul a b iha ihb => simp only [eval]; exact Nat.mul_pos iha ihb

theorem ones_pos (e : Expr) : 0 < e.ones := by
  induction e with
  | one => decide
  | add a b iha _ => simp only [ones]; omega
  | mul a b iha _ => simp only [ones]; omega

/-- `unary k` is `1 + 1 + ⋯ + 1` with `k + 1` ones. -/
def unary : Nat → Expr
  | 0 => one
  | k + 1 => add (unary k) one

theorem unary_eval (k : Nat) : (unary k).eval = k + 1 := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [unary, eval, ih]

theorem unary_ones (k : Nat) : (unary k).ones = k + 1 := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [unary, ones, ih]

end Expr

/-- `‖n‖ ≤ k`: some expression for `n` uses at most `k` ones. -/
def UpperBound (n k : Nat) : Prop := ∃ e : Expr, e.eval = n ∧ e.ones ≤ k

/-- `k ≤ ‖n‖`: every expression for `n` uses at least `k` ones. -/
def LowerBound (n k : Nat) : Prop := ∀ e : Expr, e.eval = n → k ≤ e.ones

/-- `‖n‖ = k`. -/
def HasComplexity (n k : Nat) : Prop := UpperBound n k ∧ LowerBound n k

/-- An explicit expression is a certificate for an upper bound. -/
theorem UpperBound.of_expr (e : Expr) : UpperBound e.eval e.ones := ⟨e, rfl, Nat.le_refl _⟩

/-- Trivial upper bound: `‖n‖ ≤ n` for `n ≥ 1`. -/
theorem upperBound_self {n : Nat} (h : 0 < n) : UpperBound n n :=
  ⟨Expr.unary (n - 1), by rw [Expr.unary_eval]; omega, by rw [Expr.unary_ones]; omega⟩

/-- Trivial lower bound: `1 ≤ ‖n‖`. -/
theorem lowerBound_one (n : Nat) : LowerBound n 1 := fun e _ => e.ones_pos

theorem UpperBound.mono {n k k' : Nat} (h : UpperBound n k) (hk : k ≤ k') : UpperBound n k' :=
  let ⟨e, he, hk'⟩ := h; ⟨e, he, Nat.le_trans hk' hk⟩

/-- Sub-additivity: `‖a + b‖ ≤ ‖a‖ + ‖b‖`. -/
theorem UpperBound.add {a b ka kb : Nat} (ha : UpperBound a ka) (hb : UpperBound b kb) :
    UpperBound (a + b) (ka + kb) :=
  let ⟨e, he, hk⟩ := ha; let ⟨f, hf, hl⟩ := hb
  ⟨.add e f, by simp only [Expr.eval, he, hf], by simp only [Expr.ones]; omega⟩

/-- Sub-multiplicativity: `‖a * b‖ ≤ ‖a‖ + ‖b‖`. -/
theorem UpperBound.mul {a b ka kb : Nat} (ha : UpperBound a ka) (hb : UpperBound b kb) :
    UpperBound (a * b) (ka + kb) :=
  let ⟨e, he, hk⟩ := ha; let ⟨f, hf, hl⟩ := hb
  ⟨.mul e f, by simp only [Expr.eval, he, hf], by simp only [Expr.ones]; omega⟩

end IntegerComplexity
