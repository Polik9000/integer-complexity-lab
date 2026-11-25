import ICLCertCore
open ICLCert
def d40 : String := include_str "../../data/k40/chunk_000.txt"
set_option profiler true in
theorem t40 : checkCert 1099511627775 82 [parse d40] = true := by native_decide
#print axioms t40
