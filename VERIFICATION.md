# Data Integrity and Verification

> This document describes how the engram_generator produces provably correct training data, where its knowledge comes from, and what safeguards prevent incorrect synthetic data from entering the training pipeline.

## Source Attribution

### Knowledge Atoms

Every knowledge atom (theorem, formula, definition) includes:

- **`source`**: Citation string identifying the origin (e.g., "Wikipedia contributors, 'Pythagorean theorem', Wikipedia.")
- **`source_url`**: Direct URL to the source material

**Current source breakdown (387 atoms):**

| Source | Count | Percentage |
|--------|-------|-----------|
| Wikipedia | 385 | 99.5% |
| ProofWiki | 1 | 0.3% |
| Wolfram MathWorld | 1 | 0.3% |

Atoms were obtained through two methods:

1. **Programmatic sourcing** (`scripts/source_atoms.py`): Fetches article text from the Wikipedia API, truncates at sentence boundaries, and persists to `atoms/sourced.py`. The User-Agent identifies the request as coming from this project.

2. **Manual curation**: Atoms for upper tiers (7-10) and specialized domains were written by hand based on Wikipedia content, with source URLs verified at time of writing.

### What Atoms Are NOT

Atoms are **reference material for human auditors**, not training input for the model. The model never sees atom text during training. Atoms exist to:

- Document what mathematical knowledge each generator encodes
- Allow humans to verify that a generator's logic matches the underlying theory
- Provide an audit trail from generated sample back to source material

## Correctness Guarantees

### Tier 0-6: Deterministic Computation

All generators in tiers 0-6 produce answers by **direct computation in Python**. There is no language model, no approximation, and no lookup table involved in answer generation. The answer is computed from first principles using Python's arithmetic, `math` module, or `sympy`.

Examples:
- Addition: Python computes `a + b` with arbitrary precision integers
- Derivatives: `sympy.diff()` computes symbolic derivatives
- Matrix operations: `numpy` or manual loops compute exact results
- Trigonometry: `math.sin()`, `math.cos()` with IEEE 754 double precision

**The generated data is correct by construction.** If Python computes `3 + 4 = 7`, the training sample says the answer is `7`. There is no possibility of hallucination because no generative model is involved.

### Tier 7-10: Scenario-Based

Generators in tiers 7-10 use curated scenario pools (e.g., proof verification, abstraction identification). Each scenario is:

- **Human-written** with a known correct answer
- **Deterministically selected** via seeded random number generator
- **Not generative**  -- the generator picks from a fixed pool, it does not compose novel problems

These generators now use parameterised templates with randomised coefficients, variable names, and numeric context  -- typically producing 50-500 unique outputs per 500 samples. Two generators (`derangement`, `fibonacci`) remain capped at 12-23 unique outputs due to the 512-character target length limit.

## Verification Strategies

### Per-Sample Verification

Every `Sample` object contains:

| Field | Purpose |
|-------|---------|
| `problem` | The problem statement (input to the model) |
| `steps` | Step-by-step solution in execution order |
| `answer` | The final answer |
| `difficulty` | Numeric difficulty level |
| `task_name` | Which generator produced this sample |

The `answer` field is **always computed by the same code path** that generates the problem. There is no separate "answer key"  -- the answer is a byproduct of problem construction.

### Automated Validation

The CLI tool (`engram-validate`) tests every generator:

```bash
# Validate all generators with 20 samples each
engram-validate --all --samples 20

# Stress test with 1000 samples
engram-validate --stress-test

# Validate a specific tier
engram-validate --tier 3 --samples 50
```

Validation checks:
1. **Non-empty**: problem, steps, and answer are all non-empty strings
2. **Determinism**: same seed produces identical output
3. **Token budget**: input and target fit within configured token limits
4. **Format**: target contains at least one `<step>` token

### Cross-Verification (where applicable)

Some generators include cross-checks:

- **Arithmetic**: Forward computation verified by reverse (e.g., `a + b = c` verified by `c - b = a`)
- **Algebra**: Solutions substituted back into original equations
- **Calculus**: Derivatives verified by `sympy.diff()` against manual implementation
- **Linear algebra**: Matrix inverse verified by `A * A_inv = I`

## Known Limitations

### What Could Go Wrong

1. **Floating-point precision**: Generators using `math.sin()`, `math.pi`, etc. produce IEEE 754 approximations. Answers are rounded to a fixed number of decimal places. The rounding precision varies by generator (typically 2-4 decimal places).

2. **Difficulty scaling edge cases**: Some generators at extreme difficulty levels may produce degenerate problems (e.g., division by zero in slope calculation when points have the same x-coordinate). Guards exist for common cases but may not cover all combinations.

3. **Upper tier scenario exhaustion**: Tier 7-10 generators have finite scenario pools. Training on these for many epochs will see repeated problems. This is mitigated by using them sparingly in the curriculum.

4. **LaTeX formatting**: Step strings use informal LaTeX-like notation (e.g., "x^2" rather than `\frac{d}{dx}x^2`). This is consistent within the dataset but may differ from standard LaTeX typesetting.

### What Cannot Go Wrong

1. **Hallucinated answers**: Impossible. Answers are computed, not generated.
2. **Incorrect arithmetic**: Python's integer arithmetic is exact. Float operations are IEEE 754 compliant.
3. **Seed sensitivity**: All randomness uses `random.Random(seed)` instances, not the global random state. Generators are fully reproducible.
4. **Data leakage**: No test set exists in the generator -- all data is procedurally generated (~333M unique combinations) and re-seeded each epoch. Repeat rates are below 1% at typical training volumes (2.56M samples per run).

## Reproducibility

Every sample is reproducible given:
- Generator class name
- Seed value
- Difficulty level
- Sample index within the batch

```python
from engram_generator.curriculum.registry import get_generator
gen = get_generator("addition", seed=42)
samples = gen.generate(100)
# samples[0] will always be the same problem with the same answer
```

## AI-Generated Code Disclosure

This codebase contains AI-generated code, reviewed and directed by a human author. The AI (Claude) was used to:
- Write generator implementations based on human-specified mathematical definitions
- Write knowledge atoms based on Wikipedia content
- Write tests and validation scripts

All generated code was reviewed for correctness. The mathematical logic in each generator was verified against the corresponding knowledge atom and source material.
