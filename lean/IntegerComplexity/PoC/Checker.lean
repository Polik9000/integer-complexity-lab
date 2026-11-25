import IntegerComplexity.PoC.Selfridge

/-!
# A Bool-valued lower-bound checker and its soundness (Theorem C)

* `theoremC`: the mathematical core. If every sum split inside the Selfridge cut-off and every
  divisor pair is refuted by a sound lower-bound function `lb`, then `LowerBound m (j+1)`, i.e. `‖m‖ > j`.
* `sumsFrom`, `prodsFrom`, `checkClaim`: executable (kernel-reducible, fuel-based) versions of the rules.
* `checkAll`: processes a list of claims `(m, j)` in order; each claim may use the earlier ones.
* `checkAll_sound`: `checkAll ... = true` implies every listed claim is true.

Products are enumerated here by trial division up to `√m` (fine for small `m`); the certificate
for `2^61 - 1` needs divisors generated from a verified prime factorisation instead (see report).
-/

namespace IntegerComplexity

/-- `LowerBound 0 k` holds vacuously (no expression has value 0). -/
theorem lowerBound_zero (k : Nat) : LowerBound 0 k := fun e he => absurd he (Nat.ne_of_gt e.eval_pos)

theorem LowerBound.mono {n k k' : Nat} (h : LowerBound n k) (hk : k' ≤ k) : LowerBound n k' :=
  fun e he => Nat.le_trans hk (h e he)

/-- Monotonicity of `x * (m - x)` on `x ≤ m / 2`, in subtraction-free form. -/
theorem mul_sub_mono {x0 x y : Nat} (h0 : x0 ≤ x) (hxy : x ≤ y) :
    x0 * (y + (x - x0)) ≤ x * y := by
  obtain ⟨k, rfl⟩ : ∃ k, x = x0 + k := ⟨x - x0, by omega⟩
  rw [show x0 + k - x0 = k by omega, Nat.mul_add, Nat.add_mul]
  have : x0 * k ≤ k * y := by
    rw [Nat.mul_comm]; exact Nat.mul_le_mul_left k (by omega)
  omega

/-! ## Theorem C -/

theorem theoremC (lb : Nat → Nat) (m j : Nat) (hm : 2 ≤ m)
    (hlb : ∀ v, v < m → LowerBound v (lb v))
    (hs : ∀ x, 1 ≤ x → 2 * x ≤ m → (x * (m - x)) ^ 3 ≤ 3 ^ j → j < lb x + lb (m - x))
    (hp : ∀ d, 2 ≤ d → d * d ≤ m → m % d = 0 → j < lb d + lb (m / d)) :
    LowerBound m (j + 1) := by
  intro e
  induction e with
  | one => intro h; simp only [Expr.eval] at h; omega
  | add a b _ _ =>
      intro h
      simp only [Expr.eval] at h
      simp only [Expr.ones]
      have pa := a.eval_pos; have pb := b.eval_pos
      -- the smaller summand is `x`
      have key : ∀ p q : Expr, p.eval + q.eval = m → p.eval ≤ q.eval → j < p.ones + q.ones := by
        intro p q hpq hle
        have pp := p.eval_pos; have pq := q.eval_pos
        by_cases hc : (p.eval * q.eval) ^ 3 ≤ 3 ^ j
        · have hmx : m - p.eval = q.eval := by omega
          have := hs p.eval pp (by omega) (by rw [hmx]; exact hc)
          rw [hmx] at this
          have l1 := hlb p.eval (by omega) p rfl
          have l2 := hlb q.eval (by omega) q rfl
          omega
        · exact ones_gt_of_prod_cube p q (Nat.lt_of_not_le hc)
      by_cases hab : a.eval ≤ b.eval
      · have := key a b h hab; omega
      · have := key b a (by omega) (by omega); omega
  | mul a b iha ihb =>
      intro h
      simp only [Expr.eval] at h
      simp only [Expr.ones]
      have pa := a.eval_pos; have pb := b.eval_pos
      by_cases ha1 : a.eval = 1
      · rw [ha1, Nat.one_mul] at h; have := ihb h; omega
      by_cases hb1 : b.eval = 1
      · rw [hb1, Nat.mul_one] at h; have := iha h; omega
      have key : ∀ p q : Expr, p.eval * q.eval = m → 2 ≤ p.eval → 2 ≤ q.eval →
          p.eval ≤ q.eval → j < p.ones + q.ones := by
        intro p q hpq h2p h2q hle
        have hpm : p.eval < m := by
          have : p.eval * 2 ≤ p.eval * q.eval := Nat.mul_le_mul_left _ h2q
          omega
        have hqm : q.eval < m := by
          have : 2 * q.eval ≤ p.eval * q.eval := Nat.mul_le_mul_right _ h2p
          omega
        have hsq : p.eval * p.eval ≤ m := hpq ▸ Nat.mul_le_mul_left _ hle
        have hmod : m % p.eval = 0 := by rw [← hpq]; exact Nat.mul_mod_right _ _
        have hdiv : m / p.eval = q.eval := by
          rw [← hpq]; exact Nat.mul_div_cancel_left _ (by omega)
        have := hp p.eval h2p hsq hmod
        rw [hdiv] at this
        have l1 := hlb p.eval hpm p rfl
        have l2 := hlb q.eval hqm q rfl
        omega
      by_cases hab : a.eval ≤ b.eval
      · have := key a b h (by omega) (by omega) hab; omega
      · have := key b a (by rw [Nat.mul_comm]; exact h) (by omega) (by omega) (by omega); omega

/-! ## Executable rules (structural recursion on fuel, so the kernel can evaluate them) -/

/-- Selfridge lower bound: the least `r ≥ start` with `v^3 ≤ 3^r`, searched with fuel. -/
def selfLB (v : Nat) : Nat → Nat → Nat
  | 0, r => r
  | fuel + 1, r => if 3 ^ r < v ^ 3 then selfLB v fuel (r + 1) else r

theorem selfLB_sound (v : Nat) : ∀ fuel r, LowerBound v r → LowerBound v (selfLB v fuel r)
  | 0, _, h => h
  | fuel + 1, r, h => by
      simp only [selfLB]
      split
      · exact selfLB_sound v fuel (r + 1) (lowerBound_of_cube (by assumption))
      · exact h

/-- Sum rule, for `x, x+1, …`: stops (successfully) at the first `x` outside the cut-off. -/
def sumsFrom (lb : Nat → Nat) (m j : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | fuel + 1, x =>
      if 2 * x ≤ m ∧ (x * (m - x)) ^ 3 ≤ 3 ^ j then
        decide (j < lb x + lb (m - x)) && sumsFrom lb m j fuel (x + 1)
      else true

theorem sumsFrom_sound (lb : Nat → Nat) (m j : Nat) :
    ∀ fuel x, sumsFrom lb m j fuel x = true →
      ∀ x', x ≤ x' → 2 * x' ≤ m → (x' * (m - x')) ^ 3 ≤ 3 ^ j → j < lb x' + lb (m - x')
  | 0, _, h => by simp [sumsFrom] at h
  | fuel + 1, x, h => by
      intro x' hx hx2 hc
      simp only [sumsFrom] at h
      split at h
      · next hin =>
        simp only [Bool.and_eq_true, decide_eq_true_eq] at h
        by_cases hxx : x' = x
        · subst hxx; exact h.1
        · exact sumsFrom_sound lb m j fuel (x + 1) h.2 x' (by omega) hx2 hc
      · next hout =>
        exfalso; apply hout
        refine ⟨by omega, ?_⟩
        -- monotonicity: x ≤ x' ≤ m - x'
        have hm : x * (m - x) ≤ x' * (m - x') := by
          have := mul_sub_mono (x0 := x) (x := x') (y := m - x') hx (by omega)
          rwa [show m - x' + (x' - x) = m - x by omega] at this
        exact Nat.le_trans (Nat.pow_le_pow_left hm 3) hc

/-- Product rule by trial division: every `d ≥ start` with `d*d ≤ m`, `d ∣ m`. -/
def prodsFrom (lb : Nat → Nat) (m j : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | fuel + 1, d =>
      if d * d ≤ m then
        (m % d != 0 || decide (j < lb d + lb (m / d))) && prodsFrom lb m j fuel (d + 1)
      else true

theorem prodsFrom_sound (lb : Nat → Nat) (m j : Nat) :
    ∀ fuel d, prodsFrom lb m j fuel d = true →
      ∀ d', d ≤ d' → d' * d' ≤ m → m % d' = 0 → j < lb d' + lb (m / d')
  | 0, _, h => by simp [prodsFrom] at h
  | fuel + 1, d, h => by
      intro d' hd hsq hmod
      simp only [prodsFrom] at h
      split at h
      · simp only [Bool.and_eq_true, Bool.or_eq_true, bne_iff_ne, ne_eq, decide_eq_true_eq] at h
        by_cases hdd : d' = d
        · subst hdd
          rcases h.1 with h1 | h1
          · exact absurd hmod h1
          · exact h1
        · exact prodsFrom_sound lb m j fuel (d + 1) h.2 d' (by omega) hsq hmod
      · next hout =>
        exfalso; apply hout
        exact Nat.le_trans (Nat.mul_le_mul hd hd) hsq

/-- One claim `‖m‖ > j`: Selfridge alone, or all splits refuted. -/
def checkClaim (lb : Nat → Nat) (m j fuel : Nat) : Bool :=
  decide (2 ≤ m) && (decide (3 ^ j < m ^ 3) ||
    (sumsFrom lb m j fuel 1 && prodsFrom lb m j fuel 2))

theorem checkClaim_sound (lb : Nat → Nat) (m j fuel : Nat)
    (hlb : ∀ v, v < m → LowerBound v (lb v)) (h : checkClaim lb m j fuel = true) :
    LowerBound m (j + 1) := by
  simp only [checkClaim, Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq] at h
  obtain ⟨hm, h | ⟨hs, hp⟩⟩ := h
  · exact lowerBound_of_cube h
  · exact theoremC lb m j hm hlb
      (fun x hx => sumsFrom_sound lb m j fuel 1 hs x hx)
      (fun d hd => prodsFrom_sound lb m j fuel 2 hp d hd)

/-! ## The certificate checker -/

/-- Facts proven so far, as an association list `(m, j)` meaning `‖m‖ > j`. -/
def Valid (proven : List (Nat × Nat)) : Prop := ∀ p ∈ proven, LowerBound p.1 (p.2 + 1)

/-- Best stored bound for `v` (`0` if none). -/
def lookup (v : Nat) : List (Nat × Nat) → Nat
  | [] => 0
  | p :: ps => if p.1 = v then max (p.2 + 1) (lookup v ps) else lookup v ps

theorem lookup_sound (v : Nat) : ∀ ps, Valid ps → LowerBound v (lookup v ps)
  | [], _ => fun e _ => Nat.zero_le _
  | p :: ps, h => by
      have hrest : Valid ps := fun q hq => h q (List.mem_cons_of_mem _ hq)
      simp only [lookup]
      split
      · next he =>
        have hp := h p List.mem_cons_self
        rw [he] at hp
        intro e hev
        exact Nat.max_le.mpr ⟨hp e hev, lookup_sound v ps hrest e hev⟩
      · exact lookup_sound v ps hrest

/-- The lower-bound function used by the checker. Selfridge search starts from the stored bound. -/
def lbOf (proven : List (Nat × Nat)) (v : Nat) : Nat := selfLB v 200 (max 1 (lookup v proven))

theorem lbOf_sound (proven : List (Nat × Nat)) (h : Valid proven) (v : Nat) :
    LowerBound v (lbOf proven v) := by
  apply selfLB_sound
  intro e he
  exact Nat.max_le.mpr ⟨e.ones_pos, lookup_sound v proven h e he⟩

def checkAll (fuel : Nat) : List (Nat × Nat) → List (Nat × Nat) → Bool
  | _, [] => true
  | proven, (m, j) :: rest => checkClaim (lbOf proven) m j fuel && checkAll fuel ((m, j) :: proven) rest

theorem checkAll_sound (fuel : Nat) :
    ∀ proven cert, Valid proven → checkAll fuel proven cert = true → Valid cert
  | _, [], _, _ => fun _ h => absurd h List.not_mem_nil
  | proven, (m, j) :: rest, hv, h => by
      simp only [checkAll, Bool.and_eq_true] at h
      have hc : LowerBound m (j + 1) :=
        checkClaim_sound _ m j fuel (fun v _ => lbOf_sound proven hv v) h.1
      have hv' : Valid ((m, j) :: proven) := by
        intro p hp
        rcases List.mem_cons.mp hp with rfl | hp
        · exact hc
        · exact hv p hp
      have ih := checkAll_sound fuel _ rest hv' h.2
      intro p hp
      rcases List.mem_cons.mp hp with rfl | hp
      · exact hc
      · exact ih p hp

/-- Headline soundness: a certificate that checks proves every claim in it. -/
theorem lowerBound_of_check {cert : List (Nat × Nat)} {fuel n j : Nat}
    (hc : checkAll fuel [] cert = true) (hmem : (n, j) ∈ cert) : LowerBound n (j + 1) :=
  checkAll_sound fuel [] cert (fun _ h => absurd h List.not_mem_nil) hc (n, j) hmem

end IntegerComplexity
