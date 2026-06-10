# Engram Generator

A procedural synthetic dataset generator for training reasoning AI. **2,022 generators** across **100+ scientific domains** and **11 tiers** of difficulty, producing step-by-step problem-solution pairs that force models to learn algorithms rather than memorise answers.

> This repository contains AI-generated code, reviewed and directed by a human author.

## Why This Exists

Models trained on static datasets learn to pattern-match, not to reason. They memorise input-output mappings rather than learning the underlying algorithms. When faced with unseen problem structures, they collapse.

Engram Generator produces procedurally generated training data that forces models to learn **how to think, not what to answer**:

- **2,022 generators** across 100+ scientific domains
- **~100M+ unique problem combinations** -- memorisation is physically impossible
- **Step-by-step solution chains** -- the model must decompose and reason
- **26 reasoning patterns** with balanced training exposure
- **Adaptive difficulty** -- escalates as the model improves
- **Prerequisite skill tree** -- gates advanced reasoning behind mastery of foundations
- **Deterministic verification** -- every answer is provably correct by construction

## Domain Coverage

| Domain | Generators | Topics |
|---|---|---|
| **Mathematics** | 730+ | Arithmetic, algebra, calculus, analysis, topology, differential geometry, measure theory, functional analysis, algebraic geometry, category theory, homological algebra, number theory, combinatorics, PDEs, optimization |
| **Physics** | 200+ | Classical mechanics, electromagnetism, thermodynamics, special/general relativity, optics, fluids, nuclear, quantum mechanics, statistical mechanics, particle physics, nonlinear dynamics, solid state, plasma |
| **Computer Science** | 230+ | Algorithms, data structures, cryptography, formal languages, information theory, compilers, distributed systems, ML theory, computer graphics, robotics, formal verification, NLP |
| **Chemistry** | 80+ | General, physical, organic, inorganic, spectroscopy, polymer science |
| **Biology & Health** | 90+ | Genetics, biochemistry, cell biology, bioinformatics, ecology, epidemiology, pharmacology, neuroscience, systems biology, biostatistics |
| **Engineering** | 100+ | Signal processing, control theory, materials science, aerospace, power systems, antenna theory, semiconductor, photonics, structural, heat transfer, digital electronics |
| **Quantum** | 50+ | Quantum mechanics formalism, quantum information, quantum field theory, quantum error correction |
| **Earth & Space** | 30+ | Astronomy, geology, climate science, oceanography, geophysics |
| **Social & Cognitive** | 50+ | Economics, game theory, linguistics, decision theory, network science, cognitive science, causal inference |
| **Logic & Foundations** | 50+ | Formal logic, model theory, computability, proof theory, set theory |
| **Other** | 100+ | Music theory, financial mathematics, actuarial science, medical imaging, operations research, fuzzy logic, persistent homology, wavelet theory |

## Reasoning Patterns

Training is balanced across **26 distinct reasoning strategies**, not by generator count. Without this, formula-substitution problems (55% of generators) would dominate training.

| Pattern | Description | Sample allocation |
|---|---|---|
| Formula substitution | Plug values into formula | 3.8% |
| Symbolic manipulation | Differentiation, integration, simplification | 3.8% |
| Graph traversal | BFS, DFS, shortest path, flow | 3.8% |
| Dynamic programming | Optimal substructure, memoisation | 3.8% |
| Linear algebra | Matrix decomposition, solving systems | 3.8% |
| Probabilistic reasoning | Bayes, distributions, expectations | 3.8% |
| Logical deduction | Proofs, inference, validity checking | 3.8% |
| Meta-reasoning | Proof strategy, error analysis, design | 3.8% |
| ... (18 more patterns) | | 3.8% each |

Each pattern gets **equal representation** regardless of how many generators belong to it. A recursive decomposition problem (8 generators) gets the same training exposure as formula substitution (1,187 generators).

## Tier System

Tasks are organised into 11 tiers (0-10) with prerequisite dependencies:

| Tier | Tasks | Level | Examples |
|---|---|---|---|
| 0 | 20 | Basic arithmetic | Addition, subtraction, sorting, boolean evaluation |
| 1 | 36 | Operations | Multiplication, division, Fibonacci, Caesar cipher |
| 2 | 47 | Intermediate | Modular arithmetic, derivatives, quadratics, graph reachability |
| 3 | 95 | Advanced | Integrals, determinants, base conversion, boolean algebra |
| 4 | 313 | Applied | Physics, matrix operations, probability, dynamic programming |
| 5 | 730 | Expert | Calculus depth, PDEs, cryptography, quantum mechanics |
| 6 | 521 | Graduate | Abstract algebra, topology, general relativity, information theory |
| 7 | 176 | Meta-reasoning | Proof construction, error detection, generalisation |
| 8 | 31 | Creative | Conjecture, problem transformation, isomorphism detection |
| 9 | 29 | Research | Algorithm design, impossibility proofs, hypothesis testing |
| 10 | 24 | Self-architecture | Scaling prediction, architecture analysis, loss design |

## The Arc

A model trained on this curriculum progresses from basic arithmetic to self-architectural reasoning:

```
2 + 3 = 5
    |
d/dx(3x^2 + 2x) = 6x + 2
    |
curl F = (dFz/dy - dFy/dz, ...)
    |
"This proof has an error in step 3. Here is the correction."
    |
"These two problems share an isomorphic structure."
    |
"To solve this class of problems, I would design the following algorithm."
    |
"My architecture struggles with length generalisation.
 Here is a proposed modification."
```

From following procedures to creating them. From solving problems to understanding what makes problems solvable.

## Samples

Each training sample has three parts:

```
Input:  add two 5 digit numbers
Target: 13278 + 46048 <step> 8+8=16 <step> 7+4+1=12 <step> 2+0+1=3 <step> 3+6=9 <step> 1+4=5 <step> 59326
```

- **Input**: short natural language task description
- **Target**: problem statement, solution steps, and final answer separated by `<step>` tokens
- Both capped at **512 characters**

## Tokenizer

Character-level tokenizer with 72 tokens. Every character is its own token -- no subword merging. This preserves digit atomicity (critical for arithmetic) and LaTeX structure (brace matching).

## Information Capacity

| Metric | Value |
|---|---|
| Unique problem combinations | ~100M+ (conservative) |
| Instance information | ~10 GB |
| Algorithmic information (compressed source) | ~1.85 MB |
| Compression ratio | ~5,700x |

A 13M parameter model is **6,500x too small** to memorise the dataset. A 1B model is **85x too small**. The model **must** learn the algorithms.

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
```

### Use the skill tree

```python
from engram_generator.curriculum.registry import get_all_generators
from engram_generator.curriculum.skill_tree import SkillTree

generators = get_all_generators()
tree = SkillTree(generators, retention_ratio=0.1)

print(tree.get_unlocked_tasks())
events = tree.update({"addition": 0.97, "subtraction": 0.85})
```

### Pattern-balanced sampling

```python
from engram_generator.curriculum.reasoning_patterns import (
    get_pattern_weights, get_pattern_summary,
)
from engram_generator.curriculum.registry import get_all_generators

gens = get_all_generators()
weights = get_pattern_weights(gens)
summary = get_pattern_summary(gens)

# Each of the 26 reasoning patterns gets equal training exposure
for pattern, count in sorted(summary.items(), key=lambda x: -x[1])[:5]:
    print(f"{pattern}: {count} generators -> 3.8% of training samples")
```

### Validate generators

```bash
engram-validate --all --samples 20
engram-validate --skill-tree
engram-validate --task addition --difficulty 5 --samples 100
```

## Testing

```bash
python -m pytest tests/ -v
```

**6,326 tests** across 16 test modules:

- **Sanity tests** (6,066): every generator tested at low difficulty, high difficulty, and determinism
- **Correctness tests** (75): independent mathematical verification of answers
- **Structural tests** (185): no orphans, no dangling prerequisites, no backwards cross-tier dependencies
- **Coverage: 99%** (77,452 statements, 1,104 missed)

## License

MIT

## Organisation

[www.deepnet.one](https://www.deepnet.one)
