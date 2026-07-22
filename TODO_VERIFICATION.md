# Verification System Plan

## Summary

| Category | Generators | Method | Status |
|----------|-----------|--------|--------|
| Library-verifiable | ~820 (41%) | sympy/numpy/scipy/networkx recomputation | TODO |
| Formula-only | ~1,033 (51%) | Atom with Wikipedia/Wolfram formula + worked example | TODO |
| Reference lookup | ~91 (4%) | Textbook classification tables | TODO |
| LLM verification | ~78 (4%) | Opus 4.8 / Fable reasoning review | TODO |

## Atom Coverage

- 373/2,022 generators have atoms (18%)
- Tiers 0-2: 99% covered
- Tiers 3: 62% covered
- Tiers 4-7: 10% covered
- 1,649 atoms need backfilling

## Task Breakdown

### Phase 1: Infrastructure

1. Add `example` field to Atom dataclass (base.py)
2. Add `[verify]` optional dependency group (pyproject.toml)
3. Build library verification framework (validation/library_verifier.py)
4. Build atom verification framework (validation/atom_verifier.py)

### Phase 2: Library Verifiers (820 generators)

Independent recomputation using authoritative libraries.
No circularity -- the library IS the ground truth.

Libraries: sympy (~250), numpy (~120), scipy (~80),
networkx (~60), math/stdlib (~150), builtins (~160)

### Phase 3: Atom Backfill (1,649 generators)

Each atom needs:
- name, atom_type, content (formula/theorem text)
- source + source_url (Wikipedia, Wolfram MathWorld, NIST, etc.)
- example: worked problem with known input/output
- prerequisites

Sources to check (in priority order):
1. Wikipedia (most formulas have dedicated articles)
2. Wolfram MathWorld (rigorous mathematical definitions)
3. NIST Digital Library of Mathematical Functions
4. Khan Academy (worked examples)
5. Hyperphysics (physics formulas with examples)
6. LibreTexts (chemistry, biology, engineering)

Modules to backfill (by size, largest first):
- calculus_ext (15), real_analysis (12), electromagnetism (12)
- abstract_algebra (12), linear_algebra_ext (12)
- probability_ext (12), ml_deep (12), geometry_ext (12)
- calculus_deep (12), ... (see full list in atom coverage audit)

### Phase 4: Reference Tables (91 generators)

Classification/lookup generators need lookup tables:
- Electron configurations, VSEPR geometries
- IUPAC naming rules, functional group identification
- Le Chatelier predictions, rock cycle classifications
- Mitosis phases, blood types

### Phase 5: LLM Verification (78 generators)

Stratified sample: 10 samples per generator = 780 samples
Send to Opus 4.8 / Fable for reasoning verification.
Store verdicts in lookup table.

## Validation Pipeline

```
engram-generator[verify] installs:
  sympy, numpy, scipy, networkx

validate_all.py --mode library   # Phase 2: library recomputation
validate_all.py --mode atom      # Phase 3: compare to atom examples
validate_all.py --mode reference # Phase 4: lookup table check
validate_all.py --mode llm       # Phase 5: LLM review
validate_all.py --mode all       # Everything
```

## Current Validation Results (100 seeds, 1.6M samples)

- 1,617,600 samples tested
- 0 wrong arithmetic steps
- 0 crashes
- 8 fallbacks (edge cases at extreme difficulty)
- 15,483 fully verified (arithmetic)
- 53,867 partially verified
- 1,543,571 unverifiable (domain-specific, no library check yet)
