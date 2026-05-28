# Engram Generator Audit Report

Generated: 2026-05-28 10:11:49
Seed: 42 | Samples/generator: 10

## Executive Summary

- **Pass**: 21
- **Info**: 6
- **Warning**: 0
- **Fail**: 0

## Code Quality

| Check | Status | Details |
|---|---|---|
| docstrings | INFO | 3/1736 public methods missing docstrings |
| method_size | PASS | All methods under 50 lines |
| duplication | INFO | 3 groups of duplicated _create_answer (30 total) |
| dead_code | INFO | ScenarioGenerator defined but never subclassed |
| encapsulation | INFO | 12 public attributes in __init__: engram_generator/generators/applied_math.py:PolynomialTerm.coefficient, engram_generator/generators/applied_math.py:PolynomialTerm.exponent, engram_generator/generators/applied_math.py:BivariateTermFormatter.coefficient, engram_generator/generators/applied_math.py:BivariateTermFormatter.x_exp, engram_generator/generators/applied_math.py:BivariateTermFormatter.y_exp |

## Structural Integrity

| Check | Status | Details |
|---|---|---|
| dangling_prereqs | PASS | 0 dangling prerequisites |
| backwards_prereqs | PASS | 0 backwards cross-tier prereqs |
| cycles | PASS | No cycles in prerequisite graph |
| reachability | PASS | All 373 tasks reachable |
| atom_count | PASS | 387 atoms registered |
| atom_fields | PASS | All atoms have valid fields |
| registry_size | PASS | Registry: 373 generators |
| oos_registry | PASS | OOS registry: 5 generators |

## Robustness

| Check | Status | Details |
|---|---|---|
| determinism | PASS | All 373 generators deterministic |
| bare_except | PASS | 0 bare except |
| broad_except | INFO | 6 broad except Exception: ['engram_generator/latex_render.py:37', 'engram_generator/latex_render.py:54', 'engram_generator/latex_render.py:71', 'engram_generator/latex_render.py:224', 'engram_generator/latex_render.py:280', 'engram_generator/base.py:241'] |
| parallel_safety | PASS | ParallelGenerator: 50/50 samples |

## Data Quality

| Check | Status | Details |
|---|---|---|
| target_lengths | INFO | 558/3730 exceed 256 chars, 0/3730 exceed 512. Longest: batch_norm (511 chars) |
| empty_answers | PASS | All answers non-empty |
| skip_answers | PASS | No skip fallbacks |
| latex_braces | PASS | All braces balanced |
| tokenizer_coverage | PASS | All output characters in tokenizer vocabulary |

## Correctness

| Check | Status | Details |
|---|---|---|
| step_answer | PASS | All 373 generators consistent |
| edge_crashes | PASS | No boundary crashes |
| edge_empty | PASS | No empty answers at boundaries |

## Performance

| Check | Status | Details |
|---|---|---|
| gen_speed | PASS | All 373 under 100ms/sample |
| skill_tree | PASS | Skill tree: 0.5ms/update (100 cycles) |
