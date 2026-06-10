"""Extended CS theory task generators.

8 generators across tiers 5-7 covering time complexity analysis,
space complexity, NP-completeness proofs, complexity classes,
circuit complexity, communication complexity, streaming algorithms,
and randomised complexity.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper: code snippet templates for complexity analysis
# ---------------------------------------------------------------------------

_LOOP_SNIPPETS = [
    {"code": "for i in range(n): x += 1", "ops": "n", "big_o": "O(n)"},
    {"code": "for i in range(n): for j in range(n): x += 1",
     "ops": "n^2", "big_o": "O(n^2)"},
    {"code": "for i in range(n): for j in range(i): x += 1",
     "ops": "n*(n-1)/2", "big_o": "O(n^2)"},
    {"code": "i = 1; while i < n: i *= 2",
     "ops": "log2(n)", "big_o": "O(log n)"},
    {"code": "for i in range(n): j = 1; while j < n: j *= 2",
     "ops": "n*log2(n)", "big_o": "O(n log n)"},
    {"code": "for i in range(n): for j in range(n): for k in range(n): x += 1",
     "ops": "n^3", "big_o": "O(n^3)"},
]

_RECURSIVE_SNIPPETS = [
    {"code": "def f(n): return f(n-1)+f(n-2) if n>1 else 1",
     "ops": "2^n", "big_o": "O(2^n)", "space": "O(n)"},
    {"code": "def f(n): return 2*f(n//2)+n if n>1 else 1",
     "ops": "n*log2(n)", "big_o": "O(n log n)", "space": "O(log n)"},
    {"code": "def f(n): return f(n//2)+1 if n>1 else 1",
     "ops": "log2(n)", "big_o": "O(log n)", "space": "O(log n)"},
    {"code": "def f(n): return f(n-1)+1 if n>0 else 0",
     "ops": "n", "big_o": "O(n)", "space": "O(n)"},
]

# NP-complete problem templates
_NP_COMPLETE_TEMPLATES = [
    {
        "problem": "Vertex Cover",
        "description": "Given graph G and integer k, is there a vertex set S of size <= k covering all edges?",
        "in_np": "Given S, verify each edge has at least one endpoint in S in O(|E|) time.",
        "reduction_from": "3-SAT",
        "reduction_sketch": "For each clause, create a gadget. Variable x_i maps to edge (x_i, NOT x_i). Clause gadget connects to variable endpoints.",
    },
    {
        "problem": "Hamiltonian Path",
        "description": "Given graph G, is there a path visiting every vertex exactly once?",
        "in_np": "Given path P, verify it visits all n vertices with no repeats in O(n) time.",
        "reduction_from": "3-SAT",
        "reduction_sketch": "Build diamond gadgets for each variable. Connect clause nodes to literal nodes. HP exists iff formula is satisfiable.",
    },
    {
        "problem": "Subset Sum",
        "description": "Given set S of integers and target t, is there a subset summing to t?",
        "in_np": "Given subset, sum elements and check equality with t in O(|S|) time.",
        "reduction_from": "3-SAT",
        "reduction_sketch": "Encode each variable and clause as a digit position. Construct integers so valid assignments yield target sum.",
    },
    {
        "problem": "Graph Coloring (k=3)",
        "description": "Given graph G, can vertices be colored with 3 colors so no adjacent pair shares a color?",
        "in_np": "Given coloring, check each edge has differently colored endpoints in O(|E|) time.",
        "reduction_from": "3-SAT",
        "reduction_sketch": "Create truth-setting and palette gadgets. For each clause, add OR-gadget connecting literal nodes to palette.",
    },
]

_COMPLEXITY_CLASSES = [
    {"problem": "sorting n numbers", "class": "P",
     "reason": "Merge sort runs in O(n log n) time"},
    {"problem": "shortest path in weighted graph", "class": "P",
     "reason": "Dijkstra runs in O((V+E) log V) time"},
    {"problem": "primality testing", "class": "P",
     "reason": "AKS algorithm runs in polynomial time"},
    {"problem": "2-SAT", "class": "P",
     "reason": "Solvable via implication graph SCC in O(n+m)"},
    {"problem": "3-SAT", "class": "NP-complete",
     "reason": "Cook-Levin theorem: first NP-complete problem"},
    {"problem": "graph isomorphism", "class": "NP",
     "reason": "In NP but not known to be NP-complete or in P"},
    {"problem": "TQBF (quantified Boolean formula)", "class": "PSPACE-complete",
     "reason": "Requires evaluating all quantifier alternations"},
    {"problem": "halting problem", "class": "undecidable",
     "reason": "Proven undecidable by Turing via diagonalisation"},
    {"problem": "chess (generalised nxn)", "class": "EXP-complete",
     "reason": "Optimal play requires exponential-time search"},
    {"problem": "integer factoring", "class": "NP",
     "reason": "In NP (verify factor in poly time), not known to be in P or NP-complete"},
]


# ---------------------------------------------------------------------------
# 1. Time Complexity Compute (tier 5)
# ---------------------------------------------------------------------------

@register
class TimeComplexityComputeGenerator(StepGenerator):
    """Count exact operations for code snippets and express in Big-O.

    Given a loop or recursive code snippet with parameter n, count the
    exact number of operations and derive the Big-O classification.

    Difficulty scaling:
        Difficulty 1-3: simple single loops (linear, logarithmic).
        Difficulty 4-6: nested loops or merge-sort-style recursion.
        Difficulty 7-8: triple nesting or exponential recursion.

    Prerequisites:
        big_o.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "time_complexity_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["big_o"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "count operations in code snippet and express in Big-O"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a time complexity analysis problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._rng.randint(4, 16) if difficulty <= 3 else self._rng.randint(8, 32)
        if difficulty <= 3:
            pool = [s for s in _LOOP_SNIPPETS if s["big_o"] in ("O(n)", "O(log n)")]
        elif difficulty <= 6:
            pool = [s for s in _LOOP_SNIPPETS if "n^2" in s["ops"] or "n*log" in s["ops"]]
            pool += [s for s in _RECURSIVE_SNIPPETS if "n*log" in s["ops"]]
        else:
            pool = [s for s in _LOOP_SNIPPETS if "n^3" in s["ops"]]
            pool += [s for s in _RECURSIVE_SNIPPETS if "2^n" in s["ops"]]

        snippet = self._rng.choice(pool)
        ops_expr = snippet["ops"]

        # Compute exact count for given n
        if ops_expr == "n":
            exact = n
        elif ops_expr == "n^2":
            exact = n * n
        elif ops_expr == "n*(n-1)/2":
            exact = n * (n - 1) // 2
        elif ops_expr == "log2(n)":
            exact = max(1, int(math.log2(n)))
        elif ops_expr == "n*log2(n)":
            exact = n * max(1, int(math.log2(n)))
        elif ops_expr == "n^3":
            exact = n * n * n
        elif ops_expr == "2^n":
            exact = 2 ** n
        else:
            exact = n

        return (
            f"n={n}: {snippet['code']}",
            {"n": n, "code": snippet["code"], "ops_expr": ops_expr,
             "exact": exact, "big_o": snippet["big_o"]},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for time complexity.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing operation count and Big-O.
        """
        return [
            f"count operations: {data['ops_expr']}",
            f"for n={data['n']}: {data['ops_expr']} = {data['exact']}",
            f"Big-O: {data['big_o']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the Big-O classification.

        Args:
            data: Solution data dict.

        Returns:
            Exact count and Big-O as a string.
        """
        return f"ops={data['exact']}, {data['big_o']}"


# ---------------------------------------------------------------------------
# 2. Space Complexity (tier 5)
# ---------------------------------------------------------------------------

@register
class SpaceComplexityGenerator(StepGenerator):
    """Analyse space usage of algorithms.

    Given a code snippet, determine stack depth for recursion,
    auxiliary array size, or whether the algorithm is in-place.

    Difficulty scaling:
        Difficulty 1-3: in-place or O(1) extra space algorithms.
        Difficulty 4-6: O(n) auxiliary space or O(log n) stack depth.
        Difficulty 7-8: O(n) stack depth (naive recursion) or O(n^2) auxiliary.

    Prerequisites:
        big_o.
    """

    _TEMPLATES = [
        {"name": "bubble sort", "space": "O(1)", "reason": "in-place swaps only",
         "difficulty_range": (1, 3)},
        {"name": "selection sort", "space": "O(1)", "reason": "in-place, single temp variable",
         "difficulty_range": (1, 3)},
        {"name": "binary search", "space": "O(1)", "reason": "iterative, two pointers",
         "difficulty_range": (1, 4)},
        {"name": "merge sort", "space": "O(n)", "reason": "auxiliary array for merging",
         "difficulty_range": (4, 6)},
        {"name": "quicksort (avg)", "space": "O(log n)",
         "reason": "recursion stack depth log n on average",
         "difficulty_range": (4, 6)},
        {"name": "BFS on graph", "space": "O(V)",
         "reason": "queue holds up to V vertices",
         "difficulty_range": (4, 6)},
        {"name": "naive Fibonacci recursion", "space": "O(n)",
         "reason": "recursion depth n before base case",
         "difficulty_range": (7, 8)},
        {"name": "matrix multiplication (naive)", "space": "O(n^2)",
         "reason": "output matrix of size n x n",
         "difficulty_range": (7, 8)},
        {"name": "DFS on graph", "space": "O(V)",
         "reason": "recursion stack or explicit stack holds up to V",
         "difficulty_range": (5, 7)},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "space_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["big_o"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "analyse space complexity of algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a space complexity analysis problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        pool = [t for t in self._TEMPLATES
                if t["difficulty_range"][0] <= difficulty <= t["difficulty_range"][1]]
        if not pool:
            pool = self._TEMPLATES[:3]

        template = self._rng.choice(pool)
        n = self._rng.randint(8, 64)

        # Compute concrete value
        space_str = template["space"]
        if space_str == "O(1)":
            concrete = 1
        elif space_str == "O(n)":
            concrete = n
        elif space_str == "O(log n)":
            concrete = max(1, int(math.log2(n)))
        elif space_str == "O(n^2)":
            concrete = n * n
        elif space_str == "O(V)":
            concrete = n
        else:
            concrete = n

        return (
            f"Space analysis: {template['name']}, n={n}",
            {"name": template["name"], "n": n, "space": space_str,
             "reason": template["reason"], "concrete": concrete},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for space complexity.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing space analysis reasoning.
        """
        return [
            f"algorithm: {data['name']}",
            f"reasoning: {data['reason']}",
            f"space complexity: {data['space']}",
            f"for n={data['n']}: concrete space ~ {data['concrete']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the space complexity.

        Args:
            data: Solution data dict.

        Returns:
            Space complexity class as a string.
        """
        return data["space"]


# ---------------------------------------------------------------------------
# 3. NP-Completeness Proof (tier 7)
# ---------------------------------------------------------------------------

@register
class NPCompletenessProofGenerator(StepGenerator):
    """Show a problem is NP-complete using template-based reductions.

    Demonstrates the two-step proof: (1) show problem is in NP by
    describing a polynomial-time verifier, and (2) show NP-hardness
    by reducing from a known NP-complete problem.

    Difficulty scaling:
        Difficulty 1-4: simpler problems (Vertex Cover, Subset Sum).
        Difficulty 5-8: harder reductions (Hamiltonian Path, 3-Coloring).

    Prerequisites:
        sat_verify.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "np_completeness_proof"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sat_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "prove problem is NP-complete"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an NP-completeness proof problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 4:
            pool = [t for t in _NP_COMPLETE_TEMPLATES
                    if t["problem"] in ("Vertex Cover", "Subset Sum")]
        else:
            pool = [t for t in _NP_COMPLETE_TEMPLATES
                    if t["problem"] in ("Hamiltonian Path", "Graph Coloring (k=3)")]
        if not pool:
            pool = _NP_COMPLETE_TEMPLATES

        template = self._rng.choice(pool)
        return (
            f"Prove {template['problem']} is NP-complete: {template['description']}",
            {"problem": template["problem"],
             "description": template["description"],
             "in_np": template["in_np"],
             "reduction_from": template["reduction_from"],
             "reduction_sketch": template["reduction_sketch"]},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for NP-completeness proof.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the two-part proof structure.
        """
        return [
            f"Step 1 (in NP): {data['in_np']}",
            f"Step 2 (NP-hard): reduce from {data['reduction_from']}",
            f"Reduction: {data['reduction_sketch']}",
            f"Therefore {data['problem']} is NP-complete",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the NP-completeness result.

        Args:
            data: Solution data dict.

        Returns:
            Result string.
        """
        return f"{data['problem']} is NP-complete (in NP + reduction from {data['reduction_from']})"


# ---------------------------------------------------------------------------
# 4. Complexity Class (tier 6)
# ---------------------------------------------------------------------------

@register
class ComplexityClassGenerator(StepGenerator):
    """Classify a problem into its complexity class.

    Given a problem description, identify whether it belongs to P, NP,
    co-NP, PSPACE, EXP, or is undecidable, with justification.

    Difficulty scaling:
        Difficulty 1-3: clear P or NP-complete problems.
        Difficulty 4-6: NP or PSPACE problems.
        Difficulty 7-8: EXP-complete or undecidable.

    Prerequisites:
        sat_verify.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "complexity_class"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sat_verify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "classify problem into complexity class"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a complexity classification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            pool = [c for c in _COMPLEXITY_CLASSES if c["class"] in ("P", "NP-complete")]
        elif difficulty <= 6:
            pool = [c for c in _COMPLEXITY_CLASSES
                    if c["class"] in ("NP", "NP-complete", "PSPACE-complete")]
        else:
            pool = [c for c in _COMPLEXITY_CLASSES
                    if c["class"] in ("EXP-complete", "undecidable")]
        if not pool:
            pool = _COMPLEXITY_CLASSES

        entry = self._rng.choice(pool)
        return (
            f"Classify: {entry['problem']}",
            {"problem": entry["problem"], "class": entry["class"],
             "reason": entry["reason"]},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for complexity classification.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing classification reasoning.
        """
        return [
            f"problem: {data['problem']}",
            f"reasoning: {data['reason']}",
            f"class: {data['class']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the complexity class.

        Args:
            data: Solution data dict.

        Returns:
            Complexity class as a string.
        """
        return data["class"]


# ---------------------------------------------------------------------------
# 5. Circuit Complexity (tier 6)
# ---------------------------------------------------------------------------

@register
class CircuitComplexityGenerator(StepGenerator):
    """Compute Boolean circuit size and depth for standard functions.

    For functions like parity and majority on n bits, count the number
    of gates (circuit size) and the longest input-to-output path (depth).

    Difficulty scaling:
        Difficulty 1-3: n=2-3 bits, parity.
        Difficulty 4-6: n=4-6 bits, parity or majority.
        Difficulty 7-8: n=7-8 bits, both metrics.

    Prerequisites:
        big_o.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "circuit_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["big_o"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute circuit size and depth for Boolean function"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a circuit complexity problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
            func = "parity"
        elif difficulty <= 6:
            n = self._rng.randint(4, 6)
            func = self._rng.choice(["parity", "majority"])
        else:
            n = self._rng.randint(7, 8)
            func = self._rng.choice(["parity", "majority"])

        if func == "parity":
            # Parity of n bits: tree of XOR gates
            # Size = n-1 XOR gates, depth = ceil(log2(n))
            size = n - 1
            depth = math.ceil(math.log2(n)) if n > 1 else 0
            gate_type = "XOR"
            description = f"parity of {n} bits using XOR tree"
        else:
            # Majority of n bits (n odd): sorting network approach
            # Simple bound: O(n^2) gates comparing pairs, depth O(n)
            # For small n, use exact counts
            size = n * (n - 1) // 2  # compare all pairs
            depth = 2 * n - 1  # linear depth sorting network
            gate_type = "AND/OR"
            description = f"majority of {n} bits via comparison network"

        return (
            f"Circuit for {description}",
            {"func": func, "n": n, "size": size, "depth": depth,
             "gate_type": gate_type, "description": description},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for circuit complexity.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing gate count and depth computation.
        """
        steps = [f"function: {data['description']}"]
        if data["func"] == "parity":
            steps.append(f"tree of {data['gate_type']} gates: {data['n']}-1 = {data['size']} gates")
            steps.append(f"depth = ceil(log2({data['n']})) = {data['depth']}")
        else:
            steps.append(f"comparison network: C({data['n']},2) = {data['size']} gates")
            steps.append(f"depth = 2*{data['n']}-1 = {data['depth']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the circuit metrics.

        Args:
            data: Solution data dict.

        Returns:
            Size and depth as a string.
        """
        return f"size={data['size']}, depth={data['depth']}"


# ---------------------------------------------------------------------------
# 6. Communication Complexity (tier 6)
# ---------------------------------------------------------------------------

@register
class CommunicationComplexityGenerator(StepGenerator):
    """Compute deterministic communication complexity for f(x,y).

    Alice has x, Bob has y. Compute lower bound via fooling set method
    for standard functions like equality and disjointness.

    Difficulty scaling:
        Difficulty 1-3: n=2-3 bit inputs, equality function.
        Difficulty 4-6: n=4-5 bit inputs, equality or inner product.
        Difficulty 7-8: n=6-8 bit inputs, disjointness.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "communication_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute communication complexity lower bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a communication complexity problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(2, 3)
            func = "equality"
        elif difficulty <= 6:
            n = self._rng.randint(4, 5)
            func = self._rng.choice(["equality", "inner_product"])
        else:
            n = self._rng.randint(6, 8)
            func = self._rng.choice(["equality", "disjointness"])

        if func == "equality":
            # EQ(x,y): D(EQ) = n+1 deterministic, fooling set size = 2^n
            fooling_set_size = 2 ** n
            lower_bound = n
            cc_bits = n + 1
            desc = f"EQ(x,y) on {n}-bit strings"
            fooling_desc = f"{{(x,x) : x in {{0,1}}^{n}}} has {fooling_set_size} pairs"
        elif func == "inner_product":
            # IP(x,y) = sum x_i*y_i mod 2: D(IP) = n+1
            fooling_set_size = 2 ** n
            lower_bound = n
            cc_bits = n + 1
            desc = f"IP(x,y) = <x,y> mod 2 on {n}-bit strings"
            fooling_desc = f"fooling set of size {fooling_set_size} from basis vectors"
        else:
            # DISJ(x,y): D(DISJ) = n+1
            fooling_set_size = 2 ** n
            lower_bound = n
            cc_bits = n + 1
            desc = f"DISJ(x,y) on {n}-bit strings"
            fooling_desc = f"{{(S,S^c) : S subseteq [n]}} gives {fooling_set_size} pairs"

        return (
            f"CC for {desc}",
            {"func": func, "n": n, "fooling_set_size": fooling_set_size,
             "lower_bound": lower_bound, "cc_bits": cc_bits,
             "desc": desc, "fooling_desc": fooling_desc},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for communication complexity.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing fooling set and lower bound.
        """
        return [
            f"function: {data['desc']}",
            f"fooling set: {data['fooling_desc']}",
            f"lower bound: log2({data['fooling_set_size']}) = {data['lower_bound']}",
            f"D(f) >= {data['lower_bound']}, protocol uses {data['cc_bits']} bits",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the communication complexity.

        Args:
            data: Solution data dict.

        Returns:
            Lower bound and protocol cost as a string.
        """
        return f"D(f) = {data['cc_bits']} bits"


# ---------------------------------------------------------------------------
# 7. Streaming Algorithm (tier 5)
# ---------------------------------------------------------------------------

@register
class StreamingAlgorithmGenerator(StepGenerator):
    """Simulate streaming algorithms on small sequences.

    Boyer-Moore majority vote: single pass, O(1) space to find
    majority element. Also count-distinct estimation concepts.

    Difficulty scaling:
        Difficulty 1-3: 5-8 elements, clear majority.
        Difficulty 4-6: 8-12 elements, majority by small margin.
        Difficulty 7-8: 12-16 elements, Boyer-Moore trace.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "streaming_algorithm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find majority element using Boyer-Moore voting"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Boyer-Moore majority vote problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            length = self._rng.randint(5, 8)
        elif difficulty <= 6:
            length = self._rng.randint(8, 12)
        else:
            length = self._rng.randint(12, 16)

        # Create sequence with guaranteed majority
        majority_count = length // 2 + 1
        majority_val = self._rng.randint(1, 9)
        others = [self._rng.randint(1, 9) for _ in range(length - majority_count)]
        # Ensure others differ from majority
        others = [v if v != majority_val else (v % 9) + 1 for v in others]

        seq = [majority_val] * majority_count + others
        self._rng.shuffle(seq)

        # Simulate Boyer-Moore
        candidate = seq[0]
        count = 1
        trace = [(seq[0], candidate, count)]
        for elem in seq[1:]:
            if count == 0:
                candidate = elem
                count = 1
            elif elem == candidate:
                count += 1
            else:
                count -= 1
            trace.append((elem, candidate, count))

        # Keep only a few trace entries for brevity
        key_trace = trace[:min(5, len(trace))]

        return (
            f"Boyer-Moore on {seq}",
            {"seq": seq, "majority": majority_val,
             "majority_count": majority_count, "length": length,
             "candidate": candidate, "trace": key_trace},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Boyer-Moore.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the voting process.
        """
        steps = []
        for elem, cand, cnt in data["trace"]:
            steps.append(f"read {elem}: candidate={cand}, count={cnt}")
        steps.append(
            f"final candidate={data['candidate']}, "
            f"appears {data['majority_count']}/{data['length']} times"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the majority element.

        Args:
            data: Solution data dict.

        Returns:
            Majority element as a string.
        """
        return f"majority={data['majority']}"


# ---------------------------------------------------------------------------
# 8. Randomised Complexity (tier 6)
# ---------------------------------------------------------------------------

@register
class RandomisedComplexityGenerator(StepGenerator):
    """Compute repetitions needed to reduce BPP error probability.

    In BPP, a single run has error at most 1/3. By repeating k times
    and taking majority, error drops to at most 2^{-Omega(k)}.
    Compute required k for a target error probability.

    Difficulty scaling:
        Difficulty 1-3: target error 0.1 to 0.01.
        Difficulty 4-6: target error 0.001 to 0.0001.
        Difficulty 7-8: target error 1e-6 to 1e-10.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "randomised_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute BPP error amplification repetitions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BPP error amplification problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            exponent = self._rng.randint(1, 2)
        elif difficulty <= 6:
            exponent = self._rng.randint(3, 4)
        else:
            exponent = self._rng.randint(6, 10)

        target_error = 10.0 ** (-exponent)
        # Each repetition reduces error by factor ~(2*sqrt(1/3*2/3))^k
        # Simplified: k independent trials with majority vote
        # Error after k (odd) trials with single-trial error p=1/3:
        # Using Chernoff: error <= exp(-k/18) approximately
        # So k >= 18 * ln(1/target_error)
        k_exact = 18.0 * math.log(1.0 / target_error)
        k_needed = math.ceil(k_exact)
        # Ensure k is odd for majority vote
        if k_needed % 2 == 0:
            k_needed += 1

        actual_error = round(math.exp(-k_needed / 18.0), 4)

        return (
            f"BPP amplification: target error <= {target_error}",
            {"target_error": target_error, "exponent": exponent,
             "k_needed": k_needed, "k_exact": round(k_exact, 4),
             "actual_error": actual_error},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for BPP amplification.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the computation.
        """
        return [
            f"single trial error p = 1/3",
            f"after k majority-vote trials: error <= exp(-k/18)",
            f"need exp(-k/18) <= {data['target_error']}",
            f"k >= 18*ln(1/{data['target_error']}) = 18*{data['exponent']}*ln(10) = {data['k_exact']}",
            f"k = {data['k_needed']} (odd), actual error ~ {data['actual_error']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the required repetitions.

        Args:
            data: Solution data dict.

        Returns:
            Number of repetitions and achieved error as a string.
        """
        return f"k={data['k_needed']}, error<={data['actual_error']}"
