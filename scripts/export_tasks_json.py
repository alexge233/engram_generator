"""Export all generator tasks as JSON for the interactive skill tree."""
import json
import sys
from collections import defaultdict

from engram_generator.curriculum.registry import get_all_generators
from engram_generator.curriculum.reasoning_patterns import classify_generator


DOMAIN_KEYWORDS = {
    "Mathematics": [
        "arithmetic", "algebra", "calculus", "number_theory", "combinatorics",
        "linear_algebra", "real_analysis", "complex_analysis", "topology",
        "differential_geometry", "optimization", "measure_theory",
        "functional_analysis", "algebraic_geometry", "category_theory",
        "representation_theory", "stochastic", "pde", "tensor_analysis",
        "discrete", "abstract_algebra", "homological",
    ],
    "Physics": [
        "physics", "electromagnetism", "thermodynamics", "relativity",
        "optics", "fluid_mechanics", "nuclear_physics", "analytical_mechanics",
        "statistical_mechanics", "general_relativity", "particle_physics",
        "nonlinear_dynamics", "solid_state", "plasma", "continuum",
    ],
    "Computer Science": [
        "algorithms", "cryptography", "formal_languages", "information_theory",
        "compilers", "distributed", "ml_theory", "computer_graphics", "graphs",
        "algorithm_patterns", "cs_foundations", "advanced_ml", "dimensionality",
        "networking",
    ],
    "Chemistry": [
        "chemistry", "physical_chemistry", "organic_chemistry", "inorganic",
        "spectroscopy", "polymer",
    ],
    "Biology": [
        "genetics", "biochemistry", "cell_biology", "bioinformatics",
        "ecology", "epidemiology", "pharmacology", "neuroscience",
        "systems_biology",
    ],
    "Engineering": [
        "signal_processing", "control_theory", "materials", "aerospace",
        "power_systems", "antenna", "semiconductor", "photonics",
        "structural", "digital_electronics", "telecom", "robotics",
    ],
    "Quantum": [
        "quantum",
    ],
    "Logic": [
        "logic", "proof_theory", "model_theory", "computability",
    ],
    "Earth & Space": [
        "astronomy", "geology", "climate", "oceanography", "geophysics",
    ],
    "Social": [
        "economics", "game_theory", "linguistics", "decision_theory",
        "network_science", "cognitive", "causal",
    ],
    "Meta-Reasoning": [
        "meta_reasoning", "open_problems", "bridge",
    ],
}


def get_domain(module_name: str) -> str:
    """Classify a generator's module into a domain.

    Args:
        module_name: The module name (last component).

    Returns:
        Domain string.
    """
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in module_name for kw in keywords):
            return domain
    return "Other"


def main() -> None:
    """Export tasks to JSON."""
    gens = get_all_generators()
    tasks = []

    for g in gens:
        prereqs = g.prerequisites if hasattr(g, "prerequisites") and g.prerequisites else []
        pattern = classify_generator(g)
        mod = type(g).__module__.split(".")[-1]
        tasks.append({
            "name": g.task_name,
            "tier": g.tier,
            "prereqs": prereqs,
            "pattern": pattern,
            "domain": get_domain(mod),
        })

    output = {"tasks": tasks}
    json.dump(output, sys.stdout, separators=(",", ":"))
    print(f"\n{len(tasks)} tasks exported", file=sys.stderr)


if __name__ == "__main__":
    main()
