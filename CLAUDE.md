# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Procedural synthetic dataset generator for training reasoning AI. Each generator produces step-by-step mathematical/scientific problem-solution pairs. The output trains the Engram model (separate repo at `~/code/py/engram_model`).

## Commands

```bash
# Install
pip install -e ".[dev]"

# Run all tests
python -m pytest tests/ -q

# Run a single test file
python -m pytest tests/test_structural.py -v

# Run one test class or method
python -m pytest tests/test_structural.py::TestTierConsistency::test_total_count

# Validate a specific task
engram-validate --task addition --difficulty 5 --samples 100

# Validate an entire tier
engram-validate --tier 2 --samples 50

# Validate all generators
engram-validate --all --samples 20

# Preview samples
engram-validate --preview --task derivative --difficulty 3

# Print skill tree
engram-validate --skill-tree

# Stress test (many samples)
engram-validate --stress-test --samples 1000

# Run the audit (generates AUDIT_REPORT.md)
python scripts/audit.py --sample-size 20

# Lint
ruff check engram_generator/
```

## Architecture

### Core data flow

`StepGenerator._create_problem()` -> `_create_steps()` -> `_create_answer()` -> `Sample`

Every generator subclasses `StepGenerator` (in `base.py`) and implements four abstract methods:
- `_create_problem(difficulty)` -> `(latex_problem, solution_data_dict)`
- `_create_steps(solution_data)` -> `list[str]`
- `_create_answer(solution_data)` -> `str`
- `task_description(difficulty)` -> `str`

Plus three properties: `task_name`, `tier`, `prerequisites`.

The `generate(n)` method calls `_generate_one()` in a loop. `_generate_one()` retries with lower difficulty if the target exceeds 512 characters, and falls back to a skip marker if all retries fail.

### Registration system

Generators register themselves via the `@register` decorator from `curriculum.registry`. Importing `engram_generator.generators` triggers all `__init__.py` imports which execute the decorators. The `_REGISTRY` dict maps `task_name -> class`. OOS (out-of-set) generators use `@register_oos` and live in a separate registry -- they are never included in training data.

### Prerequisite graph

Each generator declares `prerequisites` (task names that must be mastered before this task unlocks). Additional cross-domain prerequisites are in `_EXTRA_PREREQUISITES` in `curriculum/registry.py`. The `SkillTree` class (`curriculum/skill_tree.py`) manages unlocking, difficulty escalation, and mastery tracking at training time.

**Constraint**: a generator's prerequisites must not have a higher tier than the generator itself. The `test_no_backwards_cross_tier` test enforces this.

### Tier system (0-10)

- Tiers 0-3: foundational (arithmetic, algebra, basic algorithms)
- Tiers 4-6: applied/expert (physics, calculus, linear algebra, graduate math)
- Tiers 7-8: meta-reasoning (proofs, analogies, problem construction)
- Tiers 9-10: research/self-architecture (algorithm design, scaling prediction, successor design)

Tier 0 tasks are unlocked at start. Higher tiers unlock when their prerequisites are mastered.

### Atoms

Knowledge atoms (`base.Atom`) are sourced theorems/definitions linked to generators. They live in `atoms/` modules and register via `atoms/registry.py`. Atoms are for human audit only -- the model never sees atom content during training. Each atom has: `atom_type`, `name`, `content`, `tier`, `domain`, `source`, `source_url`, `prerequisites`.

### Tokenizer

`CharTokenizer` in `tokenizer.py` -- every character is its own token (no subword merging). Special tokens: `<pad>`, `<eos>`, `<step>`. The `<step>` token separates problem, solution steps, and answer in the target string. The vocabulary is fixed at 72 tokens. All generator output must use only characters in `CharTokenizer.CHARS`.

### Target format

```
problem_latex <step> step_1 <step> step_2 <step> ... <step> answer
```

Max 512 characters. The `_generate_one()` method enforces this with difficulty reduction on overflow.

## Adding a new generator

1. Create a class in the appropriate `generators/` module (or new file)
2. Subclass `StepGenerator`, implement the four abstract methods + three properties
3. Decorate with `@register`
4. Ensure `tier` >= tier of all prerequisites
5. Import the module in `generators/__init__.py`
6. Create a matching atom in the appropriate `atoms/` module (optional but expected)
7. Update the generator count in `tests/test_structural.py` and `tests/test_skill_tree_full.py`

### Generator conventions

- `_create_problem` returns `(latex_string, data_dict)` -- the dict carries all computed values needed by steps and answer
- Steps show the work: each step is one logical operation the model should learn to reproduce
- Answers must be deterministic given the problem -- no ambiguity
- Use `self._rng` (seeded `random.Random`) for all randomness -- never `random.random()`
- Difficulty 1-8 scales operand magnitude, problem complexity, or term count
- Use `Fraction` from `fractions` for exact arithmetic when the answer involves ratios
- Helper classes go in the same file, above the generators that use them
- Google-style docstrings on all public methods and classes

## Key files

- `base.py` -- `Sample`, `Atom`, `StepGenerator` base class
- `curriculum/registry.py` -- `@register`, `_EXTRA_PREREQUISITES`, `get_all_generators()`
- `curriculum/skill_tree.py` -- `SkillTree`, `SkillNode` for adaptive curriculum
- `tokenizer.py` -- `CharTokenizer` (72-token character-level vocabulary)
- `generators/__init__.py` -- import order for all generator modules
- `atoms/registry.py` -- atom registration and lookup

## Test expectations

- `test_structural.py` enforces: total count matches, no backwards cross-tier prerequisites, no dangling prerequisites, deterministic output, sample contract (non-empty problem/steps/answer, `<step>` format)
- `test_skill_tree_full.py` enforces: all tasks present in skill tree, unlocking cascades work
- When adding generators, update the hardcoded count in both files
