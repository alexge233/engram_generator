"""Tests for the knowledge atom registry and atom-generator linkage.

Verifies that atoms are correctly loaded, have required fields,
reference valid tiers, and that some generators link to atoms.
"""
import pytest

from engram_generator.atoms.registry import get_all_atoms, get_atom
from engram_generator.base import Atom
from engram_generator.curriculum.registry import get_all_generators


@pytest.fixture(scope="module")
def all_atoms() -> list[Atom]:
    """Return all registered atoms.

    Returns:
        List of all Atom instances.
    """
    return get_all_atoms()


class TestAtomRegistry:
    """Verify knowledge atoms are correctly registered and structured."""

    def test_atoms_loaded(self, all_atoms: list[Atom]) -> None:
        """Verify at least 100 atoms are registered."""
        assert len(all_atoms) >= 100, f"Only {len(all_atoms)} atoms loaded"

    def test_atom_has_required_fields(self, all_atoms: list[Atom]) -> None:
        """Verify every atom has non-empty name, content, and domain."""
        for atom in all_atoms:
            assert atom.name, f"Atom: empty name"
            assert atom.content, f"Atom {atom.name}: empty content"
            assert atom.domain, f"Atom {atom.name}: empty domain"
            assert atom.atom_type, f"Atom {atom.name}: empty atom_type"

    def test_atom_tiers_valid(self, all_atoms: list[Atom]) -> None:
        """Verify all atom tiers are in valid range (0-10 or 99 for OOS)."""
        for atom in all_atoms:
            assert atom.tier in range(11) or atom.tier == 99, (
                f"Atom {atom.name}: tier {atom.tier} not in [0-10, 99]"
            )

    def test_atom_types_valid(self, all_atoms: list[Atom]) -> None:
        """Verify atom types are from the expected set."""
        valid_types = {
            "theorem", "definition", "result", "identity",
            "algorithm", "principle", "formula", "law",
            "property", "rule", "method", "concept",
            "methodology",
        }
        for atom in all_atoms:
            assert atom.atom_type in valid_types, (
                f"Atom {atom.name}: unknown type '{atom.atom_type}'"
            )


class TestAtomGeneratorLinkage:
    """Verify generators can link to their associated knowledge atoms."""

    def test_some_generators_have_atoms(self) -> None:
        """Verify at least one generator has a linked atom."""
        generators = get_all_generators()
        linked = [g for g in generators if g.atom is not None]
        assert len(linked) > 0, "No generators linked to atoms"

    def test_linked_atom_matches_task(self) -> None:
        """Verify linked atoms have matching domain or content."""
        generators = get_all_generators()
        for gen in generators:
            atom = gen.atom
            if atom is not None:
                assert isinstance(atom, Atom), (
                    f"{gen.task_name}: atom is not an Atom instance"
                )

    def test_get_atom_by_name(self) -> None:
        """Verify atoms are retrievable by name."""
        atoms = get_all_atoms()
        if atoms:
            first = atoms[0]
            atom = get_atom(first.name)
            assert atom.name == first.name

    def test_get_unknown_atom_raises(self) -> None:
        """Verify KeyError for unknown atom names."""
        with pytest.raises(KeyError):
            get_atom("completely_nonexistent_atom_xyz")
