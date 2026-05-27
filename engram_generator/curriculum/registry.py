"""Registry of all generators and helper functions."""
from engram_generator.base import StepGenerator


_REGISTRY: dict[str, type[StepGenerator]] = {}
_OOS_REGISTRY: dict[str, type[StepGenerator]] = {}
_LOADED = False
_OOS_LOADED = False


def register(cls: type[StepGenerator]) -> type[StepGenerator]:
    """Decorator to register a generator class.

    Args:
        cls: StepGenerator subclass to register.

    Returns:
        The same class (unchanged).
    """
    instance = cls()
    _REGISTRY[instance.task_name] = cls
    return cls


def register_oos(cls: type[StepGenerator]) -> type[StepGenerator]:
    """Decorator to register an out-of-set generator.

    OOS generators are never included in training or validation.
    They are only used for final held-out evaluation.

    Args:
        cls: StepGenerator subclass to register.

    Returns:
        The same class (unchanged).
    """
    instance = cls()
    _OOS_REGISTRY[instance.task_name] = cls
    return cls


def _ensure_loaded() -> None:
    """Import all generator modules to trigger @register decorators."""
    global _LOADED
    if not _LOADED:
        import engram_generator.generators  # noqa: F401
        _LOADED = True


def get_generator(task_name: str, **kwargs) -> StepGenerator:
    """Instantiate a generator by task name.

    Args:
        task_name: Registered task name.
        **kwargs: Passed to the generator constructor.

    Returns:
        A StepGenerator instance.

    Raises:
        KeyError: If task_name is not registered.
    """
    _ensure_loaded()
    if task_name not in _REGISTRY:
        raise KeyError(
            f"Unknown task '{task_name}'. "
            f"Available: {sorted(_REGISTRY.keys())}"
        )
    return _REGISTRY[task_name](**kwargs)


def get_all_generators(**kwargs) -> list[StepGenerator]:
    """Instantiate all registered generators.

    Args:
        **kwargs: Passed to each generator constructor.

    Returns:
        List of StepGenerator instances.
    """
    _ensure_loaded()
    return [cls(**kwargs) for cls in _REGISTRY.values()]


def _ensure_oos_loaded() -> None:
    """Import OOS generator modules to trigger @register_oos decorators."""
    global _OOS_LOADED
    if not _OOS_LOADED:
        import engram_generator.generators.oos  # noqa: F401
        _OOS_LOADED = True


def get_oos_generator(task_name: str, **kwargs) -> StepGenerator:
    """Instantiate an OOS generator by task name.

    Args:
        task_name: Registered OOS task name.
        **kwargs: Passed to the generator constructor.

    Returns:
        A StepGenerator instance.

    Raises:
        KeyError: If task_name is not in OOS registry.
    """
    _ensure_oos_loaded()
    if task_name not in _OOS_REGISTRY:
        raise KeyError(f"Unknown OOS task '{task_name}'.")
    return _OOS_REGISTRY[task_name](**kwargs)


def get_all_oos_generators(**kwargs) -> list[StepGenerator]:
    """Instantiate all OOS generators for held-out evaluation.

    Args:
        **kwargs: Passed to each generator constructor.

    Returns:
        List of StepGenerator instances.
    """
    _ensure_oos_loaded()
    return [cls(**kwargs) for cls in _OOS_REGISTRY.values()]


_EXTRA_PREREQUISITES: dict[str, list[str]] = {
    "abstraction_level": ["dfa_accept", "shortest_path"],
    "algorithm_design": [
        "heap_operations",
        "hash_table_ops",
        "memoisation",
        "coin_change",
        "knapsack",
        "lis",
        "lcs",
        "turing_machine_step",
        "topo_sort",
    ],
    "algorithm_improvement": [
        "bipartite_check",
        "edit_distance",
        "polynomial_hash",
        "recurrence_solve",
    ],
    "analogy_completion": ["similar_triangles", "pattern_continue"],
    "angle_sum_triangle": ["angle_conversion"],
    "architecture_analysis": [
        "stack_operations",
        "bfs_order",
        "dfa_accept",
        "softmax_eval",
        "sigmoid_eval",
        "adam_step",
        "lr_decay",
        "momentum_sgd",
    ],
    "attention_score": ["softmax_eval", "weighted_sum"],
    "batch_norm": ["arithmetic_mean", "square_root"],
    "bayes_chain": ["total_probability"],
    "bfs_order": ["queue_operations"],
    "big_o": ["collatz", "rpn"],
    "binary_tree_traversal": ["recursive_trace"],
    "bipartite_check": ["dfs_order"],
    "break_even": ["percentage", "roi"],
    "call_stack_depth": ["recursive_trace"],
    "capacity_bound": ["joint_distribution"],
    "characteristic_equation": ["second_derivative", "integrating_factor"],
    "circle_arc_length": ["angle_conversion"],
    "coin_change": ["stars_and_bars"],
    "combination_count": ["permutation_with_rep", "power_set"],
    "complexity_analysis": [
        "bfs_order",
        "binary_tree_traversal",
        "big_o",
        "matrix_inverse",
        "matrix_trace",
        "matrix_transpose",
        "gaussian_elimination",
        "matrix_power",
    ],
    "complexity_comparison": ["logarithm", "polynomial_division"],
    "complexity_reduction": ["connected_components", "minimum_spanning_tree"],
    "compound_interest": ["percentage"],
    "conditional_independence": ["bayes_theorem"],
    "conjecture_generation": [
        "sequence_sum",
        "catalan",
        "derangement",
        "continued_fraction",
    ],
    "connected_components": ["dfs_order"],
    "conservation_energy": ["kinematics_displacement"],
    "constraint_optimisation": ["break_even"],
    "construct_polynomial": ["combination_count", "vector_norm", "cross_product"],
    "contrapositive": ["truth_table", "biconditional"],
    "convex_hull_check": ["point_in_polygon"],
    "coordinate_rotation": ["sin_cos_eval"],
    "counterexample": [
        "proof_by_contradiction",
        "quadratic_residue",
        "diophantine",
        "factorisation",
        "number_base_arithmetic",
        "twos_complement",
        "set_difference",
    ],
    "cross_domain_transfer": ["stoichiometry", "compound_interest", "pythagorean"],
    "crt": ["lcm"],
    "data_prescription": ["confusion_matrix", "correlation"],
    "deduction_chain": ["quantifier_eval"],
    "derive_formula": [
        "law_of_sines",
        "area_under_curve",
        "kirchhoff",
        "hubble_law",
        "redshift",
        "stellar_luminosity",
        "orbital_period",
        "schwarzschild_radius",
        "gravitational_lensing",
        "magnitude_distance",
        "sector_area",
    ],
    "derive_identity": [
        "trig_identity",
        "integration_by_parts",
        "partial_deriv_multi",
        "taylor_series",
        "series_convergence",
        "laplace_transform",
        "limit",
        "product_rule",
        "quotient_rule",
        "implicit_diff",
        "related_rates",
        "complex_arithmetic",
        "complex_modulus",
        "complex_division",
        "euler_formula",
        "de_moivre",
    ],
    "dfa_accept": ["regex_match"],
    "dfs_order": ["stack_operations"],
    "dimensional_analysis": ["unit_conversion_length", "unit_conversion_mass"],
    "direct_proof": ["logical_equivalence"],
    "efficiency_analysis": ["conv_output_size", "convolution"],
    "eigenvalue": ["matrix_trace"],
    "emergent_capability": [
        "attention_score",
        "neural_forward",
        "markov_chain",
        "markov_reward",
        "discounted_return",
        "q_value_update",
    ],
    "equation_construction": ["law_of_cosines"],
    "error_correction": ["hamming_distance", "string_encode_decode"],
    "error_detection": [
        "direct_proof",
        "boolean_eval",
        "logical_puzzle",
        "knights_knaves",
    ],
    "estimate_magnitude": [
        "scientific_notation",
        "escape_velocity",
        "gravitational_force",
        "pendulum_period",
        "kinetic_energy",
        "potential_energy",
        "momentum",
    ],
    "failure_analysis": ["proof_by_contradiction"],
    "failure_mode_classification": [
        "gradient_descent",
        "batch_norm",
        "bce_loss",
        "roc_auc",
        "kl_from_distributions",
    ],
    "fourier_coefficient": ["definite_integral"],
    "generalise_sequence": ["arithmetic_sequence", "geometric_sequence", "pattern_continue"],
    "gradient_analysis": ["separation_of_variables"],
    "graph_coloring": ["bipartite_check"],
    "group_table": ["set_operations"],
    "hamming_distance": ["palindrome_check", "anagram_check"],
    "hash_table_ops": ["modular"],
    "heap_operations": ["comparison"],
    "hypothesis_design": [
        "confidence_interval",
        "hypothesis_test",
        "poisson_dist",
        "variance_dist",
        "total_probability",
        "linear_regression",
    ],
    "hypothesis_test": ["confidence_interval", "z_score"],
    "implicit_diff": ["trig_identity"],
    "impossibility_proof": ["pigeonhole", "proof_by_contradiction", "inclusion_exclusion"],
    "inclusion_exclusion": ["venn_diagram_count"],
    "information_bottleneck": ["joint_distribution"],
    "integrating_factor": ["numerical_derivative"],
    "invariant_discovery": [
        "group_table",
        "ring_arithmetic",
        "eigenvalue",
        "tensor_product",
        "partial_fractions",
        "totient",
        "crt",
    ],
    "inverse_problem": [
        "separation_of_variables",
        "kinematics_velocity",
        "conservation_energy",
        "ohms_law",
        "wave_equation",
        "ideal_gas",
    ],
    "isomorphism_detection": ["group_table", "distance_2d"],
    "kinematics_displacement": ["kinematics_velocity"],
    "kinematics_velocity": ["time_arithmetic"],
    "laplace_transform": ["integration_by_parts"],
    "law_of_cosines": ["law_of_sines"],
    "learning_bound": ["combination_count", "joint_distribution", "mutual_information"],
    "line_intersection": ["slope"],
    "loss_design": ["bayes_chain", "kl_divergence"],
    "matrix_inverse": ["dot_product", "matrix_scalar"],
    "memoisation": ["call_stack_depth"],
    "meta_pattern": [
        "area_under_curve",
        "convergent_series",
        "divergence",
        "vigenere",
    ],
    "method_selection": [
        "bisection_method",
        "trapezoidal_rule",
        "euler_method_ode",
        "newton_raphson",
        "diff_equation",
        "system_ode",
    ],
    "minimal_axioms": [
        "group_table",
        "set_union",
        "group_order",
        "group_homomorphism",
    ],
    "minimum_spanning_tree": ["cycle_detect"],
    "novel_problem": ["bayes_chain", "convex_hull_check", "gaussian_elimination"],
    "numerical_derivative": ["significant_figures"],
    "partial_deriv_multi": ["implicit_diff"],
    "partial_fractions": ["fraction_arithmetic"],
    "pattern_continue": ["digit_root", "sequence_next"],
    "ph_calculation": ["logarithm"],
    "pigeonhole": ["median", "mode"],
    "policy_gradient": ["discounted_return"],
    "polygon_area": ["midpoint", "bounding_box"],
    "power_set": ["cartesian_product"],
    "present_value": ["depreciation"],
    "problem_construction": ["stoichiometry", "present_value"],
    "problem_transformation": [
        "coordinate_rotation",
        "reflection_2d",
        "volume_sphere",
        "volume_cylinder",
    ],
    "proof_by_cases": ["absolute_value"],
    "proof_by_contradiction": ["logical_equivalence"],
    "proof_by_induction": ["recursive_trace", "base_case_identify"],
    "propositional_eval": ["syllogism"],
    "recurrence_linear": ["expression_simplify"],
    "recurrence_solve": ["recurrence_linear"],
    "reduction": ["dfa_accept", "nfa_simulate"],
    "regex_match": ["substring_find"],
    "regularisation_design": ["dropout_compute", "bias_variance"],
    "related_rates": ["area_under_curve"],
    "representation_choice": [
        "eigenvalue",
        "fourier_coefficient",
        "bloch_coords",
        "quantum_gate",
        "pauli_product",
        "qubit_measure",
    ],
    "ring_arithmetic": ["product_notation"],
    "scaling_prediction": ["characteristic_equation"],
    "scientific_notation": ["floor_ceil", "rounding"],
    "sector_area": ["circle_arc_length"],
    "self_evaluation": ["recursive_trace", "memoisation"],
    "separation_of_variables": ["second_derivative"],
    "sequence_sum": ["arithmetic_sequence", "geometric_sequence"],
    "series_convergence": ["convergent_series"],
    "significant_figures": ["rounding"],
    "similar_triangles": ["perimeter_rectangle", "area_triangle"],
    "solution_elegance": ["memoisation", "graph_coloring"],
    "stoichiometry": ["balancing_equation", "molarity", "ph_calculation"],
    "string_encode_decode": ["run_length"],
    "strong_induction": ["summation", "prime_factorisation"],
    "successor_design": [
        "bellman_equation",
        "policy_gradient",
        "conv_2d",
        "neural_forward",
    ],
    "sufficiency_analysis": [
        "set_subset",
        "propositional_eval",
        "minimax",
        "nash_equilibrium",
    ],
    "symmetry_detection": ["area_circle", "sin_cos_eval"],
    "taylor_series": ["second_derivative", "convergent_series"],
    "time_arithmetic": ["unit_conversion_temp"],
    "training_diagnosis": ["compound_interest"],
    "turing_machine_step": ["boolean_algebra", "logic_gate_eval"],
    "verify_proof": [
        "direct_proof",
        "proof_by_contradiction",
        "proof_by_cases",
        "strong_induction",
    ],
    "volume_cylinder": ["volume_box", "circumference"],
    "volume_sphere": ["volume_box"],
    "weighted_sum": ["arithmetic_mean"],
}


def get_prerequisites(task_name: str) -> list[str]:
    """Get full prerequisites for a task including enrichments.

    Args:
        task_name: Task name.

    Returns:
        Combined prerequisite list (original + enrichments).
    """
    _ensure_loaded()
    cls = _REGISTRY.get(task_name)
    if cls is None:
        return []
    gen = cls()
    base = list(gen.prerequisites)
    extra = _EXTRA_PREREQUISITES.get(task_name, [])
    combined = list(dict.fromkeys(base + extra))
    return combined


def list_tasks() -> list[dict]:
    """List all registered tasks with metadata.

    Returns:
        List of dicts with task_name, tier, and prerequisites.
    """
    _ensure_loaded()
    result = []
    for cls in _REGISTRY.values():
        gen = cls()
        result.append({
            "task_name": gen.task_name,
            "tier": gen.tier,
            "prerequisites": get_prerequisites(gen.task_name),
        })
    return sorted(result, key=lambda x: (x["tier"], x["task_name"]))
