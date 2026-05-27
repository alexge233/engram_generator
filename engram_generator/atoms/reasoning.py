"""Knowledge atoms for tier 7-10 reasoning tasks.

Provides Atom objects covering meta-reasoning, creative mathematics,
research-level reasoning, and self-architecture concepts. Each atom
is a self-contained theorem, principle, methodology, or formula that
supports one or more generators in tiers 7 through 10.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(
    atom_type="theorem",
    name="proof_by_induction",
    content=(
        "To prove P(n) for all n >= n_0: "
        "(1) Base case: verify P(n_0). "
        "(2) Inductive step: assume P(k), prove P(k+1). "
        "Then P(n) holds for all n >= n_0."
    ),
    tier=7,
    domain="logic",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="methodology",
    name="error_detection",
    content=(
        "Systematic error checking: "
        "(1) Re-derive each step from the previous one independently. "
        "(2) Check dimensional consistency. "
        "(3) Verify boundary cases (n=0, n=1). "
        "(4) Substitute the answer back into the original equation."
    ),
    tier=7,
    domain="methodology",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="algorithm_design",
    content=(
        "Principles of algorithm construction: "
        "(1) Define input/output specification precisely. "
        "(2) Identify invariants maintained at each step. "
        "(3) Prove termination via a decreasing measure. "
        "(4) Analyse worst-case complexity using Big-O notation."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["proof_by_induction"],
))

register_atom(Atom(
    atom_type="theorem",
    name="gradient_analysis",
    content=(
        "Chain rule for backpropagation: "
        "if f = g_n(g_{n-1}(...g_1(x)...)), then "
        "df/dx = product_{i=1}^{n} g_i'(z_{i-1}) "
        "where z_0 = x and z_i = g_i(z_{i-1}). "
        "Gradient flows backward through each operation."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="result",
    name="scaling_prediction",
    content=(
        "Neural scaling law: accuracy = C * N^alpha, "
        "where N is parameter count, C is a constant, "
        "and alpha in (0.05, 0.3) typically. "
        "Fit alpha from two data points: "
        "alpha = log(acc2/acc1) / log(N2/N1)."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["gradient_analysis"],
))

register_atom(Atom(
    atom_type="principle",
    name="constraint_optimisation",
    content=(
        "Linear programming: maximise c^T x subject to Ax <= b, x >= 0. "
        "Optimal solution occurs at a vertex of the feasible polytope. "
        "Enumerate vertices, evaluate objective at each, select maximum."
    ),
    tier=7,
    domain="optimisation",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="methodology",
    name="problem_construction",
    content=(
        "Problem construction methodology: "
        "(1) Choose a known answer or structure. "
        "(2) Derive problem constraints from that answer. "
        "(3) Verify the problem is well-posed (unique solution). "
        "(4) Confirm the answer satisfies all constraints."
    ),
    tier=7,
    domain="methodology",
    prerequisites=["proof_by_induction"],
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_analysis",
    content=(
        "Complexity comparison: given two algorithms A and B for the same "
        "problem, compute concrete step counts T_A(n) and T_B(n) for "
        "input size n. The algorithm with smaller T(n) is preferred. "
        "Crossover point: solve T_A(n) = T_B(n) for n."
    ),
    tier=7,
    domain="computer_science",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="methodology",
    name="error_correction",
    content=(
        "Error correction procedure: "
        "(1) Identify the first incorrect step. "
        "(2) Recompute that step from verified prior steps. "
        "(3) Propagate the correction through all subsequent steps. "
        "(4) Verify the corrected answer against the original problem."
    ),
    tier=7,
    domain="methodology",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="identity",
    name="derive_identity",
    content=(
        "Algebraic identity derivation: "
        "to prove LHS = RHS, expand one side using known identities, "
        "simplify by cancellation, and arrive at the other side. "
        "Verify numerically at test points: LHS(a,b) = RHS(a,b)."
    ),
    tier=7,
    domain="algebra",
    prerequisites=["proof_by_induction"],
))

register_atom(Atom(
    atom_type="principle",
    name="construct_polynomial",
    content=(
        "Polynomial construction from roots: "
        "given roots r_1, ..., r_k, the monic polynomial is "
        "p(x) = (x - r_1)(x - r_2)...(x - r_k). "
        "Verify: p(r_i) = 0 for all i."
    ),
    tier=7,
    domain="algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="generalise_sequence",
    content=(
        "Sequence generalisation: "
        "compute first, second, ... differences until constant. "
        "If kth differences are constant, the formula is a degree-k polynomial. "
        "Fit using k+1 data points and verify at unseen indices."
    ),
    tier=7,
    domain="algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="counterexample",
    content=(
        "Disproof by counterexample: "
        "to disprove 'for all x, P(x)', find a single x_0 "
        "such that P(x_0) is false. "
        "One counterexample suffices to refute a universal claim."
    ),
    tier=7,
    domain="logic",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="methodology",
    name="inverse_problem",
    content=(
        "Inverse problem methodology: given f'(x), find f(x) by "
        "reversing the differentiation rules. "
        "Power rule inverse: integral of ax^n dx = a*x^(n+1)/(n+1) + C. "
        "Verify: d/dx[f(x)] = f'(x)."
    ),
    tier=7,
    domain="calculus",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="methodology",
    name="method_selection",
    content=(
        "Method selection heuristic: "
        "(1) Identify the problem class (linear, quadratic, system). "
        "(2) List applicable methods with their computational cost. "
        "(3) Choose the method with lowest cost for the given instance. "
        "(4) Verify the answer is consistent across methods."
    ),
    tier=7,
    domain="methodology",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="estimate_magnitude",
    content=(
        "Order-of-magnitude estimation: "
        "round each operand to its leading digit, compute the approximate "
        "result, then express as 10^k. "
        "The estimate should be within one order of the exact answer."
    ),
    tier=7,
    domain="arithmetic",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="methodology",
    name="derive_formula",
    content=(
        "Formula derivation from first principles: "
        "start with definitions or axioms, apply algebraic manipulation "
        "(expansion, factoring, substitution) step by step, "
        "and verify the result at test values."
    ),
    tier=7,
    domain="algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="sufficiency_analysis",
    content=(
        "Information sufficiency: a system of equations is solvable "
        "if the number of independent equations >= number of unknowns. "
        "Identify all unknowns, count independent equations, "
        "and determine if the system is under-, over-, or fully-determined."
    ),
    tier=7,
    domain="algebra",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="principle",
    name="isomorphism_detection",
    content=(
        "Structural isomorphism: two problems are isomorphic if there "
        "exists a bijective mapping of variables and operations that "
        "transforms one into the other. "
        "Identify the mapping and verify it preserves all relationships."
    ),
    tier=8,
    domain="abstract_algebra",
    prerequisites=["generalise_sequence"],
))

register_atom(Atom(
    atom_type="principle",
    name="cross_domain_transfer",
    content=(
        "Cross-domain transfer: map a problem from domain A to domain B "
        "where the solution is easier. "
        "Example: sum 1+2+...+n maps to triangle area = n(n+1)/2."
    ),
    tier=8,
    domain="methodology",
    prerequisites=["derive_formula"],
))

register_atom(Atom(
    atom_type="methodology",
    name="conjecture_generation",
    content=(
        "Conjecture generation: observe input-output pairs, "
        "compute finite differences to determine polynomial degree, "
        "fit coefficients, and verify at unseen points."
    ),
    tier=8,
    domain="methodology",
    prerequisites=["generalise_sequence"],
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_reduction",
    content=(
        "Complexity reduction: recognise algebraic patterns "
        "(perfect squares, difference of squares, sum of cubes) "
        "to replace multi-step expansion with a single identity application."
    ),
    tier=8,
    domain="algebra",
    prerequisites=["derive_formula"],
))

register_atom(Atom(
    atom_type="methodology",
    name="problem_transformation",
    content=(
        "Problem transformation: substitute u = g(x) to reduce a "
        "higher-order equation to a lower-order one. "
        "Example: x^4-5x^2+4=0 becomes u^2-5u+4=0 with u=x^2."
    ),
    tier=8,
    domain="algebra",
    prerequisites=["method_selection"],
))

register_atom(Atom(
    atom_type="principle",
    name="analogy_completion",
    content=(
        "Mathematical analogy: given A:B :: C:?, identify the functional "
        "relationship f such that f(A)=B, then compute f(C). "
        "Verify by checking additional examples if available."
    ),
    tier=8,
    domain="reasoning",
    prerequisites=["generalise_sequence"],
))

register_atom(Atom(
    atom_type="methodology",
    name="equation_construction",
    content=(
        "Equation construction: given roots r_1,...,r_k and leading "
        "coefficient a, construct p(x) = a * product(x - r_i). "
        "Verify p(r_i) = 0 for all i and check leading coefficient."
    ),
    tier=8,
    domain="algebra",
    prerequisites=["construct_polynomial"],
))

register_atom(Atom(
    atom_type="methodology",
    name="self_evaluation",
    content=(
        "Self-evaluation: after solving, check for traps: "
        "division by zero, extraneous solutions from squaring, "
        "domain restrictions, and sign errors. "
        "Rate confidence: high if no traps, low if traps detected."
    ),
    tier=8,
    domain="methodology",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="principle",
    name="minimal_axioms",
    content=(
        "Axiom minimality: an axiom A_i is redundant if it can be "
        "derived from the remaining axioms {A_1,...,A_n} \\ {A_i}. "
        "Test by attempting to prove A_i using only the others. "
        "The minimal set is the smallest subset that generates all theorems."
    ),
    tier=8,
    domain="logic",
    prerequisites=["derive_formula"],
))

register_atom(Atom(
    atom_type="methodology",
    name="novel_problem",
    content=(
        "Novel problem design: select two or more skills, "
        "construct a problem whose solution requires applying them "
        "in sequence. Verify that no single skill suffices."
    ),
    tier=8,
    domain="methodology",
    prerequisites=["problem_construction"],
))

register_atom(Atom(
    atom_type="principle",
    name="solution_elegance",
    content=(
        "Solution elegance: a proof is elegant if it uses fewer steps "
        "than a brute-force approach. Look for algebraic identities, "
        "symmetry, and closed-form shortcuts that bypass term-by-term "
        "computation."
    ),
    tier=8,
    domain="methodology",
    prerequisites=["complexity_reduction"],
))

register_atom(Atom(
    atom_type="theorem",
    name="algorithm_improvement",
    content=(
        "Algorithm improvement: given an O(n^2) naive solution, "
        "identify the redundant computation and replace it with "
        "a data structure (hash set, sorted structure) that reduces "
        "the dominant loop to O(1) or O(log n) per iteration."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="theorem",
    name="impossibility_proof",
    content=(
        "Information-theoretic lower bound: if there are M possible "
        "outcomes, any comparison-based algorithm needs at least "
        "ceil(log2(M)) comparisons in the worst case. "
        "For sorting: M = n!, so lower bound is Omega(n log n)."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="methodology",
    name="failure_analysis",
    content=(
        "Algorithm failure analysis: "
        "(1) Identify the failing input class. "
        "(2) Trace execution to the first incorrect operation. "
        "(3) Classify the bug: off-by-one, overflow, null access, etc. "
        "(4) Propose a targeted fix."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="principle",
    name="invariant_discovery",
    content=(
        "Invariant discovery: apply a transformation multiple times "
        "and observe which quantities remain constant. "
        "Common invariants: sum under swaps, XOR under pair-XOR, "
        "parity under even shifts, determinant under row operations."
    ),
    tier=9,
    domain="mathematics",
    prerequisites=["generalise_sequence"],
))

register_atom(Atom(
    atom_type="principle",
    name="complexity_comparison",
    content=(
        "Algorithm comparison: for two algorithms A, B solving the same "
        "problem, compute T_A(n) and T_B(n) at the given input size n. "
        "The one with fewer operations wins. "
        "Report both the winner and the speedup ratio."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="theorem",
    name="reduction",
    content=(
        "Reduction: problem A reduces to problem B (A <= B) if any "
        "instance of A can be transformed into an instance of B in "
        "polynomial time. This proves B is at least as hard as A. "
        "Lower bounds on A transfer to B."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["algorithm_design", "impossibility_proof"],
))

register_atom(Atom(
    atom_type="theorem",
    name="learning_bound",
    content=(
        "Sample complexity bounds: "
        "Hoeffding: n >= ln(2/delta) / (2*eps^2). "
        "VC bound: n >= (4/eps^2)(VC*ln(2/eps) + ln(2/delta)). "
        "PAC: n >= (d + ln(1/delta)) / eps. "
        "More complex hypothesis classes require more samples."
    ),
    tier=9,
    domain="machine_learning",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="methodology",
    name="hypothesis_design",
    content=(
        "Experiment design: "
        "(1) State the hypothesis clearly. "
        "(2) Identify the independent variable (what changes). "
        "(3) Control all other variables. "
        "(4) Define the measurement and success criterion. "
        "(5) Run sufficient repetitions for statistical significance."
    ),
    tier=9,
    domain="methodology",
    prerequisites=["method_selection"],
))

register_atom(Atom(
    atom_type="methodology",
    name="meta_pattern",
    content=(
        "Meta-pattern recognition: given multiple error instances, "
        "compute the error vector (predicted - true) for each, "
        "then check for constant offset, proportional scaling, "
        "sign flip, or conditional triggers."
    ),
    tier=9,
    domain="methodology",
    prerequisites=["error_detection", "generalise_sequence"],
))

register_atom(Atom(
    atom_type="principle",
    name="representation_choice",
    content=(
        "Representation selection: compare data structures on the "
        "operations the problem requires most: access, insert, delete, "
        "range query. Choose the structure that minimises the dominant "
        "operation cost."
    ),
    tier=9,
    domain="computer_science",
    prerequisites=["method_selection", "complexity_comparison"],
))

register_atom(Atom(
    atom_type="methodology",
    name="training_diagnosis",
    content=(
        "Training curve diagnosis: "
        "plateau -> learning rate too low or stuck in local minimum. "
        "oscillation -> learning rate too high. "
        "divergence -> exploding gradients, check for NaN. "
        "overfitting -> train loss drops but val loss rises."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="methodology",
    name="failure_mode_classification",
    content=(
        "Failure mode classification: compute error = pred - true for "
        "all samples. If mean error is significantly non-zero, "
        "the error is systematic (biased). If errors have zero mean "
        "and mixed signs, they are random. "
        "Proportional errors: error ~ k * true_value."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["error_detection"],
))

register_atom(Atom(
    atom_type="methodology",
    name="data_prescription",
    content=(
        "Data prescription: "
        "(1) Identify the model's weak capability. "
        "(2) Diagnose root cause (missing data, distribution shift). "
        "(3) Specify data type, difficulty range, and quantity. "
        "(4) Target the data at the failure mode, not general performance."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["training_diagnosis"],
))

register_atom(Atom(
    atom_type="principle",
    name="efficiency_analysis",
    content=(
        "Transformer FLOP analysis: "
        "attention: 2*n^2*d (QK^T) + 2*n^2*d (attn*V) + QKV projections. "
        "FFN: 2*n*d*d_ff (up) + 2*n*d_ff*d (down). "
        "Bottleneck depends on seq_len vs d_ff: "
        "long sequences -> attention; wide FFN -> feed-forward."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["architecture_analysis"],
))

register_atom(Atom(
    atom_type="result",
    name="emergent_capability",
    content=(
        "Emergent capabilities: some abilities appear suddenly at "
        "specific model scales. Below the threshold, accuracy is near "
        "random; above it, accuracy jumps sharply. "
        "Predict emergence by fitting a sigmoid or power law to "
        "observed data and finding the threshold crossing."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="principle",
    name="capacity_bound",
    content=(
        "Information capacity: a system with N parameters of B bits each "
        "can represent at most 2^(N*B) distinct states. "
        "For sequences of length L over vocabulary V: "
        "capacity = L * log2(V) bits."
    ),
    tier=10,
    domain="information_theory",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="methodology",
    name="loss_design",
    content=(
        "Loss function design: combine a task loss (CE, MSE) with "
        "auxiliary terms that encourage desired behaviour. "
        "Length penalty: lambda * max(0, steps - T). "
        "Regularisation: gamma * sum(w^2). "
        "KL: beta * KL(p_model || p_target)."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["gradient_analysis"],
))

register_atom(Atom(
    atom_type="principle",
    name="architecture_analysis",
    content=(
        "Neural architecture complexity: "
        "matrix multiply A(n,k)*B(k,m) -> O(nmk). "
        "Self-attention on seq_len n, d_model d -> O(n^2 d). "
        "1D convolution with kernel k on length n -> O(nk)."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["algorithm_design"],
))

register_atom(Atom(
    atom_type="methodology",
    name="successor_design",
    content=(
        "Architectural improvement: identify the bottleneck, "
        "propose a modification from the literature "
        "(adaptive halting, residual connections, linear attention, MoE), "
        "state the new complexity, and note the trade-off."
    ),
    tier=10,
    domain="deep_learning",
    prerequisites=["architecture_analysis"],
))

register_atom(Atom(
    atom_type="principle",
    name="lagrange_multiplier",
    content=(
        "Lagrange multiplier method: to optimise f(x) subject to "
        "g(x)=0, solve grad(f) = lambda * grad(g) and g(x)=0 "
        "simultaneously. At the optimum, the gradient of the "
        "objective is parallel to the gradient of the constraint."
    ),
    tier=7,
    domain="optimisation",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="result",
    name="binomial_dist",
    content=(
        "Binomial distribution: P(X=k) = C(n,k) * p^k * (1-p)^(n-k). "
        "Mean = np, variance = np(1-p). "
        "For large n, approximated by Normal(np, np(1-p))."
    ),
    tier=5,
    domain="probability",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="result",
    name="info_entropy",
    content=(
        "Shannon entropy: H(X) = -sum_i p_i * log2(p_i). "
        "Maximum entropy: H = log2(n) for uniform distribution over n outcomes. "
        "Entropy quantifies the average information content per symbol."
    ),
    tier=5,
    domain="information_theory",
    prerequisites=[],
))
