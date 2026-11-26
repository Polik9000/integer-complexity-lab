import ICLCertCore
open ICLCert

/-! Negative (mutation) tests: every mutant must be rejected. `#guard` fails the build otherwise.
Genuine data must be accepted at the true bound and rejected at bound + 1. -/

def g20 : String := include_str "../../data/k20/chunk_000.txt"
#guard checkCert 1048575 42 [parse g20] == true
#guard checkCert 1048575 43 [parse g20] == false
def m20_root_j_plus_one : String := include_str "../../data/mut20/root_j_plus_one.txt"
#guard checkCert 1048575 43 [parse m20_root_j_plus_one] == false
def m20_root_deleted : String := include_str "../../data/mut20/root_deleted.txt"
#guard checkCert 1048575 42 [parse m20_root_deleted] == false
def m20_prime_deleted : String := include_str "../../data/mut20/prime_deleted.txt"
#guard checkCert 1048575 42 [parse m20_prime_deleted] == false
def m20_composite_as_prime : String := include_str "../../data/mut20/composite_as_prime.txt"
#guard checkCert 1048575 42 [parse m20_composite_as_prime] == false
def m20_witness_one : String := include_str "../../data/mut20/witness_one.txt"
#guard checkCert 1048575 42 [parse m20_witness_one] == false
def m20_pratt_q_missing : String := include_str "../../data/mut20/pratt_q_missing.txt"
#guard checkCert 1048575 42 [parse m20_pratt_q_missing] == false
def m20_root_bad_factorisation : String := include_str "../../data/mut20/root_bad_factorisation.txt"
#guard checkCert 1048575 42 [parse m20_root_bad_factorisation] == false
def m20_claim_moved_after_root : String := include_str "../../data/mut20/claim_moved_after_root.txt"
#guard checkCert 1048575 42 [parse m20_claim_moved_after_root] == false
def m20_mid_claim_moved_to_end : String := include_str "../../data/mut20/mid_claim_moved_to_end.txt"
#eval (checkCert 1048575 42 [parse m20_mid_claim_moved_to_end])  -- informational: may be true (claim not needed)
def m20_truncated : String := include_str "../../data/mut20/truncated.txt"
#guard checkCert 1048575 42 [parse m20_truncated] == false
def m20_random_j_plus_one : String := include_str "../../data/mut20/random_j_plus_one.txt"
#eval (checkCert 1048575 42 [parse m20_random_j_plus_one])  -- informational: may be true or false

def g40 : String := include_str "../../data/k40/chunk_000.txt"
#guard checkCert 1099511627775 82 [parse g40] == true
#guard checkCert 1099511627775 83 [parse g40] == false
def m40_root_j_plus_one : String := include_str "../../data/mut40/root_j_plus_one.txt"
#guard checkCert 1099511627775 83 [parse m40_root_j_plus_one] == false
def m40_root_deleted : String := include_str "../../data/mut40/root_deleted.txt"
#guard checkCert 1099511627775 82 [parse m40_root_deleted] == false
def m40_prime_deleted : String := include_str "../../data/mut40/prime_deleted.txt"
#guard checkCert 1099511627775 82 [parse m40_prime_deleted] == false
def m40_composite_as_prime : String := include_str "../../data/mut40/composite_as_prime.txt"
#guard checkCert 1099511627775 82 [parse m40_composite_as_prime] == false
def m40_witness_one : String := include_str "../../data/mut40/witness_one.txt"
#guard checkCert 1099511627775 82 [parse m40_witness_one] == false
def m40_pratt_q_missing : String := include_str "../../data/mut40/pratt_q_missing.txt"
#guard checkCert 1099511627775 82 [parse m40_pratt_q_missing] == false
def m40_root_bad_factorisation : String := include_str "../../data/mut40/root_bad_factorisation.txt"
#guard checkCert 1099511627775 82 [parse m40_root_bad_factorisation] == false
def m40_claim_moved_after_root : String := include_str "../../data/mut40/claim_moved_after_root.txt"
#guard checkCert 1099511627775 82 [parse m40_claim_moved_after_root] == false
def m40_mid_claim_moved_to_end : String := include_str "../../data/mut40/mid_claim_moved_to_end.txt"
#eval (checkCert 1099511627775 82 [parse m40_mid_claim_moved_to_end])  -- informational: may be true (claim not needed)
def m40_truncated : String := include_str "../../data/mut40/truncated.txt"
#guard checkCert 1099511627775 82 [parse m40_truncated] == false
def m40_random_j_plus_one : String := include_str "../../data/mut40/random_j_plus_one.txt"
#eval (checkCert 1099511627775 82 [parse m40_random_j_plus_one])  -- informational: may be true or false

