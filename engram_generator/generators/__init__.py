"""Task generators organised by domain.

Each module registers its generators via the @register decorator.
Importing this package triggers all registrations.

Module naming convention:
- Domain modules: named after the subject domain (geometry, logic, etc.)
- Meta-reasoning modules: split by tier (meta_reasoning_t7, t8, t9, t10)
- Core modules: fundamental operations (arithmetic_core, arithmetic_ops)
"""
# Core arithmetic and operations
from engram_generator.generators import arithmetic_core  # noqa: F401
from engram_generator.generators import arithmetic_ops  # noqa: F401

# Mathematical domains by complexity
from engram_generator.generators import intermediate_math  # noqa: F401
from engram_generator.generators import advanced_ops  # noqa: F401
from engram_generator.generators import applied_math  # noqa: F401
from engram_generator.generators import expert_analysis  # noqa: F401
from engram_generator.generators import graduate_foundations  # noqa: F401
from engram_generator.generators import expanded_core  # noqa: F401
from engram_generator.generators import pure_math  # noqa: F401
from engram_generator.generators import advanced_analysis  # noqa: F401

# Applied science and CS
from engram_generator.generators import applied_science  # noqa: F401
from engram_generator.generators import cs_foundations  # noqa: F401

# Meta-reasoning (tiers 7-10)
from engram_generator.generators import meta_reasoning_t7  # noqa: F401
from engram_generator.generators import meta_reasoning_t8  # noqa: F401
from engram_generator.generators import meta_reasoning_t9  # noqa: F401
from engram_generator.generators import meta_reasoning_t10  # noqa: F401
from engram_generator.generators import meta_reasoning_ext  # noqa: F401
from engram_generator.generators import meta_reasoning_upper  # noqa: F401

# Domain-specific modules (new, properly structured)
from engram_generator.generators import geometry  # noqa: F401
from engram_generator.generators import logic  # noqa: F401
from engram_generator.generators import set_theory  # noqa: F401
from engram_generator.generators import strings  # noqa: F401
from engram_generator.generators import trigonometry  # noqa: F401
from engram_generator.generators import measurement  # noqa: F401
from engram_generator.generators import sequences  # noqa: F401
from engram_generator.generators import combinatorics  # noqa: F401
from engram_generator.generators import chemistry  # noqa: F401
from engram_generator.generators import economics  # noqa: F401
from engram_generator.generators import game_theory  # noqa: F401
from engram_generator.generators import automata  # noqa: F401
from engram_generator.generators import spatial  # noqa: F401
from engram_generator.generators import numerical  # noqa: F401
from engram_generator.generators import graphs  # noqa: F401
from engram_generator.generators import data_structures  # noqa: F401
from engram_generator.generators import recursion  # noqa: F401
from engram_generator.generators import bridge_deep  # noqa: F401

# Original domain modules
from engram_generator.generators import physics  # noqa: F401
from engram_generator.generators import statistics  # noqa: F401
from engram_generator.generators import quantum  # noqa: F401
from engram_generator.generators import ai_ml  # noqa: F401
from engram_generator.generators import oos  # noqa: F401
