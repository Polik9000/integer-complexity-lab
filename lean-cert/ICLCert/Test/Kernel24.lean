import ICLCert.Sound
import ICLCert.Data.K24
open ICLCert IntegerComplexity
set_option maxRecDepth 100000
set_option profiler true in
theorem k24_lb : LowerBound (2^24 - 1) 50 :=
  checkCert_sound (N := 2^24 - 1) (B := 50) (chunks := ICLCert.Data.K24.chunks) (by decide +kernel)
#print axioms k24_lb
