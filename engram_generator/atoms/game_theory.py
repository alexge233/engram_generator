"""Atoms for game theory."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="definition", name="payoff_matrix",
    content="A payoff matrix shows the outcomes for each combination of strategies by players. "
    "Each cell contains payoffs (row_player, column_player). "
    "In the Prisoner's Dilemma: (C,C)=(3,3), (C,D)=(0,5), (D,C)=(5,0), (D,D)=(1,1).",
    tier=3, domain="game_theory",
    source="Wikipedia contributors, 'Normal-form game', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal-form_game"))

register_atom(Atom(atom_type="definition", name="dominant_strategy",
    content="A strategy dominates another if it yields a better payoff regardless of what the "
    "opponent does. A player's dominant strategy (if it exists) is the optimal choice. "
    "In Prisoner's Dilemma, 'Defect' is dominant for both players.",
    tier=3, domain="game_theory",
    source="Wikipedia contributors, 'Dominant strategy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dominant_strategy",
    prerequisites=["payoff_matrix"]))

register_atom(Atom(atom_type="definition", name="nash_equilibrium",
    content="A Nash equilibrium is a strategy profile where no player can improve their payoff "
    "by unilaterally changing strategy. In pure strategies, check each cell: if neither player "
    "benefits from deviating, it is a Nash equilibrium. A game may have zero, one, or multiple NE.",
    tier=4, domain="game_theory",
    source="Wikipedia contributors, 'Nash equilibrium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nash_equilibrium",
    prerequisites=["dominant_strategy"]))

register_atom(Atom(atom_type="algorithm", name="minimax",
    content="Minimax strategy: maximise the minimum payoff. The maximising player picks the strategy "
    "whose worst-case outcome is highest. For zero-sum games, this is optimal. "
    "Minimax value = max over rows of (min over columns of payoff).",
    tier=4, domain="game_theory",
    source="Wikipedia contributors, 'Minimax', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Minimax",
    prerequisites=["payoff_matrix"]))
