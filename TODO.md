# Engram Generator -- Roadmap

Current: **v0.1.0** -- 2,022 generators across 100+ scientific domains.

## Next: Python Verification Fallback (evaluation module)

Add a `PythonVerifier` as a third evaluation tier:

1. Step exact match (after normalisation) -- fast, first pass
2. ROUGE-L / similarity -- catches near-misses
3. **Python verification (fallback)** -- for steps that fail 1 and 2, parse the arithmetic expression and evaluate it in Python to check if the maths is correct even if the format differs

This catches cases where an LLM uses a different but valid reasoning strategy (e.g. square-and-multiply instead of repeated multiplication for exponentiation, or starting GCD from either operand).

Requirements:
- Sandboxed eval (no arbitrary code execution)
- Only runs on failures from levels 1 and 2
- Reports "format mismatch but computationally correct" vs "genuinely wrong"
- Handles LaTeX notation parsing for expressions like `\frac{1}{2}`, `\mod`, `\gcd`

## Next: Depth & Coverage (v0.2.0)

### Missing domains to add

| Domain | Gap | Target generators |
|---|---|---|
| Medicine & clinical reasoning | Not covered | Diagnosis, pharmacokinetics, imaging interpretation |
| Law & legal reasoning | Not covered | Case analysis, statutory interpretation, precedent chains |
| Philosophy & epistemology | Not covered | Argument validity, fallacy identification, thought experiments |
| History & social science methods | Not covered | Source analysis, causal reasoning from evidence |
| Advanced linguistics | Shallow | Syntax transformations, semantic parsing, pragmatics |
| Systems biology | Shallow | Pathway analysis, flux balance, regulatory networks |
| Computational neuroscience | Shallow | Neural coding, population decoding, learning rules |

### Deepen existing domains

| Domain | Current | Needed |
|---|---|---|
| First-order logic | ASCII notation only | Full FOL with proper notation (requires tokenizer expansion) |
| Organic chemistry | Reaction types | Retrosynthesis chains, mechanism arrow-pushing |
| Differential geometry | Basic curvature | Fibre bundles, connections, characteristic classes |
| Algebraic topology | Euler/Betti/homology | Spectral sequences, cohomology operations |
| QFT | Tree-level only | Loop corrections, renormalisation, path integrals |
| Category theory | Small categories | Topos theory depth, higher categories |

### Update generators to use new tokenizer symbols

Tokenizer already expanded to 135 vocab (v0.1.0) with Greek letters,
logic symbols, math relations, and calculus notation. Generators still
produce ASCII workarounds (`alpha`, `<=`, `forall`). Migrate to proper
symbols (α, ≤, ∀) incrementally.

## Later: New modalities (v0.3.0)

### Code generation

Generators that output executable code as step-by-step targets:

- `python_sort` -- implement sorting algorithm, verified by execution
- `python_binary_search` -- implement search, verified by test cases
- `python_graph_bfs` -- implement BFS, verified by path correctness
- ~50-100 generators covering standard algorithms and data structures
- Requires sandboxed execution for verification (not just algebraic construction)

### Tool calling

Generators that produce structured tool-call sequences:

- `api_weather_query` -- decompose "What's the weather in London?" into API calls
- `api_multi_step` -- chain multiple tool calls with state tracking
- `api_error_recovery` -- handle tool failures and retry logic
- ~30-50 generators covering common agentic patterns

### Agentic reasoning

Multi-step observation-action-reward chains:

- `plan_and_execute` -- decompose goal into sub-tasks, execute sequentially
- `react_loop` -- interleave reasoning and action
- `tool_selection` -- choose appropriate tool from a set given a task
- Requires new sample format (not just input/target pairs)

## Infrastructure

- [ ] GitHub Actions workflow for PyPI trusted publishing
- [ ] Automated test runs on PR
- [ ] Benchmark suite: generation speed, memory usage, correctness rates
- [ ] Multi-language task descriptions (same algorithm, different natural languages)
- [ ] Difficulty auto-scaling based on model accuracy feedback
