import IntegerComplexity
-- Run: lake env lean scripts/CheckAxioms.lean
-- Expected: no `sorryAx`, and no axioms beyond Lean's standard ones (or none at all).
#print axioms IntegerComplexity.Certificates.M61.upperBound_c_m61_ub127_icl_peel
#print axioms IntegerComplexity.Certificates.M61.upperBound_c_m61_ub127_board_pr4
#print axioms IntegerComplexity.upperBound_self
