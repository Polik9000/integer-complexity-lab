import ICLCert.Sound
import ICLCert.M61.Data
import IntegerComplexity.Certificates.M61

/-!
# `‖2^61 - 1‖ = 127` — lower bound via `native_decide`

TRUST LEVEL: **native_decide**. The fact `checkCert (2^61 - 1) 127 M61Data.chunks = true` is
established by compiling and running the checker (Lean compiler + the precompiled `ICLCertCore`
shared library + the C compiler/runtime are trusted). In Lean 4.35 this shows up in
`#print axioms` as an auxiliary axiom `…._native.native_decide.ax_…`.
Everything else (`checkCert_sound`, Selfridge, Theorem C, divisor completeness, Lucas) is
kernel-checked with only `propext`, `Classical.choice`, `Quot.sound`.
-/

namespace ICLCert.M61
open IntegerComplexity

set_option profiler true in
set_option profiler.threshold 1000 in
theorem check_native : checkCert (2 ^ 61 - 1) 127 M61Data.chunks = true := by native_decide

/-- `‖2^61 - 1‖ ≥ 127`, i.e. `‖2^61 - 1‖ > 126` (trust level: native_decide). -/
theorem lowerBound_native : LowerBound (2 ^ 61 - 1) 127 := checkCert_sound check_native

/-- `‖2^61 - 1‖ = 127` (upper bound kernel-checked; lower bound trust level: native_decide). -/
theorem hasComplexity_native : HasComplexity (2 ^ 61 - 1) 127 :=
  ⟨IntegerComplexity.Certificates.M61.upperBound_c_m61_ub127_icl_peel, lowerBound_native⟩

end ICLCert.M61

#print axioms ICLCert.checkCert_sound
#print axioms ICLCert.M61.check_native
#print axioms ICLCert.M61.lowerBound_native
#print axioms ICLCert.M61.hasComplexity_native
