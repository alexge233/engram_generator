"""Reasoning pattern classifier for training sample rebalancing.

Classifies each generator by its primary reasoning pattern, enabling
weighted sampling that balances by reasoning diversity rather than
raw generator count. Without this, formula-substitution generators
(55% of total) would dominate training.
"""
from engram_generator.base import StepGenerator


PATTERN_NAMES = [
    "formula_substitution",
    "iterative_accumulation",
    "recursive_decomposition",
    "graph_traversal",
    "dynamic_programming",
    "greedy_selection",
    "linear_algebra",
    "symbolic_manipulation",
    "differential_equations",
    "modular_arithmetic",
    "logical_deduction",
    "probabilistic_reasoning",
    "statistical_inference",
    "optimization",
    "classification_lookup",
    "simulation_trace",
    "series_convergence",
    "transform_methods",
    "construction_verification",
    "counting_enumeration",
    "approximation_numerical",
    "conservation_balance",
    "encoding_decoding",
    "geometric_computation",
    "comparison_ordering",
    "dimensional_analysis",
    "meta_reasoning",
    "search_backtrack",
]

_KEYWORD_MAP: list[tuple[str, list[str]]] = [
    ("meta_reasoning", [
        "meta_reasoning", "proof_strategy", "conjecture", "research",
        "experiment_design", "architecture_search", "curriculum_design",
        "scaling_law", "debugging_strategy", "benchmark_design",
        "self_improvement", "compute_budget", "evaluation_metric",
    ]),
    ("graph_traversal", [
        "graph", "bfs", "dfs", "dijkstra", "bellman_ford", "floyd",
        "kruskal", "topological", "scc", "tarjan", "matching",
        "flow", "path_planning", "connected", "coloring",
        "articulation", "eulerian", "hamiltonian", "pagerank",
        "centrality", "network_flow",
    ]),
    ("dynamic_programming", [
        "knapsack", "lcs", "lis", "edit_distance", "coin_change",
        "dp_", "matrix_chain", "alignment", "longest_palindrome",
    ]),
    ("simulation_trace", [
        "trace", "simulate", "step", "round", "handshake",
        "protocol", "scheduling", "dfa", "nfa", "pda", "turing",
        "mealy", "moore", "transducer", "bst_", "avl_", "heap",
        "trie", "bloom", "skip_list", "b_tree", "red_black",
        "stack_op", "queue_op", "semaphore", "page_", "disk_",
        "memory_alloc", "deadlock", "file_alloc",
    ]),
    ("linear_algebra", [
        "matrix", "eigenvalue", "determinant", "svd", "qr_",
        "cholesky", "lu_", "null_space", "column_space",
        "gram_schmidt", "projection_matrix", "jordan",
        "rank_nullity", "jacobian", "singular_value",
    ]),
    ("symbolic_manipulation", [
        "derivative", "integral", "chain_rule", "product_rule",
        "taylor", "limit", "differentiation", "substitution",
        "by_parts", "partial_fraction", "curl", "divergence_theorem",
        "stokes", "greens_theorem", "laplacian", "directional_deriv",
    ]),
    ("differential_equations", [
        "ode", "pde", "heat_equation", "wave_equation",
        "schrodinger", "diffusion", "laplace_equation",
        "helmholtz", "advection", "burger", "fem_",
        "crank_nicolson", "runge_kutta", "euler_method",
        "separation_of_var", "integrating_factor",
    ]),
    ("modular_arithmetic", [
        "mod_pow", "mod_inv", "crt", "totient", "primality",
        "factorisation", "gcd", "lcm", "fermat_little", "wilson",
        "miller_rabin", "discrete_log", "quadratic_resid",
        "legendre_symbol", "jacobi_symbol", "pell_",
        "carmichael", "mobius_func", "mobius_inver",
    ]),
    ("encoding_decoding", [
        "rsa", "diffie", "encrypt", "decrypt", "cipher",
        "hash_chain", "signature", "shamir", "commitment",
        "garbled", "oblivious", "hamming_enc", "hamming_dec",
        "huffman", "reed_solomon", "bch_", "turbo",
        "polar_code", "merkle", "stream_cipher", "block_cipher",
    ]),
    ("probabilistic_reasoning", [
        "prob", "bayes", "expected_value", "distribution",
        "binomial_dist", "poisson", "normal_dist", "exponential_dist",
        "markov", "random_walk", "martingale", "renewal",
        "branching", "mixture", "extreme_value", "hazard",
        "weibull", "beta_dist", "gamma_dist", "clt_",
        "born_rule", "boltzmann",
    ]),
    ("statistical_inference", [
        "hypothesis", "confidence", "regression", "anova",
        "chi_square", "t_test", "f_test", "correlation",
        "maximum_likelihood", "bootstrap", "effect_size",
        "power_analysis", "bayesian_cred", "fisher_exact",
        "mann_whitney", "kruskal_wallis", "permutation_test",
    ]),
    ("construction_verification", [
        "group_axiom", "subgroup", "coset", "quotient_group",
        "kernel", "isomorphism", "automorphism", "homology",
        "homotopy", "fundamental_group", "covering",
        "manifold", "category", "functor", "monad",
        "adjunction", "topos", "ring_ideal", "field_ext",
        "galois", "sylow",
    ]),
    ("counting_enumeration", [
        "permutation", "catalan", "derangement", "stirling",
        "bell_number", "pascal", "partition_func",
        "composition", "pigeonhole", "inclusion_exclusion",
        "burnside", "polya", "latin_square", "ballot",
        "ramsey", "vandermonde", "multinomial",
    ]),
    ("series_convergence", [
        "convergence", "cauchy_sequence", "sequence_converg",
        "uniform_converg", "ratio_test", "root_test",
        "alternating_series", "power_series", "radius",
        "bolzano_weierstrass", "weierstrass_mtest", "squeeze",
        "abel_summ",
    ]),
    ("optimization", [
        "optim", "gradient_descent", "simplex", "linear_program",
        "kkt", "convex", "lagrange_mult", "dual_lp",
        "proximal", "subgradient", "barrier_method",
        "adam_full", "sgd_momentum",
    ]),
    ("transform_methods", [
        "fourier", "laplace_transform", "z_transform",
        "dft", "fft", "wavelet", "hilbert_transform",
        "change_of_var", "change_of_basis",
    ]),
    ("geometric_computation", [
        "area_", "volume_", "distance_", "angle_",
        "triangle_", "circle_", "polygon_", "rotation_",
        "reflection_", "convex_hull", "voronoi",
        "plane_equation", "conic_", "centroid",
        "intersection", "projection_2d",
    ]),
    ("approximation_numerical", [
        "newton_raphson", "bisection", "secant_method",
        "fixed_point_iter", "simpson", "gaussian_quadrature",
        "interpolation", "riemann_sum", "power_method",
        "gauss_seidel", "jacobi_iter", "condition_number",
        "adams_bashforth",
    ]),
    ("conservation_balance", [
        "conservation", "balance", "equilibrium", "first_law",
        "carnot", "entropy", "kirchhoff", "bernoulli",
        "nernst", "gibbs", "hess", "born_haber",
    ]),
    ("recursive_decomposition", [
        "recursive_", "tower_of_hanoi", "fibonacci",
        "merge_sort", "quicksort",
    ]),
    ("greedy_selection", [
        "sorting", "greedy", "interval_scheduling",
        "kruskal_trace", "job_scheduling", "set_cover_greedy",
        "bin_packing", "topk_quickselect",
    ]),
    ("logical_deduction", [
        "natural_deduction", "resolution", "horn_clause",
        "modal_logic", "intuitionistic", "sequent",
        "cnf_", "dnf_", "logical_consequence",
        "proof_by_", "reductio", "tarski_truth",
        "predicate_logic", "sat_verify",
    ]),
    ("comparison_ordering", [
        "comparison", "mohs", "periodic_trend", "band_gap",
        "rock_cycle", "mineral_id",
    ]),
    ("dimensional_analysis", [
        "dimensional", "unit_conversion", "significant_fig",
        "calibration",
    ]),
    ("search_backtrack", [
        "a_star", "backtrack", "constraint",
        "sat_", "csp",
    ]),
]


def classify_generator(g: StepGenerator) -> str:
    """Classify a generator by its primary reasoning pattern.

    Uses task name and module keywords to determine the dominant
    reasoning strategy required to solve the generator's problems.

    Args:
        g: A StepGenerator instance.

    Returns:
        Pattern name string from PATTERN_NAMES.
    """
    name = g.task_name
    mod = type(g).__module__.split(".")[-1]
    tier = g.tier

    if "meta_reasoning" in mod or tier >= 8:
        return "meta_reasoning"

    for pattern, keywords in _KEYWORD_MAP:
        if any(kw in name or kw in mod for kw in keywords):
            return pattern

    return "formula_substitution"


def get_pattern_weights(generators: list[StepGenerator]) -> dict[str, float]:
    """Compute per-generator sampling weight to balance reasoning patterns.

    Each pattern gets equal total weight regardless of how many generators
    belong to it. Within a pattern, weight is split equally among its
    generators.

    Args:
        generators: All generators to weight.

    Returns:
        Dict mapping task_name to sampling weight (sums to 1.0).
    """
    from collections import defaultdict

    pattern_members = defaultdict(list)
    for g in generators:
        pattern = classify_generator(g)
        pattern_members[pattern].append(g.task_name)

    n_patterns = len(pattern_members)
    if n_patterns == 0:
        return {}

    weight_per_pattern = 1.0 / n_patterns
    weights = {}
    for pattern, members in pattern_members.items():
        weight_per_gen = weight_per_pattern / len(members)
        for task_name in members:
            weights[task_name] = weight_per_gen

    return weights


def get_pattern_summary(generators: list[StepGenerator]) -> dict[str, int]:
    """Return count of generators per reasoning pattern.

    Args:
        generators: All generators.

    Returns:
        Dict mapping pattern name to generator count.
    """
    from collections import Counter
    return Counter(classify_generator(g) for g in generators)
