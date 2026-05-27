# Engram Generator

> **Alpha Version** — Not yet tested at scale. Not yet fully reviewed. Use at your own peril.

> This repository contains AI-generated code, reviewed and directed by a human author.

An infinite synthetic dataset generator for training reasoning, logic, and algorithmic learning in neural networks.

## Purpose

Models trained on static datasets learn to pattern-match, not to reason. They memorise input-output mappings rather than learning the underlying algorithms. When faced with unseen problem structures, they collapse.

Engram Generator produces procedurally generated training data that forces models to learn **how to think, not what to answer**:

- **Infinite non-repeating data** — every sample is unique, memorisation is impossible
- **Step-by-step solution chains** — the model must learn to decompose and reason, not guess
- **Adaptive difficulty** — escalates as the model improves, always training at the frontier
- **Prerequisite skill tree** — gates advanced reasoning behind mastery of foundations
- **Deterministic verification** — every answer is provably correct by construction

The scope spans arithmetic, algebra, calculus, physics, computer science, graph theory, cryptography, formal logic, proof verification, and meta-reasoning. But the goal is not domain coverage. It is to teach a model to **decompose problems into steps, maintain state across those steps, and verify its own work** — the foundation for genuine reasoning.

## Architecture

### Samples

Each training sample has three parts:

```
Input:  add two 5 digit numbers
Target: 13278 + 46048 <step> 8+8=16 <step> 7+4+1=12 <step> 2+0+1=3 <step> 3+6=9 <step> 1+4=5 <step> 59326
```

- **Input**: short natural language task description
- **Target**: problem statement, solution steps, and final answer separated by `<step>` tokens
- `<step>` is a special token excluded from loss computation — the model is only scored on mathematical content

### Three interaction modes

**Mode A — Apply formula**: formula given, solve with values
```
Input:  apply \frac{1}{2}mv^2 where m=5 v=3
Target: \frac{1}{2}(5)(3^2) <step> \frac{1}{2}(5)(9) <step> \frac{45}{2} <step> 22.5
```

**Mode B — Recall formula**: describe concept, model produces LaTeX
```
Input:  express kinetic energy in latex
Target: KE = \frac{1}{2}mv^2
```

**Mode C — Full solve**: describe task, model formulates and solves
```
Input:  find gravitational force between earth and 70kg person
Target: F = \frac{GMm}{r^2} <step> \frac{(6.67e-11)(5.97e24)(70)}{(6.37e6)^2} <step> 686.4
```

### Skill Tree

Tasks are organised into 11 tiers (0-10) with prerequisite dependencies:

```
Tier  0: Basic arithmetic (addition, subtraction, sorting)
Tier  1: Operations (multiplication, division, basic equations)
Tier  2: Intermediate (polynomials, number theory, graphs)
Tier  3: Advanced (calculus, probability, linear algebra)
Tier  4: Applied (physics, quantum mechanics, advanced algebra)
Tier  5: Expert (PDEs, transforms, neural network mathematics)
Tier  6: Graduate (tensors, differential geometry, information theory)
Tier  7: Meta-reasoning (proofs, error detection, multi-domain synthesis)
Tier  8: Creative (abstraction, conjecture, self-evaluation)
Tier  9: Research (algorithm design, architecture analysis, learning theory)
Tier 10: Self-architecture (gradient analysis, successor design, failure diagnosis)
```

A task only unlocks when its prerequisites are mastered. The model cannot attempt derivatives until it masters polynomial evaluation. It cannot attempt tensor calculus until it masters partial derivatives and matrix inversion.

### Adaptive Difficulty

Each epoch, the system checks per-task accuracy:
- **Above 95%**: difficulty escalates (harder instances)
- **Above 90%**: task is considered mastered, prerequisites unlock
- **Below 50%**: task receives extra training samples (frontier weighting)

The final output is a **competency map**: which tasks the model mastered, at what difficulty, forming a profile of mathematical capability.

### Knowledge Atoms

Upper tiers (7-10) require domain knowledge beyond what procedural generation provides. Knowledge atoms are self-contained units of mathematical knowledge:

```
Input:  theorem: chain rule
Target: if y=f(g(x)) then \frac{dy}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}
```

Atoms are:
- Self-contained (no external references)
- LaTeX throughout
- One idea per atom
- Sourced from Wikipedia, ProofWiki, Wolfram MathWorld, arXiv, or synthetically generated
- Paired with synthetic tasks that apply the knowledge

### Tokenizer

Character-level tokenizer with 61 tokens:
- Digits: `0-9`
- Letters: `a-z`
- Operators: `+ - / * ^ ( ) = : ; ? . ,`
- LaTeX: `\ { } _ & ~`
- Special: `<pad>`, `<eos>`, `<step>`
- Additional: `| !`

Every character is its own token. No subword chunking — each digit is atomic, enabling algorithmic reasoning over individual digit positions.

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

# Check what's unlocked
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

## Task Count

| Tier | Description | Tasks |
|---|---|---|
| 0 | Basic arithmetic (addition, subtraction, sorting) | 20 |
| 1 | Operations (multiplication, division, basic equations) | 36 |
| 2 | Intermediate (polynomials, number theory, graphs) | 46 |
| 3 | Advanced (calculus, probability, linear algebra) | 59 |
| 4 | Applied (physics, quantum mechanics, advanced algebra) | 57 |
| 5 | Expert (PDEs, transforms, neural network mathematics) | 55 |
| 6 | Graduate (tensors, differential geometry, information theory) | 42 |
| 7 | Meta-reasoning (proofs, error detection, multi-domain synthesis) | 18 |
| 8 | Creative (abstraction, conjecture, self-evaluation) | 13 |
| 9 | Research (algorithm design, architecture analysis, learning theory) | 14 |
| 10 | Self-architecture (gradient analysis, successor design, failure diagnosis) | 13 |
| **Total** | | **373** |

## The Arc

A model trained on this curriculum progresses from basic arithmetic to
self-architectural reasoning:

```
2 + 3 = 5
    ↓
\frac{d}{dx}(3x^2 + 2x) = 6x + 2
    ↓
\nabla \times \vec{F} = ...
    ↓
"This proof has an error in step 3 — here is the correction"
    ↓
"These two problems share an isomorphic structure"
    ↓
"To solve this class of problems, I would design the following algorithm"
    ↓
"My architecture struggles with this because gradient vanishes at layer 3.
 Here is a proposed modification."
```

From following procedures to creating them. From solving problems to
understanding what makes problems solvable.

## Verification

All generated data is provably correct by construction. Verification
strategies vary by tier:

- **Tiers 0-6**: Direct computation (Python computes the answer)
- **Tier 7**: Property checking (constraints satisfied, algebraic equivalence)
- **Tier 8**: Multi-point evaluation (formula correct at unseen test points)
- **Tier 9**: Empirical testing (proposed algorithm runs correctly)
- **Tier 10**: Implementation testing (proposed modification benchmarked)

## License

MIT

## Author

Alex Giokas
