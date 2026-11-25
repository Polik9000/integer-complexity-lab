# tests/

`python3 -m pytest -q` from the repository root. Tests cover the strict parser, both exact-table
implementations (cross-checked with each other and with literature values), the certificates,
and the upper-bound search. Every new algorithm needs tests here before its outputs count as evidence.
