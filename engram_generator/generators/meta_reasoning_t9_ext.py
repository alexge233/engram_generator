"""Extended tier 9 generators -- research-level meta-reasoning.

8 generators targeting research question formulation, literature gap
identification, experiment interpretation, algorithm adaptation,
complexity lower bounds, proof generalisation, abstraction identification,
and failure prediction. All tier 9.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ── 1. Research question formulation (tier 9) ──────────────────────


@register
class ResearchQuestionFormulateGenerator(StepGenerator):
    """Formulate a precise, testable research question from a domain and phenomenon.

    Given a scientific domain and an observed phenomenon or gap, produces
    a structured research question that is specific, measurable, and
    falsifiable. Uses template-based generation with randomised domains,
    phenomena, and hypothesis components.

    Input format:
        ``formulate research question for domain and phenomenon``

    Target format:
        ``domain: graph algorithms, phenomenon: shortest path in
        dynamic graphs <step> gap: existing algorithms assume static
        edges <step> question: does maintaining a priority queue of
        affected vertices reduce update cost from O(V*E) to O(E*log V)
        when edges change? <step> testable: yes, compare update cost
        on random dynamic graphs <step> research question formulated``

    Difficulty scaling:
        Difficulty 1-3: well-defined CS/math domains.
        Difficulty 4-6: interdisciplinary domains.
        Difficulty 7-8: open-ended ML/AI domains.

    Prerequisites:
        hypothesis_design.
    """

    _SCENARIOS = [
        {
            "domain": "graph algorithms",
            "phenomenon": "shortest path recomputation in dynamic graphs",
            "gap": "existing algorithms assume static edges",
            "question": "does maintaining a priority queue of affected vertices reduce "
                        "update cost from O(V*E) to O(E*log V) when edges change?",
            "testable": "compare update cost on random dynamic graphs with k edge changes",
        },
        {
            "domain": "numerical optimisation",
            "phenomenon": "loss plateaus in non-convex landscapes",
            "gap": "gradient descent stalls near saddle points",
            "question": "does adding noise proportional to the Hessian's smallest eigenvalue "
                        "escape saddle points faster than uniform noise?",
            "testable": "measure escape time on benchmark non-convex functions",
        },
        {
            "domain": "distributed systems",
            "phenomenon": "consensus latency under network partitions",
            "gap": "Raft and Paxos degrade to sequential commits during partitions",
            "question": "can speculative execution of uncommitted log entries reduce "
                        "latency by more than 30% during partial partitions?",
            "testable": "inject partitions in a 5-node cluster, measure commit latency",
        },
        {
            "domain": "natural language processing",
            "phenomenon": "length generalisation failure in transformers",
            "gap": "models trained on short sequences fail on longer ones",
            "question": "does relative positional encoding with learned decay "
                        "improve accuracy on sequences 2x training length?",
            "testable": "train on length<=128, evaluate on length 256 and 512",
        },
        {
            "domain": "computational biology",
            "phenomenon": "protein folding energy landscape ruggedness",
            "gap": "Monte Carlo sampling misses low-energy conformations",
            "question": "does a coarse-to-fine sampling strategy with adaptive "
                        "resolution reduce missed minima by more than 50%?",
            "testable": "compare found minima count on benchmark proteins",
        },
        {
            "domain": "reinforcement learning",
            "phenomenon": "reward sparsity in long-horizon tasks",
            "gap": "standard RL struggles when reward signal is delayed by 100+ steps",
            "question": "does hindsight relabelling with learned subgoals improve "
                        "sample efficiency by an order of magnitude?",
            "testable": "compare episodes-to-solve on sparse-reward mazes",
        },
        {
            "domain": "cryptography",
            "phenomenon": "side-channel leakage in constant-time implementations",
            "gap": "cache timing attacks bypass algorithmic constant-time guarantees",
            "question": "does memory-oblivious data layout reduce timing "
                        "variance below the noise floor of modern CPUs?",
            "testable": "measure timing variance across 10^6 invocations",
        },
        {
            "domain": "information theory",
            "phenomenon": "lossy compression near the rate-distortion bound",
            "gap": "practical codecs are 15-30% above the theoretical limit",
            "question": "does a learned entropy model with autoregressive context "
                        "close the gap to within 5% of the bound?",
            "testable": "measure bits-per-pixel on standard image benchmarks",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "research_question_formulate"

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
            difficulty: Controls scenario complexity.

        Returns:
            Natural language description.
        """
        return "formulate a precise, testable research question"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a research question formulation problem.

        Args:
            difficulty: Controls scenario pool size.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        pool = self._SCENARIOS[:max(3, min(len(self._SCENARIOS), 2 + difficulty))]
        scenario = self._rng.choice(pool)
        problem = (f"domain: {scenario['domain']}; "
                   f"phenomenon: {scenario['phenomenon']}")
        return problem, dict(scenario)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate research question formulation steps.

        Args:
            data: Solution data with gap, question, and testability.

        Returns:
            Steps showing gap identification and question construction.
        """
        return [
            f"gap: {data['gap']}",
            f"question: {data['question']}",
            f"testable: {data['testable']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the formulated research question.

        Args:
            data: Solution data.

        Returns:
            The research question.
        """
        return data["question"]


# ── 2. Literature gap identification (tier 9) ─────────────────────


@register
class LiteratureGapIdentifyGenerator(StepGenerator):
    """Identify what is missing from a set of existing results.

    Given 3-4 existing theorems or methods in a domain, identifies a
    gap: a missing case, an unaddressed assumption, or an opportunity
    for unification. Template-based with randomised result descriptions.

    Input format:
        ``given these results, identify what is missing``

    Target format:
        ``result 1: sorting in O(n log n) via comparisons <step>
        result 2: radix sort in O(nk) for bounded keys <step>
        result 3: counting sort in O(n+k) for integer keys <step>
        gap: no known O(n) comparison sort; also no sort optimal
        for partially sorted input <step> opportunity: adaptive
        sort that is O(n) for nearly sorted, O(n log n) worst case``

    Difficulty scaling:
        Difficulty 1-3: clearly missing special case.
        Difficulty 4-6: missing generalisation.
        Difficulty 7-8: cross-domain unification gap.

    Prerequisites:
        method_selection.
    """

    _DOMAINS = [
        {
            "results": [
                "sorting in O(n log n) via comparisons (mergesort)",
                "radix sort in O(nk) for bounded integer keys",
                "counting sort in O(n+k) for keys in [0,k]",
            ],
            "gap": "no comparison sort breaks O(n log n); none adapts to partial order",
            "opportunity": "adaptive sort: O(n) for nearly sorted, O(n log n) worst case",
        },
        {
            "results": [
                "BFS finds shortest path in unweighted graphs O(V+E)",
                "Dijkstra finds shortest path with non-negative weights O((V+E)log V)",
                "Bellman-Ford handles negative weights O(VE)",
            ],
            "gap": "no algorithm handles negative weights in O((V+E)log V)",
            "opportunity": "Johnson's algorithm uses reweighting for sparse graphs with negative edges",
        },
        {
            "results": [
                "SGD converges for convex losses at O(1/sqrt(T))",
                "Adam adapts learning rate per parameter",
                "L-BFGS uses curvature but requires full gradient",
            ],
            "gap": "no optimiser combines curvature with mini-batch efficiency",
            "opportunity": "stochastic quasi-Newton methods approximate curvature from mini-batches",
        },
        {
            "results": [
                "dropout regularises by randomly zeroing activations",
                "weight decay penalises large weights via L2",
                "batch normalisation stabilises training distributions",
            ],
            "gap": "no single technique addresses both overfitting and internal covariate shift",
            "opportunity": "combined dropout + normalisation with adaptive rate scheduling",
        },
        {
            "results": [
                "RSA: security from integer factoring, key >= 2048 bits",
                "ECC: security from discrete log on elliptic curves, key >= 256 bits",
                "AES: symmetric encryption, 128/256-bit keys",
            ],
            "gap": "none is post-quantum secure for key exchange",
            "opportunity": "lattice-based cryptography (e.g., Kyber) for quantum-resistant key exchange",
        },
        {
            "results": [
                "Euler method: O(h) local error, simple but inaccurate",
                "RK4: O(h^4) local error, widely used",
                "implicit methods: stable for stiff equations but require solving nonlinear systems",
            ],
            "gap": "no explicit method handles stiffness without step-size restriction",
            "opportunity": "exponential integrators factor out linear stiff part analytically",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "literature_gap_identify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls domain complexity.

        Returns:
            Natural language description.
        """
        return "identify what is missing from these existing results"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a literature gap identification problem.

        Args:
            difficulty: Controls domain pool size.

        Returns:
            Tuple of (results_description, solution_data).
        """
        pool = self._DOMAINS[:max(2, min(len(self._DOMAINS), 1 + difficulty))]
        domain = self._rng.choice(pool)
        result_lines = "; ".join(
            f"result {i + 1}: {r}" for i, r in enumerate(domain["results"])
        )
        return result_lines, dict(domain)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gap identification steps.

        Args:
            data: Solution data with results, gap, and opportunity.

        Returns:
            Steps listing results, identifying gap, and suggesting opportunity.
        """
        steps = [f"known: {r[:60]}" for r in data["results"][:2]]
        steps.append(f"gap: {data['gap'][:80]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the identified gap and opportunity.

        Args:
            data: Solution data.

        Returns:
            Gap summary.
        """
        return f"{data['gap']}; {data['opportunity']}"


# ── 3. Experiment interpretation (tier 9) ──────────────────────────


@register
class ExperimentInterpretGenerator(StepGenerator):
    """Interpret experimental results to support or refute a hypothesis.

    Given a hypothesis and numerical results (means, standard deviations,
    sample sizes), determines whether the evidence supports the hypothesis
    using simple statistical reasoning (effect size, overlap of confidence
    intervals).

    Input format:
        ``interpret these experimental results``

    Target format:
        ``hypothesis: method A is faster than B <step>
        A: mean=12.3, std=1.5, n=30 <step>
        B: mean=15.1, std=2.0, n=30 <step>
        difference=2.8, pooled_std=1.77 <step>
        effect_size=1.58 (large) <step>
        conclusion: supports hypothesis (large effect)``

    Difficulty scaling:
        Difficulty 1-3: clear support or refutation.
        Difficulty 4-6: ambiguous results requiring nuance.
        Difficulty 7-8: confounded or insufficient sample size.

    Prerequisites:
        hypothesis_design.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "experiment_interpret"

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
            difficulty: Controls result ambiguity.

        Returns:
            Natural language description.
        """
        return "interpret these experimental results"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an experiment interpretation problem.

        Constructs two group means with standard deviations and computes
        effect size (Cohen's d). Difficulty controls how clearly the
        evidence supports or refutes the hypothesis.

        Args:
            difficulty: Controls ambiguity of results.

        Returns:
            Tuple of (hypothesis_and_data, solution_data).
        """
        hypotheses = [
            ("method A is faster than B", "time", "lower"),
            ("method A has higher accuracy than B", "accuracy", "higher"),
            ("algorithm X uses less memory than Y", "memory_mb", "lower"),
            ("approach P converges in fewer iterations than Q", "iterations", "lower"),
        ]
        hyp_text, metric, direction = self._rng.choice(hypotheses)

        n = self._rng.randint(10, 50)
        mean_b = round(self._rng.uniform(10.0, 50.0), 1)
        std_b = round(self._rng.uniform(1.0, 5.0), 1)

        if difficulty <= 3:
            # Clear effect
            shift = self._rng.uniform(2.0, 4.0) * std_b
        elif difficulty <= 6:
            # Small effect
            shift = self._rng.uniform(0.3, 0.8) * std_b
        else:
            # Negligible or reversed
            shift = self._rng.uniform(-0.5, 0.3) * std_b

        if direction == "lower":
            mean_a = round(mean_b - shift, 1)
        else:
            mean_a = round(mean_b + shift, 1)
        std_a = round(self._rng.uniform(1.0, 5.0), 1)

        import math
        pooled_std = round(math.sqrt((std_a ** 2 + std_b ** 2) / 2), 4)
        diff = round(abs(mean_a - mean_b), 4)
        effect_size = round(diff / pooled_std, 4) if pooled_std > 0 else 0.0

        if effect_size >= 0.8:
            effect_label = "large"
        elif effect_size >= 0.5:
            effect_label = "medium"
        elif effect_size >= 0.2:
            effect_label = "small"
        else:
            effect_label = "negligible"

        supports = self._check_support(mean_a, mean_b, direction, effect_size)

        problem = (f"hypothesis: {hyp_text}; "
                   f"A: mean={mean_a}, std={std_a}, n={n}; "
                   f"B: mean={mean_b}, std={std_b}, n={n}")
        return problem, {
            "hypothesis": hyp_text, "metric": metric,
            "direction": direction,
            "mean_a": mean_a, "std_a": std_a,
            "mean_b": mean_b, "std_b": std_b, "n": n,
            "diff": diff, "pooled_std": pooled_std,
            "effect_size": effect_size, "effect_label": effect_label,
            "supports": supports,
        }

    def _check_support(self, mean_a: float, mean_b: float,
                       direction: str, effect_size: float) -> str:
        """Determine if results support the hypothesis.

        Args:
            mean_a: Mean of group A.
            mean_b: Mean of group B.
            direction: Whether A should be 'lower' or 'higher'.
            effect_size: Cohen's d.

        Returns:
            Conclusion string.
        """
        correct_direction = ((direction == "lower" and mean_a < mean_b) or
                             (direction == "higher" and mean_a > mean_b))
        if not correct_direction:
            return "refutes hypothesis (wrong direction)"
        if effect_size >= 0.5:
            return "supports hypothesis (meaningful effect)"
        if effect_size >= 0.2:
            return "weakly supports hypothesis (small effect)"
        return "inconclusive (negligible effect)"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate interpretation reasoning steps.

        Args:
            data: Solution data with statistics.

        Returns:
            Steps showing computation and conclusion.
        """
        return [
            f"A: mean={data['mean_a']}, std={data['std_a']}, n={data['n']}",
            f"B: mean={data['mean_b']}, std={data['std_b']}, n={data['n']}",
            f"difference={data['diff']}, pooled_std={data['pooled_std']}",
            f"effect_size(Cohen's d)={data['effect_size']} ({data['effect_label']})",
            f"conclusion: {data['supports']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the interpretation conclusion.

        Args:
            data: Solution data.

        Returns:
            Conclusion string.
        """
        return data["supports"]


# ── 4. Algorithm adaptation (tier 9) ───────────────────────────────


@register
class AlgorithmAdaptGenerator(StepGenerator):
    """Adapt an algorithm from problem A to a related problem B.

    Given an algorithm designed for one problem, identifies what must
    change to solve a related but different problem. Keeps the core
    structure but modifies data structures, comparisons, or invariants.

    Input format:
        ``adapt algorithm for problem A to solve problem B``

    Target format:
        ``original: Dijkstra for shortest path <step>
        new problem: longest path in DAG <step>
        change 1: replace min-heap with topological sort <step>
        change 2: replace min with max in relaxation <step>
        keeps: vertex relaxation structure <step>
        adapted algorithm described``

    Difficulty scaling:
        Difficulty 1-3: simple substitution (min->max, +->*).
        Difficulty 4-6: data structure change.
        Difficulty 7-8: invariant modification.

    Prerequisites:
        algorithm_design.
    """

    _ADAPTATIONS = [
        {
            "original": "BFS for shortest path in unweighted graph",
            "new_problem": "shortest path in graph with 0/1 weights",
            "changes": [
                "replace queue with deque (0-1 BFS)",
                "push weight-0 edges to front, weight-1 to back",
            ],
            "keeps": "level-by-level exploration structure",
        },
        {
            "original": "Dijkstra for shortest path",
            "new_problem": "longest path in a DAG",
            "changes": [
                "replace min-heap with topological sort order",
                "replace min relaxation with max relaxation",
                "initialise distances to -infinity instead of +infinity",
            ],
            "keeps": "vertex relaxation framework",
        },
        {
            "original": "binary search for sorted array lookup",
            "new_problem": "find insertion point in sorted array",
            "changes": [
                "on match, continue searching left for first occurrence",
                "return lo instead of mid on termination",
            ],
            "keeps": "halving search space each iteration",
        },
        {
            "original": "merge sort for sorting integers",
            "new_problem": "counting inversions in an array",
            "changes": [
                "during merge, when right element precedes left, count inversions",
                "inversions += len(left) - left_index",
            ],
            "keeps": "divide-conquer-merge structure",
        },
        {
            "original": "DFS for cycle detection in directed graph",
            "new_problem": "topological sort of directed graph",
            "changes": [
                "record finish order during DFS",
                "reverse finish order gives topological order",
            ],
            "keeps": "DFS traversal with visited/in-progress states",
        },
        {
            "original": "Kadane's algorithm for max subarray sum",
            "new_problem": "max subarray product",
            "changes": [
                "track both max and min running product (negative * negative = positive)",
                "swap max/min when current element is negative",
            ],
            "keeps": "single-pass scan with running aggregate",
        },
        {
            "original": "Floyd-Warshall for all-pairs shortest paths",
            "new_problem": "transitive closure of a directed graph",
            "changes": [
                "replace min(d[i][k]+d[k][j], d[i][j]) with OR(d[i][k] AND d[k][j], d[i][j])",
                "initialise matrix with boolean reachability instead of distances",
            ],
            "keeps": "triple nested loop structure over intermediate vertices",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "algorithm_adapt"

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
            difficulty: Controls adaptation complexity.

        Returns:
            Natural language description.
        """
        return "adapt this algorithm for a related problem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an algorithm adaptation problem.

        Args:
            difficulty: Controls pool size.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        pool = self._ADAPTATIONS[:max(2, min(len(self._ADAPTATIONS), 2 + difficulty))]
        adaptation = self._rng.choice(pool)
        problem = (f"original: {adaptation['original']}; "
                   f"new problem: {adaptation['new_problem']}")
        return problem, dict(adaptation)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate adaptation reasoning steps.

        Args:
            data: Solution data with changes and preserved structure.

        Returns:
            Steps showing each change and what is preserved.
        """
        steps = [f"original algorithm: {data['original']}"]
        for i, change in enumerate(data["changes"]):
            steps.append(f"change {i + 1}: {change}")
        steps.append(f"preserved: {data['keeps']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return a summary of the adaptation.

        Args:
            data: Solution data.

        Returns:
            Summary of changes.
        """
        changes_str = "; ".join(data["changes"])
        return f"adapt by: {changes_str}"


# ── 5. Complexity lower bound argument (tier 9) ───────────────────


@register
class ComplexityLowerBoundGenerator(StepGenerator):
    """Argue why a problem cannot be solved faster than a stated bound.

    Uses information-theoretic or adversary arguments to establish lower
    bounds on computational problems. Template-based with randomised
    problem parameters.

    Input format:
        ``argue lower bound for this problem``

    Target format:
        ``problem: find minimum in unsorted array of n elements <step>
        argument: adversary can hide minimum in any of n positions <step>
        each comparison eliminates at most 1 candidate <step>
        need at least n-1 comparisons <step> Omega(n)``

    Difficulty scaling:
        Difficulty 1-3: counting arguments (n-1 for minimum).
        Difficulty 4-6: information-theoretic (log2 for search).
        Difficulty 7-8: adversary arguments.

    Prerequisites:
        complexity_comparison.
    """

    _BOUNDS = [
        {
            "problem": "find minimum in unsorted array of n={n} elements",
            "argument": "adversary can hide minimum in any of {n} positions",
            "reasoning": "each comparison eliminates at most 1 candidate",
            "bound": "n-1 = {nm1} comparisons",
            "complexity": "Omega(n)",
            "compute": lambda n: {"n": n, "nm1": n - 1},
        },
        {
            "problem": "find both min and max in array of n={n} elements",
            "argument": "need n-1 comparisons for min, but can share information",
            "reasoning": "tournament method: ceil(3n/2) - 2 comparisons suffice and are necessary",
            "bound": "ceil(3*{n}/2) - 2 = {result} comparisons",
            "complexity": "Omega(n)",
            "compute": lambda n: {"n": n, "result": -(-3 * n // 2) - 2},
        },
        {
            "problem": "determine if element exists in sorted array of n={n}",
            "argument": "each comparison splits remaining candidates in half",
            "reasoning": "decision tree has n+1 leaves (n positions + not found)",
            "bound": "ceil(log2({np1})) = {result} comparisons",
            "complexity": "Omega(log n)",
            "compute": lambda n: {"n": n, "np1": n + 1,
                                   "result": (n + 1 - 1).bit_length()},
        },
        {
            "problem": "merge two sorted arrays of n={n} elements each",
            "argument": "output has C(2n,n) possible orderings",
            "reasoning": "each comparison determines one relative order",
            "bound": "at least 2*{n} - 1 = {result} comparisons",
            "complexity": "Omega(n)",
            "compute": lambda n: {"n": n, "result": 2 * n - 1},
        },
        {
            "problem": "compute the median of n={n} unsorted elements",
            "argument": "must examine every element at least once",
            "reasoning": "any unexamined element could be the median",
            "bound": "at least {n} comparisons",
            "complexity": "Omega(n)",
            "compute": lambda n: {"n": n},
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "complexity_lower_bound"

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
            difficulty: Controls bound complexity.

        Returns:
            Natural language description.
        """
        return "argue why this problem has the stated lower bound"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a lower bound argument problem.

        Args:
            difficulty: Controls pool size and n.

        Returns:
            Tuple of (problem_statement, solution_data).
        """
        pool = self._BOUNDS[:max(2, min(len(self._BOUNDS), 1 + difficulty))]
        template = self._rng.choice(pool)
        n = self._rng.randint(8, 64 + difficulty * 32)
        computed = template["compute"](n)

        problem_text = template["problem"].format(**computed)
        argument = template["argument"].format(**computed)
        reasoning = template["reasoning"]
        bound_text = template["bound"].format(**computed)
        complexity = template["complexity"]

        problem = f"lower bound: {problem_text}"
        return problem, {
            "problem_text": problem_text,
            "argument": argument,
            "reasoning": reasoning,
            "bound": bound_text,
            "complexity": complexity,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate lower bound argument steps.

        Args:
            data: Solution data with argument chain.

        Returns:
            Steps showing the argument.
        """
        return [
            f"argument: {data['argument']}",
            f"reasoning: {data['reasoning']}",
            f"bound: {data['bound']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the complexity lower bound.

        Args:
            data: Solution data.

        Returns:
            Complexity string.
        """
        return data["complexity"]


# ── 6. Proof generalisation (tier 9) ──────────────────────────────


@register
class ProofGeneralizeGenerator(StepGenerator):
    """Generalise a proof from a specific case to arbitrary n.

    Given a proof that works for a specific value (n=3, n=4, etc.),
    identifies what must change to make it work for general n.
    Template-based with randomised specific cases.

    Input format:
        ``generalise this proof from n=k to arbitrary n``

    Target format:
        ``specific proof: sum of first 3 odd numbers = 3^2 <step>
        1+3+5 = 9 = 3^2 <step>
        pattern: sum of first n odd numbers = n^2 <step>
        generalisation: replace 3 with n, use induction <step>
        base case: n=1, sum=1=1^2 <step>
        inductive step: assume sum_k = k^2, then sum_{k+1} =
        k^2 + (2k+1) = (k+1)^2``

    Difficulty scaling:
        Difficulty 1-3: arithmetic sums.
        Difficulty 4-6: combinatorial identities.
        Difficulty 7-8: algebraic structure proofs.

    Prerequisites:
        verify_proof.
    """

    _PROOFS = [
        {
            "specific": "sum of first {k} odd numbers = {k}^2",
            "values": lambda k: {"k": k, "sum_val": k ** 2,
                                  "terms": "+".join(str(2 * i - 1) for i in range(1, k + 1))},
            "pattern": "sum of first n odd numbers = n^2",
            "base": "n=1: 1 = 1^2",
            "inductive": "assume sum_k = k^2; sum_{k+1} = k^2 + (2k+1) = (k+1)^2",
            "method": "induction",
        },
        {
            "specific": "sum 1+2+...+{k} = {k}({k}+1)/2",
            "values": lambda k: {"k": k, "sum_val": k * (k + 1) // 2,
                                  "terms": "+".join(str(i) for i in range(1, k + 1))},
            "pattern": "sum 1+2+...+n = n(n+1)/2",
            "base": "n=1: 1 = 1*2/2 = 1",
            "inductive": "assume sum_k = k(k+1)/2; sum_{k+1} = k(k+1)/2 + (k+1) = (k+1)(k+2)/2",
            "method": "induction",
        },
        {
            "specific": "2^{k} > {k} for k={k}",
            "values": lambda k: {"k": k, "pow_val": 2 ** k},
            "pattern": "2^n > n for all n >= 1",
            "base": "n=1: 2 > 1",
            "inductive": "assume 2^k > k; then 2^{k+1} = 2*2^k > 2k >= k+1 for k >= 1",
            "method": "induction",
        },
        {
            "specific": "number of subsets of {{1,...,{k}}} = 2^{k} = {pow_val}",
            "values": lambda k: {"k": k, "pow_val": 2 ** k},
            "pattern": "|P({1,...,n})| = 2^n",
            "base": "n=0: P(empty) = {empty}, |P| = 1 = 2^0",
            "inductive": "assume |P({1,...,k})| = 2^k; adding element k+1 doubles subsets: 2*2^k = 2^{k+1}",
            "method": "induction",
        },
        {
            "specific": "n^3 - n divisible by 6 for n={k}: {k}^3-{k} = {val}",
            "values": lambda k: {"k": k, "val": k ** 3 - k},
            "pattern": "n^3 - n is divisible by 6 for all n >= 1",
            "base": "n=1: 1-1 = 0, divisible by 6",
            "inductive": "n^3-n = n(n-1)(n+1), product of 3 consecutive integers, always divisible by 6",
            "method": "direct factoring",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "proof_generalize"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["verify_proof"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls proof complexity.

        Returns:
            Natural language description.
        """
        return "generalise this specific-case proof to arbitrary n"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof generalisation problem.

        Args:
            difficulty: Controls pool and specific k.

        Returns:
            Tuple of (specific_proof_statement, solution_data).
        """
        pool = self._PROOFS[:max(2, min(len(self._PROOFS), 1 + difficulty))]
        template = self._rng.choice(pool)
        k = self._rng.randint(3, 6 + difficulty)
        vals = template["values"](k)
        specific_text = template["specific"].format(**vals)

        problem = f"specific case: {specific_text}"
        return problem, {
            "specific": specific_text,
            "vals": vals,
            "pattern": template["pattern"],
            "base": template["base"],
            "inductive": template["inductive"],
            "method": template["method"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proof generalisation steps.

        Args:
            data: Solution data with pattern and induction steps.

        Returns:
            Steps showing pattern identification and generalisation.
        """
        return [
            f"verified: {data['specific']}",
            f"pattern: {data['pattern']}",
            f"method: {data['method']}",
            f"base case: {data['base']}",
            f"general step: {data['inductive']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the general pattern.

        Args:
            data: Solution data.

        Returns:
            General pattern string.
        """
        return data["pattern"]


# ── 7. Abstraction identification (tier 9) ────────────────────────


@register
class AbstractionIdentifyGenerator(StepGenerator):
    """Identify a common abstraction shared by two different problems.

    Given descriptions of two seemingly different problems, identifies
    the underlying mathematical structure they share (e.g., both reduce
    to shortest path, both are fixed-point iterations).

    Input format:
        ``what abstraction do these two problems share``

    Target format:
        ``problem 1: routing packets in a network <step>
        problem 2: finding cheapest flight with connections <step>
        shared structure: both are shortest path in weighted graph <step>
        abstraction: weighted digraph with additive edge costs``

    Difficulty scaling:
        Difficulty 1-3: obvious shared structure.
        Difficulty 4-6: requires domain translation.
        Difficulty 7-8: deep structural similarity.

    Prerequisites:
        method_selection.
    """

    _PAIRS = [
        {
            "problem_1": "routing packets in a network with latency costs",
            "problem_2": "finding cheapest flight itinerary with connections",
            "abstraction": "shortest path in weighted digraph",
            "explanation": "both minimise total additive cost along a path in a directed graph",
        },
        {
            "problem_1": "scheduling jobs on machines to minimise total time",
            "problem_2": "assigning students to project groups to maximise satisfaction",
            "abstraction": "bipartite matching / assignment problem",
            "explanation": "both optimise a sum over a bijective assignment between two sets",
        },
        {
            "problem_1": "finding connected components in a social network",
            "problem_2": "determining equivalence classes from a relation",
            "abstraction": "union-find / equivalence relation partitioning",
            "explanation": "both partition elements into disjoint groups based on transitive closure",
        },
        {
            "problem_1": "training a neural network to convergence",
            "problem_2": "solving a system of equations by iterative refinement",
            "abstraction": "fixed-point iteration",
            "explanation": "both apply a contraction mapping repeatedly until the state stabilises",
        },
        {
            "problem_1": "parsing a nested expression with parentheses",
            "problem_2": "evaluating a recursive function call tree",
            "abstraction": "tree traversal / stack-based recursion",
            "explanation": "both process hierarchical structure using a stack (explicit or implicit)",
        },
        {
            "problem_1": "image segmentation by pixel similarity",
            "problem_2": "market segmentation by customer features",
            "abstraction": "clustering in metric space",
            "explanation": "both partition points in a feature space to minimise intra-cluster distance",
        },
        {
            "problem_1": "reservoir sampling from a data stream",
            "problem_2": "selecting jury members fairly from a population",
            "abstraction": "uniform random sampling without replacement",
            "explanation": "both select k items from n with equal probability for each subset",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "abstraction_identify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls abstraction depth.

        Returns:
            Natural language description.
        """
        return "identify the common abstraction in these two problems"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an abstraction identification problem.

        Args:
            difficulty: Controls pair pool.

        Returns:
            Tuple of (two_problem_descriptions, solution_data).
        """
        pool = self._PAIRS[:max(2, min(len(self._PAIRS), 2 + difficulty))]
        pair = self._rng.choice(pool)
        problem = (f"problem 1: {pair['problem_1']}; "
                   f"problem 2: {pair['problem_2']}")
        return problem, dict(pair)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate abstraction identification steps.

        Args:
            data: Solution data with problems and shared abstraction.

        Returns:
            Steps showing analysis and identification.
        """
        return [
            f"problem 1: {data['problem_1']}",
            f"problem 2: {data['problem_2']}",
            f"shared structure: {data['abstraction']}",
            f"why: {data['explanation']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the identified abstraction.

        Args:
            data: Solution data.

        Returns:
            Abstraction name.
        """
        return data["abstraction"]


# ── 8. Failure prediction (tier 9) ────────────────────────────────


@register
class FailurePredictGenerator(StepGenerator):
    """Predict whether an algorithm will fail on a given edge case.

    Given an algorithm description and an edge case, determines whether
    the algorithm handles it correctly. Identifies the failure mechanism
    or confirms correctness with reasoning.

    Input format:
        ``will this algorithm fail on this edge case``

    Target format:
        ``algorithm: quicksort with fixed pivot = first element <step>
        edge case: already sorted array of n=1000 <step>
        analysis: pivot is always minimum, partition is maximally
        unbalanced <step> consequence: O(n^2) instead of O(n log n)
        <step> prediction: fails (quadratic degradation)``

    Difficulty scaling:
        Difficulty 1-3: obvious failure modes.
        Difficulty 4-6: subtle boundary cases.
        Difficulty 7-8: interaction of multiple factors.

    Prerequisites:
        algorithm_design.
    """

    _CASES = [
        {
            "algorithm": "quicksort with pivot = first element",
            "edge_case": "already sorted array of n=1000",
            "analysis": "pivot is always minimum, partition is maximally unbalanced",
            "consequence": "O(n^2) instead of O(n log n), stack depth = n",
            "fails": True,
            "prediction": "fails (quadratic degradation on sorted input)",
        },
        {
            "algorithm": "binary search returning first match",
            "edge_case": "array with all elements equal, searching for that value",
            "analysis": "finds middle element, but first occurrence is at index 0",
            "consequence": "returns wrong index (middle instead of first)",
            "fails": True,
            "prediction": "fails (returns arbitrary match, not leftmost)",
        },
        {
            "algorithm": "hash table with linear probing",
            "edge_case": "load factor > 0.9, keys clustering",
            "analysis": "primary clustering: consecutive occupied slots grow into long runs",
            "consequence": "average probe length degrades from O(1) to O(n)",
            "fails": True,
            "prediction": "fails (performance degrades to linear scan)",
        },
        {
            "algorithm": "Dijkstra's algorithm with standard priority queue",
            "edge_case": "graph with negative edge weights",
            "analysis": "greedy choice assumes no shorter path exists via unvisited nodes",
            "consequence": "negative edge can create shorter path through already-visited node",
            "fails": True,
            "prediction": "fails (produces incorrect shortest paths)",
        },
        {
            "algorithm": "merge sort on linked list",
            "edge_case": "list with single element",
            "analysis": "base case: list of length 1 is already sorted",
            "consequence": "returns the single element list unchanged",
            "fails": False,
            "prediction": "handles correctly (base case returns input unchanged)",
        },
        {
            "algorithm": "BFS for shortest path in unweighted graph",
            "edge_case": "disconnected graph, target in unreachable component",
            "analysis": "BFS explores all reachable vertices, never finds target",
            "consequence": "returns no path / infinity distance",
            "fails": False,
            "prediction": "handles correctly if implementation checks for unreachable target",
        },
        {
            "algorithm": "gradient descent with fixed learning rate 0.1",
            "edge_case": "loss function with condition number 10000",
            "analysis": "step size must be < 2/L for convergence, L is largest eigenvalue",
            "consequence": "oscillates or diverges along high-curvature direction",
            "fails": True,
            "prediction": "fails (diverges due to learning rate exceeding stability bound)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "failure_predict"

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
            difficulty: Controls case complexity.

        Returns:
            Natural language description.
        """
        return "predict whether this algorithm fails on the given edge case"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a failure prediction problem.

        Args:
            difficulty: Controls pool size.

        Returns:
            Tuple of (algorithm_and_edge_case, solution_data).
        """
        pool = self._CASES[:max(3, min(len(self._CASES), 2 + difficulty))]
        case = self._rng.choice(pool)
        problem = (f"algorithm: {case['algorithm']}; "
                   f"edge case: {case['edge_case']}")
        return problem, dict(case)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate failure prediction reasoning steps.

        Args:
            data: Solution data with analysis.

        Returns:
            Steps showing analysis and prediction.
        """
        return [
            f"algorithm: {data['algorithm']}",
            f"edge case: {data['edge_case']}",
            f"analysis: {data['analysis']}",
            f"consequence: {data['consequence']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the failure prediction.

        Args:
            data: Solution data.

        Returns:
            Prediction string.
        """
        return data["prediction"]
