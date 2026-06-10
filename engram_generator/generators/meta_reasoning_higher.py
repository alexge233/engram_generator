"""Higher-tier meta-reasoning generators -- tiers 8-10.

Eight generators that require synthesizing knowledge across domains:
proof synthesis, conjecture testing, algorithm correctness, computational
tradeoffs, architecture critique, scaling law extrapolation, error
taxonomy, and method comparison.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class LemmaDatabase:
    """Stores template lemmas for proof synthesis problems.

    Provides named lemmas grouped by theorem domain so that proof
    synthesis generators can pick a theorem and its required lemmas.
    """

    _THEOREMS: dict[str, dict] = {
        "triangle_inequality": {
            "statement": "|a+b| <= |a| + |b|",
            "lemmas": ["absolute_value_nonneg", "square_both_sides",
                       "expand_square"],
            "order": [0, 1, 2],
        },
        "am_gm": {
            "statement": "(a+b)/2 >= sqrt(ab) for a,b >= 0",
            "lemmas": ["nonneg_square", "expand_difference_square",
                       "sqrt_monotone"],
            "order": [0, 1, 2],
        },
        "cauchy_schwarz": {
            "statement": "(sum a_i*b_i)^2 <= (sum a_i^2)*(sum b_i^2)",
            "lemmas": ["nonneg_quadratic_form", "discriminant_nonpositive",
                       "expand_product_sums"],
            "order": [2, 0, 1],
        },
        "pigeon_basic": {
            "statement": "n+1 objects in n boxes => some box has >= 2",
            "lemmas": ["contradiction_assume_all_one",
                       "count_sum_equals_n", "n_less_n_plus_1"],
            "order": [0, 1, 2],
        },
        "bezout_identity": {
            "statement": "gcd(a,b) = ax + by for some integers x,y",
            "lemmas": ["euclidean_algorithm", "back_substitution",
                       "division_algorithm"],
            "order": [2, 0, 1],
        },
    }

    def random_theorem(self, rng: "random.Random") -> dict:
        """Select a random theorem and its lemma set.

        Args:
            rng: Seeded random instance.

        Returns:
            Dict with statement, lemmas, and order.
        """
        key = rng.choice(list(self._THEOREMS.keys()))
        return {"name": key, **self._THEOREMS[key]}


class AlgorithmInvariantDB:
    """Stores loop invariants for common algorithms.

    Provides algorithm templates with their invariant, init condition,
    maintenance argument, and termination argument.
    """

    _ALGORITHMS: dict[str, dict] = {
        "insertion_sort": {
            "description": "insertion sort on array A[0..n-1]",
            "invariant": "A[0..j-1] is sorted and contains the same elements as original A[0..j-1]",
            "init": "j=1: A[0..0] is trivially sorted",
            "maintenance": "insert A[j] into correct position in A[0..j-1], preserving sorted order",
            "termination": "j=n: A[0..n-1] is sorted",
        },
        "binary_search": {
            "description": "binary search for key in sorted array A[lo..hi]",
            "invariant": "if key is in A, then A[lo] <= key <= A[hi]",
            "init": "lo=0, hi=n-1: if key is in A, it is in A[0..n-1]",
            "maintenance": "mid=(lo+hi)/2: if A[mid]<key then lo=mid+1, else hi=mid; invariant preserved",
            "termination": "lo>hi: key not found, or lo==hi and A[lo]==key",
        },
        "linear_search": {
            "description": "linear search for key in array A[0..n-1]",
            "invariant": "key is not in A[0..i-1]",
            "init": "i=0: A[0..-1] is empty, invariant holds vacuously",
            "maintenance": "if A[i]!=key, key is not in A[0..i], increment i",
            "termination": "i=n: key not in A[0..n-1], or A[i]==key found",
        },
        "bubble_sort": {
            "description": "bubble sort on array A[0..n-1]",
            "invariant": "after pass i, the i largest elements are in their final positions",
            "init": "i=0: no passes done, 0 elements are in final position (vacuously true)",
            "maintenance": "pass i+1 bubbles next largest to position n-1-i",
            "termination": "i=n-1: all elements in final positions, array sorted",
        },
    }

    def random_algorithm(self, rng: "random.Random",
                          difficulty: int) -> dict:
        """Select a random algorithm appropriate for difficulty.

        Args:
            rng: Seeded random instance.
            difficulty: Controls algorithm complexity.

        Returns:
            Dict with description, invariant, init, maintenance, termination.
        """
        if difficulty <= 4:
            keys = ["linear_search", "insertion_sort"]
        else:
            keys = list(self._ALGORITHMS.keys())
        key = rng.choice(keys)
        return {"name": key, **self._ALGORITHMS[key]}


class TradeoffAnalyser:
    """Analyses time-space tradeoffs for data structure choices.

    Stores performance profiles for common data structures and computes
    which is optimal under given constraints.
    """

    _STRUCTURES: dict[str, dict] = {
        "hash_table": {
            "time_lookup": "O(1) average",
            "time_insert": "O(1) average",
            "space": "O(n)",
            "weakness": "O(n) worst case, no ordering",
        },
        "sorted_array": {
            "time_lookup": "O(log n)",
            "time_insert": "O(n)",
            "space": "O(n)",
            "weakness": "expensive insertion",
        },
        "balanced_bst": {
            "time_lookup": "O(log n)",
            "time_insert": "O(log n)",
            "space": "O(n)",
            "weakness": "higher constant factor than array",
        },
        "linked_list": {
            "time_lookup": "O(n)",
            "time_insert": "O(1)",
            "space": "O(n)",
            "weakness": "no random access, poor cache locality",
        },
    }

    def random_pair(self, rng: "random.Random") -> tuple[str, dict, str, dict]:
        """Select two data structures to compare.

        Args:
            rng: Seeded random instance.

        Returns:
            Tuple of (name_a, profile_a, name_b, profile_b).
        """
        keys = list(self._STRUCTURES.keys())
        rng.shuffle(keys)
        a, b = keys[0], keys[1]
        return a, self._STRUCTURES[a], b, self._STRUCTURES[b]


class BottleneckDatabase:
    """Stores architecture bottleneck templates for critique problems.

    Maps architecture patterns to their known bottleneck and
    suggested improvement.
    """

    _BOTTLENECKS: list[dict] = [
        {
            "arch": "Transformer with full self-attention, seq_len=4096, d=512",
            "bottleneck": "attention is O(n^2 d), quadratic in sequence length",
            "fix": "use linear attention or sparse attention (e.g. Linformer, BigBird)",
        },
        {
            "arch": "Large embedding table, vocab=100000, d=1024",
            "bottleneck": "embedding table is 100M params, dominates model size",
            "fix": "use shared embeddings, factored embeddings, or hash-based embeddings",
        },
        {
            "arch": "Deep FFN, 4*d_model hidden dim, 48 layers",
            "bottleneck": "FFN parameters scale as 8*d^2 per layer, total 48*8*d^2",
            "fix": "use mixture of experts to increase capacity without proportional compute",
        },
        {
            "arch": "RNN with hidden size 2048, sequence length 1000",
            "bottleneck": "sequential processing, O(n) time with no parallelism",
            "fix": "replace with attention-based model for parallel processing",
        },
        {
            "arch": "CNN feature extractor, 12 layers, 3x3 kernels",
            "bottleneck": "receptive field limited to 25 pixels, misses global context",
            "fix": "add global average pooling, self-attention, or dilated convolutions",
        },
    ]

    def random_bottleneck(self, rng: "random.Random") -> dict:
        """Select a random architecture bottleneck template.

        Args:
            rng: Seeded random instance.

        Returns:
            Dict with arch, bottleneck, and fix fields.
        """
        return rng.choice(self._BOTTLENECKS)


class ErrorTypeDB:
    """Stores ML error type templates for taxonomy problems.

    Maps error categories to descriptions, symptoms, and diagnostic
    strategies.
    """

    _ERROR_TYPES: dict[str, dict] = {
        "data_error": {
            "description": "corrupted or mislabelled training examples",
            "symptom": "noisy loss curve, high variance in predictions",
            "diagnostic": "inspect worst-loss examples, check for duplicates",
        },
        "label_noise": {
            "description": "systematically incorrect labels in a subset",
            "symptom": "confident wrong predictions on specific patterns",
            "diagnostic": "cross-validate with clean subset, check inter-annotator agreement",
        },
        "distribution_shift": {
            "description": "test distribution differs from training distribution",
            "symptom": "low train loss but high test loss, calibration degrades",
            "diagnostic": "compare feature distributions, use domain adaptation",
        },
        "model_capacity": {
            "description": "model too small to represent the target function",
            "symptom": "high train and test loss, underfitting",
            "diagnostic": "increase model size, check if train loss decreases",
        },
        "optimization": {
            "description": "optimiser fails to find good minimum",
            "symptom": "loss plateaus early, sensitive to learning rate",
            "diagnostic": "try different optimiser, learning rate schedule, or initialisation",
        },
    }

    def random_scenario(self, rng: "random.Random",
                         num_errors: int) -> list[tuple[str, dict]]:
        """Select random error types for a taxonomy problem.

        Args:
            rng: Seeded random instance.
            num_errors: Number of error types to include.

        Returns:
            List of (error_name, error_info) tuples.
        """
        keys = list(self._ERROR_TYPES.keys())
        rng.shuffle(keys)
        selected = keys[:num_errors]
        return [(k, self._ERROR_TYPES[k]) for k in selected]


@register
class ProofSynthesisGenerator(StepGenerator):
    """Outline which lemmas to use and in what order for a given theorem.

    Given a theorem statement and a set of available lemmas, the task is
    to determine which lemmas are needed and the order to apply them.

    Input format:
        ``outline proof strategy for theorem``

    Target format:
        ``theorem: |a+b|<=|a|+|b| <step> available: [absolute_value_nonneg,
        square_both_sides, expand_square] <step> step 1: expand_square
        <step> step 2: absolute_value_nonneg <step> step 3: square_both_sides
        <step> order: expand_square, absolute_value_nonneg, square_both_sides``

    Difficulty scaling:
        d1-2: 3 lemmas, direct order.
        d3-5: 3 lemmas, reordered.
        d6-8: 3 lemmas with 1-2 distractors.

    Prerequisites:
        verify_proof.

    Example:
        >>> gen = ProofSynthesisGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'proof_synthesis'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with lemma database.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._db = LemmaDatabase()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "proof_synthesis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["verify_proof"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls lemma count and distractors.

        Returns:
            Natural language description.
        """
        return "outline proof strategy for theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof synthesis problem.

        Args:
            difficulty: Controls distractor count.

        Returns:
            Tuple of (theorem_and_lemmas, solution_data).
        """
        theorem = self._db.random_theorem(self._rng)
        lemmas = list(theorem["lemmas"])
        order = list(theorem["order"])
        distractors: list[str] = []
        if difficulty >= 6:
            distractor_pool = [
                "unrelated_lemma_A", "unrelated_lemma_B",
                "tangent_result_C",
            ]
            num_distractors = min(difficulty - 5, 2)
            distractors = distractor_pool[:num_distractors]
        available = lemmas + distractors
        self._rng.shuffle(available)
        ordered_lemmas = [lemmas[i] for i in order]
        problem = (
            f"theorem: {theorem['statement']}, "
            f"available: [{', '.join(available)}]"
        )
        return problem, {
            "theorem_name": theorem["name"],
            "statement": theorem["statement"],
            "available": available,
            "ordered_lemmas": ordered_lemmas,
            "distractors": distractors,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proof strategy steps.

        Args:
            data: Solution data with ordered lemmas.

        Returns:
            Steps showing each lemma in the correct order.
        """
        steps = []
        for i, lemma in enumerate(data["ordered_lemmas"], 1):
            steps.append(f"step {i}: {lemma}")
        if data["distractors"]:
            steps.append(
                f"unused: {', '.join(data['distractors'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ordered lemma sequence.

        Args:
            data: Solution data.

        Returns:
            Comma-separated lemma order.
        """
        return ", ".join(data["ordered_lemmas"])


@register
class ConjectureTestGenerator(StepGenerator):
    """Design computational tests to verify or refute a conjecture.

    Given a mathematical conjecture, chooses test parameters, predicts
    outcomes, and checks edge cases.

    Input format:
        ``design tests for conjecture``

    Target format:
        ``conjecture: n^2+n+41 is prime for all n>=0 <step>
        test n=0: 41 (prime) <step> test n=1: 43 (prime)
        <step> test n=5: 71 (prime) <step> edge case n=40:
        1681=41^2 (NOT prime) <step> conjecture refuted at n=40``

    Difficulty scaling:
        d1-3: simple conjecture with small counterexample.
        d4-6: conjecture needing larger search.
        d7-8: conjecture with subtle edge case.

    Prerequisites:
        hypothesis_design.

    Example:
        >>> gen = ConjectureTestGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conjecture_test'
    """

    _CONJECTURES: list[dict] = [
        {
            "statement": "n^2+n+41 is prime for all n>=0",
            "test_points": [0, 1, 5, 10],
            "values": [41, 43, 71, 151],
            "results": ["prime", "prime", "prime", "prime"],
            "edge_n": 40,
            "edge_value": 1681,
            "edge_result": "NOT prime (41^2)",
            "verdict": "refuted at n=40",
        },
        {
            "statement": "2^p-1 is prime for all primes p",
            "test_points": [2, 3, 5, 7],
            "values": [3, 7, 31, 127],
            "results": ["prime", "prime", "prime", "prime"],
            "edge_n": 11,
            "edge_value": 2047,
            "edge_result": "NOT prime (23*89)",
            "verdict": "refuted at p=11",
        },
        {
            "statement": "sum of first n odd numbers equals n^2",
            "test_points": [1, 2, 3, 5],
            "values": [1, 4, 9, 25],
            "results": ["1=1^2", "4=2^2", "9=3^2", "25=5^2"],
            "edge_n": 10,
            "edge_value": 100,
            "edge_result": "100=10^2 (holds)",
            "verdict": "conjecture holds (provable by induction)",
        },
        {
            "statement": "every even number > 2 is sum of two primes",
            "test_points": [4, 6, 10, 20],
            "values": [4, 6, 10, 20],
            "results": ["2+2", "3+3", "3+7", "3+17"],
            "edge_n": 100,
            "edge_value": 100,
            "edge_result": "3+97 (holds)",
            "verdict": "conjecture holds for tested values (Goldbach)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conjecture_test"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hypothesis_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls conjecture complexity.

        Returns:
            Natural language description.
        """
        return "design tests for conjecture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a conjecture testing problem.

        Args:
            difficulty: Controls which conjecture is chosen.

        Returns:
            Tuple of (conjecture_statement, solution_data).
        """
        conj = self._rng.choice(self._CONJECTURES)
        num_tests = min(2 + difficulty // 2, len(conj["test_points"]))
        problem = f"conjecture: {conj['statement']}"
        return problem, {
            "statement": conj["statement"],
            "test_points": conj["test_points"][:num_tests],
            "values": conj["values"][:num_tests],
            "results": conj["results"][:num_tests],
            "edge_n": conj["edge_n"],
            "edge_value": conj["edge_value"],
            "edge_result": conj["edge_result"],
            "verdict": conj["verdict"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate test design and execution steps.

        Args:
            data: Solution data with test points and results.

        Returns:
            Steps showing each test and the edge case.
        """
        steps = []
        for pt, val, res in zip(data["test_points"],
                                 data["values"],
                                 data["results"]):
            steps.append(f"test n={pt}: {val} ({res})")
        steps.append(
            f"edge case n={data['edge_n']}: "
            f"{data['edge_value']} ({data['edge_result']})"
        )
        steps.append(data["verdict"])
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the conjecture test verdict.

        Args:
            data: Solution data.

        Returns:
            Verdict string.
        """
        return data["verdict"]


@register
class AlgorithmCorrectnessGenerator(StepGenerator):
    """Prove loop invariant for a simple algorithm.

    States the invariant, proves initialisation, maintenance, and
    termination for algorithms like insertion sort and binary search.

    Input format:
        ``prove correctness of algorithm via loop invariant``

    Target format:
        ``algorithm: insertion sort on A[0..n-1] <step>
        invariant: A[0..j-1] is sorted <step>
        init: j=1, A[0..0] trivially sorted <step>
        maintenance: insert A[j] preserving order <step>
        termination: j=n, A[0..n-1] sorted <step>
        algorithm correct by loop invariant``

    Difficulty scaling:
        d1-4: linear search, insertion sort.
        d5-8: any algorithm including binary search, bubble sort.

    Prerequisites:
        algorithm_design.

    Example:
        >>> gen = AlgorithmCorrectnessGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'algorithm_correctness'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with algorithm invariant database.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._db = AlgorithmInvariantDB()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "algorithm_correctness"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["algorithm_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls algorithm complexity.

        Returns:
            Natural language description.
        """
        return "prove correctness of algorithm via loop invariant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an algorithm correctness problem.

        Args:
            difficulty: Controls algorithm pool.

        Returns:
            Tuple of (algorithm_description, solution_data).
        """
        algo = self._db.random_algorithm(self._rng, difficulty)
        n = self._rng.randint(4, 6 + difficulty)
        problem = f"algorithm: {algo['description']}, n={n}"
        return problem, {
            "name": algo["name"],
            "description": algo["description"],
            "invariant": algo["invariant"],
            "init": algo["init"],
            "maintenance": algo["maintenance"],
            "termination": algo["termination"],
            "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate loop invariant proof steps.

        Args:
            data: Solution data with invariant and proof parts.

        Returns:
            Steps showing invariant, init, maintenance, termination.
        """
        return [
            f"invariant: {data['invariant']}",
            f"init: {data['init']}",
            f"maintenance: {data['maintenance']}",
            f"termination: {data['termination']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the correctness verdict.

        Args:
            data: Solution data.

        Returns:
            Correctness statement.
        """
        return f"{data['name']} correct by loop invariant"


@register
class ComputationalTradeoffGenerator(StepGenerator):
    """Analyse time-space tradeoff between data structures.

    Compares two data structures on lookup time, insertion time, and
    space, then recommends one based on given constraints.

    Input format:
        ``analyse time-space tradeoff and recommend``

    Target format:
        ``compare hash_table vs sorted_array <step>
        hash_table: lookup O(1), insert O(1), space O(n) <step>
        sorted_array: lookup O(log n), insert O(n), space O(n) <step>
        constraint: n=10000, mostly lookups <step>
        recommendation: hash_table (O(1) lookups dominate)
        <step> hash_table``

    Difficulty scaling:
        d1-3: two structures, simple constraint.
        d4-6: add quantitative comparison.
        d7-8: add multi-criteria analysis.

    Prerequisites:
        complexity_comparison.

    Example:
        >>> gen = ComputationalTradeoffGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'computational_tradeoff'
    """

    _CONSTRAINTS = [
        {"desc": "mostly lookups, rare inserts", "favours": "lookup"},
        {"desc": "equal lookups and inserts", "favours": "balanced"},
        {"desc": "frequent inserts, rare lookups", "favours": "insert"},
        {"desc": "memory-constrained environment", "favours": "space"},
    ]

    def __init__(self, **kwargs) -> None:
        """Initialise with tradeoff analyser.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._analyser = TradeoffAnalyser()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "computational_tradeoff"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complexity_comparison"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls analysis depth.

        Returns:
            Natural language description.
        """
        return "analyse time-space tradeoff and recommend"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tradeoff analysis problem.

        Args:
            difficulty: Controls constraint complexity.

        Returns:
            Tuple of (comparison_spec, solution_data).
        """
        name_a, prof_a, name_b, prof_b = self._analyser.random_pair(self._rng)
        constraint = self._rng.choice(self._CONSTRAINTS)
        n = self._rng.choice([1000, 5000, 10000, 50000, 100000])
        recommendation = self._recommend(
            name_a, prof_a, name_b, prof_b, constraint["favours"]
        )
        problem = f"compare {name_a} vs {name_b}, n={n}, {constraint['desc']}"
        return problem, {
            "name_a": name_a, "prof_a": prof_a,
            "name_b": name_b, "prof_b": prof_b,
            "constraint": constraint, "n": n,
            "recommendation": recommendation,
        }

    def _recommend(self, name_a: str, prof_a: dict,
                    name_b: str, prof_b: dict,
                    favours: str) -> str:
        """Determine which structure to recommend.

        Args:
            name_a: First structure name.
            prof_a: First structure profile.
            name_b: Second structure name.
            prof_b: Second structure profile.
            favours: What the constraint favours (lookup/insert/balanced/space).

        Returns:
            Name of the recommended structure.
        """
        if favours == "lookup":
            if "O(1)" in prof_a["time_lookup"]:
                return name_a
            if "O(1)" in prof_b["time_lookup"]:
                return name_b
        if favours == "insert":
            if "O(1)" in prof_a["time_insert"]:
                return name_a
            if "O(1)" in prof_b["time_insert"]:
                return name_b
        return name_a

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tradeoff analysis steps.

        Args:
            data: Solution data with profiles and recommendation.

        Returns:
            Steps showing each structure's profile and recommendation.
        """
        pa = data["prof_a"]
        pb = data["prof_b"]
        return [
            (f"{data['name_a']}: lookup {pa['time_lookup']}, "
             f"insert {pa['time_insert']}, space {pa['space']}"),
            (f"{data['name_b']}: lookup {pb['time_lookup']}, "
             f"insert {pb['time_insert']}, space {pb['space']}"),
            f"constraint: {data['constraint']['desc']}",
            f"recommendation: {data['recommendation']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the recommended structure.

        Args:
            data: Solution data.

        Returns:
            Name of the recommended data structure.
        """
        return data["recommendation"]


@register
class ModelArchitectureCritiqueGenerator(StepGenerator):
    """Identify bottleneck in a model architecture and suggest improvement.

    Given an architecture description, identifies the computational
    bottleneck and proposes a concrete improvement.

    Input format:
        ``critique architecture and suggest improvement``

    Target format:
        ``arch: Transformer with full self-attention, seq_len=4096, d=512
        <step> bottleneck: attention is O(n^2 d), quadratic in seq_len
        <step> impact: 4096^2*512=8.6B ops per layer
        <step> fix: use linear attention (e.g. Linformer)
        <step> linear attention``

    Difficulty scaling:
        d1-3: identify single bottleneck.
        d4-6: quantify bottleneck with numbers.
        d7-8: propose specific improvement with complexity reduction.

    Prerequisites:
        architecture_analysis.

    Example:
        >>> gen = ModelArchitectureCritiqueGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'model_architecture_critique'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with bottleneck database.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._db = BottleneckDatabase()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "model_architecture_critique"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["architecture_analysis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls analysis depth.

        Returns:
            Natural language description.
        """
        return "critique architecture and suggest improvement"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an architecture critique problem.

        Args:
            difficulty: Controls analysis depth.

        Returns:
            Tuple of (architecture_description, solution_data).
        """
        entry = self._db.random_bottleneck(self._rng)
        problem = f"arch: {entry['arch']}"
        return problem, {
            "arch": entry["arch"],
            "bottleneck": entry["bottleneck"],
            "fix": entry["fix"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate architecture critique steps.

        Args:
            data: Solution data with bottleneck and fix.

        Returns:
            Steps showing bottleneck identification and proposed fix.
        """
        return [
            f"bottleneck: {data['bottleneck']}",
            f"fix: {data['fix']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the suggested fix.

        Args:
            data: Solution data.

        Returns:
            Fix description string.
        """
        return data["fix"]


@register
class ScalingLawExtrapolateGenerator(StepGenerator):
    """Fit power law to performance data and predict at new scale.

    Given performance L at 3 scales, fits L(N) = a * N^{-alpha} and
    predicts at a fourth scale.

    Input format:
        ``fit scaling law and extrapolate``

    Target format:
        ``N=1000: L=2.5, N=4000: L=1.8, N=16000: L=1.3 <step>
        fit: ln(L)=ln(a)-alpha*ln(N) <step>
        alpha=(ln(2.5)-ln(1.3))/(ln(16000)-ln(1000))=0.2355
        <step> a=2.5*1000^0.2355=8.4321
        <step> predict N=64000: 8.4321*64000^{-0.2355}=0.9375
        <step> 0.9375``

    Difficulty scaling:
        d1-3: 2x scale jumps, clean exponent.
        d4-6: 4x scale jumps.
        d7-8: mixed scale jumps with noise.

    Prerequisites:
        scaling_prediction.

    Example:
        >>> gen = ScalingLawExtrapolateGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'scaling_law_extrapolate'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with no extra state.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "scaling_law_extrapolate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["scaling_prediction"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls scale range.

        Returns:
            Natural language description.
        """
        return "fit scaling law and extrapolate"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scaling law fitting and extrapolation problem.

        Args:
            difficulty: Controls scale factor and noise.

        Returns:
            Tuple of (observations, solution_data).
        """
        alpha = round(self._rng.uniform(0.1, 0.4), 4)
        a = round(self._rng.uniform(5.0, 20.0), 4)
        base_n = self._rng.choice([100, 500, 1000, 2000])
        factor = 2 if difficulty <= 3 else 4
        scales = [base_n, base_n * factor, base_n * factor * factor]
        losses = [round(a * (n ** (-alpha)), 4) for n in scales]
        target_n = scales[-1] * factor
        target_loss = round(a * (target_n ** (-alpha)), 4)
        ln_l1 = math.log(losses[0])
        ln_l3 = math.log(losses[2])
        ln_n1 = math.log(scales[0])
        ln_n3 = math.log(scales[2])
        fitted_alpha = round(
            (ln_l1 - ln_l3) / (ln_n3 - ln_n1), 4
        ) if ln_n3 != ln_n1 else alpha
        fitted_a = round(
            losses[0] * (scales[0] ** fitted_alpha), 4
        )
        obs_parts = [
            f"N={scales[i]}: L={losses[i]}" for i in range(3)
        ]
        problem = ", ".join(obs_parts)
        return problem, {
            "scales": scales, "losses": losses,
            "alpha": alpha, "a": a,
            "fitted_alpha": fitted_alpha, "fitted_a": fitted_a,
            "target_n": target_n, "target_loss": target_loss,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate scaling law fitting and prediction steps.

        Args:
            data: Solution data with fitted parameters and prediction.

        Returns:
            Steps showing fit procedure and extrapolation.
        """
        return [
            "fit: ln(L)=ln(a)-alpha*ln(N)",
            f"alpha={data['fitted_alpha']}",
            f"a={data['fitted_a']}",
            f"predict N={data['target_n']}: L={data['target_loss']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the predicted loss at the target scale.

        Args:
            data: Solution data.

        Returns:
            Predicted loss as a string.
        """
        return str(data["target_loss"])


@register
class ErrorTaxonomyGenerator(StepGenerator):
    """Classify error types in an ML system.

    Given a description of ML system failures, classifies errors into
    categories: data error, label noise, distribution shift, model
    capacity, and optimization issues.

    Input format:
        ``classify error types in ML system``

    Target format:
        ``symptoms: high train loss, insensitive to data size <step>
        candidate: model_capacity - model too small <step>
        candidate: optimization - stuck in bad minimum <step>
        diagnostic: increase model size, check train loss trend <step>
        primary: model_capacity``

    Difficulty scaling:
        d1-3: 2 error types to classify.
        d4-6: 3 error types.
        d7-8: 4 error types with ambiguous symptoms.

    Prerequisites:
        error_detection.

    Example:
        >>> gen = ErrorTaxonomyGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'error_taxonomy'
    """

    def __init__(self, **kwargs) -> None:
        """Initialise with error type database.

        Args:
            **kwargs: Passed to parent constructor.
        """
        super().__init__(**kwargs)
        self._db = ErrorTypeDB()

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "error_taxonomy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["error_detection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of error types.

        Returns:
            Natural language description.
        """
        return "classify error types in ML system"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an error taxonomy problem.

        Args:
            difficulty: Controls number of errors to classify.

        Returns:
            Tuple of (symptom_description, solution_data).
        """
        num_errors = min(2 + difficulty // 3, 4)
        errors = self._db.random_scenario(self._rng, num_errors)
        symptoms = [e[1]["symptom"] for e in errors]
        problem = f"symptoms: {'; '.join(symptoms)}"
        return problem, {
            "errors": errors,
            "num_errors": num_errors,
            "primary": errors[0][0],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate error classification steps.

        Args:
            data: Solution data with error types and diagnostics.

        Returns:
            Steps showing each candidate error and diagnostic strategy.
        """
        steps = []
        for name, info in data["errors"]:
            steps.append(f"candidate: {name} - {info['description']}")
        diagnostics = [info["diagnostic"] for _, info in data["errors"]]
        steps.append(f"diagnostic: {'; '.join(diagnostics)}")
        steps.append(f"primary: {data['primary']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the primary error classification.

        Args:
            data: Solution data.

        Returns:
            Primary error type name.
        """
        return data["primary"]


@register
class MethodComparisonGenerator(StepGenerator):
    """Compare two approaches on multiple criteria and recommend one.

    Evaluates two methods on accuracy, complexity, and interpretability,
    then provides a justified recommendation.

    Input format:
        ``compare methods and recommend``

    Target format:
        ``method A: decision tree vs method B: neural network <step>
        accuracy: A=moderate, B=high <step>
        complexity: A=O(n log n), B=O(n*d*epochs) <step>
        interpretability: A=high, B=low <step>
        for small data with explainability requirement: recommend A
        <step> decision_tree``

    Difficulty scaling:
        d1-3: 2 criteria comparison.
        d4-6: 3 criteria with constraint.
        d7-8: 4 criteria with nuanced tradeoff.

    Prerequisites:
        method_selection.

    Example:
        >>> gen = MethodComparisonGenerator(seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'method_comparison'
    """

    _COMPARISONS: list[dict] = [
        {
            "a_name": "decision_tree", "b_name": "neural_network",
            "accuracy": ("moderate", "high"),
            "complexity": ("O(n log n)", "O(n*d*epochs)"),
            "interpretability": ("high", "low"),
            "scalability": ("moderate", "high"),
            "constraint": "small data with explainability requirement",
            "winner": "decision_tree",
        },
        {
            "a_name": "linear_regression", "b_name": "random_forest",
            "accuracy": ("low-moderate", "high"),
            "complexity": ("O(n*d)", "O(n*d*trees)"),
            "interpretability": ("high", "moderate"),
            "scalability": ("high", "moderate"),
            "constraint": "large dataset with linear relationships",
            "winner": "linear_regression",
        },
        {
            "a_name": "SVM", "b_name": "logistic_regression",
            "accuracy": ("high", "moderate"),
            "complexity": ("O(n^2)", "O(n*d)"),
            "interpretability": ("low", "high"),
            "scalability": ("low", "high"),
            "constraint": "large-scale classification with probability outputs",
            "winner": "logistic_regression",
        },
        {
            "a_name": "k_nearest_neighbors", "b_name": "naive_bayes",
            "accuracy": ("moderate", "moderate"),
            "complexity": ("O(n*d) per query", "O(n*d) training, O(d) inference"),
            "interpretability": ("moderate", "high"),
            "scalability": ("low", "high"),
            "constraint": "real-time inference with limited compute",
            "winner": "naive_bayes",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "method_comparison"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of criteria.

        Returns:
            Natural language description.
        """
        return "compare methods and recommend"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a method comparison problem.

        Args:
            difficulty: Controls number of criteria shown.

        Returns:
            Tuple of (comparison_spec, solution_data).
        """
        comp = self._rng.choice(self._COMPARISONS)
        criteria = ["accuracy", "complexity"]
        if difficulty >= 4:
            criteria.append("interpretability")
        if difficulty >= 7:
            criteria.append("scalability")
        problem = f"method A: {comp['a_name']} vs method B: {comp['b_name']}"
        return problem, {
            "comp": comp,
            "criteria": criteria,
            "winner": comp["winner"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-criterion comparison and recommendation steps.

        Args:
            data: Solution data with comparison details.

        Returns:
            Steps showing each criterion and final recommendation.
        """
        comp = data["comp"]
        steps = []
        for criterion in data["criteria"]:
            a_val, b_val = comp[criterion]
            steps.append(f"{criterion}: A={a_val}, B={b_val}")
        steps.append(f"constraint: {comp['constraint']}")
        steps.append(f"recommend: {comp['winner']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the recommended method.

        Args:
            data: Solution data.

        Returns:
            Name of the recommended method.
        """
        return data["winner"]
