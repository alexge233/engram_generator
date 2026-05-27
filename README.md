# Engram Generator

> **Alpha Version** -- Not yet tested at scale. Not yet fully reviewed. Use at your own peril.

> This repository contains AI-generated code, reviewed and directed by a human author.

A procedural synthetic dataset generator for training reasoning, logic, and algorithmic learning in neural networks. 373 generators across 11 tiers, backed by 387 knowledge atoms sourced from Wikipedia, ProofWiki, and Wolfram MathWorld. Estimated **333 million** unique problem combinations.

## Combinatorial Space

The generator is procedural, not infinite. Its combinatorial space varies by tier.

| Tier | Generators | Est. Unique Combinations | Avg / Generator | Weakest Generator |
|---|---|---|---|---|
| 0 | 20 | ~35M | ~1.7M | truth_table (164) |
| 1 | 36 | ~44M | ~1.2M | fibonacci (23) |
| 2 | 46 | ~48M | ~1.0M | square_root (59) |
| 3 | 59 | ~68M | ~1.2M | call_stack_depth (51) |
| 4 | 57 | ~56M | ~988K | volume_sphere (74) |
| 5 | 55 | ~35M | ~644K | newton_raphson (51) |
| 6 | 42 | ~24M | ~561K | derangement (12) |
| 7 | 18 | ~8M | ~456K | proof_by_induction (98) |
| 8 | 13 | ~32K | ~2.5K | cross_domain_transfer (58) |
| 9 | 14 | ~11M | ~773K | complexity_analysis (384) |
| 10 | 13 | ~4M | ~342K | efficiency_analysis (224) |
| **Total** | **373** | **~333M** | | |

Tiers 0-6 randomise operands across digit ranges, producing effectively unlimited unique problems. Tiers 7-10 use parameterised scenario templates where structural templates repeat, but coefficients and variable names change each epoch. Two generators (`derangement`, `fibonacci`) are hard-capped at 12-23 unique outputs by the 512-character target length limit.

At a typical training run (10K steps, batch_size 256 = 2.56M samples), the expected repeat rate is **< 1%**.

## Knowledge Pipeline

The generator's correctness chain runs from authoritative sources down to training samples:

```
Wikipedia / ProofWiki / Wolfram MathWorld
    |
    v
Knowledge Atoms (387 self-contained units)
    |  - One theorem, formula, or definition per atom
    |  - Full source citation and URL
    |  - Human audit reference (never seen by model)
    v
Generators (373 procedural task constructors)
    |  - Each generator encodes one atom's logic in code
    |  - Answers computed by Python, not looked up
    |  - Difficulty-scaled, re-seeded each epoch
    v
Training Samples (problem + steps + answer)
    |  - Natural language input
    |  - LaTeX problem statement
    |  - Step-by-step solution chain
    |  - Deterministically verifiable answer
    v
Model Training (character-level tokenizer, <step> masking)
```

### Knowledge Atoms

387 atoms sourced from:

| Source | Count | Usage |
|---|---|---|
| [Wikipedia](https://en.wikipedia.org/) | 385 | Theorems, definitions, formulas. Article text fetched via API or manually curated |
| [ProofWiki](https://proofwiki.org/) | 1 | Power rule derivative proof |
| [Wolfram MathWorld](https://mathworld.wolfram.com/) | 1 | Second fundamental theorem of calculus |

Each atom is a self-contained unit:

```python
Atom(
    atom_type="theorem",
    name="chain_rule",
    content="if y=f(g(x)) then dy/dx = f'(g(x)) * g'(x)",
    tier=5,
    domain="calculus",
    source="Wikipedia, 'Chain rule'",
    source_url="https://en.wikipedia.org/wiki/Chain_rule",
    prerequisites=["derivative"],
)
```

Atoms are **reference material for human auditors**, not training input for the model. The model never sees atom text during training. Atoms exist to:

- Document what mathematical knowledge each generator encodes
- Allow humans to verify that a generator's logic matches the underlying theory
- Provide an audit trail from generated sample back to source material

No other sources (arXiv, textbooks, etc.) were used. All 387 atoms trace back to the three sources listed above.

### Generators

Each generator turns an atom's mathematical knowledge into procedurally generated problems:

- **Tiers 0-6**: answers computed by Python arithmetic, `math`, `sympy`, or `numpy`, correct by construction
- **Tiers 7-10**: parameterised scenario templates with randomised coefficients, human-curated with known correct answers
- All randomisation via `random.Random(seed)`, fully deterministic and reproducible

## Purpose

Models trained on static datasets learn to pattern-match, not to reason. They memorise input-output mappings rather than learning the underlying algorithms. When faced with unseen problem structures, they collapse.

Engram Generator produces procedurally generated training data that forces models to learn **how to think, not what to answer**:

- **Procedurally generated** -- ~333M unique combinations, re-seeded each epoch
- **Step-by-step solution chains** -- the model must learn to decompose and reason, not guess
- **Adaptive difficulty** -- escalates as the model improves, always training at the frontier
- **Prerequisite skill tree** -- gates advanced reasoning behind mastery of foundations
- **Deterministic verification** -- every answer is provably correct by construction
- **Full source attribution** -- 387 atoms linked to Wikipedia, ProofWiki, and Wolfram MathWorld

## Architecture

### Samples

Each training sample has three parts:

```
Input:  add two 5 digit numbers
Target: 13278 + 46048 <step> 8+8=16 <step> 7+4+1=12 <step> 2+0+1=3 <step> 3+6=9 <step> 1+4=5 <step> 59326
```

- **Input**: short natural language task description
- **Target**: problem statement, solution steps, and final answer separated by `<step>` tokens
- `<step>` is a special token excluded from loss computation. The model is only scored on mathematical content

Both input and target are capped at **512 tokens**. Generators that produce targets longer than 512 characters automatically retry at lower difficulty.

### Three interaction modes

**Mode A -- Apply formula**: formula given, solve with values
```
Input:  apply \frac{1}{2}mv^2 where m=5 v=3
Target: \frac{1}{2}(5)(3^2) <step> \frac{1}{2}(5)(9) <step> \frac{45}{2} <step> 22.5
```

**Mode B -- Recall formula**: describe concept, model produces LaTeX
```
Input:  express kinetic energy in latex
Target: KE = \frac{1}{2}mv^2
```

**Mode C -- Full solve**: describe task, model formulates and solves
```
Input:  find gravitational force between earth and 70kg person
Target: F = \frac{GMm}{r^2} <step> \frac{(6.67e-11)(5.97e24)(70)}{(6.37e6)^2} <step> 686.4
```

### Tokenizer

Character-level tokenizer with 75 tokens:

- Digits: `0-9` (10)
- Lowercase: `a-z` (26)
- Uppercase: `A-Z` (26)
- Operators: `+ - / * ^ ( ) [ ] { } = : ; ? . , \ _ | ! & ~ ' < > % # @ "` (28)
- Unicode: `$ ° x -- -> n u` (7)
- Special: `<pad>`, `<eos>`, `<step>` (3)

**Why character-level?** Subword tokenisers (BPE, SentencePiece) merge frequent character sequences into single tokens. This is efficient for natural language but destructive for algorithmic reasoning:

1. **Digit atomicity**: in `13278 + 46048`, each digit must be individually addressable for carry propagation. BPE might merge `132` into one token, hiding the digit boundaries the model needs to reason about.
2. **LaTeX structure**: `\frac{d}{dx}` has syntactic meaning at the character level. Subword merges would break the brace-matching structure.
3. **Step decomposition**: the model must learn to process one operation per step. Character-level tokens force it to attend to each symbol, not skip over merged chunks.
4. **No vocabulary mismatch**: every character the generator produces exists in the vocabulary. No `[UNK]` tokens, no silent truncation.

The tradeoff is longer sequences (each character is a token), which is why inputs and targets are capped at 512 tokens.

### Skill Tree

Tasks are organised into 11 tiers (0-10) with prerequisite dependencies. A task only unlocks when all its prerequisites are mastered. The competency map is fully functional -- progressive mastery from tier 0 through tier 10 results in all 373 tasks unlocked and mastered.

Run `engram-validate --skill-tree` for a rich interactive tree. Arrows (`<-`) show cross-tier prerequisites. Nesting shows same-tier dependencies.

```
Engram Curriculum (373 tasks)
+-- Tier 0 -- Basic arithmetic (20 tasks)
|   +-- addition
|   |   +-- perimeter_rectangle
|   +-- boolean_eval
|   +-- subtraction
|   +-- sorting
|   +-- ...
+-- Tier 1 -- Operations (36 tasks)
|   +-- multiplication <- addition
|   |   +-- area_rectangle
|   |   |   +-- area_triangle
|   |   +-- pythagorean <- addition
|   |   +-- sin_cos_eval
|   |       +-- tan_eval
|   +-- division <- subtraction
|   +-- implication <- boolean_eval
|   |   +-- biconditional
|   |   +-- syllogism
|   +-- ...
+-- Tier 2-6: polynomials -> calculus -> physics -> graduate
+-- Tier 7-8: proofs -> meta-reasoning -> creative
+-- Tier 9 -- Research (14 tasks)
|   +-- algorithm_design <- method_selection, sorting
|   |   +-- algorithm_improvement
|   |   +-- complexity_comparison
|   |   +-- impossibility_proof
|   +-- ...
+-- Tier 10 -- Self-architecture (13 tasks)
    +-- architecture_analysis <- matrix_multiply
    |   +-- efficiency_analysis
    |   +-- successor_design <- algorithm_improvement
    +-- scaling_prediction <- exponentiation, polynomial_eval
        +-- training_diagnosis
            +-- data_prescription
```

Full tree: [SKILL_TREE.md](SKILL_TREE.md)

### Adaptive Difficulty

Each epoch, the system checks per-task accuracy:
- **Above 95%**: difficulty escalates (harder instances)
- **Above 90%**: task is considered mastered, prerequisites unlock
- **Below 50%**: task receives extra training samples (frontier weighting)

The final output is a **competency map**: which tasks the model mastered, at what difficulty, forming a profile of mathematical capability.

## The Arc

A model trained on this curriculum progresses from basic arithmetic to self-architectural reasoning:

```
2 + 3 = 5
    |
\frac{d}{dx}(3x^2 + 2x) = 6x + 2
    |
\nabla \times \vec{F} = ...
    |
"This proof has an error in step 3. Here is the correction."
    |
"These two problems share an isomorphic structure."
    |
"To solve this class of problems, I would design the following algorithm."
    |
"My architecture struggles with this because gradient vanishes at layer 3.
 Here is a proposed modification."
```

From following procedures to creating them. From solving problems to understanding what makes problems solvable.

## Verification

All generated data is provably correct by construction. See [VERIFICATION.md](VERIFICATION.md) for full details.

- **Tiers 0-6**: Direct computation (Python computes the answer)
- **Tier 7**: Property checking (constraints satisfied, algebraic equivalence)
- **Tier 8**: Multi-point evaluation (formula correct at unseen test points)
- **Tier 9**: Empirical testing (proposed algorithm runs correctly)
- **Tier 10**: Implementation testing (proposed modification benchmarked)

## Installation

```bash
pip install -e .
```

## Usage

### Generate samples

```python
from engram_generator.curriculum.registry import get_generator

gen = get_generator("addition", min_difficulty=3, max_difficulty=5)
samples = gen.generate(100)

for sample in samples[:3]:
    print(f"Input:  {sample.input_text}")
    print(f"Target: {sample.target_text}")
    print(f"Answer: {sample.answer}")
    print()
```

### Use the skill tree

```python
from engram_generator.curriculum.registry import get_all_generators
from engram_generator.curriculum.skill_tree import SkillTree

generators = get_all_generators()
tree = SkillTree(generators, retention_ratio=0.1)

# Check what is unlocked
print(tree.get_unlocked_tasks())
print(tree.get_frontier_tasks())

# After validation, update with per-task accuracy
events = tree.update({"addition": 0.97, "subtraction": 0.85})
print(events)  # {"addition": "escalated to difficulty 2"}
```

### Validate generators

```bash
# Validate a specific task
engram-validate --task addition --difficulty 5 --samples 100 --verbose

# Validate an entire tier
engram-validate --tier 0 --samples 50

# Validate everything
engram-validate --all --samples 20

# Print the skill tree
engram-validate --skill-tree

# Stress test (1000 samples per task)
engram-validate --stress-test
```

### Tokenize samples

```python
from engram_generator.tokenizer import CharTokenizer

tok = CharTokenizer()
sample_text = "13278 + 46048 <step> 8+8=16 <step> 59326"

ids = tok.encode(sample_text)
step_mask = tok.get_step_mask(ids)  # True where <step> tokens are

# Use step_mask to set labels to -100 at <step> positions
# so the model is not penalised for step boundary tokens
```

## Testing

```bash
# Run full test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=engram_generator --cov-report=term
```

185 tests across 12 test modules covering:

- **Structural integrity** -- no orphan tasks, no dangling prerequisites, no backwards cross-tier dependencies, no duplicate names
- **Sample contracts** -- every generator produces non-empty input, target, answer, and step tokens
- **Determinism** -- identical seeds produce identical output
- **Difficulty scaling** -- higher difficulty yields harder problems
- **Skill tree** -- mastery tracking, difficulty escalation, prerequisite unlocking, sampling weights
- **Out-of-set (OOS)** -- held-out generators are valid, at tier 99, and separate from training
- **Knowledge atoms** -- 387 atoms loaded, linked to generators, valid fields
- **Tokenizer** -- roundtrip encode/decode, step token handling, vocabulary coverage
- **LaTeX renderer** -- fraction rendering, Unicode conversion, graceful fallback
- **Parallel generation** -- multiprocess correctness, determinism, mixed-task generation

**Coverage: 98%** (17,874 statements, 401 missed)

## Project Structure

```
engram_generator/
    __init__.py          # Package init with version and alpha disclaimer
    base.py              # Sample, Atom, StepGenerator base classes
    base_domains.py      # Domain-specific base classes (Formula, Scenario, Graph, ...)
    tokenizer.py         # Character-level tokenizer (75 tokens)
    latex_render.py      # LaTeX to Unicode terminal renderer
    parallel.py          # Multiprocess sample generation
    cli.py               # engram-validate CLI tool
    curriculum/
        registry.py      # Generator + OOS registration, prerequisite enrichment
        skill_tree.py    # Adaptive curriculum with mastery tracking
    generators/          # 42 domain-named modules, 373 generators
        arithmetic_core.py, arithmetic_ops.py, geometry.py, logic.py, ...
        meta_reasoning_t7.py ... meta_reasoning_t10.py
        oos.py           # Out-of-set held-out evaluation generators
    atoms/               # 387 knowledge atoms (theorems, definitions, formulas)
        registry.py      # Atom registration and lookup
        calculus.py, physics.py, geometry.py, ...
    validators/          # Sample validation utilities
tests/                   # 185 tests, 98% coverage
```

## License

MIT

## Organisation

[www.deepnet.one](https://www.deepnet.one)
