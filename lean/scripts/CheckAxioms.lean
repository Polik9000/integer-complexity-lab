import IntegerComplexity
-- Run: lake env lean scripts/CheckAxioms.lean
-- Expected: no `sorryAx`, and no axioms beyond Lean's standard ones (or none at all).
#print axioms IntegerComplexity.Certificates.M61.upperBound_c_m61_ub127_icl_peel
#print axioms IntegerComplexity.Certificates.M61.upperBound_c_m61_ub127_board_pr4
#print axioms IntegerComplexity.upperBound_self
-- EXP-0004 proof of concept (expected: at most [propext, Quot.sound])
#print axioms IntegerComplexity.Expr.selfridge
#print axioms IntegerComplexity.lowerBound_of_cube
#print axioms IntegerComplexity.theoremC
#print axioms IntegerComplexity.checkAll_sound
#print axioms IntegerComplexity.lowerBound_of_check
#print axioms IntegerComplexity.PoC.M10.exact
