import ICLCert.M61.Data

/-! Negative tests on the full certificate (native evaluation via `#guard`; each ~2 min).
1. Genuine data, bound 128 (i.e. claim `‖N‖ > 127`): must be rejected.
2. Root claim raised from `> 126` to `> 127` (last chunk mutated), bound 128: must be rejected. -/

namespace ICLCert.M61Neg
open ICLCert

def s031_root127 : String := include_str "../../data/k61mut/chunk_031_root127.txt"

def mutChunks : List (List Rec) := M61Data.chunks.take 31 ++ [parse s031_root127]

set_option profiler true in
#guard checkCert (2 ^ 61 - 1) 128 M61Data.chunks == false

set_option profiler true in
#guard checkCert (2 ^ 61 - 1) 128 mutChunks == false

-- sanity: the mutated list has the same length as the genuine one
#guard mutChunks.length == 32

end ICLCert.M61Neg
