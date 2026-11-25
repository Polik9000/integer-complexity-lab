import ICLCert.Sound
import ICLCert.Data.K30
open ICLCert IntegerComplexity
set_option maxRecDepth 100000
set_option profiler true in
theorem k30_lb : LowerBound (2^30 - 1) 63 :=
  checkCert_sound (N := 2^30 - 1) (B := 63) (chunks := ICLCert.Data.K30.chunks) (by decide +kernel)
#print axioms k30_lb
