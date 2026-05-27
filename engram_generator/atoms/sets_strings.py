"""Knowledge atoms for set theory and string/pattern manipulation."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Set Theory ──────────────────────────────────────────────────────

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
    tier=2, domain="sets",
    source="Wikipedia contributors, 'Inclusion-exclusion principle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle",
    prerequisites=["set_union", "set_intersection", "set_cardinality"]))

# ── String / Pattern ───────────────────────────────────────────────

register_atom(Atom(atom_type="algorithm", name="string_reverse",
    content="Reversing a string produces the characters in opposite order. "
    "'hello' reversed is 'olleh'. Reversal is its own inverse: reversing twice yields the original.",
    tier=0, domain="strings",
    source="Wikipedia contributors, 'String (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/String_(computer_science)"))

register_atom(Atom(atom_type="algorithm", name="character_count",
    content="Count occurrences of a character in a string by scanning left to right and incrementing "
    "a counter each time the target character is found. 'banana' has 3 'a's.",
    tier=0, domain="strings",
    source="Wikipedia contributors, 'String (computer science)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/String_(computer_science)"))

register_atom(Atom(atom_type="algorithm", name="palindrome_check",
    content="A palindrome reads the same forwards and backwards. 'racecar' is a palindrome; 'hello' is not. "
    "Check by comparing the string to its reverse, or by comparing characters from both ends inward.",
    tier=0, domain="strings",
    source="Wikipedia contributors, 'Palindrome', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Palindrome",
    prerequisites=["string_reverse"]))

register_atom(Atom(atom_type="algorithm", name="substring_find",
    content="Finding a substring within a string: scan the text for the first position where "
    "the pattern matches. The naive algorithm checks every position, taking O(n*m) time. "
    "Return the zero-based index or -1 if not found.",
    tier=1, domain="strings",
    source="Wikipedia contributors, 'String-searching algorithm', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/String-searching_algorithm"))

register_atom(Atom(atom_type="algorithm", name="anagram_check",
    content="Two strings are anagrams if one can be rearranged to form the other. "
    "Equivalently, they are anagrams if they have the same character frequency counts. "
    "'listen' and 'silent' are anagrams.",
    tier=1, domain="strings",
    source="Wikipedia contributors, 'Anagram', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Anagram",
    prerequisites=["character_count"]))

register_atom(Atom(atom_type="algorithm", name="pattern_continue",
    content="Pattern continuation: identify the rule governing a sequence and predict the next element. "
    "Common patterns include arithmetic progressions (add constant), geometric (multiply constant), "
    "repeating cycles, and interleaved sequences.",
    tier=1, domain="strings",
    source="Wikipedia contributors, 'Pattern recognition', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pattern_recognition"))

register_atom(Atom(atom_type="algorithm", name="hamming_distance",
    content="The Hamming distance between two strings of equal length is the number of positions "
    "at which the corresponding characters differ. For '1011' and '1001', the Hamming distance is 1 "
    "(they differ at position 2).",
    tier=2, domain="strings",
    source="Wikipedia contributors, 'Hamming distance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hamming_distance",
    prerequisites=["character_count"]))

register_atom(Atom(atom_type="algorithm", name="string_encode_decode",
    content="Run-length encoding compresses consecutive repeated characters: 'aaabbc' becomes '3a2b1c'. "
    "Decoding reverses this: repeat each character by its count. This is lossless compression.",
    tier=2, domain="strings",
    source="Wikipedia contributors, 'Run-length encoding', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Run-length_encoding",
    prerequisites=["character_count"]))

register_atom(Atom(atom_type="definition", name="regex_match",
    content="Regular expressions define patterns for string matching. "
    "Basic syntax: '.' matches any character, '*' matches zero or more of the preceding, "
    "'+' matches one or more, '?' matches zero or one, '[abc]' matches any of a/b/c, "
    "'\\d' matches a digit. A string matches a regex if the entire string conforms to the pattern.",
    tier=3, domain="strings",
    source="Wikipedia contributors, 'Regular expression', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Regular_expression",
    prerequisites=["pattern_continue"]))
