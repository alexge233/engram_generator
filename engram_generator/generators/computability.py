"""Computability theory generators.

6 generators across tiers 6-7 covering the halting problem, reductions,
Rice's theorem, RE classification, Kolmogorov complexity, and Godel
numbering.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── TIER 6 ────────────────────────────────────────────────────────


@register
class GodelNumberGenerator(StepGenerator):
    """Compute the Godel number of a logical formula.

    Assign primes to symbols and encode a formula as the product of
    prime powers: godel(s1 s2 ... sn) = p1^code(s1) * p2^code(s2) * ...

    Difficulty scaling:
        Difficulty 1-3: formula length 2-3 symbols.
        Difficulty 4-6: formula length 3-4 symbols.
        Difficulty 7-8: formula length 4-5 symbols.
    """

    _PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    _SYMBOL_CODES = {
        "0": 1, "S": 2, "+": 3, "*": 4, "=": 5,
        "(": 6, ")": 7, "x": 8, "y": 9, "z": 10,
        "NOT": 11, "AND": 12, "OR": 13, "->": 14,
        "forall": 15, "exists": 16,
    }

    _FORMULAS_BY_DIFFICULTY = {
        "easy": [
            ["S", "0"],
            ["x", "=", "0"],
            ["S", "(", "0", ")"],
        ],
        "medium": [
            ["x", "+", "y"],
            ["S", "(", "x", ")"],
            ["x", "=", "S", "0"],
        ],
        "hard": [
            ["x", "+", "S", "0"],
            ["forall", "x", "=", "x"],
            ["exists", "x", "S", "(", "x", ")"],
            ["x", "*", "y", "=", "0"],
        ],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "godel_number"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["prime_factorisation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute Godel number of a formula"

    def _pick_formula(self, difficulty: int) -> list[str]:
        """Pick a formula appropriate for the difficulty.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            List of symbol strings.
        """
        if difficulty <= 3:
            pool = self._FORMULAS_BY_DIFFICULTY["easy"]
        elif difficulty <= 6:
            pool = (self._FORMULAS_BY_DIFFICULTY["easy"]
                    + self._FORMULAS_BY_DIFFICULTY["medium"])
        else:
            pool = (self._FORMULAS_BY_DIFFICULTY["easy"]
                    + self._FORMULAS_BY_DIFFICULTY["medium"]
                    + self._FORMULAS_BY_DIFFICULTY["hard"])
        return list(self._rng.choice(pool))

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Godel numbering problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        formula = self._pick_formula(difficulty)
        # Truncate to keep output short
        formula = formula[:min(len(formula), 5)]

        codes = [self._SYMBOL_CODES.get(s, 1) for s in formula]
        primes = self._PRIMES[:len(formula)]

        factors = []
        godel = 1
        for p, c in zip(primes, codes):
            factors.append(f"{p}^{c}")
            godel *= p ** c

        formula_str = " ".join(formula)
        return (
            f"Compute Godel number of: {formula_str}. "
            f"Symbol codes: {dict((s, self._SYMBOL_CODES[s]) for s in formula if s in self._SYMBOL_CODES)}",
            {"formula": formula_str, "codes": codes,
             "primes": primes, "factors": factors,
             "godel": godel},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing prime power computation.
        """
        steps = [f"formula: {sd['formula']}"]
        for i, (p, c) in enumerate(zip(sd["primes"], sd["codes"])):
            steps.append(f"position {i+1}: prime={p}, code={c}, "
                         f"{p}^{c}={p**c}")
        steps.append(f"product = {' * '.join(sd['factors'])} = {sd['godel']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Godel number.

        Args:
            sd: Solution data dict.

        Returns:
            The Godel number as a string.
        """
        return str(sd["godel"])


# ── TIER 7 ────────────────────────────────────────────────────────


@register
class HaltingProblemGenerator(StepGenerator):
    """Show undecidability of the halting problem via diagonalization.

    Present a template-based diagonalization argument: assume decider H
    exists, construct program D that calls H on itself and does the
    opposite, derive contradiction.

    Difficulty scaling:
        Difficulty 1-3: basic diagonalization with fixed names.
        Difficulty 4-6: randomised program/decider names.
        Difficulty 7-8: extended argument with explicit contradiction.
    """

    _DECIDER_NAMES = ["H", "HALT", "Decide", "Oracle"]
    _PROGRAM_NAMES = ["D", "Diagonal", "Paradox", "Contrarian"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "halting_problem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["proof_by_contradiction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove halting problem undecidability by diagonalization"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a halting problem diagonalization argument.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        h_name = self._rng.choice(
            self._DECIDER_NAMES[:min(2 + difficulty // 2,
                                     len(self._DECIDER_NAMES))]
        )
        d_name = self._rng.choice(
            self._PROGRAM_NAMES[:min(2 + difficulty // 2,
                                     len(self._PROGRAM_NAMES))]
        )

        return (
            f"Assume {h_name}(P,x) decides if P halts on x. "
            f"Construct {d_name} and derive contradiction.",
            {"h": h_name, "d": d_name},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the diagonalization argument.
        """
        h, d = sd["h"], sd["d"]
        return [
            f"assume {h}(P,x) decides halting",
            f"define {d}(P): if {h}(P,P)=halts then loop, "
            f"else halt",
            f"run {d}({d}): if {h}({d},{d})=halts then "
            f"{d} loops (contradiction)",
            f"if {h}({d},{d})=loops then {d} halts "
            f"(contradiction)",
            f"therefore {h} cannot exist",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the undecidability conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            Statement that halting is undecidable.
        """
        return "the halting problem is undecidable"


@register
class ReductionComputabilityGenerator(StepGenerator):
    """Reduce problem A to problem B using an oracle.

    Given a decidable oracle for B, show how to solve A by transforming
    inputs and querying the oracle. Template-based with randomised
    problem pairs.

    Difficulty scaling:
        Difficulty 1-3: simple reductions with direct transformations.
        Difficulty 4-6: reductions requiring input encoding.
        Difficulty 7-8: reductions with composition of transformations.
    """

    _REDUCTIONS = [
        {
            "a": "EMPTY_TM (is L(M) empty?)",
            "b": "HALTING",
            "transform": "given M, build M' that on input w "
                         "simulates M on w; query HALT(M',w)",
            "conclusion": "if HALTING were decidable, "
                          "EMPTY_TM would be decidable",
        },
        {
            "a": "EQUIVALENCE (L(M1)=L(M2)?)",
            "b": "EMPTY_TM",
            "transform": "build M' accepting symmetric difference "
                         "L(M1) XOR L(M2); query EMPTY(M')",
            "conclusion": "if EMPTY_TM were decidable, "
                          "EQUIVALENCE would be decidable",
        },
        {
            "a": "ALL_TM (does M accept all strings?)",
            "b": "HALTING",
            "transform": "given M, build M' that on input w "
                         "runs M on all strings up to |w|; "
                         "query HALT(M',epsilon)",
            "conclusion": "if HALTING were decidable, "
                          "ALL_TM would be decidable",
        },
        {
            "a": "REGULAR_TM (is L(M) regular?)",
            "b": "EMPTY_TM",
            "transform": "given M, build M' whose language is "
                         "regular iff L(M) is empty; query EMPTY(M')",
            "conclusion": "if EMPTY_TM were decidable, "
                          "REGULAR_TM would be decidable",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reduction_computability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["turing_machine_step"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "reduce problem A to problem B"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reduction problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(2 + difficulty // 2, len(self._REDUCTIONS))
        reduction = self._rng.choice(self._REDUCTIONS[:pool_size])

        return (
            f"Show: {reduction['a']} reduces to "
            f"{reduction['b']}. "
            f"Assume oracle for {reduction['b']}.",
            reduction,
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the reduction.
        """
        return [
            f"goal: reduce {sd['a']} to {sd['b']}",
            f"transformation: {sd['transform']}",
            f"conclusion: {sd['conclusion']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the reduction conclusion.

        Args:
            sd: Solution data dict.

        Returns:
            The conclusion of the reduction.
        """
        return sd["conclusion"]


@register
class RiceTheoremGenerator(StepGenerator):
    """Apply Rice's theorem to classify a property as undecidable.

    Given a property of recursively enumerable languages, determine if
    it is trivial (holds for all or no RE languages) or non-trivial
    (holds for some but not all). Non-trivial properties are undecidable.

    Difficulty scaling:
        Difficulty 1-3: clearly non-trivial properties.
        Difficulty 4-6: mix of trivial and non-trivial.
        Difficulty 7-8: subtler properties requiring justification.
    """

    _PROPERTIES = [
        {
            "desc": "L(M) is finite",
            "trivial": False,
            "reason": "some TMs accept finite languages, "
                      "some accept infinite ones",
        },
        {
            "desc": "L(M) contains the empty string",
            "trivial": False,
            "reason": "some TMs accept epsilon, some do not",
        },
        {
            "desc": "L(M) = Sigma*",
            "trivial": False,
            "reason": "some TMs accept everything, some do not",
        },
        {
            "desc": "L(M) is empty",
            "trivial": False,
            "reason": "some TMs accept nothing, some accept "
                      "at least one string",
        },
        {
            "desc": "L(M) is a subset of L(M) (always true)",
            "trivial": True,
            "reason": "every RE language is a subset of itself; "
                      "holds for all TMs",
        },
        {
            "desc": "L(M) contains at least 3 strings",
            "trivial": False,
            "reason": "some TMs accept >=3 strings, some fewer",
        },
        {
            "desc": "L(M) is context-free",
            "trivial": False,
            "reason": "some RE languages are CF, some are not",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rice_theorem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["halting_problem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "apply Rice's theorem to classify property"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Rice's theorem problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(3 + difficulty // 2, len(self._PROPERTIES))
        prop = self._rng.choice(self._PROPERTIES[:pool_size])

        return (
            f"Property: {prop['desc']}. "
            f"Is this decidable by Rice's theorem?",
            prop,
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing Rice's theorem application.
        """
        steps = [f"property: {sd['desc']}"]
        if sd["trivial"]:
            steps.append("property is trivial (holds for all or no TMs)")
            steps.append("Rice's theorem does not apply")
            steps.append("decidability not ruled out by Rice's")
        else:
            steps.append(f"non-trivial because: {sd['reason']}")
            steps.append(
                "by Rice's theorem: any non-trivial property "
                "of RE languages is undecidable"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return whether the property is decidable.

        Args:
            sd: Solution data dict.

        Returns:
            Decidability classification.
        """
        if sd["trivial"]:
            return "trivial property, Rice's does not apply"
        return "undecidable (by Rice's theorem)"


@register
class RecursiveEnumerableGenerator(StepGenerator):
    """Classify a language as recursive, RE-only, or neither.

    Given a language description, determine whether it is recursive
    (decidable), RE but not recursive, or not RE. Template-based with
    well-known examples.

    Difficulty scaling:
        Difficulty 1-3: clearly recursive languages.
        Difficulty 4-6: mix of recursive and RE-only.
        Difficulty 7-8: includes non-RE languages.
    """

    _LANGUAGES = [
        {
            "desc": "{w | w is a valid C program that compiles}",
            "class": "recursive",
            "reason": "compilation is a decidable syntactic check",
        },
        {
            "desc": "{<M> | M halts on empty input}",
            "class": "RE-only",
            "reason": "simulate M; if it halts, accept. "
                      "Complement is not RE",
        },
        {
            "desc": "{<M> | M does NOT halt on empty input}",
            "class": "not RE",
            "reason": "complement of the halting problem on "
                      "empty input; not RE",
        },
        {
            "desc": "{<M> | L(M) is non-empty}",
            "class": "RE-only",
            "reason": "dovetail all inputs; accept if any halts "
                      "and accepts. Complement not RE",
        },
        {
            "desc": "{a^n b^n | n >= 0}",
            "class": "recursive",
            "reason": "context-free and decidable by pushdown automaton",
        },
        {
            "desc": "{<M> | L(M) = Sigma*}",
            "class": "not RE",
            "reason": "complement of ALL_TM is not RE",
        },
        {
            "desc": "{w | w in {0,1}* and |w| is even}",
            "class": "recursive",
            "reason": "regular language, decidable by DFA",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "recursive_enumerable"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["halting_problem"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify language: recursive, RE-only, or not RE"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an RE classification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            # Only recursive languages
            pool = [l for l in self._LANGUAGES
                    if l["class"] == "recursive"]
        elif difficulty <= 6:
            # Recursive and RE-only
            pool = [l for l in self._LANGUAGES
                    if l["class"] != "not RE"]
        else:
            pool = self._LANGUAGES

        lang = self._rng.choice(pool)
        return (
            f"Classify: {lang['desc']}",
            lang,
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the classification reasoning.
        """
        return [
            f"language: {sd['desc']}",
            f"reason: {sd['reason']}",
            f"classification: {sd['class']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the language classification.

        Args:
            sd: Solution data dict.

        Returns:
            One of 'recursive', 'RE-only', 'not RE'.
        """
        return sd["class"]


@register
class KolmogorovComplexityGenerator(StepGenerator):
    """Bound the Kolmogorov complexity K(x) of a structured string.

    For strings with clear patterns (e.g., n repetitions of a character),
    bound K(x) <= |shortest program| + O(1). Show that K(x) <= log(n) + c
    for repetitive strings of length n.

    Difficulty scaling:
        Difficulty 1-3: single-character repetition (e.g., "000...0").
        Difficulty 4-6: simple patterns (e.g., "0101...01").
        Difficulty 7-8: composite patterns with longer programs.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kolmogorov_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "bound Kolmogorov complexity of string"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Kolmogorov complexity bounding problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            char = self._rng.choice(["0", "1", "a"])
            n = self._rng.randint(8, 32)
            string_desc = f"'{char}' repeated {n} times"
            pattern = char
            program_desc = f"print '{char}' n times (n={n})"
            log_n = math.ceil(math.log2(max(n, 2)))
            bound = f"log2({n}) + c = {log_n} + c"
        elif difficulty <= 6:
            unit = self._rng.choice(["01", "ab", "10", "001"])
            n = self._rng.randint(4, 16)
            string_desc = f"'{unit}' repeated {n} times"
            pattern = unit
            program_desc = (f"print '{unit}' n times "
                            f"(n={n}, |unit|={len(unit)})")
            log_n = math.ceil(math.log2(max(n, 2)))
            bound = f"log2({n}) + {len(unit)} + c = {log_n} + {len(unit)} + c"
        else:
            base = self._rng.choice(["0", "1"])
            n = self._rng.randint(16, 64)
            suffix = self._rng.choice(["111", "000", "abc"])
            string_desc = (f"'{base}' repeated {n} times "
                           f"followed by '{suffix}'")
            pattern = base
            program_desc = (f"print '{base}'*{n} + '{suffix}' "
                            f"(n={n}, suffix_len={len(suffix)})")
            log_n = math.ceil(math.log2(max(n, 2)))
            bound = (f"log2({n}) + {len(suffix)} + c "
                     f"= {log_n} + {len(suffix)} + c")

        str_len = n * len(pattern)

        return (
            f"Bound K(x) for x = {string_desc} (|x|={str_len}).",
            {"string_desc": string_desc, "str_len": str_len,
             "program_desc": program_desc, "bound": bound,
             "log_n": math.ceil(math.log2(max(n, 2))),
             "n": n},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            Steps showing the K(x) bound derivation.
        """
        return [
            f"string: {sd['string_desc']}, length={sd['str_len']}",
            f"program: {sd['program_desc']}",
            f"program encodes n={sd['n']} in "
            f"log2({sd['n']})={sd['log_n']} bits",
            f"K(x) <= {sd['bound']}",
            f"K(x) << |x| = {sd['str_len']} (highly compressible)",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the Kolmogorov complexity bound.

        Args:
            sd: Solution data dict.

        Returns:
            The upper bound expression.
        """
        return f"K(x) <= {sd['bound']}"
