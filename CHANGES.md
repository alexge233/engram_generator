# Changes

## 2026-07-07

### Problem field enrichment (fix/problem-field-missing-values)

Added `_enrich_problem` classmethod to `StepGenerator` that detects bare-formula
problem fields (e.g. `V = IR` with no numeric values) and appends the given
parameter values so the model has all information needed to solve the problem.

**Enrichment pipeline:**

1. Regex extraction of `var=value` assignments from step 1.
2. Fallback to `solution_data` dict when step 1 uses substitution format.
3. Leak guards: `_INTERNAL_KEYS` frozenset and `_RESULT_KEY_PATTERNS` regex
   exclude answer keys, boolean flags, and derived values.

**Supporting helpers in `StepGenerator`:**

- `_significand` — extracts base digits from scientific notation floats for
  fuzzy matching (e.g. `6.674` from `6.674e-11`).
- `_val_in_text` — checks if a numeric value appears in text via exact match,
  absolute value, float-to-int coercion, or significand matching.
- `_format_list` — formats lists for problem display, converting
  `Fraction(n, d)` objects to readable `n/d` notation.
- `_list_appears_in` — validates that a short numeric list's values actually
  appear in step 1 before enriching, with Fraction LaTeX matching.

**Per-generator domain knowledge fixes:**

Nine generators had domain-specific reference data (atomic weights, codon
tables, bond counts, etc.) that only appeared in step 1. Moved this data
into the problem field so the model receives it as input:

- `molar_mass` — atomic masses per element
- `dihybrid_cross` — phenotype names for dominant/recessive traits
- `genetic_code_redundancy` — codon sequences per amino acid
- `hybridisation` — bond and lone pair counts
- `heat_treatment` — HRC hardness ranges
- `molecular_orbital_diagram` — total electron count
- `schwarzschild_metric` — mass, radius, G, and c constants
- `hamiltonian` — full Lagrangian expression
- `phase_space` — V(q) potential expression

**Tests (`tests/test_enrich_problem.py`):**

42 unit tests across 7 test classes covering all enrichment helpers and
per-generator domain knowledge fixes:

- `TestSignificand` (5 tests)
- `TestValInText` (7 tests)
- `TestFormatList` (4 tests)
- `TestListAppearsIn` (7 tests)
- `TestEnrichProblem` (9 tests)
- `TestGeneratorDomainKnowledge` (9 tests)
- `TestEnrichNoLeaks` (1 broad test across all 2,022 generators)

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
