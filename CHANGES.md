# Changes

## 2026-06-10

### State space analysis and README update

- Calculated per-tier state space: ~10^81 total unique problems across all
  generators and difficulty levels (same order as atoms in the observable
  universe)
- Added detailed model capacity analysis: even 405B (Llama-3.1) can only
  memorise ~438M samples vs 10^81 possible — gap of 10^72 orders of magnitude
- Key insight: algorithmic information is 1.85 MB; even 1M param model has 14x
  headroom to store algorithms, but no model can memorise instances
- Updated README: replaced vague "~100M+" with proper state space tables,
  per-tier breakdowns, model capacity comparison, and information-theoretic
  argument

### Demo script for YouTube video

- Created `scripts/demo.py`: animated terminal demo that walks through all 11
  tiers with colour output, state space visualisation, model capacity table,
  speed test, and "The Arc" closing sequence
- Supports `--speed slow|normal|fast` and `--no-color` flags
- Created `VIDEO_PLAN.md`: full script, talking points, recording checklist,
  and post-production notes for a 5-8 minute YouTube video

## 2026-06-09

### Generators expanded to 2,022

- Expanded from 385 to 2,022 generators across 100+ scientific domains
- Added 6,326 tests (sanity + correctness), 99% coverage
- Implemented reasoning pattern weighted sampling (26 patterns, equal allocation)
- Rewrote README for website publication
