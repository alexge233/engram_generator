"""Registry for knowledge atoms — theorems, formulas, and definitions."""
from engram_generator.base import Atom


_ATOMS: dict[str, Atom] = {}

_TASK_TO_ATOM: dict[str, str] = {
    "adam_step": "adam_optimizer",
    "batch_norm": "batch_normalization",
    "bce_loss": "binary_cross_entropy",
    "bias_variance": "bias_variance_tradeoff",
    "dropout_compute": "dropout",
    "lr_decay": "learning_rate_decay",
    "momentum": "momentum_sgd",
    "mse_loss": "mean_squared_error",
    "q_value_update": "q_learning",
    "oos_symbolic_logic": "propositional_logic",
    "oos_unit_conversion": "unit_conversion",
    "oos_state_machine": "finite_state_machine",
    "oos_program_trace": "program_tracing",
    "oos_musical_interval": "musical_interval",
}


def register_atom(atom: Atom) -> Atom:
    """Register a knowledge atom.

    Args:
        atom: The atom to register.

    Returns:
        The same atom.
    """
    _ATOMS[atom.name] = atom
    return atom


def get_atom(name: str) -> Atom:
    """Retrieve an atom by name or by task name alias.

    Args:
        name: Atom name or task name.

    Returns:
        The matching atom.

    Raises:
        KeyError: If atom not found.
    """
    if name in _ATOMS:
        return _ATOMS[name]
    mapped = _TASK_TO_ATOM.get(name)
    if mapped and mapped in _ATOMS:
        return _ATOMS[mapped]
    raise KeyError(name)


def get_atoms_for_tier(tier: int) -> list[Atom]:
    """Return all atoms for a given tier.

    Args:
        tier: Tier number.

    Returns:
        List of atoms at that tier.
    """
    return [a for a in _ATOMS.values() if a.tier == tier]


def get_atoms_for_domain(domain: str) -> list[Atom]:
    """Return all atoms for a given domain.

    Args:
        domain: Domain name.

    Returns:
        List of atoms in that domain.
    """
    return [a for a in _ATOMS.values() if a.domain == domain]


def get_all_atoms() -> list[Atom]:
    """Return all registered atoms.

    Returns:
        List of all atoms.
    """
    return list(_ATOMS.values())
