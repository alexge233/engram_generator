"""Atoms for string and pattern manipulation."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


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
