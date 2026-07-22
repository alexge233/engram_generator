"""Base classes for the engram generator framework."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import re


STEP_TOKEN = "<step>"


@dataclass
class Sample:
    """A single training sample with problem, steps, and answer.

    Attributes:
        input_text: Task instruction in natural language.
        target_text: Full target separated by STEP_TOKEN.
        difficulty: Difficulty level of this sample.
        task_name: Name of the generator that produced this sample.
        tier: Skill tree tier of this task.
        problem: Problem statement in LaTeX.
        steps: Intermediate solution steps in execution order.
        answer: Final answer string.
    """

    input_text: str
    target_text: str
    difficulty: int
    task_name: str = ""
    tier: int = 0
    problem: str = ""
    steps: list[str] = field(default_factory=list)
    answer: str = ""
    atom: "Atom | None" = None


@dataclass
class Atom:
    """A self-contained knowledge atom.

    Represents one theorem, definition, or formula as a minimal
    self-contained unit of mathematical knowledge sourced from
    authoritative references.

    Attributes:
        atom_type: Category (theorem, definition, result, identity, algorithm, principle).
        name: Short identifier.
        content: Full theorem/formula text from authoritative source.
        tier: Skill tree tier this atom belongs to.
        domain: Subject domain.
        source: Citation string (author, title, edition, page/section).
        source_url: URL to the authoritative source.
        prerequisites: Atom names that should be learned first.
    """

    atom_type: str
    name: str
    content: str
    tier: int
    domain: str
    example: str = ""
    source: str = ""
    source_url: str = ""
    prerequisites: list[str] = field(default_factory=list)


class StepGenerator(ABC):
    """Base class for all task generators in the curriculum.

    Produces samples containing a natural language input, a LaTeX problem
    statement, solution steps in execution order, and a final answer.

    Attributes:
        task_name: Unique identifier for this task type.
        tier: Skill tree tier (0-10).
        prerequisites: Task names required before this unlocks.
        DECIMAL_PLACES: Maximum decimal places in numeric outputs.
    """

    DECIMAL_PLACES = 4

    def __init__(self, min_difficulty: int = 1, max_difficulty: int = 8,
                 seed: int = 42) -> None:
        """Initialise the generator.

        Args:
            min_difficulty: Minimum difficulty level.
            max_difficulty: Maximum difficulty level.
            seed: Random seed for reproducibility.
        """
        self._min_difficulty = min_difficulty
        self._max_difficulty = max_difficulty
        self._rng = random.Random(seed)

    @property
    @abstractmethod
    def task_name(self) -> str:
        """Return the unique task identifier."""
        ...

    @property
    @abstractmethod
    def tier(self) -> int:
        """Return the skill tree tier (0-10)."""
        ...

    @property
    def prerequisites(self) -> list[str]:
        """Return task names required before this unlocks."""
        return []

    @property
    def atom(self) -> "Atom | None":
        """Return the knowledge atom linked to this task, if any."""
        try:
            from engram_generator.atoms.registry import get_atom
            return get_atom(self.task_name)
        except (KeyError, ImportError):
            return None

    @abstractmethod
    def task_description(self, difficulty: int) -> str:
        """Generate the natural language input for this task.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short, meaningful task description.
        """
        ...

    @abstractmethod
    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a problem and its solution data.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text_in_latex, solution_data_dict).
        """
        ...

    @abstractmethod
    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate solution steps from the solution data.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        ...

    @abstractmethod
    def _create_answer(self, solution_data: dict) -> str:
        """Extract the final answer from solution data.

        Args:
            solution_data: All computed solution information.

        Returns:
            Final answer as a string.
        """
        ...

    @property
    def min_difficulty(self) -> int:
        """Return current minimum difficulty."""
        return self._min_difficulty

    @property
    def max_difficulty(self) -> int:
        """Return current maximum difficulty."""
        return self._max_difficulty

    def set_difficulty(self, min_difficulty: int, max_difficulty: int) -> None:
        """Update the difficulty range.

        Args:
            min_difficulty: New minimum.
            max_difficulty: New maximum.
        """
        self._min_difficulty = int(min_difficulty)
        self._max_difficulty = int(max_difficulty)

    def generate(self, num_samples: int,
                 include_atom: bool = False) -> list[Sample]:
        """Generate a batch of samples.

        Args:
            num_samples: Number of samples to generate.
            include_atom: If True, attach the knowledge atom to each sample.

        Returns:
            List of Sample instances.
        """
        samples = [self._generate_one() for _ in range(num_samples)]
        if include_atom:
            atom = self.atom
            for sample in samples:
                sample.atom = atom
        return samples

    def _generate_one(self, max_retries: int = 10) -> Sample:
        """Generate a single sample with crash protection and length capping.

        Retries with lower difficulty if the target exceeds 512 characters.
        Catches any exception during generation and retries with a new seed
        to prevent experiment crashes from edge case bugs.

        Args:
            max_retries: Maximum retry attempts.

        Returns:
            A Sample with all fields populated.

        Raises:
            RuntimeError: If all retries are exhausted.
        """
        difficulty = self._rng.randint(self._min_difficulty, self._max_difficulty)

        for attempt in range(max_retries):
            try:
                problem, solution_data = self._create_problem(difficulty)
                steps = self._create_steps(solution_data)
                answer = self._create_answer(solution_data)
                steps = [self._cap_decimals(s) for s in steps]
                answer = self._cap_decimals(answer)
                problem = self._enrich_problem(
                    problem, steps, solution_data, answer,
                )
                target = self._format_target(problem, steps, answer)

                if len(target) > 512 and difficulty > 1:
                    difficulty = max(1, difficulty - 1)
                    continue

                return Sample(
                    input_text=self.task_description(difficulty),
                    target_text=target,
                    difficulty=difficulty,
                    task_name=self.task_name,
                    tier=self.tier,
                    problem=problem,
                    steps=steps,
                    answer=answer,
                )
            except Exception:
                difficulty = max(1, difficulty - 1)
                continue

        return self._fallback_sample(difficulty)

    def _fallback_sample(self, difficulty: int) -> Sample:
        """Generate a minimal valid sample when all retries fail.

        Args:
            difficulty: Last attempted difficulty.

        Returns:
            A structurally valid sample with a skip marker.
        """
        return Sample(
            input_text=self.task_description(difficulty),
            target_text=f"skip {STEP_TOKEN} skip",
            difficulty=difficulty,
            task_name=self.task_name,
            tier=self.tier,
            problem="skip",
            steps=["skip"],
            answer="skip",
        )

    def _format_target(self, problem: str, steps: list[str],
                       answer: str) -> str:
        """Join problem, steps, and answer with step tokens.

        Args:
            problem: LaTeX problem statement.
            steps: Solution steps.
            answer: Final answer.

        Returns:
            Formatted target string.
        """
        parts = [problem] + steps + [answer]
        return f" {STEP_TOKEN} ".join(parts)

    @classmethod
    def _cap_decimals(cls, text: str) -> str:
        """Round floating-point numbers in text to DECIMAL_PLACES.

        Finds all decimal numbers (e.g. 3.141592653) and rounds them.
        Integers and scientific notation exponents are left unchanged.

        Args:
            text: String potentially containing decimal numbers.

        Returns:
            String with decimals capped.
        """
        dp = cls.DECIMAL_PLACES

        def _round_match(m: re.Match) -> str:
            full = m.group(0)
            if 'e' in full.lower():
                parts = re.split(r'[eE]', full)
                mantissa = round(float(parts[0]), dp)
                mant_s = f"{mantissa:.{dp}f}".rstrip('0').rstrip('.')
                return f"{mant_s}e{parts[1]}"
            val = round(float(full), dp)
            if val == int(val) and '.' not in full[:full.index('.') + 1]:
                return str(int(val))
            rounded = f"{val:.{dp}f}".rstrip('0').rstrip('.')
            return rounded

        return re.sub(r'-?\d+\.\d{5,}(?:[eE][+-]?\d+)?', _round_match, text)

    def normalise_step(self, step: str) -> str:
        """Normalise a reasoning step for comparison.

        Handles commutativity (3*9=27 matches 9*3=27), numeric
        equivalence (125.0 matches 125), and whitespace. Generators
        with task-specific step formats can override this method.

        Uses a cached normaliser instance to avoid per-call overhead.

        Args:
            step: Raw step string from the reasoning chain.

        Returns:
            Canonical form for comparison.
        """
        if not hasattr(self, "_normaliser"):
            from engram_generator.evaluation.normaliser import OperationNormaliser
            self._normaliser = OperationNormaliser()
        return self._normaliser.normalise(step)

    def parse_chain(
        self, target_text: str, has_problem: bool = True,
    ) -> "ReasoningChain":
        """Parse a target string into a ReasoningChain.

        Args:
            target_text: Full target with <step> delimiters.
            has_problem: If True (default), first segment is the
                problem statement. Set False for model outputs
                that only contain reasoning steps.

        Returns:
            ReasoningChain with problem, steps, and answer.
        """
        from engram_generator.evaluation.reasoning_chain import ReasoningChain
        return ReasoningChain(target_text, has_problem=has_problem)

    def _operand_range(self, difficulty: int) -> tuple[int, int]:
        """Return the (lower, upper) bounds for operands at given difficulty.

        Args:
            difficulty: Number of digits.

        Returns:
            Tuple of (lower_bound, upper_bound).
        """
        lower = 10 ** (difficulty - 1) if difficulty > 1 else 0
        upper = 10 ** difficulty - 1
        return lower, upper

    _INTERNAL_KEYS = frozenset({
        "target", "answer", "solve_for", "mode", "type", "kind",
        "direction", "method", "strategy", "approach", "variant",
        "result", "converges", "diverges", "is_cauchy", "is_analytic",
        "is_valid", "is_stable", "is_bounded", "is_connected",
        "is_in_ring", "has_fp", "path_connected", "b_converges",
        "discriminant", "disc",
        "trace", "det", "determinant",
        "alg_mult", "geo_mult", "lef",
        "mag_sum", "pair_sum", "nb", "nr",
        "q_re", "q_im", "r_re", "r_im",
        "a_coeff", "b_coeff", "c_coeff",
        "conclusion_val", "given_val",
        "H", "E", "U", "W", "S",
        "r1", "r2", "r3",
        "constant", "degree",
        "a_re", "a_im", "b_re", "b_im",
        "two_gm", "r_sq", "c_sq", "numerator", "denominator",
        "force", "v_esc", "r_s",
        "time_term", "ratio",
        "d_stress", "d_strain",
        "root", "count", "posterior", "products",
    })

    _RESULT_KEY_PATTERNS = re.compile(
        r"^(is_|has_|can_|should_)"
        r"|_(sum|mult|result|answer|output|sq|term|products?|value)$"
        r"|^(converges|diverges|stable|unstable|bounded|analytic|connected)$"
        r"|^(solution|confidence|trap_value|target_acc|verbose|roots)$"
    )

    @staticmethod
    def _format_list(val: list | tuple) -> str:
        """Format a list for display in a problem string.

        Converts Fraction objects to readable ``n/d`` notation instead
        of the default ``Fraction(n, d)`` repr. Nested lists are
        formatted one level deep.

        Args:
            val: List or tuple of numeric values, possibly containing
                ``fractions.Fraction`` objects or nested sequences.

        Returns:
            Bracket-enclosed, comma-separated string of formatted values.
        """
        from fractions import Fraction
        parts = []
        for item in val:
            if isinstance(item, Fraction):
                parts.append(f"{item.numerator}/{item.denominator}")
            elif isinstance(item, (list, tuple)):
                inner = ", ".join(
                    f"{x.numerator}/{x.denominator}" if isinstance(x, Fraction) else str(x)
                    for x in item
                )
                parts.append(f"[{inner}]")
            else:
                parts.append(str(item))
        return f"[{', '.join(parts)}]"

    @classmethod
    def _enrich_problem(cls, problem: str, steps: list[str],
                        solution_data: dict | None = None,
                        answer: str | None = None) -> str:
        """Append given values if the problem is a bare formula.

        Many generators return a formula template (e.g. ``V = IR``) as the
        problem but only introduce the concrete parameter values in step 1
        or keep them only in the solution data dict. This detects that case
        and folds the given values into the problem so the model has all
        information needed to solve it.

        Args:
            problem: Original problem string from ``_create_problem``.
            steps: Solution steps from ``_create_steps``.
            solution_data: The solution data dict from ``_create_problem``.
            answer: The computed answer string from ``_create_answer``.

        Returns:
            Enriched problem string, or the original if no enrichment needed.
        """
        if not steps:
            return problem

        step1 = steps[0]

        # Try to extract var=value assignments from step 1
        assignments = re.findall(
            r"[A-Za-z_][A-Za-z_0-9]*\s*=\s*-?[\d.eE+\-]+(?:/[\d.]+)?",
            step1,
        )

        if assignments:
            answer_str_early = str(answer) if answer else ""
            safe_assignments = []
            values_in_step1 = set()
            for match in assignments:
                rhs = match.split("=", 1)[1].strip()
                try:
                    if answer_str_early and float(rhs) == float(answer_str_early):
                        continue
                except (ValueError, TypeError):
                    if rhs == answer_str_early:
                        continue
                safe_assignments.append(match)
                nums = re.findall(
                    r"[\d]+\.?[\d]*", rhs,
                )
                values_in_step1.update(
                    n for n in nums if len(n) > 1 or int(n) > 2
                )

            if values_in_step1:
                problem_nums = set(re.findall(r"[\d]+\.?[\d]*", problem))
                overlap = values_in_step1 & problem_nums
                if len(overlap) < len(values_in_step1) * 0.5:
                    given = ", ".join(a.strip() for a in safe_assignments)
                    if given:
                        return f"{problem}, {given}"

        # Fallback: use solution_data dict if the problem has no numbers
        # and step 1 uses substitution format like (10)(9) instead of var=val
        if solution_data is None:
            return problem

        problem_nums = set(re.findall(r"[\d]+\.?[\d]*", problem))
        meaningful = {n for n in problem_nums if len(n) > 1 or int(n) > 2}
        if meaningful:
            return problem

        target_var = solution_data.get("target", "")
        answer_str = str(answer) if answer else str(solution_data.get("answer", ""))

        given_parts = []
        for key, val in solution_data.items():
            if key in cls._INTERNAL_KEYS or key == target_var:
                continue
            if cls._RESULT_KEY_PATTERNS.search(key):
                continue
            if isinstance(val, bool):
                continue

            if isinstance(val, (list, tuple)):
                if not cls._list_appears_in(val, step1, answer_str):
                    continue
                given_parts.append(f"{key}={cls._format_list(val)}")
                continue

            from fractions import Fraction
            if isinstance(val, Fraction):
                frac_s = f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
                alt_s = f"{val.numerator}/{val.denominator}"
                if frac_s in step1 or alt_s in step1:
                    given_parts.append(f"{key}={val}")
                continue

            if not isinstance(val, (int, float)):
                continue

            val_s = str(val)
            try:
                if float(val_s) == float(answer_str):
                    continue
            except (ValueError, TypeError):
                if val_s == answer_str:
                    continue

            val_in_step1 = cls._val_in_text(val, val_s, step1)
            if not val_in_step1:
                continue
            given_parts.append(f"{key}={val}")

        if not given_parts:
            return problem

        return f"{problem}, {', '.join(given_parts)}"

    @staticmethod
    def _significand(val: float) -> str:
        """Extract the significand from a float for fuzzy matching.

        Returns the base digits (e.g. ``6.674`` from ``6.674e-11``) only
        when the value uses scientific notation (very large or very small).
        Returns empty string otherwise.
        """
        if val == 0 or not isinstance(val, float):
            return ""
        av = abs(val)
        if 0.01 <= av < 1e4:
            return ""
        formatted = f"{val:.4g}"
        if "e" in formatted:
            return formatted.split("e")[0].rstrip("0").rstrip(".")
        return ""

    @classmethod
    def _val_in_text(cls, val: float, val_s: str, text: str) -> bool:
        """Check if a numeric value appears in text, with fuzzy matching.

        Uses digit-boundary awareness to avoid false positives where a
        short number like ``25`` matches inside ``125``.

        Args:
            val: The numeric value to search for.
            val_s: String representation of val.
            text: The text to search in (typically step 1).

        Returns:
            True if the value appears as a standalone number in the text.
        """
        if cls._digit_boundary_match(val_s, text):
            return True
        abs_s = str(abs(val))
        if len(abs_s) > 1 and cls._digit_boundary_match(abs_s, text):
            return True
        if isinstance(val, float) and val == int(val) and abs(val) > 2:
            int_s = str(int(val))
            if len(int_s) > 2 and cls._digit_boundary_match(int_s, text):
                return True
        sig = cls._significand(val)
        if sig and len(sig) >= 3 and sig in text:
            return True
        return False

    @staticmethod
    def _digit_boundary_match(needle: str, haystack: str) -> bool:
        """Check if needle appears in haystack at digit boundaries.

        Args:
            needle: The numeric string to find.
            haystack: The text to search in.

        Returns:
            True if needle appears and is not embedded inside a larger number.
        """
        pattern = r"(?<!\d)" + re.escape(needle) + r"(?!\d)"
        return bool(re.search(pattern, haystack))

    @classmethod
    def _list_appears_in(cls, val: list | tuple, step1: str,
                         answer_str: str) -> bool:
        """Check if a short numeric list's values appear in step 1."""
        from fractions import Fraction
        if len(val) > 10:
            return False
        items_with_orig = []
        for item in val:
            if isinstance(item, bool):
                return False
            if isinstance(item, Fraction):
                items_with_orig.append((float(item), item))
            elif isinstance(item, (int, float)):
                items_with_orig.append((item, None))
            elif isinstance(item, (list, tuple)) and len(item) <= 4:
                for sub in item:
                    if isinstance(sub, bool):
                        continue
                    if isinstance(sub, Fraction):
                        items_with_orig.append((float(sub), sub))
                    elif isinstance(sub, (int, float)):
                        items_with_orig.append((sub, None))
            else:
                return False
        if not items_with_orig:
            return False
        meaningful = [(n, orig) for n, orig in items_with_orig
                      if abs(n) > 2 or (isinstance(n, float) and n != int(n))]
        if not meaningful:
            return False
        matched = 0
        for n, orig in meaningful:
            if cls._val_in_text(n, str(n), step1):
                matched += 1
            elif isinstance(orig, Fraction):
                frac_s = f"\\frac{{{orig.numerator}}}{{{orig.denominator}}}"
                alt_s = f"{orig.numerator}/{orig.denominator}"
                if frac_s in step1 or alt_s in step1:
                    matched += 1
        if matched < len(meaningful) * 0.5:
            return False
        list_str = str(val)
        if list_str == answer_str or list_str.strip("[]()") == answer_str:
            return False
        return True
