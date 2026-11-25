/-!
# ICLCertCore — the executable lower-bound certificate checker (no imports beyond `Init`)

This module contains only *definitions*. Their soundness is proved in `ICLCert.Sound`
(which imports Mathlib). Keeping the executable part free of Mathlib lets Lake precompile it
(`precompileModules = true`), so `native_decide` runs it as native code.

Everything here is total and defined by structural recursion on explicit fuel, so the kernel can
also evaluate it (`decide +kernel`) on small certificates. Insufficient fuel can only make a check
*fail*; it never makes a false claim pass (see the soundness proofs).

Semantics follow `research/2026-11-25-certificate-architecture.md` §5 with table size `T = 1`
(no table: `LB(v) = max(1, λ(v), proven(v) + 1)`).
-/

namespace ICLCert

/-! ## A binary trie keyed by `Nat`. Every node stores its own key, so a malformed trie can only
make lookups fail. -/

inductive Trie where
  | leaf : Trie
  | node (e : Option (Nat × Nat)) (l r : Trie) : Trie

namespace Trie

/-- Look up `key`; `rem` is the part of the key still to be walked (start with `rem = key`). -/
def find? : Trie → Nat → Nat → Option Nat
  | leaf, _, _ => none
  | node e l r, key, rem =>
    if rem ≤ 1 then
      match e with
      | some (k, v) => if k = key then some v else none
      | none => none
    else if rem % 2 = 0 then find? l key (rem / 2) else find? r key (rem / 2)

/-- Insert `(key, v)`; if `key` is already stored with value `v'`, store `comb v' v`. -/
def insert (comb : Nat → Nat → Nat) : Nat → Trie → Nat → Nat → Nat → Trie
  | 0, t, _, _, _ => t
  | f + 1, leaf, key, v, rem =>
    if rem ≤ 1 then node (some (key, v)) leaf leaf
    else if rem % 2 = 0 then node none (insert comb f leaf key v (rem / 2)) leaf
    else node none leaf (insert comb f leaf key v (rem / 2))
  | f + 1, node e l r, key, v, rem =>
    if rem ≤ 1 then
      match e with
      | some (k, v') => if k = key then node (some (key, comb v' v)) l r else node (some (key, v)) l r
      | none => node (some (key, v)) l r
    else if rem % 2 = 0 then node e (insert comb f l key v (rem / 2)) r
    else node e l (insert comb f r key v (rem / 2))

end Trie

/-! ## Arithmetic helpers -/

/-- `powModAux fuel acc b e m = acc * b ^ e % m` (binary exponentiation; correct for any fuel). -/
def powModAux : Nat → Nat → Nat → Nat → Nat → Nat
  | 0, acc, b, e, m => acc * b ^ e % m
  | f + 1, acc, b, e, m =>
    if e = 0 then acc % m
    else powModAux f (if e % 2 = 1 then acc * b % m else acc) (b * b % m) (e / 2) m

/-- `powMod b e m = b ^ e % m`. -/
def powMod (b e m : Nat) : Nat := powModAux 128 1 b e m

/-- Trial division: no `d` with `start ≤ d`, `d * d ≤ n` divides `n`. -/
def tdLoop (n : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | f + 1, d => if d * d ≤ n then (n % d != 0) && tdLoop n f (d + 1) else true

/-- Primality by trial division (used only below `2^16`). -/
def tdPrime (n : Nat) : Bool := decide (2 ≤ n) && tdLoop n n 2

/-- Divide out all factors `q` from `n`. -/
def strip : Nat → Nat → Nat → Nat
  | 0, n, _ => n
  | f + 1, n, q => if 2 ≤ q ∧ 0 < n ∧ n % q = 0 then strip f (n / q) q else n

def stripAll (n : Nat) : List Nat → Nat
  | [] => n
  | q :: qs => stripAll (strip 128 n q) qs

def sortedLt : List Nat → Bool
  | a :: b :: rest => decide (a < b) && sortedLt (b :: rest)
  | _ => true

def smallBound : Nat := 65536

/-- `q` is a known prime: a verified Pratt record, or `q < 2^16` and prime by trial division. -/
def primeK (primes : Trie) (q : Nat) : Bool :=
  (primes.find? q q).isSome || (decide (q < smallBound) && tdPrime q)

/-- One Pratt/Lucas record. -/
def prattOK (primes : Trie) (p a : Nat) (qs : List Nat) : Bool :=
  if p < smallBound then tdPrime p
  else
    sortedLt qs && qs.all (primeK primes) && stripAll (p - 1) qs == 1 &&
      powMod a (p - 1) p == 1 && qs.all (fun q => powMod a ((p - 1) / q) p != 1)

/-! ## Lower-bound function and claim rules -/

/-- Selfridge search: least `r' ≥ r` with `c ≤ 3^r'` (`c = v^3`), with fuel. -/
def selfFrom (c : Nat) : Nat → Nat → Nat
  | 0, r => r
  | f + 1, r => if 3 ^ r < c then selfFrom c f (r + 1) else r

/-- `LB(v) = max(1, λ(v), proven(v) + 1)`. -/
def lb (claims : Trie) (v : Nat) : Nat :=
  selfFrom (v ^ 3) 256 (max 1 (match claims.find? v v with | some j => j + 1 | none => 0))

/-- Sum rule for `x, x+1, …` while `2x ≤ m` and `(x(m-x))^3 ≤ t` (`t = 3^j`). -/
def sumsLoop (claims : Trie) (m j t : Nat) : Nat → Nat → Bool
  | 0, _ => false
  | f + 1, x =>
    if 2 * x ≤ m ∧ (x * (m - x)) ^ 3 ≤ t then
      decide (j < lb claims x + lb claims (m - x)) && sumsLoop claims m j t f (x + 1)
    else true

/-- `[1, p, …, p^e]`. -/
def powers (p : Nat) : Nat → List Nat
  | 0 => [1]
  | e + 1 => 1 :: (powers p e).map (p * ·)

/-- All products `∏ p_i^{a_i}` with `a_i ≤ e_i`. -/
def divisorsOf : List (Nat × Nat) → List Nat
  | [] => [1]
  | (p, e) :: rest =>
    let ds := divisorsOf rest
    (powers p e).flatMap (fun a => ds.map (a * ·))

def fprod : List (Nat × Nat) → Nat
  | [] => 1
  | (p, e) :: rest => p ^ e * fprod rest

def prodsOK (claims : Trie) (m j : Nat) (f : List (Nat × Nat)) : Bool :=
  (divisorsOf f).all fun d =>
    !(decide (2 ≤ d) && decide (d * d ≤ m)) || decide (j < lb claims d + lb claims (m / d))

def claimOK (claims primes : Trie) (m j : Nat) (f : List (Nat × Nat)) : Bool :=
  decide (2 ≤ m) && sortedLt (f.map (·.1)) && f.all (fun pe => primeK primes pe.1) &&
    fprod f == m &&
    (decide (3 ^ j < m ^ 3) || (sumsLoop claims m j (3 ^ j) m 1 && prodsOK claims m j f))

/-! ## Records and the streaming checker -/

inductive Rec where
  | prime (p a : Nat) (qs : List Nat)
  | claim (m j : Nat) (f : List (Nat × Nat))

structure State where
  claims : Trie
  primes : Trie

def State.init : State := ⟨.leaf, .leaf⟩

def insFuel : Nat := 256

def step (st : State) : Rec → Option State
  | .prime p a qs =>
    if prattOK st.primes p a qs then some ⟨st.claims, st.primes.insert (fun _ v => v) insFuel p 0 p⟩
    else none
  | .claim m j f =>
    if claimOK st.claims st.primes m j f then some ⟨st.claims.insert max insFuel m j m, st.primes⟩
    else none

def run : State → List Rec → Option State
  | st, [] => some st
  | st, r :: rs =>
    match step st r with
    | some st' => run st' rs
    | none => none

/-- Process a list of chunks (each chunk a list of records) in order. -/
def runChunks : State → List (List Rec) → Option State
  | st, [] => some st
  | st, c :: cs =>
    match run st c with
    | some st' => runChunks st' cs
    | none => none

/-- The certificate proves `‖N‖ ≥ B`. -/
def checkCert (N B : Nat) (chunks : List (List Rec)) : Bool :=
  match runChunks State.init chunks with
  | some st => decide (B ≤ lb st.claims N)
  | none => false

/-! ## Unverified parser (not part of the trust chain: soundness holds for every record list)

Line format (ASCII, one record per line):
* `P p a q1 q2 …`   — Pratt record
* `C m j p1 e1 p2 e2 …` — claim with factorisation
-/

/-- Parse space-separated decimal numbers up to `\n` (or end). Returns numbers and next index. -/
def parseNums (b : ByteArray) : Nat → Nat → Nat → Bool → List Nat → List Nat × Nat
  | 0, i, _, _, acc => (acc.reverse, i)
  | f + 1, i, cur, inNum, acc =>
    if h : i < b.size then
      let c := b[i]
      if c == 10 then ((if inNum then cur :: acc else acc).reverse, i + 1)
      else if 48 ≤ c && c ≤ 57 then parseNums b f (i + 1) (cur * 10 + (c.toNat - 48)) true acc
      else parseNums b f (i + 1) 0 false (if inNum then cur :: acc else acc)
    else ((if inNum then cur :: acc else acc).reverse, i)

def pairs : List Nat → List (Nat × Nat)
  | a :: b :: rest => (a, b) :: pairs rest
  | _ => []

def parseLines (b : ByteArray) : Nat → Nat → List Rec → List Rec
  | 0, _, acc => acc.reverse
  | f + 1, i, acc =>
    if h : i < b.size then
      let c := b[i]
      let (ns, i') := parseNums b b.size (i + 1) 0 false []
      let acc' :=
        if c == 80 then (match ns with | p :: a :: qs => Rec.prime p a qs :: acc | _ => acc)
        else if c == 67 then (match ns with | m :: j :: fs => Rec.claim m j (pairs fs) :: acc | _ => acc)
        else acc
      parseLines b f i' acc'
    else acc.reverse

def parse (s : String) : List Rec :=
  let b := s.toUTF8
  parseLines b (b.size + 1) 0 []

end ICLCert
