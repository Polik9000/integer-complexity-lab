import IntegerComplexity.PoC.Checker

/-!
# Certificate checker with a binary-trie store (`O(log m)` lookups)

Soundness does not depend on the trie being well-formed: every node stores its own key, a lookup
only returns a value from a node whose stored key equals the queried key, and the invariant is
simply "every stored entry is a true claim". A malformed trie can only make checking fail.
-/

namespace IntegerComplexity

inductive Trie where
  | leaf : Trie
  | node (k j : Nat) (l r : Trie) : Trie

namespace Trie

/-- Every stored entry `(k, j)` is a true claim `‖k‖ > j`. -/
def Valid : Trie → Prop
  | leaf => True
  | node k j l r => LowerBound k (j + 1) ∧ l.Valid ∧ r.Valid

/-- Lower bound for `v` stored in `t`; `rem` is the part of the key still to be walked (start: `v`). -/
def get : Trie → Nat → Nat → Nat
  | leaf, _, _ => 0
  | node k j l r, v, rem =>
      if rem ≤ 1 then (if k = v then j + 1 else 0)
      else if rem % 2 = 0 then get l v (rem / 2) else get r v (rem / 2)

theorem get_sound : ∀ (t : Trie) (v rem : Nat), t.Valid → LowerBound v (t.get v rem)
  | leaf, _, _, _ => fun e _ => Nat.zero_le _
  | node k j l r, v, rem, ⟨hk, hl, hr⟩ => by
      simp only [get]
      split
      · split
        · next h => subst h; exact hk
        · exact fun e _ => Nat.zero_le _
      · split
        · exact get_sound l v _ hl
        · exact get_sound r v _ hr

/-- Insert the claim `‖k‖ > j`. -/
def insert : Nat → Trie → Nat → Nat → Nat → Trie
  | 0, t, _, _, _ => t
  | f + 1, leaf, k, j, rem =>
      if rem ≤ 1 then node k j leaf leaf
      else if rem % 2 = 0 then node 0 0 (insert f leaf k j (rem / 2)) leaf
      else node 0 0 leaf (insert f leaf k j (rem / 2))
  | f + 1, node k' j' l r, k, j, rem =>
      if rem ≤ 1 then (if k' = k then node k (max j j') l r else node k j l r)
      else if rem % 2 = 0 then node k' j' (insert f l k j (rem / 2)) r
      else node k' j' l (insert f r k j (rem / 2))

theorem insert_valid : ∀ (f : Nat) (t : Trie) (k j rem : Nat), t.Valid → LowerBound k (j + 1) →
    (insert f t k j rem).Valid
  | 0, _, _, _, _, ht, _ => ht
  | f + 1, leaf, k, j, rem, _, hk => by
      simp only [insert]
      split
      · exact ⟨hk, trivial, trivial⟩
      · split
        · exact ⟨lowerBound_zero _, insert_valid f leaf k j _ trivial hk, trivial⟩
        · exact ⟨lowerBound_zero _, trivial, insert_valid f leaf k j _ trivial hk⟩
  | f + 1, node k' j' l r, k, j, rem, ⟨hk', hl, hr⟩, hk => by
      simp only [insert]
      split
      · split
        · next h =>
          subst h
          refine ⟨?_, hl, hr⟩
          intro e he
          have := hk e he; have := hk' e he
          simp only [Nat.max_def]; split <;> omega
        · exact ⟨hk, hl, hr⟩
      · split
        · exact ⟨hk', insert_valid f l k j _ hl hk, hr⟩
        · exact ⟨hk', hl, insert_valid f r k j _ hr hk⟩

end Trie

def lbT (t : Trie) (v : Nat) : Nat := selfLB v 200 (max 1 (t.get v v))

theorem lbT_sound (t : Trie) (h : t.Valid) (v : Nat) : LowerBound v (lbT t v) := by
  apply selfLB_sound
  intro e he
  exact Nat.max_le.mpr ⟨e.ones_pos, Trie.get_sound t v v h e he⟩

/-- Check claims in order, inserting each accepted claim into the trie. -/
def checkAllT (fuel : Nat) : Trie → List (Nat × Nat) → Bool
  | _, [] => true
  | t, (m, j) :: rest => checkClaim (lbT t) m j fuel && checkAllT fuel (Trie.insert 80 t m j m) rest

theorem checkAllT_sound (fuel : Nat) :
    ∀ t cert, t.Valid → checkAllT fuel t cert = true → Valid cert
  | _, [], _, _ => fun _ h => absurd h List.not_mem_nil
  | t, (m, j) :: rest, hv, h => by
      simp only [checkAllT, Bool.and_eq_true] at h
      have hc : LowerBound m (j + 1) :=
        checkClaim_sound _ m j fuel (fun v _ => lbT_sound t hv v) h.1
      have ih := checkAllT_sound fuel _ rest (Trie.insert_valid 80 t m j m hv hc) h.2
      intro p hp
      rcases List.mem_cons.mp hp with rfl | hp
      · exact hc
      · exact ih p hp

theorem lowerBound_of_checkT {cert : List (Nat × Nat)} {fuel n j : Nat}
    (hc : checkAllT fuel .leaf cert = true) (hmem : (n, j) ∈ cert) : LowerBound n (j + 1) :=
  checkAllT_sound fuel .leaf cert trivial hc (n, j) hmem

end IntegerComplexity
