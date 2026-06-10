# Changes

## 2026-06-10

### v0.1.0 release preparation

- Calculated per-tier state space: ~10^81 total unique problems across all
  generators and difficulty levels (same order as atoms in the observable
  universe)
- Added detailed model capacity analysis: even 405B (Llama-3.1) can only
  memorise ~438M samples vs 10^81 possible -- gap of 10^72 orders of magnitude
- Key insight: algorithmic information is 1.85 MB; even 1M param model has 14x
  headroom to store algorithms, but no model can memorise instances
- README rewritten: state space tables, all 26 reasoning patterns listed,
  tokenizer rationale, model capacity comparison
- Added ASCII art logo with ANSI terminal colours
- Added pyproject.toml URLs, classifiers, LICENSE (MIT)
- Removed internal development files from version control

## 2026-06-09

### Generators expanded to 2,022

- Expanded from 385 to 2,022 generators across 100+ scientific domains
- Added 6,326 tests (sanity + correctness), 99% coverage
- Implemented reasoning pattern weighted sampling (26 patterns, equal allocation)
