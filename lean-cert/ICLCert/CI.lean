import ICLCert.Sound
import ICLCert.Test.Kernel20

/-! CI target: everything that needs no generated data outside the repository.
`checkCert_sound`, divisor completeness and Pratt soundness, and the kernel-only (`decide +kernel`)
proof of `‖2^20 - 1‖ > 41`. The full `2^61 - 1` run (`ICLCert.M61.Native`, trust level native_decide)
needs the 94 MB data from `scripts/gen_lean_data.py` and is run by hand (see README). -/
#print axioms ICLCert.checkCert_sound
#print axioms ICLCert.mem_divisorsOf
#print axioms ICLCert.prattOK_sound
#print axioms k20_lb
