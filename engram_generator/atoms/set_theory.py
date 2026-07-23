"""Atoms for set theory."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="definition", name="set_membership",
    content="An element x is a member of set S (x in S) if x appears in S. "
    "The empty set {} has no members. Membership is the fundamental relation in set theory.",
    tier=0, domain="sets",
    source="Wikipedia contributors, 'Element (mathematics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Element_(mathematics)"))

register_atom(Atom(atom_type="definition", name="set_union",
    content="The union of sets A and B (A ∪ B) contains all elements that are in A, in B, or in both. "
    "A ∪ B = {x : x ∈ A or x ∈ B}. Union is commutative and associative.",
    tier=0, domain="sets",
    source="Wikipedia contributors, 'Union (set theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Union_(set_theory)"))

register_atom(Atom(atom_type="definition", name="set_intersection",
    content="The intersection of A and B (A ∩ B) contains elements in both A and B. "
    "A ∩ B = {x : x ∈ A and x ∈ B}. If A ∩ B is empty, A and B are disjoint.",
    tier=0, domain="sets",
    source="Wikipedia contributors, 'Intersection (set theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Intersection_(set_theory)"))

register_atom(Atom(atom_type="definition", name="set_difference",
    content="The difference A \\ B contains elements in A but not in B. "
    "A \\ B = {x : x ∈ A and x ∉ B}. The symmetric difference A △ B = (A \\ B) ∪ (B \\ A).",
    tier=1, domain="sets",
    source="Wikipedia contributors, 'Complement (set theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Complement_(set_theory)",
    prerequisites=["set_union", "set_intersection"]))

register_atom(Atom(atom_type="definition", name="set_subset",
    content="A is a subset of B (A ⊆ B) if every element of A is also in B. "
    "A is a proper subset (A ⊂ B) if A ⊆ B and A ≠ B. The empty set is a subset of every set.",
    tier=1, domain="sets",
    source="Wikipedia contributors, 'Subset', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Subset",
    prerequisites=["set_membership"]))

register_atom(Atom(atom_type="definition", name="set_cardinality",
    content="The cardinality |S| of a finite set is the number of elements it contains. "
    "|{}| = 0. |{a, b, c}| = 3. For union: |A ∪ B| = |A| + |B| - |A ∩ B| (inclusion-exclusion).",
    tier=1, domain="sets",
    source="Wikipedia contributors, 'Cardinality', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cardinality"))

register_atom(Atom(atom_type="definition", name="power_set",
    content="The power set P(S) is the set of all subsets of S, including the empty set and S itself. "
    "If |S| = n, then |P(S)| = 2^n. For S = {a, b}, P(S) = {{}, {a}, {b}, {a, b}}.",
    tier=2, domain="sets",
    source="Wikipedia contributors, 'Power set', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Power_set",
    prerequisites=["set_subset", "set_cardinality"]))

register_atom(Atom(atom_type="definition", name="cartesian_product",
    content="The Cartesian product A × B is the set of all ordered pairs (a, b) where a ∈ A and b ∈ B. "
    "|A × B| = |A| * |B|. For A = {1, 2} and B = {x, y}: A × B = {(1,x), (1,y), (2,x), (2,y)}.",
    tier=2, domain="sets",
    source="Wikipedia contributors, 'Cartesian product', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cartesian_product",
    prerequisites=["set_cardinality"]))

register_atom(Atom(atom_type="formula", name="venn_diagram_count",
    content="For two sets: |A ∪ B| = |A| + |B| - |A ∩ B|. "
    "For three sets: |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|. "
    "This is the inclusion-exclusion principle.",
    example="|A|=30, |B|=20, |A and B|=10. |A or B| = 30 + 20 - 10 = 40",
    tier=2, domain="sets",
    source="Wikipedia contributors, 'Inclusion-exclusion principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
    prerequisites=["set_union", "set_intersection", "set_cardinality"]))
