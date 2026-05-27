"""Atoms for combinatorics."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="formula", name="combination_count",
    content="C(n,k) = n! / (k! * (n-k)!) counts the number of ways to choose k items from n "
    "without regard to order. Also written as 'n choose k'. C(5,2) = 10.",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Combination', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Combination"))

register_atom(Atom(atom_type="formula", name="permutation_with_rep",
    content="Permutations with repetition: n^k arrangements when choosing k items from n with replacement. "
    "Without repetition: P(n,k) = n! / (n-k)!. Multiset permutations of n items with groups of "
    "sizes n1,n2,...: n! / (n1! * n2! * ...).",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Permutation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Permutation"))

register_atom(Atom(atom_type="theorem", name="pigeonhole",
    content="The pigeonhole principle: if n items are put into m containers with n > m, then at "
    "least one container holds more than one item. Generalised: at least one container holds "
    "ceil(n/m) items. Used to prove existence results.",
    tier=2, domain="combinatorics",
    source="Wikipedia contributors, 'Pigeonhole principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pigeonhole_principle"))

register_atom(Atom(atom_type="formula", name="inclusion_exclusion",
    content="Inclusion-exclusion counts the union of overlapping sets: "
    "|A1 ∪ ... ∪ An| = sum|Ai| - sum|Ai ∩ Aj| + sum|Ai ∩ Aj ∩ Ak| - ... "
    "For derangements: D(n) = n! * sum_{k=0}^{n} (-1)^k / k!.",
    tier=3, domain="combinatorics",
    source="Wikipedia contributors, 'Inclusion-exclusion principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
    prerequisites=["combination_count", "venn_diagram_count"]))

register_atom(Atom(atom_type="formula", name="stars_and_bars",
    content="Stars and bars: the number of ways to distribute n identical objects into k "
    "distinct bins is C(n+k-1, k-1). Example: distributing 5 candies among 3 children "
    "gives C(7,2) = 21 ways.",
    tier=3, domain="combinatorics",
    source="Wikipedia contributors, 'Stars and bars (combinatorics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)",
    prerequisites=["combination_count"]))
