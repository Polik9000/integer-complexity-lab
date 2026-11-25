import ICLCertCore
import IntegerComplexity.PoC.Checker
import Mathlib.NumberTheory.LucasPrimality

/-!
# Soundness of the certificate checker `ICLCert.checkCert`

Main theorem:

  `checkCert_sound : checkCert N B chunks = true → IntegerComplexity.LowerBound N B`

for **every** `N B : ℕ` and **every** list of record chunks. Nothing about the records (their
origin, the parser, the generator, the order) is assumed. The proof uses the repository's
`theoremC`, `sumsFrom_sound` and `lowerBound_of_cube` (`IntegerComplexity.PoC.*`, copied unchanged)
and Mathlib for primality (`lucas_primality`) and divisibility.
-/

namespace ICLCert
open IntegerComplexity

/-! ## Trie invariant -/

namespace Trie

def Valid (P : Nat → Nat → Prop) : Trie → Prop
  | leaf => True
  | node e l r => (∀ k v, e = some (k, v) → P k v) ∧ Valid P l ∧ Valid P r

theorem find?_sound {P : Nat → Nat → Prop} :
    ∀ (t : Trie) (key rem v : Nat), t.Valid P → t.find? key rem = some v → P key v
  | leaf, _, _, _, _, h => by simp [find?] at h
  | node e l r, key, rem, v, ⟨he, hl, hr⟩, h => by
    simp only [find?] at h
    split at h
    · rcases e with _ | ⟨k, v'⟩
      · simp at h
      · simp only at h
        split at h
        · next hk => subst hk; cases h; exact he _ _ rfl
        · simp at h
    · split at h
      · exact find?_sound l key _ v hl h
      · exact find?_sound r key _ v hr h

theorem insert_valid {P : Nat → Nat → Prop} (comb : Nat → Nat → Nat)
    (hcomb : ∀ k v' v, P k v' → P k v → P k (comb v' v)) :
    ∀ (f : Nat) (t : Trie) (key v rem : Nat), t.Valid P → P key v →
      (insert comb f t key v rem).Valid P
  | 0, _, _, _, _, ht, _ => ht
  | f + 1, leaf, key, v, rem, _, hk => by
    simp only [insert]
    split
    · exact ⟨(fun k v' h => by cases h; exact hk), trivial, trivial⟩
    · split
      · exact ⟨(fun _ _ h => by cases h), insert_valid comb hcomb f leaf key v _ trivial hk, trivial⟩
      · exact ⟨(fun _ _ h => by cases h), trivial, insert_valid comb hcomb f leaf key v _ trivial hk⟩
  | f + 1, node e l r, key, v, rem, ⟨he, hl, hr⟩, hk => by
    simp only [insert]
    split
    · rcases e with _ | ⟨k', v'⟩
      · exact ⟨(fun _ _ h => by cases h; exact hk), hl, hr⟩
      · simp only
        split
        · next hkk =>
          subst hkk
          exact ⟨(fun _ _ h => by cases h; exact hcomb _ _ _ (he _ _ rfl) hk), hl, hr⟩
        · exact ⟨(fun _ _ h => by cases h; exact hk), hl, hr⟩
    · split
      · exact ⟨he, insert_valid comb hcomb f l key v _ hl hk, hr⟩
      · exact ⟨he, hl, insert_valid comb hcomb f r key v _ hr hk⟩

end Trie

/-- Invariant of the claims trie: every entry `(m, j)` is a true claim `‖m‖ > j`. -/
def ClaimP (k j : Nat) : Prop := LowerBound k (j + 1)

/-- Invariant of the primes trie: every key is prime. -/
def PrimeP (k _ : Nat) : Prop := k.Prime

/-! ## Lower-bound function -/

theorem LowerBound.max {n a b : Nat} (ha : LowerBound n a) (hb : LowerBound n b) :
    LowerBound n (max a b) :=
  fun e he => Nat.max_le.mpr ⟨ha e he, hb e he⟩

theorem selfFrom_sound (v : Nat) :
    ∀ f r, LowerBound v r → LowerBound v (selfFrom (v ^ 3) f r)
  | 0, _, h => h
  | f + 1, r, h => by
    simp only [selfFrom]
    split
    · exact selfFrom_sound v f (r + 1) (lowerBound_of_cube (by assumption))
    · exact h

theorem lb_sound {claims : Trie} (hc : claims.Valid ClaimP) (v : Nat) :
    LowerBound v (lb claims v) := by
  unfold lb
  apply selfFrom_sound
  apply LowerBound.max (lowerBound_one v)
  split
  · next j hj => exact Trie.find?_sound claims v v j hc hj
  · exact fun _ _ => Nat.zero_le _

/-! ## Sum rule: reduces to the repository's `sumsFrom` -/

theorem sumsLoop_eq (claims : Trie) (m j : Nat) :
    ∀ f x, sumsLoop claims m j (3 ^ j) f x = sumsFrom (lb claims) m j f x
  | 0, _ => rfl
  | f + 1, x => by
    simp only [sumsLoop, sumsFrom, sumsLoop_eq claims m j f (x + 1)]

/-! ## Product rule: completeness of the divisor list -/

theorem mem_powers (p : Nat) : ∀ e a, a ≤ e → p ^ a ∈ powers p e
  | 0, a, h => by simp [Nat.le_zero.mp h, powers]
  | e + 1, 0, _ => by simp [powers]
  | e + 1, a + 1, h => by
    simp only [powers, List.mem_cons, List.mem_map]
    right
    exact ⟨p ^ a, mem_powers p e a (by omega), by rw [Nat.pow_succ, Nat.mul_comm]⟩

/-- **Divisor completeness**: if every `p` in `f` is prime, every divisor of `∏ p^e` is listed. -/
theorem mem_divisorsOf : ∀ (f : List (Nat × Nat)), (∀ pe ∈ f, pe.1.Prime) →
    ∀ d, d ∣ fprod f → d ∈ divisorsOf f
  | [], _, d, hd => by simp [fprod] at hd; simp [divisorsOf, hd]
  | (p, e) :: rest, hp, d, hd => by
    simp only [fprod] at hd
    obtain ⟨d1, d2, h1, h2, rfl⟩ := Nat.dvd_mul.mp hd
    have pp : p.Prime := hp (p, e) List.mem_cons_self
    obtain ⟨a, ha, rfl⟩ := (Nat.dvd_prime_pow pp).mp h1
    have ih := mem_divisorsOf rest (fun pe h => hp pe (List.mem_cons_of_mem _ h)) d2 h2
    simp only [divisorsOf, List.mem_flatMap, List.mem_map]
    exact ⟨p ^ a, mem_powers p e a ha, d2, ih, rfl⟩

theorem prodsOK_sound {claims : Trie} {m j : Nat} {f : List (Nat × Nat)}
    (hf : ∀ pe ∈ f, pe.1.Prime) (hm : fprod f = m) (h : prodsOK claims m j f = true) :
    ∀ d, 2 ≤ d → d * d ≤ m → m % d = 0 → j < lb claims d + lb claims (m / d) := by
  intro d h2 hsq hmod
  have hmem : d ∈ divisorsOf f := mem_divisorsOf f hf d (hm ▸ Nat.dvd_of_mod_eq_zero hmod)
  unfold prodsOK at h
  have := List.all_eq_true.mp h d hmem
  simp only [Bool.or_eq_true, Bool.not_eq_true', Bool.and_eq_false_iff, decide_eq_false_iff_not,
    decide_eq_true_eq] at this
  rcases this with (h' | h') | h'
  · omega
  · omega
  · exact h'

/-! ## Primality -/

theorem tdLoop_sound (n : Nat) :
    ∀ f d, tdLoop n f d = true → ∀ d', d ≤ d' → d' * d' ≤ n → n % d' ≠ 0
  | 0, _, h => by simp [tdLoop] at h
  | f + 1, d, h => by
    intro d' hd hsq
    simp only [tdLoop] at h
    split at h
    · simp only [Bool.and_eq_true, bne_iff_ne, ne_eq] at h
      by_cases hdd : d' = d
      · subst hdd; exact h.1
      · exact tdLoop_sound n f (d + 1) h.2 d' (by omega) hsq
    · next hout => exact absurd (Nat.le_trans (Nat.mul_le_mul hd hd) hsq) hout

theorem tdPrime_sound {n : Nat} (h : tdPrime n = true) : n.Prime := by
  simp only [tdPrime, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨h2, ht⟩ := h
  by_contra hnp
  have hmp : (Nat.minFac n).Prime := Nat.minFac_prime (by omega)
  have hsq := Nat.minFac_sq_le_self (by omega) hnp
  have := tdLoop_sound n n 2 ht (Nat.minFac n) hmp.two_le (by rw [← Nat.pow_two]; exact hsq)
  exact this (Nat.mod_eq_zero_of_dvd (Nat.minFac_dvd n))

theorem primeK_sound {primes : Trie} (hp : primes.Valid PrimeP) {q : Nat}
    (h : primeK primes q = true) : q.Prime := by
  simp only [primeK, Bool.or_eq_true, Option.isSome_iff_exists, Bool.and_eq_true,
    decide_eq_true_eq] at h
  rcases h with ⟨v, hv⟩ | ⟨_, ht⟩
  · exact Trie.find?_sound primes q q v hp hv
  · exact tdPrime_sound ht

theorem strip_dvd {r q : Nat} (hr : r.Prime) (hq : q.Prime) (hrq : r ≠ q) :
    ∀ f n, r ∣ n → r ∣ strip f n q
  | 0, _, h => h
  | f + 1, n, h => by
    simp only [strip]
    split
    · next hc =>
      apply strip_dvd hr hq hrq f
      have hn : n = q * (n / q) := (Nat.mul_div_cancel' (Nat.dvd_of_mod_eq_zero hc.2.2)).symm
      rw [hn] at h
      rcases (Nat.Prime.dvd_mul hr).mp h with h' | h'
      · rcases (Nat.dvd_prime hq).mp h' with h'' | h''
        · exact absurd h'' hr.one_lt.ne'
        · exact absurd h'' hrq
      · exact h'
    · exact h

theorem stripAll_sound {r : Nat} (hr : r.Prime) :
    ∀ (qs : List Nat) n, (∀ q ∈ qs, q.Prime) → r ∣ n → stripAll n qs = 1 → r ∈ qs
  | [], n, _, hd, h => by
    simp only [stripAll] at h; subst h
    exact absurd (Nat.le_of_dvd Nat.one_pos hd) (by have := hr.two_le; omega)
  | q :: qs, n, hq, hd, h => by
    by_cases hrq : r = q
    · subst hrq; exact List.mem_cons_self
    · simp only [stripAll] at h
      exact List.mem_cons_of_mem _ (stripAll_sound hr qs _ (fun q' h' => hq q' (List.mem_cons_of_mem _ h'))
        (strip_dvd hr (hq q List.mem_cons_self) hrq 128 n hd) h)

theorem powModAux_eq : ∀ f acc b e m, powModAux f acc b e m = acc * b ^ e % m
  | 0, _, _, _, _ => rfl
  | f + 1, acc, b, e, m => by
    simp only [powModAux]
    split
    · next he => subst he; simp
    · rw [powModAux_eq f]
      show _ ≡ _ [MOD m]
      have h1 : (if e % 2 = 1 then acc * b % m else acc) ≡ acc * b ^ (e % 2) [MOD m] := by
        split
        · next h => rw [h, pow_one]; exact Nat.mod_modEq _ _
        · next h => rw [show e % 2 = 0 by omega, pow_zero, mul_one]
      have h2 : (b * b % m) ^ (e / 2) ≡ b ^ (2 * (e / 2)) [MOD m] := by
        rw [pow_mul, ← pow_two, sq]; exact (Nat.mod_modEq _ _).pow _
      calc _ ≡ acc * b ^ (e % 2) * b ^ (2 * (e / 2)) [MOD m] := h1.mul h2
        _ = acc * b ^ e := by rw [mul_assoc, ← pow_add, Nat.mod_add_div]

theorem powMod_eq (b e m : Nat) : powMod b e m = b ^ e % m := by
  simp [powMod, powModAux_eq]

/-- `(a : ZMod p) ^ k = 1 ↔ a ^ k % p = 1` for `p ≥ 2`. -/
theorem zmod_pow_eq_one_iff {p : Nat} (hp : 2 ≤ p) (a k : Nat) :
    ((a : ZMod p) ^ k = 1) ↔ a ^ k % p = 1 := by
  rw [← Nat.cast_pow, ← Nat.cast_one, ZMod.natCast_eq_natCast_iff', Nat.mod_eq_of_lt (by omega : 1 < p)]

/-- **Pratt/Lucas soundness.** -/
theorem prattOK_sound {primes : Trie} (hv : primes.Valid PrimeP) {p a : Nat} {qs : List Nat}
    (h : prattOK primes p a qs = true) : p.Prime := by
  unfold prattOK at h
  split at h
  · exact tdPrime_sound h
  · next hbig =>
    simp only [Bool.and_eq_true, List.all_eq_true, beq_iff_eq, bne_iff_ne, ne_eq] at h
    obtain ⟨⟨⟨⟨_, hq⟩, hstrip⟩, hpow⟩, hnot⟩ := h
    have hp2 : 2 ≤ p := by simp only [smallBound] at hbig; omega
    have hqp : ∀ q ∈ qs, q.Prime := fun q hq' => primeK_sound hv (hq q hq')
    apply lucas_primality p (a : ZMod p)
    · rw [zmod_pow_eq_one_iff hp2, ← powMod_eq]; exact hpow
    · intro q hqprime hqdvd
      have hmem := stripAll_sound hqprime qs (p - 1) hqp hqdvd hstrip
      rw [Ne, zmod_pow_eq_one_iff hp2, ← powMod_eq]
      exact hnot q hmem

/-! ## Claims -/

theorem fprod_mem_prime {primes : Trie} (hv : primes.Valid PrimeP) {f : List (Nat × Nat)}
    (h : f.all (fun pe => primeK primes pe.1) = true) : ∀ pe ∈ f, pe.1.Prime :=
  fun pe hpe => primeK_sound hv (List.all_eq_true.mp h pe hpe)

theorem claimOK_sound {claims primes : Trie} (hc : claims.Valid ClaimP) (hp : primes.Valid PrimeP)
    {m j : Nat} {f : List (Nat × Nat)} (h : claimOK claims primes m j f = true) :
    LowerBound m (j + 1) := by
  unfold claimOK at h
  simp only [Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq, beq_iff_eq] at h
  obtain ⟨⟨⟨⟨hm, _⟩, hall⟩, hprod⟩, hrest⟩ := h
  rcases hrest with hcube | ⟨hs, hpr⟩
  · exact lowerBound_of_cube hcube
  · apply theoremC (lb claims) m j hm (fun v _ => lb_sound hc v)
    · rw [sumsLoop_eq] at hs
      exact fun x hx => sumsFrom_sound (lb claims) m j m 1 hs x hx
    · exact prodsOK_sound (fprod_mem_prime hp hall) hprod hpr

/-! ## The streaming checker -/

def State.Valid (st : State) : Prop := st.claims.Valid ClaimP ∧ st.primes.Valid PrimeP

theorem step_valid {st st' : State} {r : Rec} (hv : st.Valid) (h : step st r = some st') :
    st'.Valid := by
  obtain ⟨hc, hp⟩ := hv
  cases r with
  | prime p a qs =>
    simp only [step] at h
    split at h
    · next hok =>
      cases h
      refine ⟨hc, Trie.insert_valid _ (fun _ _ _ _ h => h) _ _ _ _ _ hp (prattOK_sound hp hok)⟩
    · cases h
  | claim m j f =>
    simp only [step] at h
    split at h
    · next hok =>
      cases h
      refine ⟨Trie.insert_valid max ?_ _ _ _ _ _ hc (claimOK_sound hc hp hok), hp⟩
      intro k v' v h1 h2 e he
      have := h1 e he; have := h2 e he
      show max v' v + 1 ≤ e.ones
      omega
    · cases h

theorem run_valid : ∀ (st : State) (rs : List Rec) {st' : State}, st.Valid → run st rs = some st' →
    st'.Valid
  | st, [], _, hv, h => by simp only [run] at h; cases h; exact hv
  | st, r :: rs, _, hv, h => by
    simp only [run] at h
    split at h
    · next st1 h1 => exact run_valid st1 rs (step_valid hv h1) h
    · cases h

theorem runChunks_valid : ∀ (st : State) (cs : List (List Rec)) {st' : State}, st.Valid →
    runChunks st cs = some st' → st'.Valid
  | st, [], _, hv, h => by simp only [runChunks] at h; cases h; exact hv
  | st, c :: cs, _, hv, h => by
    simp only [runChunks] at h
    split at h
    · next st1 h1 => exact runChunks_valid st1 cs (run_valid st c hv h1) h
    · cases h

/-- **Soundness of the checker**, for every target `N`, bound `B` and every input. -/
theorem checkCert_sound {N B : Nat} {chunks : List (List Rec)} (h : checkCert N B chunks = true) :
    LowerBound N B := by
  unfold checkCert at h
  split at h
  · next st hst =>
    have hv := runChunks_valid State.init chunks ⟨trivial, trivial⟩ hst
    exact LowerBound.mono (lb_sound hv.1 N) (of_decide_eq_true h)
  · cases h

end ICLCert
