import ICLCert.Sound
import ICLCert.Data.K20
open ICLCert IntegerComplexity
set_option maxRecDepth 100000
set_option profiler true in
theorem k20_lb : LowerBound (2^20 - 1) 42 :=
  checkCert_sound (N := 2^20 - 1) (B := 42) (chunks := ICLCert.Data.K20.chunks) (by decide +kernel)
#print axioms k20_lb
