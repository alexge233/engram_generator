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
    # Tier 7: wire in new domains
    "verify_proof": ["direct_proof", "proof_by_contradiction"],
    "dimensional_analysis": ["unit_conversion_length", "unit_conversion_mass"],
    "symmetry_detection": ["area_circle", "sin_cos_eval"],
    "proof_by_induction": ["recursive_trace", "base_case_identify"],
    "error_detection": ["direct_proof", "boolean_eval"],
    "complexity_analysis": ["bfs_order", "binary_tree_traversal", "big_o"],
    "construct_polynomial": ["combination_count"],
    "estimate_magnitude": ["scientific_notation"],
    "inverse_problem": ["separation_of_variables"],
    "method_selection": ["bisection_method", "trapezoidal_rule"],
    "constraint_optimisation": ["break_even"],
    "generalise_sequence": ["arithmetic_sequence", "geometric_sequence", "pattern_continue"],
    "counterexample": ["proof_by_contradiction"],
    "sufficiency_analysis": ["set_subset", "propositional_eval"],
    # Tier 8: wire through tier 7
    "isomorphism_detection": ["group_table", "distance_2d"],
    "analogy_completion": ["similar_triangles", "pattern_continue"],
    "conjecture_generation": ["sequence_sum"],
    "cross_domain_transfer": ["stoichiometry", "compound_interest", "pythagorean"],
    "equation_construction": ["law_of_cosines"],
    "self_evaluation": ["recursive_trace", "memoisation"],
    "problem_transformation": ["coordinate_rotation", "reflection_2d"],
    "abstraction_level": ["dfa_accept", "shortest_path"],
    # Tier 9: wire through 7-8
    "algorithm_design": ["heap_operations", "hash_table_ops", "memoisation"],
    "invariant_discovery": ["group_table", "ring_arithmetic"],
    "learning_bound": ["combination_count", "joint_distribution"],
    "failure_analysis": ["proof_by_contradiction"],
    "impossibility_proof": ["pigeonhole", "proof_by_contradiction"],
    "information_bottleneck": ["joint_distribution"],
    # Tier 10: wire through 8-9
    "architecture_analysis": ["stack_operations", "bfs_order", "dfa_accept"],
    "gradient_analysis": ["separation_of_variables"],
    "loss_design": ["bayes_chain", "kl_divergence"],
    "training_diagnosis": ["compound_interest"],
    # Bridge enrichments for tiers 4-6 connectivity
    "derive_formula": ["law_of_sines", "area_under_curve"],
    "derive_identity": ["trig_identity"],
    "error_correction": ["hamming_distance"],
    "problem_construction": ["stoichiometry", "present_value"],
    "complexity_reduction": ["connected_components", "minimum_spanning_tree"],
    "minimal_axioms": ["group_table", "set_union"],
    "novel_problem": ["bayes_chain", "convex_hull_check"],
    "solution_elegance": ["memoisation", "graph_coloring"],
    "algorithm_improvement": ["bipartite_check", "edit_distance"],
    "hypothesis_design": ["confidence_interval", "hypothesis_test"],
    "meta_pattern": ["area_under_curve", "convergent_series"],
    "reduction": ["dfa_accept", "nfa_simulate"],
    "representation_choice": ["eigenvalue", "fourier_coefficient"],
    "capacity_bound": ["joint_distribution"],
    "data_prescription": ["confusion_matrix", "correlation"],
    "efficiency_analysis": ["conv_output_size", "convolution"],
    "emergent_capability": ["attention_score", "neural_forward"],
    "failure_mode_classification": ["gradient_descent", "batch_norm"],
    "scaling_prediction": ["characteristic_equation"],
    "successor_design": ["bellman_equation", "policy_gradient"],
    "regularisation_design": ["dropout_compute", "bias_variance"],
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
