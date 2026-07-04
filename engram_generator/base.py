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
    """

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
        self._min_difficulty = min_difficulty
        self._max_difficulty = max_difficulty

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
                problem = self._enrich_problem(problem, steps, solution_data)
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
    })


    @classmethod
    def _enrich_problem(cls, problem: str, steps: list[str],
                        solution_data: dict | None = None) -> str:
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
            values_in_step1 = set()
            for match in assignments:
                nums = re.findall(
                    r"[\d]+\.?[\d]*", match.split("=", 1)[1],
                )
                values_in_step1.update(
                    n for n in nums if len(n) > 1 or int(n) > 2
                )

            if values_in_step1:
                problem_nums = set(re.findall(r"[\d]+\.?[\d]*", problem))
                overlap = values_in_step1 & problem_nums
                if len(overlap) < len(values_in_step1) * 0.5:
                    given = ", ".join(a.strip() for a in assignments)
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
        answer_str = str(solution_data.get("answer", ""))

        given_parts = []
        for key, val in solution_data.items():
            if key in cls._INTERNAL_KEYS or key == target_var:
                continue
            if not isinstance(val, (int, float)):
                continue
            val_s = str(val)
            # Only include values that appear in step 1 (given params)
            # but not values that only appear in later steps or the answer
            if val_s not in step1 and str(abs(val)) not in step1:
                continue
            # Skip if this is the final answer
            if val_s == answer_str:
                continue
            given_parts.append(f"{key}={val}")

        if not given_parts:
            return problem

        return f"{problem}, {', '.join(given_parts)}"
