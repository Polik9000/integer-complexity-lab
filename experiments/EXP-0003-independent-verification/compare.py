"""Compare He's values with EXP-0002 and with Iraids et al. 2012 Table 3."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
from test_exact_single import IRAIDS_A  # A(k) = ||2^k-1|| - 2k, k <= 39

he = {d["k"]: d["hqz"] for d in map(json.loads, open(sys.argv[1]))}
ours = {d["k"]: d["exact"] for d in map(json.loads,
        open(ROOT / "experiments/EXP-0002-exact-mersenne-pilot/results_k20-61.jsonl"))}
bad = [(k, v, ours.get(k), IRAIDS_A.get(k)) for k, v in sorted(he.items())
       if (k in ours and ours[k] != v) or (k in IRAIDS_A and 2 * k + IRAIDS_A[k] != v)]
print(f"He values: {len(he)}; compared with EXP-0002: {sum(k in ours for k in he)}, "
      f"with Iraids Table 3: {sum(k in IRAIDS_A for k in he)}; mismatches: {bad}")
sys.exit(1 if bad else 0)
