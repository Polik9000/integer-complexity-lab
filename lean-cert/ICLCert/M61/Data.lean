import ICLCertCore

/-! The 32 text chunks of the table-free certificate for `2^61 - 1` (generated data, not committed;
regenerate with `python3 scripts/gen_lean_data.py text tablefree_k61.jsonl.gz data/k61 32`).
The text is parsed by the unverified `ICLCert.parse`; soundness does not depend on the parser. -/

namespace ICLCert.M61Data

def s000 : String := include_str "../../data/k61/chunk_000.txt"
def s001 : String := include_str "../../data/k61/chunk_001.txt"
def s002 : String := include_str "../../data/k61/chunk_002.txt"
def s003 : String := include_str "../../data/k61/chunk_003.txt"
def s004 : String := include_str "../../data/k61/chunk_004.txt"
def s005 : String := include_str "../../data/k61/chunk_005.txt"
def s006 : String := include_str "../../data/k61/chunk_006.txt"
def s007 : String := include_str "../../data/k61/chunk_007.txt"
def s008 : String := include_str "../../data/k61/chunk_008.txt"
def s009 : String := include_str "../../data/k61/chunk_009.txt"
def s010 : String := include_str "../../data/k61/chunk_010.txt"
def s011 : String := include_str "../../data/k61/chunk_011.txt"
def s012 : String := include_str "../../data/k61/chunk_012.txt"
def s013 : String := include_str "../../data/k61/chunk_013.txt"
def s014 : String := include_str "../../data/k61/chunk_014.txt"
def s015 : String := include_str "../../data/k61/chunk_015.txt"
def s016 : String := include_str "../../data/k61/chunk_016.txt"
def s017 : String := include_str "../../data/k61/chunk_017.txt"
def s018 : String := include_str "../../data/k61/chunk_018.txt"
def s019 : String := include_str "../../data/k61/chunk_019.txt"
def s020 : String := include_str "../../data/k61/chunk_020.txt"
def s021 : String := include_str "../../data/k61/chunk_021.txt"
def s022 : String := include_str "../../data/k61/chunk_022.txt"
def s023 : String := include_str "../../data/k61/chunk_023.txt"
def s024 : String := include_str "../../data/k61/chunk_024.txt"
def s025 : String := include_str "../../data/k61/chunk_025.txt"
def s026 : String := include_str "../../data/k61/chunk_026.txt"
def s027 : String := include_str "../../data/k61/chunk_027.txt"
def s028 : String := include_str "../../data/k61/chunk_028.txt"
def s029 : String := include_str "../../data/k61/chunk_029.txt"
def s030 : String := include_str "../../data/k61/chunk_030.txt"
def s031 : String := include_str "../../data/k61/chunk_031.txt"

/-- The certificate as a list of parsed chunks. -/
def chunks : List (List Rec) := [parse s000, parse s001, parse s002, parse s003, parse s004, parse s005, parse s006, parse s007, parse s008, parse s009, parse s010, parse s011, parse s012, parse s013, parse s014, parse s015, parse s016, parse s017, parse s018, parse s019, parse s020, parse s021, parse s022, parse s023, parse s024, parse s025, parse s026, parse s027, parse s028, parse s029, parse s030, parse s031]

end ICLCert.M61Data
