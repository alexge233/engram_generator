"""Knowledge atoms — self-contained theorems, definitions, and formulas.

Each domain module registers its atoms via register_atom().
Importing this package triggers all registrations.
"""
# Original domain atoms
from engram_generator.atoms import physics  # noqa: F401
from engram_generator.atoms import science  # noqa: F401
from engram_generator.atoms import reasoning  # noqa: F401
from engram_generator.atoms import mathematics  # noqa: F401
from engram_generator.atoms import calculus  # noqa: F401
from engram_generator.atoms import sourced  # noqa: F401
from engram_generator.atoms import ai_ml  # noqa: F401
from engram_generator.atoms import oos  # noqa: F401

# New domain atoms (properly separated)
from engram_generator.atoms import geometry  # noqa: F401
from engram_generator.atoms import logic  # noqa: F401
from engram_generator.atoms import set_theory  # noqa: F401
from engram_generator.atoms import strings  # noqa: F401
from engram_generator.atoms import trigonometry  # noqa: F401
from engram_generator.atoms import measurement  # noqa: F401
from engram_generator.atoms import sequences  # noqa: F401
from engram_generator.atoms import combinatorics  # noqa: F401
from engram_generator.atoms import chemistry  # noqa: F401
from engram_generator.atoms import economics  # noqa: F401
from engram_generator.atoms import game_theory  # noqa: F401
from engram_generator.atoms import automata  # noqa: F401
from engram_generator.atoms import spatial  # noqa: F401
from engram_generator.atoms import numerical  # noqa: F401
from engram_generator.atoms import graph_ds_recursion  # noqa: F401
from engram_generator.atoms import bridge_deep  # noqa: F401
from engram_generator.atoms import missing_fill  # noqa: F401
