"""Task generators organised by domain.

Each module registers its generators via the @register decorator.
Importing this package triggers all registrations.
"""
# Original tier-based modules
from engram_generator.generators import tier0  # noqa: F401
from engram_generator.generators import tier1  # noqa: F401
from engram_generator.generators import tier2  # noqa: F401
from engram_generator.generators import tier3  # noqa: F401
from engram_generator.generators import tier4  # noqa: F401
from engram_generator.generators import tier5  # noqa: F401
from engram_generator.generators import tier6  # noqa: F401
from engram_generator.generators import tier7  # noqa: F401
from engram_generator.generators import tier8  # noqa: F401
from engram_generator.generators import tier9  # noqa: F401
from engram_generator.generators import tier10  # noqa: F401

# Domain-specific modules (original)
from engram_generator.generators import physics  # noqa: F401
from engram_generator.generators import statistics  # noqa: F401
from engram_generator.generators import advanced_math  # noqa: F401
from engram_generator.generators import quantum  # noqa: F401
from engram_generator.generators import computer_science  # noqa: F401
from engram_generator.generators import science_extended  # noqa: F401
from engram_generator.generators import reasoning_extended  # noqa: F401
from engram_generator.generators import math_extended  # noqa: F401
from engram_generator.generators import ai_ml  # noqa: F401
from engram_generator.generators import expanded  # noqa: F401
from engram_generator.generators import expanded_upper  # noqa: F401

# New domain modules (properly separated)
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
