"""Linguistics generators.

5 generators across tiers 3-6 covering Chomsky hierarchy classification,
morpheme parsing, syntax tree construction, phonetic feature identification,
and regular language checking.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Chomsky Classify (tier 5)
# ---------------------------------------------------------------------------

@register
class ChomskyClassifyGenerator(StepGenerator):
    """Classify a grammar in the Chomsky hierarchy.

    Given a grammar description with production rules, determine whether
    it is regular (Type 3), context-free (Type 2), context-sensitive
    (Type 1), or unrestricted (Type 0) based on the form of its rules.
    """

    _GRAMMARS: list[dict] = [
        {
            "rules": "A -> aB; A -> a; B -> bA; B -> b",
            "explanation": "all rules have form A -> aB or A -> a (right-linear)",
            "classification": "Type 3 (regular)",
            "level": "regular",
        },
        {
            "rules": "S -> aSb; S -> ab",
            "explanation": "LHS is single nonterminal; RHS has mixed terminals and nonterminals",
            "classification": "Type 2 (context-free)",
            "level": "context-free",
        },
        {
            "rules": "S -> aSBC; CB -> BC; aB -> ab; bB -> bb; bC -> bc; cC -> cc",
            "explanation": "CB -> BC has |LHS| <= |RHS| but LHS is not single nonterminal",
            "classification": "Type 1 (context-sensitive)",
            "level": "context-sensitive",
        },
        {
            "rules": "S -> ACaB; Aa -> a; A -> eps",
            "explanation": "A -> eps shrinks the string; no length-preserving guarantee",
            "classification": "Type 0 (unrestricted)",
            "level": "unrestricted",
        },
        {
            "rules": "S -> aS; S -> bS; S -> eps",
            "explanation": "all rules have form A -> xB or A -> x or A -> eps (regular)",
            "classification": "Type 3 (regular)",
            "level": "regular",
        },
        {
            "rules": "S -> SS; S -> (S); S -> ()",
            "explanation": "LHS is single nonterminal; context-free productions",
            "classification": "Type 2 (context-free)",
            "level": "context-free",
        },
        {
            "rules": "S -> abc; S -> aAbc; Ab -> bA; Ac -> Bbcc; bB -> Bb; aB -> aaA; aB -> aa",
            "explanation": "context-dependent rules like Ab -> bA; length non-decreasing",
            "classification": "Type 1 (context-sensitive)",
            "level": "context-sensitive",
        },
        {
            "rules": "S -> aB; B -> bC; C -> c",
            "explanation": "all rules A -> xB or A -> x (right-linear grammar)",
            "classification": "Type 3 (regular)",
            "level": "regular",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chomsky_classify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["cfg_derivation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "classify grammar in Chomsky hierarchy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Chomsky classification problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._GRAMMARS)
        grammar = self._GRAMMARS[idx]
        problem = f"grammar: {grammar['rules']}; classify in Chomsky hierarchy"
        return problem, {
            "rules": grammar["rules"],
            "explanation": grammar["explanation"],
            "classification": grammar["classification"],
            "level": grammar["level"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate classification reasoning steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps explaining the classification logic.
        """
        return [
            f"examine rules: {sd['rules']}",
            f"analysis: {sd['explanation']}",
            f"classify: {sd['classification']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Chomsky hierarchy classification.

        Args:
            sd: All computed solution information.

        Returns:
            Classification label.
        """
        return sd["classification"]


# ---------------------------------------------------------------------------
# 2. Morpheme Parse (tier 3)
# ---------------------------------------------------------------------------

@register
class MorphemeParseGenerator(StepGenerator):
    """Count morphemes in an English word.

    Identifies prefix, root, and suffix components of a word and returns
    the total morpheme count. E.g., 'unhappiness' = un + happy + ness = 3.
    """

    _WORDS: list[dict] = [
        {"word": "unhappiness", "parts": ["un", "happy", "ness"], "count": 3},
        {"word": "unkindly", "parts": ["un", "kind", "ly"], "count": 3},
        {"word": "rewriting", "parts": ["re", "writ", "ing"], "count": 3},
        {"word": "disagree", "parts": ["dis", "agree"], "count": 2},
        {"word": "teacher", "parts": ["teach", "er"], "count": 2},
        {"word": "replayed", "parts": ["re", "play", "ed"], "count": 3},
        {"word": "unbreakable", "parts": ["un", "break", "able"], "count": 3},
        {"word": "displacement", "parts": ["dis", "place", "ment"], "count": 3},
        {"word": "preschool", "parts": ["pre", "school"], "count": 2},
        {"word": "misjudgment", "parts": ["mis", "judg", "ment"], "count": 3},
        {"word": "reopened", "parts": ["re", "open", "ed"], "count": 3},
        {"word": "unfairness", "parts": ["un", "fair", "ness"], "count": 3},
        {"word": "bicycle", "parts": ["bi", "cycle"], "count": 2},
        {"word": "predetermined", "parts": ["pre", "determin", "ed"], "count": 3},
        {"word": "international", "parts": ["inter", "nation", "al"], "count": 3},
        {"word": "cat", "parts": ["cat"], "count": 1},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "morpheme_parse"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "count morphemes in English word"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a morpheme parsing problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Higher difficulty picks words with more morphemes
        candidates = [w for w in self._WORDS if w["count"] >= min(difficulty // 2 + 1, 3)]
        if not candidates:
            candidates = self._WORDS
        word_entry = candidates[self._rng.randint(0, len(candidates) - 1)]
        problem = f"count morphemes: '{word_entry['word']}'"
        return problem, {
            "word": word_entry["word"],
            "parts": word_entry["parts"],
            "count": word_entry["count"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate morpheme identification steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing the decomposition.
        """
        parts_str = " + ".join(sd["parts"])
        return [
            f"word: {sd['word']}",
            f"decompose: {parts_str}",
            f"count: {sd['count']} morphemes",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the morpheme count.

        Args:
            sd: All computed solution information.

        Returns:
            Morpheme count.
        """
        return str(sd["count"])


# ---------------------------------------------------------------------------
# 3. Syntax Tree (tier 4)
# ---------------------------------------------------------------------------

@register
class SyntaxTreeGenerator(StepGenerator):
    """Build a simple parse tree for an English sentence.

    Uses phrase structure rules (S -> NP VP, NP -> Det N, VP -> V NP)
    and outputs the tree as bracketed notation.
    """

    _DETERMINERS: list[str] = ["the", "a", "this", "that", "each"]
    _NOUNS: list[str] = ["cat", "dog", "bird", "fish", "man", "child"]
    _VERBS: list[str] = ["chased", "saw", "caught", "found", "liked"]
    _ADJECTIVES: list[str] = ["big", "small", "old", "red", "fast"]
    _PREPOSITIONS: list[str] = ["in", "on", "near", "by"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "syntax_tree"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "build parse tree as bracketed notation"

    def _pick(self, items: list[str]) -> str:
        """Pick a random item from a list.

        Args:
            items: List of choices.

        Returns:
            A randomly chosen item.
        """
        return items[self._rng.randint(0, len(items) - 1)]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a syntax tree problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        det1 = self._pick(self._DETERMINERS)
        n1 = self._pick(self._NOUNS)
        v = self._pick(self._VERBS)
        det2 = self._pick(self._DETERMINERS)
        n2 = self._pick(self._NOUNS)

        # Basic: S -> NP VP, NP -> Det N, VP -> V NP
        sentence = f"{det1} {n1} {v} {det2} {n2}"
        np1 = f"[NP [Det {det1}] [N {n1}]]"
        np2 = f"[NP [Det {det2}] [N {n2}]]"
        vp = f"[VP [V {v}] {np2}]"
        tree = f"[S {np1} {vp}]"

        steps = [
            f"S -> NP VP",
            f"NP -> Det N: {np1}",
            f"VP -> V NP: {vp}",
        ]

        # Add PP for higher difficulty
        if difficulty >= 5:
            prep = self._pick(self._PREPOSITIONS)
            det3 = self._pick(self._DETERMINERS)
            n3 = self._pick(self._NOUNS)
            pp_np = f"[NP [Det {det3}] [N {n3}]]"
            pp = f"[PP [P {prep}] {pp_np}]"
            vp = f"[VP [V {v}] {np2} {pp}]"
            tree = f"[S {np1} {vp}]"
            sentence = f"{det1} {n1} {v} {det2} {n2} {prep} {det3} {n3}"
            steps.append(f"PP -> P NP: {pp}")

        # Add AdjP for higher difficulty
        if difficulty >= 7:
            adj = self._pick(self._ADJECTIVES)
            np1 = f"[NP [Det {det1}] [AdjP [Adj {adj}]] [N {n1}]]"
            tree = f"[S {np1} {vp}]"
            sentence = f"{det1} {adj} {n1} {v} {det2} {n2}"
            if difficulty >= 5:
                prep = self._pick(self._PREPOSITIONS)
                det3 = self._pick(self._DETERMINERS)
                n3 = self._pick(self._NOUNS)
                sentence += f" {prep} {det3} {n3}"
            steps.insert(1, f"NP -> Det AdjP N: {np1}")

        problem = f"rules: S->NP VP, NP->Det N, VP->V NP; parse: '{sentence}'"
        return problem, {"tree": tree, "steps": steps}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate parse tree construction steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps showing rule applications.
        """
        return sd["steps"]

    def _create_answer(self, sd: dict) -> str:
        """Return the bracketed parse tree.

        Args:
            sd: All computed solution information.

        Returns:
            Bracketed notation tree.
        """
        return sd["tree"]


# ---------------------------------------------------------------------------
# 4. Phonetic Features (tier 4)
# ---------------------------------------------------------------------------

@register
class PhoneticFeaturesGenerator(StepGenerator):
    """Identify distinctive features of a phoneme.

    Given a phoneme symbol, determine its voicing (voiced/voiceless),
    place of articulation, and manner of articulation.
    """

    _PHONEMES: list[dict] = [
        {"symbol": "/p/", "voicing": "voiceless", "place": "bilabial", "manner": "plosive"},
        {"symbol": "/b/", "voicing": "voiced", "place": "bilabial", "manner": "plosive"},
        {"symbol": "/t/", "voicing": "voiceless", "place": "alveolar", "manner": "plosive"},
        {"symbol": "/d/", "voicing": "voiced", "place": "alveolar", "manner": "plosive"},
        {"symbol": "/k/", "voicing": "voiceless", "place": "velar", "manner": "plosive"},
        {"symbol": "/g/", "voicing": "voiced", "place": "velar", "manner": "plosive"},
        {"symbol": "/f/", "voicing": "voiceless", "place": "labiodental", "manner": "fricative"},
        {"symbol": "/v/", "voicing": "voiced", "place": "labiodental", "manner": "fricative"},
        {"symbol": "/s/", "voicing": "voiceless", "place": "alveolar", "manner": "fricative"},
        {"symbol": "/z/", "voicing": "voiced", "place": "alveolar", "manner": "fricative"},
        {"symbol": "/m/", "voicing": "voiced", "place": "bilabial", "manner": "nasal"},
        {"symbol": "/n/", "voicing": "voiced", "place": "alveolar", "manner": "nasal"},
        {"symbol": "/l/", "voicing": "voiced", "place": "alveolar", "manner": "lateral"},
        {"symbol": "/r/", "voicing": "voiced", "place": "alveolar", "manner": "approximant"},
        {"symbol": "/w/", "voicing": "voiced", "place": "bilabial", "manner": "approximant"},
        {"symbol": "/j/", "voicing": "voiced", "place": "palatal", "manner": "approximant"},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "phonetic_features"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["set_membership"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "identify phoneme distinctive features"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a phonetic features identification problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Pick one or two phonemes depending on difficulty
        if difficulty >= 5:
            indices = self._rng.sample(range(len(self._PHONEMES)), 2)
            phonemes = [self._PHONEMES[i] for i in indices]
            symbols = ", ".join(p["symbol"] for p in phonemes)
            problem = f"identify features of {symbols} and compare"
            # Find shared and distinct features
            shared = []
            distinct = []
            for feat in ["voicing", "place", "manner"]:
                if phonemes[0][feat] == phonemes[1][feat]:
                    shared.append(f"{feat}={phonemes[0][feat]}")
                else:
                    distinct.append(
                        f"{feat}: {phonemes[0]['symbol']}={phonemes[0][feat]}, "
                        f"{phonemes[1]['symbol']}={phonemes[1][feat]}"
                    )
            return problem, {
                "phonemes": phonemes,
                "shared": shared,
                "distinct": distinct,
                "compare": True,
            }
        else:
            idx = difficulty % len(self._PHONEMES)
            phoneme = self._PHONEMES[idx]
            problem = f"identify features: {phoneme['symbol']}"
            return problem, {
                "phonemes": [phoneme],
                "compare": False,
            }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate feature identification steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps listing each feature.
        """
        steps = []
        for p in sd["phonemes"]:
            steps.append(
                f"{p['symbol']}: {p['voicing']}, {p['place']}, {p['manner']}"
            )
        if sd["compare"]:
            if sd["shared"]:
                steps.append(f"shared: {'; '.join(sd['shared'])}")
            if sd["distinct"]:
                steps.append(f"differ: {'; '.join(sd['distinct'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the phoneme feature set.

        Args:
            sd: All computed solution information.

        Returns:
            Feature description string.
        """
        parts = []
        for p in sd["phonemes"]:
            parts.append(f"{p['symbol']}: {p['voicing']} {p['place']} {p['manner']}")
        return "; ".join(parts)


# ---------------------------------------------------------------------------
# 5. Regular Language Check (tier 6)
# ---------------------------------------------------------------------------

@register
class RegularLanguageCheckGenerator(StepGenerator):
    """Determine whether a given language is regular.

    Applies closure properties or pumping lemma arguments to decide
    regularity. Provides the reasoning chain for the verdict.
    """

    _LANGUAGES: list[dict] = [
        {
            "desc": "L = {w in {a,b}* | w contains substring 'ab'}",
            "is_regular": True,
            "argument": "matched by regex (a|b)*ab(a|b)*; build 3-state DFA",
            "verdict": "REGULAR",
        },
        {
            "desc": "L = {a^n b^n | n >= 0}",
            "is_regular": False,
            "argument": "pumping: s=a^p b^p, y=a^k, pump down gives a^(p-k) b^p not in L",
            "verdict": "NOT REGULAR",
        },
        {
            "desc": "L = {w in {0,1}* | w has even number of 1s}",
            "is_regular": True,
            "argument": "2-state DFA: q0 (even, accept), q1 (odd); 0 self-loops, 1 toggles",
            "verdict": "REGULAR",
        },
        {
            "desc": "L = {a^n | n is prime}",
            "is_regular": False,
            "argument": "pumping: s=a^p (p prime, p>=pumping length), y=a^k; "
                        "|xy^0z|=p-k, |xy^2z|=p+k; gap between consecutive primes grows",
            "verdict": "NOT REGULAR",
        },
        {
            "desc": "L = {w in {a,b}* | |w| is even}",
            "is_regular": True,
            "argument": "2-state DFA: q0 (even length, accept), q1 (odd); every symbol toggles",
            "verdict": "REGULAR",
        },
        {
            "desc": "L = {ww^R | w in {a,b}*}",
            "is_regular": False,
            "argument": "pumping: s=a^p b^p b^p a^p, y=a^k in first segment; "
                        "pumped string breaks palindrome symmetry",
            "verdict": "NOT REGULAR",
        },
        {
            "desc": "L = {a^i b^j | i != j}",
            "is_regular": False,
            "argument": "complement is {a^n b^n} union a*b*\\{a^i b^j|i!=j}; "
                        "if L were regular, complement would be too, but a^n b^n is not regular",
            "verdict": "NOT REGULAR",
        },
        {
            "desc": "L = {w in {a,b}* | every a is immediately followed by b}",
            "is_regular": True,
            "argument": "regex: (ab|b)*; 2-state DFA with dead state for a not followed by b",
            "verdict": "REGULAR",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "regular_language_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["pumping_lemma"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "determine if language is regular"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a regular language check problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._LANGUAGES)
        lang = self._LANGUAGES[idx]
        problem = f"{lang['desc']}; is this language regular?"
        return problem, {
            "desc": lang["desc"],
            "is_regular": lang["is_regular"],
            "argument": lang["argument"],
            "verdict": lang["verdict"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate regularity analysis steps.

        Args:
            sd: All computed solution information.

        Returns:
            Steps explaining the argument.
        """
        return [
            f"language: {sd['desc']}",
            f"argument: {sd['argument']}",
            f"verdict: {sd['verdict']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the regularity verdict.

        Args:
            sd: All computed solution information.

        Returns:
            REGULAR or NOT REGULAR.
        """
        return sd["verdict"]
