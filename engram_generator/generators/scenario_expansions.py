"""Expanded scenario pools for meta-reasoning generators.

Adds additional scenarios to generators with small hardcoded pools,
bringing each from ~4 to ~12 unique scenarios without modifying
the original generator files.

This module is imported after the generators, so it can access and
extend their class-level data dictionaries.
"""
from engram_generator.generators.meta_reasoning_t9 import (
    AlgorithmImprovementGenerator,
    FailureAnalysisGenerator,
    ImpossibilityProofGenerator,
)
from engram_generator.generators.meta_reasoning_t10 import (
    LossDesignGenerator,
    SuccessorDesignGenerator,
)
from engram_generator.generators.meta_reasoning_ext import (
    MinimalAxiomsGenerator,
    HypothesisDesignGenerator,
    ReductionGenerator,
    RepresentationChoiceGenerator,
    DataPrescriptionGenerator,
)


# ── AlgorithmImprovement: 4 → 12 ──────────────────────────────────

_EXTRA_IMPROVEMENTS = {
    5: "matrix_chain",
    6: "string_matching",
    7: "graph_coloring",
    8: "convex_hull",
}
AlgorithmImprovementGenerator._IMPROVEMENTS.update(_EXTRA_IMPROVEMENTS)
AlgorithmImprovementGenerator._NAIVE.update({
    "matrix_chain": "try all parenthesisations: O(4^n / n^1.5)",
    "string_matching": "check every position: O(nm)",
    "graph_coloring": "try all k-colorings: O(k^n)",
    "convex_hull": "check all triples for boundary: O(n^3)",
})
AlgorithmImprovementGenerator._IMPROVED.update({
    "matrix_chain": "dynamic programming: O(n^3)",
    "string_matching": "KMP: O(n+m) with failure function",
    "graph_coloring": "greedy with degree ordering: O(V+E)",
    "convex_hull": "Graham scan: O(n log n)",
})
AlgorithmImprovementGenerator._INSIGHTS.update({
    "matrix_chain": "overlapping subproblems — memoize subchain costs",
    "string_matching": "reuse partial match info via failure function",
    "graph_coloring": "process high-degree vertices first to reduce conflicts",
    "convex_hull": "sort by angle, maintain convex invariant with stack",
})
AlgorithmImprovementGenerator._TEST_INPUTS.update({
    "matrix_chain": [10, 30, 5, 60],
    "string_matching": [1, 0, 1, 0, 1, 1],
    "graph_coloring": [1, 2, 3, 4, 5],
    "convex_hull": [0, 3, 1, 1, 2, 4],
})
AlgorithmImprovementGenerator._TEST_RESULTS.update({
    "matrix_chain": "optimal cost 4500",
    "string_matching": "pattern found at index 2",
    "graph_coloring": "3 colors sufficient",
    "convex_hull": "hull: (0,3),(2,4),(1,1)",
})


# ── FailureAnalysis: 4 → 10 ───────────────────────────────────────

FailureAnalysisGenerator._FAILURE_TYPES.update({
    5: "infinite_loop",
    6: "stack_overflow",
    7: "race_condition",
    8: "null_pointer",
})
FailureAnalysisGenerator._ALGORITHMS.update({
    "infinite_loop": "while x != target: x = f(x)",
    "stack_overflow": "def recurse(n): return recurse(n+1)",
    "race_condition": "counter += 1 (two threads, no lock)",
    "null_pointer": "return node.left.value",
})
FailureAnalysisGenerator._FAILING_INPUTS.update({
    "infinite_loop": "f(x) cycles: f(3)=5, f(5)=3, target=7",
    "stack_overflow": "n=1000000 (exceeds stack depth)",
    "race_condition": "two threads increment counter 1000 times each",
    "null_pointer": "node.left is None",
})
FailureAnalysisGenerator._FAILURE_EXPLANATIONS.update({
    "infinite_loop": [
        "f creates cycle: 3 -> 5 -> 3 -> ...",
        "target 7 is unreachable from this cycle",
        "loop never terminates",
        "fix: add visited set or iteration limit",
    ],
    "stack_overflow": [
        "no base case to stop recursion",
        "each call adds to stack",
        "stack depth exceeded at ~10000 frames",
        "fix: add base case or convert to iteration",
    ],
    "race_condition": [
        "read-modify-write is not atomic",
        "thread A reads 5, thread B reads 5",
        "both write 6 instead of 7",
        "fix: use mutex/lock or atomic increment",
    ],
    "null_pointer": [
        "node.left may be None",
        "accessing .value on None raises error",
        "fix: check if node.left is not None before access",
    ],
})
FailureAnalysisGenerator._BUG_NAMES.update({
    "infinite_loop": "infinite loop (no termination)",
    "stack_overflow": "stack overflow (missing base case)",
    "race_condition": "race condition (unsynchronised access)",
    "null_pointer": "null pointer dereference",
})


# ── ImpossibilityProof: 4 → 8 ─────────────────────────────────────

ImpossibilityProofGenerator._PROBLEMS.update({
    "matrix_multiply": "matrix multiplication",
    "convex_hull": "convex hull in 2D",
    "comparison_sort": "comparison-based sorting (general)",
    "connectivity": "graph connectivity (undirected)",
})
ImpossibilityProofGenerator._BOUNDS.update({
    "matrix_multiply": "Omega(n^2) (must read all entries)",
    "convex_hull": "Omega(n log n) (reduces from sorting)",
    "comparison_sort": "Omega(n log n) (decision tree argument)",
    "connectivity": "Omega(V + E) (must examine all edges)",
})
ImpossibilityProofGenerator._PROOF_STEPS.update({
    "matrix_multiply": [
        "result matrix has n^2 entries",
        "each entry depends on at least one input entry",
        "must read Omega(n^2) inputs",
    ],
    "convex_hull": [
        "reduce sorting to convex hull: given x1..xn, map to (xi, xi^2)",
        "convex hull of parabola gives sorted order",
        "sorting is Omega(n log n), so convex hull is too",
    ],
    "comparison_sort": [
        "n! possible permutations of n elements",
        "each comparison is a binary decision",
        "decision tree has n! leaves, height >= log2(n!) = Omega(n log n)",
    ],
    "connectivity": [
        "adversary can hide a disconnecting edge",
        "algorithm must check all edges to be certain",
        "lower bound: Omega(V + E)",
    ],
})


# ── LossDesign: 4 → 10 ────────────────────────────────────────────

LossDesignGenerator._LOSS_TYPES.update({
    5: "contrastive",
    6: "triplet",
    7: "focal",
    8: "dice",
})
LossDesignGenerator._BEHAVIOURS.update({
    "contrastive": "pull similar items together and push dissimilar apart",
    "triplet": "ensure anchor is closer to positive than negative by margin",
    "focal": "focus training on hard misclassified examples",
    "dice": "maximise overlap between predicted and ground truth segmentation",
})


# ── SuccessorDesign: 4 → 10 ───────────────────────────────────────

SuccessorDesignGenerator._LIMITATION_TYPES.update({
    5: "poor_calibration",
    6: "catastrophic_forgetting",
    7: "mode_collapse",
    8: "gradient_starvation",
})
SuccessorDesignGenerator._LIMITATIONS.update({
    "poor_calibration": "model confidence doesn't match actual accuracy",
    "catastrophic_forgetting": "fine-tuning destroys pretrained knowledge",
    "mode_collapse": "generator produces only a few distinct outputs",
    "gradient_starvation": "some components receive near-zero gradient signal",
})
SuccessorDesignGenerator._BOTTLENECKS.update({
    "poor_calibration": "softmax temperatures not calibrated to accuracy",
    "catastrophic_forgetting": "weight updates for new task overwrite old task knowledge",
    "mode_collapse": "discriminator saturates, generator finds single mode",
    "gradient_starvation": "loss dominated by one objective, others starve",
})
SuccessorDesignGenerator._PROPOSALS.update({
    "poor_calibration": "add temperature scaling layer trained on held-out validation set",
    "catastrophic_forgetting": "use EWC: penalise changes to weights important for old tasks",
    "mode_collapse": "use minibatch discrimination + diverse training objectives",
    "gradient_starvation": "use GradNorm or uncertainty weighting to balance loss components",
})


# ── MinimalAxioms: extend axiom sets ──────────────────────────────

_extra_axiom_sets = [
    {
        "axioms": ["a*b=b*a", "a*1=a", "1*a=a", "a*(b*c)=(a*b)*c"],
        "redundant_idx": 2,
        "redundant_name": "A3",
        "derivation": "by A1, 1*a = a*1 = a (by A2)",
        "minimal": ["a*b=b*a", "a*1=a", "a*(b*c)=(a*b)*c"],
    },
    {
        "axioms": ["a+(-a)=0", "0+a=a", "a+0=a", "a+b=b+a"],
        "redundant_idx": 2,
        "redundant_name": "A3",
        "derivation": "by A4, a+0 = 0+a = a (by A2)",
        "minimal": ["a+(-a)=0", "0+a=a", "a+b=b+a"],
    },
    {
        "axioms": ["a∪b=b∪a", "a∪∅=a", "∅∪a=a", "a∪a=a"],
        "redundant_idx": 2,
        "redundant_name": "A3",
        "derivation": "by A1, ∅∪a = a∪∅ = a (by A2)",
        "minimal": ["a∪b=b∪a", "a∪∅=a", "a∪a=a"],
    },
    {
        "axioms": ["max(a,b)=max(b,a)", "max(a,a)=a", "max(a,-inf)=a", "-inf <= a"],
        "redundant_idx": 3,
        "redundant_name": "A4",
        "derivation": "A4 follows from A3: max(a,-inf)=a implies -inf <= a",
        "minimal": ["max(a,b)=max(b,a)", "max(a,a)=a", "max(a,-inf)=a"],
    },
]

# Append to the generator's _get_axiom_sets pool
_orig_get_axiom_sets = MinimalAxiomsGenerator._get_axiom_sets

def _expanded_get_axiom_sets(self, difficulty):
    """Extended axiom sets with 4 additional entries."""
    base = _orig_get_axiom_sets(self, difficulty)
    return base + _extra_axiom_sets

MinimalAxiomsGenerator._get_axiom_sets = _expanded_get_axiom_sets


# ── HypothesisDesign: extend experiment types ─────────────────────

HypothesisDesignGenerator._EXPERIMENT_TYPES.update({
    5: "regularisation",
    6: "architecture",
    7: "tokenisation",
    8: "curriculum",
})

HypothesisDesignGenerator._EXPERIMENTS = getattr(
    HypothesisDesignGenerator, '_EXPERIMENTS', {}
)
HypothesisDesignGenerator._EXPERIMENTS.update({
    "regularisation": {
        "hypothesis": "L2 weight decay reduces overfitting",
        "control": "fix model, data, learning rate, epochs",
        "variable": "weight_decay: {0, 1e-4, 1e-3, 1e-2}",
        "measure": "train-val accuracy gap",
        "criterion": "helps if gap reduces by > 5%",
        "conditions": 4,
    },
    "architecture": {
        "hypothesis": "residual connections improve deep network training",
        "control": "fix depth, width, data, learning rate",
        "variable": "skip connections: {none, every 2 layers}",
        "measure": "final validation accuracy",
        "criterion": "helps if accuracy improves by > 3%",
        "conditions": 2,
    },
    "tokenisation": {
        "hypothesis": "character-level tokenisation helps arithmetic",
        "control": "fix model size, data, training steps",
        "variable": "tokeniser: {BPE 30K, character-level}",
        "measure": "exact match on multi-digit addition",
        "criterion": "character helps if accuracy > 20% higher",
        "conditions": 2,
    },
    "curriculum": {
        "hypothesis": "difficulty curriculum speeds convergence",
        "control": "fix model, data distribution, total steps",
        "variable": "ordering: {random, easy-to-hard, hard-to-easy}",
        "measure": "steps to reach 90% accuracy",
        "criterion": "easy-to-hard helps if fewer steps needed",
        "conditions": 3,
    },
})


# ── Reduction: extend reduction types ─────────────────────────────

ReductionGenerator._REDUCTION_TYPES.update({
    5: "halting_to_equivalence",
    6: "clique_to_independent",
    7: "sat_to_coloring",
    8: "sorting_to_selection",
})

ReductionGenerator._REDUCTIONS = getattr(ReductionGenerator, '_REDUCTIONS', {})
ReductionGenerator._REDUCTIONS.update({
    "halting_to_equivalence": {
        "from": "halting problem", "to": "program equivalence",
        "steps": [
            "given program P, construct Q that ignores input and runs P",
            "P halts iff Q is equivalent to a program that always halts",
            "if we could decide equivalence, we could decide halting",
            "halting is undecidable, so equivalence is undecidable",
        ],
        "bound": "undecidable",
        "test_input": "P = while(true) {}",
        "test_result": "P never halts, so Q != halt_program",
    },
    "clique_to_independent": {
        "from": "clique", "to": "independent set",
        "steps": [
            "take complement graph G' (edges become non-edges)",
            "clique in G = independent set in G'",
            "finding max clique reduces to finding max independent set",
        ],
        "bound": "NP-hard",
        "test_input": "K3 in G -> independent set of 3 in G'",
        "test_result": "complement preserves size",
    },
    "sat_to_coloring": {
        "from": "3-SAT", "to": "3-coloring",
        "steps": [
            "create gadget for each variable (true/false nodes)",
            "create gadget for each clause",
            "3-colorable iff satisfiable",
        ],
        "bound": "NP-hard",
        "test_input": "(x1 OR x2) AND (NOT x1 OR x3)",
        "test_result": "graph with 3-coloring encodes satisfying assignment",
    },
    "sorting_to_selection": {
        "from": "sorting", "to": "selection (kth smallest)",
        "steps": [
            "if we can select kth element in f(n)",
            "sort by selecting 1st, 2nd, ..., nth element",
            "n selections = n * f(n)",
            "but selection has Theta(n) algorithm, so this gives O(n^2) sort",
            "this is a WEAK reduction — doesn't prove lower bound",
        ],
        "bound": "Theta(n) for selection",
        "test_input": "[3,1,4,1,5], k=3",
        "test_result": "3rd smallest = 3",
    },
})


# ── RepresentationChoice: extend choice types ─────────────────────

RepresentationChoiceGenerator._CHOICE_TYPES.update({
    5: "dense_vs_sparse",
    6: "float_vs_fixed",
    7: "row_vs_col_major",
    8: "index_vs_scan",
})

RepresentationChoiceGenerator._CHOICES = getattr(
    RepresentationChoiceGenerator, '_CHOICES', {}
)
RepresentationChoiceGenerator._CHOICES.update({
    "dense_vs_sparse": {
        "problem": "store and multiply large matrices with >95% zeros",
        "options": [
            {"name": "dense array", "space": "O(n^2)", "access": "O(1)", "multiply": "O(n^3)"},
            {"name": "CSR sparse", "space": "O(nnz)", "access": "O(log nnz)", "multiply": "O(nnz)"},
        ],
        "winner": "CSR sparse",
        "reason": "95% zeros means nnz << n^2, massive space and compute savings",
    },
    "float_vs_fixed": {
        "problem": "neural network inference on edge device with limited precision",
        "options": [
            {"name": "float32", "space": "4 bytes", "accuracy": "full", "speed": "slow on edge"},
            {"name": "int8 fixed", "space": "1 byte", "accuracy": "~1% loss", "speed": "4x faster"},
        ],
        "winner": "int8 fixed",
        "reason": "4x speedup and 4x memory reduction for ~1% accuracy loss",
    },
    "row_vs_col_major": {
        "problem": "iterate over rows of a large matrix frequently",
        "options": [
            {"name": "row-major (C)", "access": "sequential reads", "cache": "excellent"},
            {"name": "col-major (Fortran)", "access": "strided reads", "cache": "poor for row access"},
        ],
        "winner": "row-major",
        "reason": "sequential memory access maximises cache line utilisation",
    },
    "index_vs_scan": {
        "problem": "10M records, query by exact key 1000 times/sec",
        "options": [
            {"name": "B-tree index", "space": "O(n)", "query": "O(log n)", "build": "O(n log n)"},
            {"name": "sequential scan", "space": "O(1)", "query": "O(n)", "build": "O(1)"},
        ],
        "winner": "B-tree index",
        "reason": "1000 queries/sec * O(n) scan is infeasible; index amortises build cost",
    },
})


# ── DataPrescription: extend weakness types ───────────────────────

DataPrescriptionGenerator._WEAKNESS_TYPES.update({
    5: "class_imbalance",
    6: "distribution_shift",
    7: "label_noise",
    8: "domain_gap",
})

DataPrescriptionGenerator._WEAKNESSES = getattr(
    DataPrescriptionGenerator, '_WEAKNESSES', {}
)
DataPrescriptionGenerator._WEAKNESSES.update({
    "class_imbalance": {
        "weakness": "model ignores minority class (1% of data)",
        "root_cause": "severe class imbalance in training data",
        "data_type": "oversampled minority class examples + synthetic via SMOTE",
        "quantity": 10000,
        "spec": "balance classes to 50/50 or use focal loss weighting",
    },
    "distribution_shift": {
        "weakness": "model trained on clean images fails on noisy real-world photos",
        "root_cause": "training distribution doesn't match deployment distribution",
        "data_type": "augmented images: blur, noise, lighting variation, occlusion",
        "quantity": 20000,
        "spec": "match deployment noise characteristics in training data",
    },
    "label_noise": {
        "weakness": "model memorises incorrect labels",
        "root_cause": "5-10% of training labels are wrong",
        "data_type": "cleaned labels via majority vote of 3 annotators",
        "quantity": 0,
        "spec": "re-annotate suspicious samples (high loss after convergence)",
    },
    "domain_gap": {
        "weakness": "model trained on English fails on French inputs",
        "root_cause": "no multilingual data in training set",
        "data_type": "parallel corpus and translated examples",
        "quantity": 50000,
        "spec": "add target-language data, consider multilingual pretraining",
    },
})
