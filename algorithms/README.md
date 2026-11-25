# algorithms/

Python package (`import algorithms...`, run from the repository root) plus C sources.

| Module | Purpose |
|--------|---------|
| `expression.py` | Strict parser/evaluator for `1 + * ( )` expressions (no eval); Lean export |
| `exact_table.py` | Exact ‖n‖ for small n (pure Python), reading C tables, optimal-expression reconstruction |
| `c/complexity_table.c` | Exact ‖n‖ for all n ≤ N (C; 4·10⁸ in ~35 s, 1 byte per n) |
| `exact_single.py` | Exact ‖n‖ for one large n (budgeted exhaustive search; conditional correctness argument in research/proof-exact-search.md) |
| `upper_bound_search.py` | Heuristic upper bounds for huge n ("peel" search), emits certificates |

Correctness argument for the table pruning: an expression with k ones has value ≤ 3^{k/3}, so
‖a‖ + ‖n−a‖ ≥ 3 log₃(a(n−a)). This is increasing in a on [1, n/2], so the scan of a can stop
at the first a with (a(n−a))³ > 3^{best−1}.
