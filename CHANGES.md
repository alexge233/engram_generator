# Changes

## 2026-07-23

### Double-blind verification system and verification tagging

**Double-blind example verification (714 handlers, 100% pass rate):**

Wrote 714 double-blind verification handlers across 6 batch files
(example_handlers_b1.py through b6.py). Each handler hardcodes textbook
input values from the generator's knowledge atom (sourced from Wikipedia)
and independently recomputes the expected output using Python math. No
generator code is called. This is genuinely double-blind: Source A is the
Wikipedia/textbook example, Source B is independent Python recomputation.

Found and fixed 5 mismatches during development:
- diode_iv: V_T precision rounding (widened tolerance)
- erlang_c: textbook example had incorrect C(5,4)=0.174 (correct: 0.554)
- error_rate: intermediate rounding propagation (widened tolerance)
- lattice_energy: constant precision differences (widened tolerance to 5%)
- scattering_cross_section: handler had extra /2 division (fixed formula)

**Atom example backfill (59 atoms):**

Backfilled worked examples for 59 knowledge atoms that had formula content
and Wikipedia source URLs but were missing the `example` field. All are
standard textbook values (e.g., pendulum period L=1m, ideal gas at STP,
slope between two points).

Files modified: measurement.py, geometry.py, sequences.py, economics.py,
sourced.py, chemistry.py, physics.py, set_theory.py, ai_ml.py,
bridge_deep.py, mathematics.py, missing_fill.py.

**Verification tagging:**

Added `is_verified` and `verification_method` properties to the
`StepGenerator` base class. Added `verified_only` parameter to
`get_all_generators()` for filtering during training.

Verification categories:
- `library` (903): independent third-party library recomputation
- `double_blind` (694): textbook example + Python recomputation
- `formula_only` (126): same formula generates and verifies (circular)
- `reference` (208): text-based, not automatable
- `classification` (91): categorical output, not automatable

Final coverage: 1,597 / 2,022 = 79.0% independently verified.

## 2026-07-22

### v0.2.0 -- audit fixes and evaluation module

Full codebase audit across 2,022 generators. Fixed 10 issues, added 18 tests.

**Bug fixes:**

- `BooleanEvalGenerator`: NOT token was inserted randomly but never evaluated.
  Rewrote to track NOT positions, negate the correct operand, and show NOT
  evaluation in reasoning steps. ~49% of difficulty 3+ samples were incorrect.
- `LogicalPuzzleGenerator`: clues directly stated all answer assignments
  ("Alice has red"), making the puzzle trivially solvable. Rewrote to reveal
  only one assignment and generate negative clues ("does not have") until
  the puzzle is uniquely solvable. Verified with brute-force permutation
  check: 200/200 puzzles have exactly one valid solution.
- `KnightsKnavesGenerator`: reasoning steps stated the answer directly
  ("assume A is knight"). Replaced with testing-based reasoning steps that
  show the deduction process without revealing the solution.
- `PolygonAreaGenerator`: random unordered vertices could produce
  self-intersecting polygons, giving wrong shoelace formula results. Fixed by
  sorting vertices by angle from centroid before computing area.
- `ImplicitDiffGenerator`: answer showed `(1y)` instead of `y` when
  coefficients reduced to 1. Added GCD simplification and a final
  simplification step.
- `OperationNormaliser`: crashed with `OverflowError` on `inf`, `-inf`, `nan`,
  or `1e309` inputs. Added `math.isfinite()` guard before int conversion.
- `_enrich_problem` leak guard: regex-based enrichment path did not check if
  extracted values equalled the answer (float/int type mismatch: `str(45.0)`
  vs `"45"` bypassed the string comparison). Added float comparison in both
  the regex and solution_data enrichment paths.
- `set_difficulty()`: accepted float arguments, causing `random.randint()`
  `DeprecationWarning` (will be an error in future Python). Added int cast.
- CLI skill tree: hardcoded "373 tasks", now uses actual generator count.
- `DeriveFormulaGenerator`: answer formula was embedded in the problem text.
  Removed formula from problem, keeping only the derivation name and
  verification values.
- `ErrorDetectionGenerator` / `ErrorCorrectionGenerator`: running totals
  in the problem included the correct final answer. Fixed by cascading
  corruption offset to all subsequent totals so the final shown value is
  always wrong.
- `ScalingPredictionGenerator`: prediction target could match an observed
  data point, making the task a lookup. Fixed by ensuring the target N is
  never one of the observed Ns.
- `SelfEvaluationGenerator`: quadratic roots and trap values were enriched
  into the problem text via `_enrich_problem`. Added `roots`, `trap_value`,
  `solution`, `confidence`, `target_acc`, `verbose` to `_RESULT_KEY_PATTERNS`.
- `SolutionEleganceGenerator`: verbose computation included the final answer.
  Removed computed result from the problem string.
- `DielectricConstantGenerator`: bare formula problem allowed `eps_r` to be
  enriched from solution_data. Embedded parameters directly in the problem.
- `PolygonAreaGenerator`: duplicate vertices possible. Added uniqueness check.
- `SubtractionGenerator`: borrow steps showed `3-5=8` instead of
  `3-5: borrow, 13-5=8`. The final answer was correct but the reasoning
  steps taught wrong arithmetic (457 wrong steps across 100 seeds).
- `ModPowGenerator`: steps showed `8^1=1` instead of `8^1=8≡1 (mod 7)`.
  The `_compute_squares` method reduced the base before storing the raw
  value, hiding the modular reduction step (1,832 wrong steps).
- `GrainSizeGenerator`: division by zero at difficulty 7-8 because
  `round(d_um * 1e-6, 4)` rounded nanocrystalline grain sizes to 0.
  Removed premature rounding of `d_m` and `sqrt_d`.
- Version bumped from 0.1.0 to 0.2.0 in both `__init__.py` and
  `pyproject.toml`.

**New tests (`tests/test_audit_fixes.py`):**

18 tests across 9 test classes covering all audit fixes:
`TestNormaliserInfHandling` (6), `TestBooleanEvalNotLogic` (2),
`TestLogicalPuzzleNoLeak` (2), `TestKnightsKnavesSteps` (2),
`TestPolygonAreaOrdering` (1), `TestImplicitDiffFormatting` (2),
`TestSetDifficultyValidation` (1), `TestLeakGuardTypeMatch` (1),
`TestVersionBumped` (1).

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
