"""Expanded scenario pools for meta-reasoning generators.

Adds additional scenarios to generators with small hardcoded pools,
bringing each from ~4 to ~12 unique scenarios without modifying
the original generator files.

This module is imported after the generators, so it can access and
extend their class-level data dictionaries.
"""
from engram_generator.generators.meta_reasoning_t9 import (
    AlgorithmTemplate,
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
    "matrix_chain": AlgorithmTemplate("matrix_chain_naive",
        ["enumerate parenthesisations", "compute cost for each", "return minimum"], "O(4^n/n^1.5)"),
    "string_matching": AlgorithmTemplate("string_match_naive",
        ["for each position i", "check if pattern matches at i", "return i if match"], "O(nm)"),
    "graph_coloring": AlgorithmTemplate("coloring_naive",
        ["for each possible k-coloring", "check validity", "return first valid"], "O(k^n)"),
    "convex_hull": AlgorithmTemplate("hull_naive",
        ["for each triple", "check all others on one side", "collect boundary"], "O(n^3)"),
})
AlgorithmImprovementGenerator._IMPROVED.update({
    "matrix_chain": AlgorithmTemplate("matrix_chain_dp",
        ["define dp[i][j] = min cost for i..j", "try each split k", "return dp[1][n]"], "O(n^3)"),
    "string_matching": AlgorithmTemplate("kmp",
        ["build failure function", "scan text using failure to skip"], "O(n+m)"),
    "graph_coloring": AlgorithmTemplate("greedy_coloring",
        ["sort by degree descending", "assign smallest unused color"], "O(V+E)"),
    "convex_hull": AlgorithmTemplate("graham_scan",
        ["find lowest point", "sort by angle", "scan with stack"], "O(n log n)"),
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
SuccessorDesignGenerator._NEW_PROPERTIES.update({
    "poor_calibration": "calibrated softmax with learned temperature per class",
    "catastrophic_forgetting": "elastic weight consolidation with Fisher information matrix",
    "mode_collapse": "diversity-promoting generator with minibatch features",
    "gradient_starvation": "multi-objective optimizer with per-loss adaptive weights",
})
SuccessorDesignGenerator._TRADEOFFS.update({
    "poor_calibration": "accuracy may decrease slightly; inference cost +1 scalar multiply",
    "catastrophic_forgetting": "slower training due to Fisher computation; memory for old task weights",
    "mode_collapse": "higher compute per batch; may reduce sample quality for diversity",
    "gradient_starvation": "extra parameters for weight learning; may oscillate if alpha too high",
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
            {"name": "dense array", "space": "O(n^2)", "access": "O(1)", "insert": "O(1)", "multiply": "O(n^3)"},
            {"name": "CSR sparse", "space": "O(nnz)", "access": "O(log nnz)", "insert": "O(nnz)", "multiply": "O(nnz)"},
        ],
        "winner": "CSR sparse",
        "reason": "95% zeros means nnz << n^2, massive space and compute savings",
    },
    "float_vs_fixed": {
        "problem": "neural network inference on edge device with limited precision",
        "options": [
            {"name": "float32", "space": "4 bytes", "access": "O(1)", "insert": "N/A", "accuracy": "full"},
            {"name": "int8 fixed", "space": "1 byte", "access": "O(1)", "insert": "N/A", "accuracy": "~1% loss"},
        ],
        "winner": "int8 fixed",
        "reason": "4x speedup and 4x memory reduction for ~1% accuracy loss",
    },
    "row_vs_col_major": {
        "problem": "iterate over rows of a large matrix frequently",
        "options": [
            {"name": "row-major (C)", "space": "O(n^2)", "access": "sequential", "insert": "O(1)"},
            {"name": "col-major (Fortran)", "space": "O(n^2)", "access": "strided", "insert": "O(1)"},
        ],
        "winner": "row-major",
        "reason": "sequential memory access maximises cache line utilisation",
    },
    "index_vs_scan": {
        "problem": "10M records, query by exact key 1000 times/sec",
        "options": [
            {"name": "B-tree index", "space": "O(n)", "access": "O(log n)", "insert": "O(log n)"},
            {"name": "sequential scan", "space": "O(1)", "access": "O(n)", "insert": "O(1)"},
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

# DataPrescription: sync _PRESCRIPTIONS and _WEAKNESSES
# Add new entries to _PRESCRIPTIONS (the dict _create_problem actually uses)
DataPrescriptionGenerator._PRESCRIPTIONS.update({
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


# ── Additional scenarios to push 7-9 unique generators above 10 ────

# DataPrescription: 7 → 11
DataPrescriptionGenerator._PRESCRIPTIONS.update({
    "temporal_drift": {
        "weakness": "model degrades over time as data distribution shifts",
        "root_cause": "no mechanism to detect or adapt to temporal drift",
        "data_type": "timestamped data with periodic retraining windows",
        "quantity": 10000,
        "spec": "add recent data monthly, retrain on sliding 6-month window",
    },
    "adversarial_fragility": {
        "weakness": "model fails on slightly perturbed inputs",
        "root_cause": "decision boundary too close to training examples",
        "data_type": "adversarially perturbed examples (FGSM, PGD)",
        "quantity": 5000,
        "spec": "adversarial training: generate perturbations during training",
    },
    "spurious_correlation": {
        "weakness": "model relies on background features instead of target object",
        "root_cause": "training data has confounding features correlated with labels",
        "data_type": "counterfactual data with swapped backgrounds",
        "quantity": 8000,
        "spec": "collect examples where confound is decorrelated from label",
    },
})

# HypothesisDesign: 7 → 11
HypothesisDesignGenerator._EXPERIMENTS.update({
    "pretraining_scale": {
        "hypothesis": "larger pretraining corpus improves downstream accuracy",
        "control": "fix model size, fine-tuning data, epochs",
        "variable": "pretrain corpus size: {1B, 10B, 100B tokens}",
        "measure": "downstream task accuracy after fine-tuning",
        "criterion": "10B+ outperforms 1B by > 5% accuracy",
        "conditions": 3,
    },
    "optimizer_comparison": {
        "hypothesis": "AdamW outperforms SGD on transformer training",
        "control": "fix model, data, learning rate schedule, epochs",
        "variable": "optimizer: {SGD+momentum, Adam, AdamW}",
        "measure": "final validation loss and convergence speed",
        "criterion": "AdamW reaches same loss in 30% fewer steps",
        "conditions": 3,
    },
    "context_length": {
        "hypothesis": "longer context window improves reasoning tasks",
        "control": "fix model size, training data, compute budget",
        "variable": "max context: {512, 2048, 8192 tokens}",
        "measure": "accuracy on multi-step reasoning benchmarks",
        "criterion": "8192 outperforms 512 by > 10% on 5+ step problems",
        "conditions": 3,
    },
})

# ImpossibilityProof: 7 → 11
ImpossibilityProofGenerator._PROBLEMS.update({
    "string_matching": "exact string matching",
    "selection": "selection (kth element)",
    "diameter": "graph diameter",
    "distinct": "element distinctness",
})
ImpossibilityProofGenerator._BOUNDS.update({
    "string_matching": "Omega(n+m) (must read input)",
    "selection": "Omega(n) (must examine all elements)",
    "diameter": "Omega(V + E) (must traverse graph)",
    "distinct": "Omega(n log n) (comparison model)",
})
ImpossibilityProofGenerator._PROOF_STEPS.update({
    "string_matching": [
        "text has n characters, pattern has m",
        "any character could be the start of a match",
        "must read all n characters of text",
        "must compare against m characters of pattern",
    ],
    "selection": [
        "any element could be the kth smallest",
        "algorithm must examine every element at least once",
        "adversary can hide kth element anywhere",
        "lower bound: Omega(n) comparisons",
    ],
    "diameter": [
        "diameter requires finding farthest pair",
        "any edge could be on the longest path",
        "must examine all edges",
        "lower bound: Omega(V + E)",
    ],
    "distinct": [
        "equivalent to sorting in comparison model",
        "n! possible orderings of n distinct elements",
        "comparison tree height >= log2(n!)",
        "= Omega(n log n) by Stirling",
    ],
})


# ── Push 8-unique generators to 12 ─────────────────────────────────

# FailureAnalysis: add 4 more bug types
FailureAnalysisGenerator._FAILURE_TYPES.update({9: "memory_leak", 10: "deadlock", 11: "stale_cache", 12: "precision_loss"})
FailureAnalysisGenerator._ALGORITHMS.update({
    "memory_leak": "results = []; for batch in data: results.append(process(batch))",
    "deadlock": "lock_A(); lock_B();  # thread 1\nlock_B(); lock_A();  # thread 2",
    "stale_cache": "cache[key] = compute(key); ... data changes ... return cache[key]",
    "precision_loss": "total = 0.0; for x in large_list: total += x  # float32",
})
FailureAnalysisGenerator._FAILING_INPUTS.update({
    "memory_leak": "10M batches, each 1KB",
    "deadlock": "two threads acquiring locks in opposite order",
    "stale_cache": "cache hit after underlying data was modified",
    "precision_loss": "sum of 1e8 values near 1.0 in float32",
})
FailureAnalysisGenerator._FAILURE_EXPLANATIONS.update({
    "memory_leak": ["results list grows without bound", "10M * 1KB = 10GB memory", "fix: process and discard, or use generator"],
    "deadlock": ["thread 1 holds A, waits for B", "thread 2 holds B, waits for A", "fix: acquire locks in consistent order"],
    "stale_cache": ["cache was populated before data change", "returns outdated result", "fix: invalidate cache on data write"],
    "precision_loss": ["float32 has ~7 significant digits", "adding 1.0 to 1e8 loses the 1.0", "fix: use Kahan summation or float64"],
})
FailureAnalysisGenerator._BUG_NAMES.update({
    "memory_leak": "unbounded memory growth",
    "deadlock": "deadlock (circular wait)",
    "stale_cache": "stale cache (cache invalidation failure)",
    "precision_loss": "catastrophic cancellation / precision loss",
})

# Reduction: add 4 more reductions
ReductionGenerator._REDUCTIONS.update({
    "ham_to_tsp": {
        "from": "Hamiltonian path", "to": "travelling salesman (decision)",
        "steps": ["given graph G, set all edge weights to 1", "ask: is there a tour of cost <= n?",
                  "tour of cost n exists iff Hamiltonian path exists"],
        "bound": "NP-hard", "test_input": "complete graph K5", "test_result": "tour exists (cost=5)"},
    "3col_to_sat": {
        "from": "3-coloring", "to": "SAT",
        "steps": ["for each vertex v, create 3 boolean vars (r_v, g_v, b_v)",
                  "clause: at least one color per vertex", "clause: at most one color",
                  "clause: adjacent vertices different color"],
        "bound": "NP-hard", "test_input": "triangle graph", "test_result": "6 clauses, satisfiable"},
    "subset_to_knapsack": {
        "from": "subset sum", "to": "0/1 knapsack",
        "steps": ["set item weights = values = subset elements", "set capacity = target sum",
                  "knapsack optimal = target iff subset sum has solution"],
        "bound": "NP-hard", "test_input": "{3,7,1,8}, target=11", "test_result": "{3,7,1}=11"},
    "max_flow_to_matching": {
        "from": "max flow", "to": "maximum bipartite matching",
        "steps": ["create source s, sink t", "s -> left vertices (cap 1)", "right vertices -> t (cap 1)",
                  "edges between sides (cap 1)", "max flow = max matching"],
        "bound": "poly-time", "test_input": "K_{2,3} bipartite", "test_result": "matching size 2"},
})

# AlgorithmImprovement: add 4 more pairs via scenario_expansions
AlgorithmImprovementGenerator._IMPROVEMENTS.update({9: "fibonacci_memo", 10: "matrix_search", 11: "interval_merge", 12: "prefix_sum"})
from engram_generator.generators.meta_reasoning_t9 import AlgorithmTemplate as AT
AlgorithmImprovementGenerator._NAIVE.update({
    "fibonacci_memo": AT("fib_naive", ["if n<=1 return n", "return fib(n-1)+fib(n-2)"], "O(2^n)"),
    "matrix_search": AT("matrix_search_naive", ["for each row", "for each col", "if match return"], "O(nm)"),
    "interval_merge": AT("interval_merge_naive", ["for each pair of intervals", "check overlap", "merge if overlapping"], "O(n^2)"),
    "prefix_sum": AT("range_sum_naive", ["for each query (l,r)", "sum elements l..r"], "O(n) per query"),
})
AlgorithmImprovementGenerator._IMPROVED.update({
    "fibonacci_memo": AT("fib_dp", ["dp[0]=0, dp[1]=1", "for i=2..n: dp[i]=dp[i-1]+dp[i-2]"], "O(n)"),
    "matrix_search": AT("staircase_search", ["start top-right", "if match return", "if too large go left, else go down"], "O(n+m)"),
    "interval_merge": AT("sort_merge", ["sort by start", "scan: merge if overlap with current"], "O(n log n)"),
    "prefix_sum": AT("prefix_array", ["build prefix[i] = sum(0..i)", "query: prefix[r]-prefix[l-1]"], "O(1) per query"),
})
AlgorithmImprovementGenerator._INSIGHTS.update({
    "fibonacci_memo": "overlapping subproblems — each fib(k) computed once with memoisation",
    "matrix_search": "sorted rows+cols let you eliminate row or column each step",
    "interval_merge": "sorting makes overlap detection linear (just check adjacent)",
    "prefix_sum": "precompute cumulative sums for O(1) range queries",
})
AlgorithmImprovementGenerator._TEST_INPUTS.update({
    "fibonacci_memo": [10], "matrix_search": [1, 2, 3, 4],
    "interval_merge": [1, 3, 2, 6, 8, 10], "prefix_sum": [1, 2, 3, 4, 5],
})
AlgorithmImprovementGenerator._TEST_RESULTS.update({
    "fibonacci_memo": "fib(10)=55", "matrix_search": "found at (1,2)",
    "interval_merge": "merged: [1,6],[8,10]", "prefix_sum": "sum(2..4)=9",
})

# EfficiencyAnalysis: add via _CONFIGS expansion
# This generator uses int-keyed _CONFIGS, so we add more config entries
from engram_generator.generators.meta_reasoning_ext import EfficiencyAnalysisGenerator
EfficiencyAnalysisGenerator._CONFIGS.update({
    9: {"arch": "GPT-3 175B", "d_model": 12288, "n_layers": 96, "n_heads": 96, "seq_len": 2048, "vocab": 50257},
    10: {"arch": "BERT-base", "d_model": 768, "n_layers": 12, "n_heads": 12, "seq_len": 512, "vocab": 30522},
    11: {"arch": "ViT-L/16", "d_model": 1024, "n_layers": 24, "n_heads": 16, "seq_len": 196, "vocab": 1000},
    12: {"arch": "Mamba-1.4B", "d_model": 2048, "n_layers": 48, "n_heads": 1, "seq_len": 8192, "vocab": 50280},
})

# LossDesign: already at 8 — _BEHAVIOURS has 8 entries and generic builder works
# The issue is that problem text is "desired: {behaviour}" which can collide on RNG
# Add 4 more behaviours to push above 10
LossDesignGenerator._BEHAVIOURS.update({
    "reconstruction": "reconstruct input from compressed representation",
    "ranking": "ensure correct pairwise ordering of items by score",
    "calibration": "make predicted probabilities match true frequencies",
    "sparsity": "encourage sparse activations in hidden layers",
})

# MinimalAxioms: uses _get_axiom_sets helper — already patched to return 8
# Add 4 more axiom sets to the expansion list
_extra_axiom_sets.extend([
    {"axioms": ["a*1=a", "a*0=0", "0*a=0", "a*(b+c)=a*b+a*c"],
     "redundant_idx": 2, "redundant_name": "A3",
     "derivation": "by A2 with b=0: a*0 = a*0; also 0*a = 0 by commutativity if applicable",
     "minimal": ["a*1=a", "a*0=0", "a*(b+c)=a*b+a*c"]},
    {"axioms": ["p AND True = p", "p AND False = False", "p OR True = True", "p OR False = p", "NOT NOT p = p"],
     "redundant_idx": 3, "redundant_name": "A4",
     "derivation": "by A1 and A3: p OR False = NOT(NOT p AND NOT False) = NOT(NOT p AND True) = NOT(NOT p) = p",
     "minimal": ["p AND True = p", "p AND False = False", "p OR True = True", "NOT NOT p = p"]},
])

# SuccessorDesign: already at 8 — all dicts synced
# Add more limitation types
SuccessorDesignGenerator._LIMITATION_TYPES.update({9: "no_memory", 10: "single_pass", 11: "fixed_precision", 12: "no_attention"})
SuccessorDesignGenerator._LIMITATIONS.update({
    "no_memory": "model has no persistent memory across inputs",
    "single_pass": "model processes input in one forward pass, cannot iterate",
    "fixed_precision": "model uses fixed numerical precision (e.g. float16)",
    "no_attention": "model lacks attention mechanism (MLP-only)",
})
SuccessorDesignGenerator._BOTTLENECKS.update({
    "no_memory": "cannot accumulate knowledge from previous examples",
    "single_pass": "computation depth bounded by number of layers",
    "fixed_precision": "numerical errors accumulate in deep computations",
    "no_attention": "cannot selectively focus on relevant input parts",
})
SuccessorDesignGenerator._PROPOSALS.update({
    "no_memory": "add external memory bank with read/write heads",
    "single_pass": "add iterative refinement loop with learned halting",
    "fixed_precision": "mixed precision: fp32 for accumulators, fp16 for activations",
    "no_attention": "add sparse attention or linear attention mechanism",
})
SuccessorDesignGenerator._NEW_PROPERTIES.update({
    "no_memory": "persistent key-value memory bank across sequences",
    "single_pass": "adaptive computation time with PonderNet-style halting",
    "fixed_precision": "automatic mixed precision with loss scaling",
    "no_attention": "linear attention with kernel feature maps",
})
SuccessorDesignGenerator._TRADEOFFS.update({
    "no_memory": "memory grows with usage; need garbage collection strategy",
    "single_pass": "variable compute cost per input; harder to batch",
    "fixed_precision": "some operations must stay fp32; slight memory overhead",
    "no_attention": "may lose expressiveness compared to full attention",
})

# RepresentationChoice: already at 8 — adding 4 more
RepresentationChoiceGenerator._CHOICES.update({
    "heap_vs_sorted": {
        "problem": "repeatedly extract minimum element from dynamic collection",
        "options": [
            {"name": "sorted array", "space": "O(n)", "access": "O(1) min", "insert": "O(n)"},
            {"name": "binary heap", "space": "O(n)", "access": "O(1) min", "insert": "O(log n)"},
        ],
        "winner": "binary heap",
        "reason": "O(log n) insert vs O(n) for sorted array when insertions are frequent",
    },
    "trie_vs_hash": {
        "problem": "autocomplete: find all words with given prefix",
        "options": [
            {"name": "hash table", "space": "O(total chars)", "access": "O(k) exact", "insert": "O(k)"},
            {"name": "trie", "space": "O(total chars)", "access": "O(k) prefix", "insert": "O(k)"},
        ],
        "winner": "trie",
        "reason": "trie supports prefix queries natively; hash table requires scanning all keys",
    },
    "graph_matrix_vs_list": {
        "problem": "frequent edge existence queries on dense graph (>50% edges)",
        "options": [
            {"name": "adjacency matrix", "space": "O(V^2)", "access": "O(1)", "insert": "O(1)"},
            {"name": "adjacency list", "space": "O(V+E)", "access": "O(degree)", "insert": "O(1)"},
        ],
        "winner": "adjacency matrix",
        "reason": "O(1) edge query; dense graph means E ~ V^2 so space is similar",
    },
    "btree_vs_lsm": {
        "problem": "database with heavy write workload, occasional reads",
        "options": [
            {"name": "B-tree", "space": "O(n)", "access": "O(log n)", "insert": "O(log n) random IO"},
            {"name": "LSM-tree", "space": "O(n)", "access": "O(log n) + compaction", "insert": "O(1) sequential"},
        ],
        "winner": "LSM-tree",
        "reason": "sequential writes are 100x faster than random; compaction amortises read cost",
    },
})
