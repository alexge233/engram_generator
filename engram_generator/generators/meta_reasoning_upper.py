"""Expanded generators for upper tiers 7-10.

Adds 9 more generators to bring the total to 247.
"""
from engram_generator.base import StepGenerator, STEP_TOKEN
from engram_generator.curriculum.registry import register


# ── TIER 7 (15 → 18) ───────────────────────────────────────────────

@register
class VerifyProofGenerator(StepGenerator):
    """Verify if a given proof step is valid or contains an error."""

    @property
    def task_name(self) -> str:
        return "verify_proof"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["proof_by_induction", "error_detection"]

    def task_description(self, difficulty: int) -> str:
        return "verify proof step"

    _PROOF_TEMPLATES = [
        {
            "claim_tpl": "{a}*n^2 > {b}*n for n >= {base}",
            "steps_tpl": [
                "base: {a}*{base}^2={a_base_sq} > {b_base}={b}*{base}",
                "assume {a}*k^2 > {b}*k",
                "{a}*(k+1)^2 = {a}*k^2+{c}*k+{a} > {b}*k+{c}*k+{a} > {b}*(k+1)",
            ],
            "valid": True,
            "reason": "all steps follow by induction",
            "gen": "_gen_quad_bound",
        },
        {
            "claim_tpl": "sum 1..n = n(n+1)/{d}",
            "steps_tpl": [
                "base: 1 = 1*2/{d}",
                "assume sum 1..k = k(k+1)/{d}",
                "sum 1..k+1 = k(k+1)/{d} + k+1 = (k+1)(k+2)/{d}",
            ],
            "valid_when_d_eq_2": True,
            "reason_true": "correct induction",
            "reason_false": "formula uses wrong denominator; correct is n(n+1)/2",
            "gen": "_gen_sum_formula",
        },
        {
            "claim_tpl": "all horses are the same colour",
            "steps_tpl": [
                "base: 1 horse trivially same colour",
                "assume any k horses same colour",
                "for k+1: first k same colour, last k same colour, overlap => all same",
            ],
            "valid": False,
            "reason": "overlap is empty when k=1, induction step fails",
            "gen": None,
        },
        {
            "claim_tpl": "n! > {a}^n for n >= {base}",
            "steps_tpl": [
                "base: {base}!={base_fact} > {a_pow_base}={a}^{base}",
                "assume k! > {a}^k",
                "(k+1)! = (k+1)*k! > (k+1)*{a}^k > {a}*{a}^k = {a}^{{k+1}} since k+1>={a}",
            ],
            "valid": True,
            "reason": "induction step valid for k>={base}",
            "gen": "_gen_factorial_bound",
        },
        {
            "claim_tpl": "sum of first n odd numbers = n^{p}",
            "steps_tpl": [
                "base: 1 = 1^{p}",
                "assume 1+3+...+(2k-1) = k^{p}",
                "add (2k+1): k^{p} + 2k+1 should equal (k+1)^{p}",
            ],
            "valid_when_p_eq_2": True,
            "reason_true": "algebraic identity (k+1)^2 = k^2+2k+1 holds",
            "reason_false": "identity only holds for p=2, not p={p}",
            "gen": "_gen_odd_sum",
        },
        {
            "claim_tpl": "every natural number > 1 is divisible by a prime",
            "steps_tpl": [
                "base: {base_prime} is prime, divides itself",
                "assume true for all 2..k-1",
                "if k is prime, done; if k=ab with a,b<k, then a has a prime factor",
            ],
            "valid": True,
            "reason": "strong induction, correct",
            "gen": "_gen_prime_div",
        },
        {
            "claim_tpl": "sqrt({n}) is irrational",
            "steps_tpl": [
                "assume sqrt({n}) = a/b in lowest terms",
                "{n}*b^2 = a^2, so {n} divides a^2",
            ],
            "valid_depends": True,
            "gen": "_gen_sqrt_irrat",
        },
        {
            "claim_tpl": "if a|bc and gcd(a,b)=1 then a|c",
            "steps_tpl": [
                "gcd(a,b)=1 means ax+by=1 for integers x,y (Bezout)",
                "multiply by c: acx+bcy=c",
                "a divides acx trivially, a divides bcy since a|bc, so a|c",
            ],
            "valid": True,
            "reason": "Bezout's identity correctly applied",
            "gen": "_gen_bezout",
        },
        {
            "claim_tpl": "d/dx(x^{n}) = {n}x^{nm1} for all n >= 1",
            "steps_tpl": [
                "base: d/dx(x) = 1 = 1*x^0",
                "assume d/dx(x^k) = kx^{{k-1}}",
                "d/dx(x^{{k+1}}) = d/dx(x*x^k) = x^k + x*kx^{{k-1}} = (k+1)x^k",
            ],
            "valid": True,
            "reason": "product rule and induction correct",
            "gen": "_gen_derivative",
        },
        {
            "claim_tpl": "{a}^n < n! for all n >= 1",
            "steps_tpl": [
                "base: {a}^1={a} < 1!=1... wait, {a} > 1",
                "base case fails",
            ],
            "valid": False,
            "reason": "base case is false: {a}^1={a} > 1!=1",
            "gen": "_gen_false_exp_fact",
        },
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        template = self._rng.choice(self._PROOF_TEMPLATES)
        gen_method = template.get("gen")
        if gen_method and hasattr(self, gen_method):
            proof = getattr(self, gen_method)(template, difficulty)
        else:
            proof = self._default_proof(template)
        step_str = "; ".join(proof["steps"])
        problem = f"claim: {proof['claim']}; proof: {step_str}"
        return problem, proof

    def _default_proof(self, template: dict) -> dict:
        """Build a proof dict from a template with no numeric variation."""
        return {
            "claim": template["claim_tpl"],
            "steps": template["steps_tpl"],
            "valid": template.get("valid", False),
            "reason": template.get("reason", "see analysis"),
        }

    def _gen_quad_bound(self, tpl: dict, difficulty: int) -> dict:
        """Generate a quadratic bound proof with random coefficients."""
        a = self._rng.randint(1, 3 + difficulty)
        b = self._rng.randint(1, 2 * a)
        base = self._rng.randint(2, 4)
        c = 2 * a
        claim = tpl["claim_tpl"].format(a=a, b=b, base=base)
        steps = [
            s.format(a=a, b=b, base=base, a_base_sq=a * base * base,
                     b_base=b * base, c=c)
            for s in tpl["steps_tpl"]
        ]
        return {"claim": claim, "steps": steps,
                "valid": True, "reason": tpl["reason"]}

    def _gen_sum_formula(self, tpl: dict, difficulty: int) -> dict:
        """Generate a sum formula proof, sometimes with wrong denominator."""
        d = self._rng.choice([2, 2, 2, 3, 4])
        valid = (d == 2)
        claim = tpl["claim_tpl"].format(d=d)
        steps = [s.format(d=d) for s in tpl["steps_tpl"]]
        reason = tpl["reason_true"] if valid else tpl["reason_false"]
        return {"claim": claim, "steps": steps,
                "valid": valid, "reason": reason}

    def _gen_factorial_bound(self, tpl: dict, difficulty: int) -> dict:
        """Generate factorial vs exponential bound proof."""
        a = self._rng.choice([2, 2, 3])
        base = self._rng.randint(max(a + 1, 3), max(a + 1, 3) + difficulty)
        import math
        base_fact = math.factorial(base)
        a_pow_base = a ** base
        valid = (base_fact > a_pow_base)
        claim = tpl["claim_tpl"].format(a=a, base=base)
        steps = [s.format(a=a, base=base, base_fact=base_fact,
                          a_pow_base=a_pow_base) for s in tpl["steps_tpl"]]
        reason = tpl["reason"].format(base=base) if valid else f"base case fails: {base}!={base_fact} <= {a}^{base}={a_pow_base}"
        return {"claim": claim, "steps": steps,
                "valid": valid, "reason": reason}

    def _gen_odd_sum(self, tpl: dict, difficulty: int) -> dict:
        """Generate odd sum proof, sometimes with wrong exponent."""
        p = self._rng.choice([2, 2, 2, 3])
        valid = (p == 2)
        claim = tpl["claim_tpl"].format(p=p)
        steps = [s.format(p=p) for s in tpl["steps_tpl"]]
        reason = tpl["reason_true"] if valid else tpl["reason_false"].format(p=p)
        return {"claim": claim, "steps": steps,
                "valid": valid, "reason": reason}

    def _gen_prime_div(self, tpl: dict, difficulty: int) -> dict:
        """Generate prime divisibility proof with random base prime."""
        base_prime = self._rng.choice([2, 3, 5, 7])
        claim = tpl["claim_tpl"]
        steps = [s.format(base_prime=base_prime) for s in tpl["steps_tpl"]]
        return {"claim": claim, "steps": steps,
                "valid": True, "reason": tpl["reason"]}

    def _gen_sqrt_irrat(self, tpl: dict, difficulty: int) -> dict:
        """Generate sqrt irrationality claim for random n."""
        perfect_squares = {1, 4, 9, 16, 25, 36, 49}
        n = self._rng.randint(2, 15 + difficulty * 3)
        valid = n not in perfect_squares
        claim = tpl["claim_tpl"].format(n=n)
        steps = [s.format(n=n) for s in tpl["steps_tpl"]]
        if valid:
            reason = f"sqrt({n}) is indeed irrational; proof by contradiction is correct"
        else:
            import math
            root = int(math.isqrt(n))
            reason = f"fails: sqrt({n})={root} is rational (perfect square)"
        return {"claim": claim, "steps": steps,
                "valid": valid, "reason": reason}

    def _gen_bezout(self, tpl: dict, difficulty: int) -> dict:
        """Generate Bezout identity proof with example values."""
        a_val = self._rng.choice([3, 5, 7, 11, 13])
        b_val = self._rng.choice([2, 4, 6, 8, 10])
        claim = f"if a|bc and gcd(a,b)=1 then a|c (e.g. a={a_val},b={b_val})"
        steps = list(tpl["steps_tpl"])
        steps.append(f"example: a={a_val}, b={b_val}, verified")
        return {"claim": claim, "steps": steps,
                "valid": True, "reason": tpl["reason"]}

    def _gen_derivative(self, tpl: dict, difficulty: int) -> dict:
        """Generate derivative proof for x^n with random n."""
        n = self._rng.randint(2, 6 + difficulty)
        claim = tpl["claim_tpl"].format(n=n, nm1=n - 1)
        steps = [s.format(n=n, nm1=n - 1) for s in tpl["steps_tpl"]]
        return {"claim": claim, "steps": steps,
                "valid": True, "reason": tpl["reason"]}

    def _gen_false_exp_fact(self, tpl: dict, difficulty: int) -> dict:
        """Generate a false exponential < factorial claim."""
        a = self._rng.randint(2, 4 + difficulty)
        claim = tpl["claim_tpl"].format(a=a)
        steps = [s.format(a=a) for s in tpl["steps_tpl"]]
        reason = tpl["reason"].format(a=a)
        return {"claim": claim, "steps": steps,
                "valid": False, "reason": reason}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"check: {s}" for s in sd["steps"]]

    def _create_answer(self, sd: dict) -> str:
        status = "VALID" if sd["valid"] else "INVALID"
        return f"{status}: {sd['reason']}"


@register
class DimensionalAnalysisGenerator(StepGenerator):
    """Check dimensional consistency of a physics formula."""

    @property
    def task_name(self) -> str:
        return "dimensional_analysis"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        return "check dimensional consistency"

    _FORMULA_TEMPLATES = [
        {"formula": "v = d/t", "lhs": "m/s", "rhs": "m/s", "consistent": True},
        {"formula": "F = ma", "lhs": "kg*m/s^2", "rhs": "kg*m/s^2", "consistent": True},
        {"formula": "E = mc^2", "lhs": "kg*m^2/s^2", "rhs": "kg*(m/s)^2", "consistent": True},
        {"formula": "v = d*t", "lhs": "m/s", "rhs": "m*s", "consistent": False},
        {"formula": "F = m/a", "lhs": "kg*m/s^2", "rhs": "kg/(m/s^2)", "consistent": False},
        {"formula": "P = F*v", "lhs": "kg*m^2/s^3", "rhs": "kg*m/s^2*m/s", "consistent": True},
        {"formula": "W = F*d", "lhs": "kg*m^2/s^2", "rhs": "kg*m/s^2*m", "consistent": True},
        {"formula": "p = mv", "lhs": "kg*m/s", "rhs": "kg*m/s", "consistent": True},
        {"formula": "KE = mv^2", "lhs": "kg*m^2/s^2", "rhs": "kg*(m/s)^2", "consistent": False},
        {"formula": "T = 2*pi*sqrt(L/g)", "lhs": "s", "rhs": "sqrt(m/(m/s^2))=s", "consistent": True},
        {"formula": "PV = nRT", "lhs": "Pa*m^3", "rhs": "mol*(J/(mol*K))*K=J", "consistent": True},
        {"formula": "F = G*m1*m2/r", "lhs": "N", "rhs": "N*m (missing /r)", "consistent": False},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        f = self._rng.choice(self._FORMULA_TEMPLATES)
        coeff = self._rng.randint(1, 9 + difficulty)
        var_label = self._rng.choice(["x", "y", "z", "q", "w", "r", "s"])
        prefix = self._rng.choice(["", f"({coeff}) * ", f"scale={coeff}: "])
        problem = (
            f"is {prefix}{f['formula']} dimensionally consistent? "
            f"LHS=[{f['lhs']}] RHS=[{f['rhs']}] (var={var_label}, k={coeff})"
        )
        data = dict(f)
        data["coeff"] = coeff
        data["var_label"] = var_label
        return problem, data

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"LHS: {sd['lhs']}", f"RHS: {sd['rhs']}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["consistent"] else "NO"


@register
class SymmetryDetectionGenerator(StepGenerator):
    """Detect if a function or expression has a symmetry property."""

    @property
    def task_name(self) -> str:
        return "symmetry_detection"

    @property
    def tier(self) -> int:
        return 7

    @property
    def prerequisites(self) -> list[str]:
        return ["polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        return "detect symmetry"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        sym_type = self._rng.choice(["even", "odd", "neither"])

        if sym_type == "even":
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^2 + {b}"
            reason = "f(-x) = f(x)"
        elif sym_type == "odd":
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^3 + {b}x"
            reason = "f(-x) = -f(x)"
        else:
            a = self._rng.randint(1, 5)
            b = self._rng.randint(1, 5)
            c = self._rng.randint(1, 5)
            func = f"f(x) = {a}x^3 + {b}x^2 + {c}"
            reason = "f(-x) != f(x) and f(-x) != -f(x)"

        problem = f"classify symmetry: {func}"
        return problem, {"func": func, "type": sym_type, "reason": reason}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"compute f(-x)", sd["reason"]]

    def _create_answer(self, sd: dict) -> str:
        return sd["type"]


# ── TIER 8 (11 → 13) ───────────────────────────────────────────────

@register
class AbstractionLevelGenerator(StepGenerator):
    """Given a concrete problem, identify the abstract pattern."""

    @property
    def task_name(self) -> str:
        return "abstraction_level"

    @property
    def tier(self) -> int:
        return 8

    @property
    def prerequisites(self) -> list[str]:
        return ["isomorphism_detection"]

    def task_description(self, difficulty: int) -> str:
        return "identify abstract pattern"

    _PATTERN_TEMPLATES = [
        {"concrete_tpl": "find shortest route between cities {c1} and {c2} through {n} waypoints",
         "abstract": "shortest path in weighted graph", "category": "graph_traversal"},
        {"concrete_tpl": "maximise profit given weight limit {w}kg and {n} items with different values",
         "abstract": "0/1 knapsack optimisation", "category": "dynamic_programming"},
        {"concrete_tpl": "find if a {n}-letter word can be built from {m} magazine letter cutouts",
         "abstract": "multiset subset check", "category": "counting"},
        {"concrete_tpl": "schedule {n} non-overlapping meetings to maximise attendance",
         "abstract": "interval scheduling maximisation", "category": "greedy"},
        {"concrete_tpl": "find the minimum number of coins to make change for amount {n}",
         "abstract": "minimum coin change (unbounded knapsack)", "category": "dynamic_programming"},
        {"concrete_tpl": "assign {n} tasks to {m} workers minimising total cost",
         "abstract": "assignment problem (bipartite matching)", "category": "graph_matching"},
        {"concrete_tpl": "determine if a {n}-piece jigsaw puzzle can be completed",
         "abstract": "exact cover / constraint satisfaction", "category": "backtracking"},
        {"concrete_tpl": "rank {n} web pages by importance based on link structure",
         "abstract": "eigenvector centrality (PageRank)", "category": "linear_algebra"},
        {"concrete_tpl": "find the longest common subsequence of two strings of length {n} and {m}",
         "abstract": "longest common subsequence", "category": "dynamic_programming"},
        {"concrete_tpl": "detect whether a social network of {n} people has two opposing factions",
         "abstract": "bipartite graph check (2-coloring)", "category": "graph_theory"},
        {"concrete_tpl": "compress a {n}KB file by finding repeated patterns",
         "abstract": "dictionary-based compression (LZ77/LZW)", "category": "information_theory"},
        {"concrete_tpl": "predict weather {n} days ahead using historical transition data from {m} states",
         "abstract": "Markov chain state prediction", "category": "stochastic_process"},
    ]

    _CITY_NAMES = ["Alpha", "Bravo", "Cedar", "Delta", "Echo", "Foxtrot",
                   "Gamma", "Haven", "Iris", "Jade", "Kilo", "Lima"]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._PATTERN_TEMPLATES)
        n = self._rng.randint(3, 8 + difficulty * 2)
        m = self._rng.randint(2, 6 + difficulty)
        w = self._rng.randint(10, 50 + difficulty * 10)
        c1, c2 = self._rng.sample(self._CITY_NAMES, 2)
        concrete = tpl["concrete_tpl"].format(n=n, m=m, w=w, c1=c1, c2=c2)
        p = {"concrete": concrete, "abstract": tpl["abstract"],
             "category": tpl["category"]}
        problem = f"abstractify: {p['concrete']}"
        return problem, p

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"concrete: {sd['concrete']}",
            f"pattern: {sd['abstract']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['abstract']} ({sd['category']})"


@register
class DualProblemGenerator(StepGenerator):
    """Given a problem, state its dual."""

    @property
    def task_name(self) -> str:
        return "dual_problem"

    @property
    def tier(self) -> int:
        return 8

    @property
    def prerequisites(self) -> list[str]:
        return ["problem_transformation"]

    def task_description(self, difficulty: int) -> str:
        return "state the dual problem"

    _DUAL_TEMPLATES = [
        {"primal_tpl": "find minimum spanning tree for {n} nodes and {m} edges",
         "dual": "find maximum weight cut", "domain": "graph theory"},
        {"primal_tpl": "minimise cost of {n} variables subject to {m} constraints",
         "dual": "maximise lower bound from constraints", "domain": "linear programming"},
        {"primal_tpl": "find shortest path in network with {n} nodes",
         "dual": "find maximum flow (by max-flow min-cut)", "domain": "network flow"},
        {"primal_tpl": "maximise entropy of a distribution over {n} outcomes",
         "dual": "minimise KL divergence from uniform", "domain": "information theory"},
        {"primal_tpl": "find minimum vertex cover in graph with {n} vertices",
         "dual": "find maximum independent set", "domain": "graph theory"},
        {"primal_tpl": "minimise error on {n} training samples with {m} features",
         "dual": "maximise margin (SVM)", "domain": "machine learning"},
        {"primal_tpl": "find shortest tour visiting {n} cities",
         "dual": "find lower bound via LP relaxation", "domain": "combinatorial optimisation"},
        {"primal_tpl": "maximise likelihood over {n} observations",
         "dual": "minimise cross-entropy", "domain": "statistics"},
        {"primal_tpl": "find minimum cut in flow network with {n} nodes",
         "dual": "find maximum flow", "domain": "network flow"},
        {"primal_tpl": "compress {n}KB of data (minimise bits)",
         "dual": "maximise information preserved", "domain": "information theory"},
        {"primal_tpl": "find densest subgraph among {n} vertices",
         "dual": "find sparsest cut", "domain": "graph theory"},
        {"primal_tpl": "minimise total weighted completion time for {n} jobs on {m} machines",
         "dual": "maximise schedule efficiency", "domain": "scheduling"},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._DUAL_TEMPLATES)
        n = self._rng.randint(4, 15 + difficulty * 5)
        m = self._rng.randint(2, 8 + difficulty * 2)
        primal = tpl["primal_tpl"].format(n=n, m=m)
        d = {"primal": primal, "dual": tpl["dual"], "domain": tpl["domain"]}
        problem = f"dual of: {d['primal']}"
        return problem, d

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"domain: {sd['domain']}", f"primal: {sd['primal']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["dual"]


# ── TIER 9 (11 → 13) ───────────────────────────────────────────────

@register
class InformationBottleneckGenerator(StepGenerator):
    """Identify what information a compression step loses."""

    @property
    def task_name(self) -> str:
        return "information_bottleneck"

    @property
    def tier(self) -> int:
        return 9

    @property
    def prerequisites(self) -> list[str]:
        return ["info_entropy", "complexity_comparison"]

    def task_description(self, difficulty: int) -> str:
        return "analyse information bottleneck"

    _SCENARIO_TEMPLATES = [
        {"op_tpl": "mean pooling a sequence of {n} embeddings of dim {d}",
         "preserves": "average magnitude and direction",
         "loses": "positional order, individual token identity"},
        {"op_tpl": "PCA reducing {d_in}D to {d_out}D",
         "preserves_tpl": "top {d_out} variance components",
         "loses_tpl": "{d_lost} minor variance directions, possible nonlinear structure"},
        {"op_tpl": "quantising {dtype_from} weights to {dtype_to}",
         "preserves": "approximate magnitude and sign",
         "loses": "precision within quantisation bins, outlier fidelity"},
        {"op_tpl": "hashing a string to {bits} bits",
         "preserves_tpl": "identity (collision probability ~1/2^{bits})",
         "loses": "content, length, structure, reversibility"},
        {"op_tpl": "max pooling a {h}x{w} feature map with stride {stride}",
         "preserves": "strongest activation in each region",
         "loses": "spatial precision, weaker activations, exact position of max"},
        {"op_tpl": "SVD truncating to rank {k} from rank {n}",
         "preserves_tpl": "best rank-{k} approximation in Frobenius norm",
         "loses_tpl": "{lost} singular values and their associated structure"},
        {"op_tpl": "downsampling audio from {sr_in}kHz to {sr_out}kHz",
         "preserves_tpl": "frequencies below {nyquist}kHz (Nyquist)",
         "loses_tpl": "all frequencies above {nyquist}kHz, audio fidelity"},
        {"op_tpl": "converting {ch}-channel image to grayscale",
         "preserves": "luminance (weighted sum of channels)",
         "loses": "colour information, ability to distinguish same-brightness colours"},
        {"op_tpl": "tokenising text with BPE ({vocab}K vocab)",
         "preserves": "most common subword patterns",
         "loses": "character-level granularity, rare character sequences split arbitrarily"},
        {"op_tpl": "knowledge distillation from {big}B to {small}B model",
         "preserves": "soft label distribution on training data",
         "loses": "capacity for rare/complex patterns, tail distribution accuracy"},
        {"op_tpl": "applying dropout with p={p}",
         "preserves": "expected activation values (rescaled)",
         "loses": "co-adaptation between neurons, deterministic output"},
        {"op_tpl": "replacing continuous actions with {n} discrete buckets",
         "preserves": "approximate action selection",
         "loses": "fine-grained control, smoothness of policy"},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._SCENARIO_TEMPLATES)
        n = self._rng.randint(8, 64 + difficulty * 16)
        d = self._rng.choice([64, 128, 256, 512, 768, 1024])
        d_in = self._rng.choice([50, 100, 200, 500])
        d_out = self._rng.randint(2, max(3, d_in // 5))
        d_lost = d_in - d_out
        bits = self._rng.choice([16, 32, 64, 128, 256])
        h = self._rng.choice([7, 14, 28, 56])
        w = h
        stride = self._rng.choice([2, 3, 4])
        k = self._rng.randint(2, 20)
        rank_n = self._rng.randint(k + 5, k + 50)
        sr_in = self._rng.choice([44, 48, 96])
        sr_out = self._rng.choice([8, 16, 22])
        nyquist = sr_out // 2
        ch = self._rng.choice([3, 4])
        vocab = self._rng.choice([16, 30, 32, 50, 64])
        big = self._rng.choice([7, 13, 30, 70, 175])
        small = self._rng.choice([b for b in [1, 3, 7, 13] if b < big]) if big > 1 else 1
        p = round(self._rng.choice([0.1, 0.2, 0.3, 0.4, 0.5]), 1)
        dtype_from = self._rng.choice(["fp32", "fp16", "bf16"])
        dtype_to = self._rng.choice(["int8", "int4", "int2"])
        fmt = dict(n=n, d=d, d_in=d_in, d_out=d_out, d_lost=d_lost,
                   bits=bits, h=h, w=w, stride=stride, k=k,
                   lost=rank_n - k, sr_in=sr_in, sr_out=sr_out,
                   nyquist=nyquist, ch=ch, vocab=vocab, big=big,
                   small=small, p=p, dtype_from=dtype_from,
                   dtype_to=dtype_to)
        operation = tpl["op_tpl"].format(**fmt)
        preserves = tpl.get("preserves_tpl", tpl.get("preserves", ""))
        if "preserves_tpl" in tpl:
            preserves = tpl["preserves_tpl"].format(**fmt)
        else:
            preserves = tpl["preserves"]
        loses = tpl.get("loses_tpl", tpl.get("loses", ""))
        if "loses_tpl" in tpl:
            loses = tpl["loses_tpl"].format(**fmt)
        else:
            loses = tpl["loses"]
        s = {"operation": operation, "preserves": preserves, "loses": loses}
        problem = f"what does '{s['operation']}' lose?"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"preserves: {sd['preserves']}", f"loses: {sd['loses']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["loses"]


@register
class ConvergenceProofGenerator(StepGenerator):
    """Determine if an iterative algorithm converges."""

    @property
    def task_name(self) -> str:
        return "convergence_proof"

    @property
    def tier(self) -> int:
        return 9

    @property
    def prerequisites(self) -> list[str]:
        return ["invariant_discovery", "learning_bound"]

    def task_description(self, difficulty: int) -> str:
        return "prove convergence"

    _CONVERGENCE_TEMPLATES = [
        {"algo_tpl": "x_{{n+1}} = x_n/{r}", "converges": True, "limit_tpl": "0",
         "reason_tpl": "contraction mapping, ratio=1/{r} < 1"},
        {"algo_tpl": "x_{{n+1}} = {r}*x_n", "converges": False, "limit_tpl": "diverges",
         "reason_tpl": "expansion, ratio={r} > 1"},
        {"algo_tpl": "x_{{n+1}} = (x_n + {a}/x_n)/2", "converges": True,
         "limit_tpl": "sqrt({a})",
         "reason_tpl": "Newton's method for sqrt({a}), quadratic convergence"},
        {"algo_tpl": "x_{{n+1}} = cos(x_n), x_0={x0:.1f}", "converges": True,
         "limit_tpl": "0.7391 (Dottie number)",
         "reason_tpl": "|cos'(x)| = |sin(x)| < 1 near fixed point"},
        {"algo_tpl": "x_{{n+1}} = x_n - f(x_n)/f'(x_n), x_0={x0}", "converges": True,
         "limit_tpl": "root of f",
         "reason_tpl": "Newton-Raphson, quadratic convergence near simple roots"},
        {"algo_tpl": "x_{{n+1}} = {r:.1f}*x_n*(1-x_n)", "converges": False,
         "limit_tpl": "chaotic",
         "reason_tpl": "logistic map with r={r:.1f} enters period-doubling chaos"},
        {"algo_tpl": "x_{{n+1}} = (x_n + {a}/x_n)/2, x_0={x0}", "converges": True,
         "limit_tpl": "sqrt({a})",
         "reason_tpl": "AM-GM inequality, converges to sqrt({a})"},
        {"algo_tpl": "a_{{n+1}} = sqrt({c} + a_n), a_0={a0}", "converges": True,
         "limit_tpl": "{fp}",
         "reason_tpl": "bounded above by {fp}, monotonically increasing"},
        {"algo_tpl": "x_{{n+1}} = x_n^{p}, x_0={x0:.1f}", "converges": False,
         "limit_tpl": "diverges if |x_0|>1",
         "reason_tpl": "iterating power {p} diverges unless |x_0|<=1"},
        {"algo_tpl": "SGD with lr={lr} on convex loss", "converges": True,
         "limit_tpl": "neighbourhood of minimum",
         "reason_tpl": "convexity guarantees descent; fixed lr={lr} causes oscillation near minimum"},
        {"algo_tpl": "x_{{n+1}} = sin(x_n), x_0={x0:.2f}", "converges": True,
         "limit_tpl": "0",
         "reason_tpl": "|sin(x)| < |x| for x != 0, contracts to 0"},
        {"algo_tpl": "power iteration on {n}x{n} matrix", "converges": True,
         "limit_tpl": "dominant eigenvector",
         "reason_tpl": "converges if dominant eigenvalue of {n}x{n} matrix is unique and real"},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._CONVERGENCE_TEMPLATES)
        r = self._rng.randint(2, 4 + difficulty)
        a = self._rng.randint(2, 10 + difficulty * 3)
        x0 = round(self._rng.uniform(0.5, 5.0), 1)
        c_val = self._rng.randint(2, 6)
        a0 = self._rng.choice([0, 1])
        import math
        fp = round((1 + math.sqrt(1 + 4 * c_val)) / 2, 2)
        p = self._rng.choice([2, 3])
        lr = round(self._rng.uniform(0.001, 0.1), 3)
        n = self._rng.randint(3, 10 + difficulty)
        r_logistic = round(self._rng.uniform(3.57, 4.0), 2)
        fmt = dict(r=r, a=a, x0=x0, c=c_val, a0=a0, fp=fp, p=p,
                   lr=lr, n=n)
        if "logistic" in tpl.get("reason_tpl", ""):
            fmt["r"] = r_logistic
        algorithm = tpl["algo_tpl"].format(**fmt)
        limit = tpl["limit_tpl"].format(**fmt)
        reason = tpl["reason_tpl"].format(**fmt)
        c = {"algorithm": algorithm, "converges": tpl["converges"],
             "limit": limit, "reason": reason}
        problem = f"does {c['algorithm']} converge?"
        return problem, c

    def _create_steps(self, sd: dict) -> list[str]:
        return [sd["reason"]]

    def _create_answer(self, sd: dict) -> str:
        if sd["converges"]:
            return f"YES, limit={sd['limit']}"
        return "NO, diverges"


# ── TIER 10 (11 → 13) ──────────────────────────────────────────────

@register
class RegularisationDesignGenerator(StepGenerator):
    """Design a regularisation strategy for a stated overfitting problem."""

    @property
    def task_name(self) -> str:
        return "regularisation_design"

    @property
    def tier(self) -> int:
        return 10

    @property
    def prerequisites(self) -> list[str]:
        return ["loss_design", "training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        return "design regularisation"

    _SCENARIO_TEMPLATES = [
        {"symptom_tpl": "train loss {tl}, val loss {vl}, {params}M params on {data}K samples",
         "diagnosis": "severe overfitting due to param/data ratio",
         "strategy": "L2 weight decay + dropout + data augmentation",
         "reason": "reduce effective capacity and increase data diversity"},
        {"symptom_tpl": "attention concentrating on single token for all {n} inputs at layer {layer}",
         "diagnosis": "attention collapse",
         "strategy": "attention entropy regularisation + multi-head diversity loss",
         "reason": "penalise low-entropy attention distributions"},
        {"symptom_tpl": "loss={loss} but generated text is repetitive after {steps}K steps",
         "diagnosis": "mode collapse in generation",
         "strategy": "nucleus sampling + repetition penalty + unlikelihood training",
         "reason": "diversify output distribution during both training and inference"},
        {"symptom_tpl": "validation accuracy plateaus at {val_acc}% while train reaches {train_acc}%",
         "diagnosis": "overfitting with insufficient generalisation",
         "strategy": "early stopping + mixup augmentation + label smoothing",
         "reason": "prevent memorisation and soften decision boundaries"},
        {"symptom_tpl": "loss spikes every {freq} steps then recovers (lr={lr})",
         "diagnosis": "learning rate too high, unstable optimisation",
         "strategy": "reduce lr, add warmup, use gradient clipping",
         "reason": "stabilise gradient magnitudes and step sizes"},
        {"symptom_tpl": "all {d}-dim hidden representations collapse to similar vectors",
         "diagnosis": "representation collapse (dimensional collapse)",
         "strategy": "VICReg or Barlow Twins variance/covariance regularisation",
         "reason": "force dimensions to be informative and decorrelated"},
        {"symptom_tpl": "GAN generator produces same {res}x{res} image regardless of {z}-dim noise",
         "diagnosis": "mode collapse in GAN",
         "strategy": "minibatch discrimination + spectral normalisation",
         "reason": "force generator to produce diverse outputs"},
        {"symptom_tpl": "fine-tuned {params}M model forgets {n} pre-trained capabilities",
         "diagnosis": "catastrophic forgetting",
         "strategy": "EWC (elastic weight consolidation) + low learning rate + replay buffer",
         "reason": "constrain weight changes important to previous tasks"},
        {"symptom_tpl": "embeddings in {d}-dim space have cosine similarity > {sim}",
         "diagnosis": "anisotropic embedding space",
         "strategy": "contrastive loss + whitening + temperature scaling",
         "reason": "spread representations uniformly across the hypersphere"},
        {"symptom_tpl": "model {conf}% confident on {n} out-of-distribution inputs",
         "diagnosis": "poor calibration / overconfidence",
         "strategy": "temperature scaling + mixup + OOD detection head",
         "reason": "calibrate confidence to match actual accuracy"},
        {"symptom_tpl": "gradients vanish in first {n} of {total} layers",
         "diagnosis": "vanishing gradients",
         "strategy": "residual connections + careful initialisation + batch normalisation",
         "reason": "ensure gradient signal reaches all layers"},
        {"symptom_tpl": "model has {params}M params but task needs only ~{needed}M",
         "diagnosis": "overparameterised for task",
         "strategy": "pruning + knowledge distillation + quantisation",
         "reason": "remove redundant parameters while preserving accuracy"},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._SCENARIO_TEMPLATES)
        tl = round(self._rng.uniform(0.001, 0.05), 3)
        vl = round(self._rng.uniform(1.5, 4.0), 1)
        params = self._rng.choice([10, 50, 100, 350, 700])
        data = self._rng.choice([5, 10, 20, 50])
        n = self._rng.randint(3, 20 + difficulty * 5)
        layer = self._rng.randint(1, 12)
        loss = round(self._rng.uniform(0.1, 1.5), 2)
        steps = self._rng.randint(5, 50)
        val_acc = self._rng.randint(45, 75)
        train_acc = self._rng.randint(90, 99)
        freq = self._rng.randint(100, 1000)
        lr = round(self._rng.uniform(0.001, 0.1), 3)
        d = self._rng.choice([128, 256, 512, 768, 1024])
        res = self._rng.choice([64, 128, 256, 512])
        z = self._rng.choice([64, 100, 128, 256])
        sim = round(self._rng.uniform(0.85, 0.98), 2)
        conf = self._rng.randint(85, 99)
        total = self._rng.randint(12, 48)
        needed = max(1, params // self._rng.randint(5, 15))
        fmt = dict(tl=tl, vl=vl, params=params, data=data, n=n,
                   layer=layer, loss=loss, steps=steps, val_acc=val_acc,
                   train_acc=train_acc, freq=freq, lr=lr, d=d, res=res,
                   z=z, sim=sim, conf=conf, total=total, needed=needed)
        symptom = tpl["symptom_tpl"].format(**fmt)
        s = {"symptom": symptom, "diagnosis": tpl["diagnosis"],
             "strategy": tpl["strategy"], "reason": tpl["reason"]}
        problem = f"symptom: {s['symptom']}"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"diagnosis: {sd['diagnosis']}", f"reason: {sd['reason']}"]

    def _create_answer(self, sd: dict) -> str:
        return sd["strategy"]


@register
class BottleneckIdentificationGenerator(StepGenerator):
    """Identify the computational bottleneck in a model architecture."""

    @property
    def task_name(self) -> str:
        return "bottleneck_identification"

    @property
    def tier(self) -> int:
        return 10

    @property
    def prerequisites(self) -> list[str]:
        return ["efficiency_analysis", "architecture_analysis"]

    def task_description(self, difficulty: int) -> str:
        return "identify bottleneck"

    _BOTTLENECK_TEMPLATES = [
        {"arch_tpl": "transformer with seq_len={seq}, d_model={d}, {layers} layers",
         "bottleneck": "self-attention (O(n^2) in seq_len)",
         "flops_tpl": "{seq}^2 * {d} * {layers} per layer",
         "fix": "sparse attention, linear attention, or sliding window"},
        {"arch_tpl": "MLP with {params}M params, batch_size={bs}",
         "bottleneck": "memory bandwidth (not compute-bound at small batch)",
         "flops_tpl": "{params}M params * 2 FLOPs, but large memory transfer",
         "fix": "increase batch size to amortise memory transfer"},
        {"arch_tpl": "engram with {iters} iterations, {lpi} layers per iteration",
         "bottleneck": "sequential iteration dependency (can't parallelise)",
         "flops_tpl": "{iters} * {lpi}L forward = {total_layers} layer passes",
         "fix": "reduce iterations via better halting, or wider per-iteration compute"},
        {"arch_tpl": "CNN with {layers} layers, {k}x{k} kernels, no skip connections",
         "bottleneck": "vanishing gradients in deep stack",
         "flops_tpl": "moderate per-layer, but gradient signal dies after {layers} layers",
         "fix": "add residual connections (ResNet)"},
        {"arch_tpl": "RNN processing sequence of length {seq}",
         "bottleneck": "sequential dependency prevents parallelism",
         "flops_tpl": "{seq} sequential steps, each O(d^2)",
         "fix": "replace with transformer or use chunked processing"},
        {"arch_tpl": "GAN with {res}x{res} output resolution",
         "bottleneck": "discriminator gradient signal at high resolution",
         "flops_tpl": "generator + discriminator per step at {res}x{res}",
         "fix": "progressive growing, multi-scale discriminator"},
        {"arch_tpl": "diffusion model with {steps} denoising steps",
         "bottleneck": "inference latency ({steps} forward passes)",
         "flops_tpl": "{steps} * model_forward",
         "fix": "DDIM (fewer steps), distillation, consistency models"},
        {"arch_tpl": "mixture of {n_experts} experts, top-{top_k} routing",
         "bottleneck": "all-to-all communication for expert routing across GPUs",
         "flops_tpl": "{top_k}/{n_experts} of total params active per token",
         "fix": "expert parallelism, reduce number of experts, local routing"},
        {"arch_tpl": "KV cache for {ctx}K context window, d_model={d}",
         "bottleneck_tpl": "memory: {ctx}K * {d} * 2 * num_layers * 2 bytes per request",
         "flops_tpl": "attention fast, but cache fills GPU memory at {ctx}K context",
         "fix": "GQA, paged attention, quantised KV cache"},
        {"arch_tpl": "embedding table with {vocab}K vocab, d_model={d}",
         "bottleneck_tpl": "softmax over {vocab}K classes at output",
         "flops_tpl": "{vocab}K * {d} per token for final projection",
         "fix": "adaptive softmax, hierarchical softmax, or approximation"},
        {"arch_tpl": "ViT with {img}x{img} image, patches of {patch}x{patch}",
         "bottleneck_tpl": "{n_patches} patches, attention is O({n_patches}^2)",
         "flops_tpl": "{attn_entries} attention entries per head per layer",
         "fix": "hierarchical patches (Swin), pooling, or linear attention"},
        {"arch_tpl": "autoregressive decoder generating {seq} tokens",
         "bottleneck": "sequential token generation (can't parallelise)",
         "flops_tpl": "{seq} forward passes with growing KV cache",
         "fix": "speculative decoding, parallel decoding, or Medusa heads"},
    ]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tpl = self._rng.choice(self._BOTTLENECK_TEMPLATES)
        seq = self._rng.choice([512, 1024, 2048, 4096, 8192, 16384])
        d = self._rng.choice([256, 512, 768, 1024, 2048, 4096])
        layers = self._rng.randint(6, 48)
        params = self._rng.choice([100, 350, 700, 1000, 7000])
        bs = self._rng.randint(1, 4)
        iters = self._rng.randint(4, 32)
        lpi = self._rng.randint(4, 12)
        k = self._rng.choice([3, 5, 7])
        res = self._rng.choice([256, 512, 1024])
        steps = self._rng.choice([100, 250, 500, 1000, 2000])
        n_experts = self._rng.choice([8, 16, 32, 64, 128])
        top_k = self._rng.choice([1, 2])
        ctx = self._rng.choice([8, 16, 32, 64, 128])
        vocab = self._rng.choice([32, 50, 100, 250])
        img = self._rng.choice([224, 384, 512, 1024])
        patch = self._rng.choice([8, 16, 32])
        n_patches = (img // patch) ** 2
        attn_entries = n_patches * n_patches
        total_layers = iters * lpi
        fmt = dict(seq=seq, d=d, layers=layers, params=params, bs=bs,
                   iters=iters, lpi=lpi, total_layers=total_layers,
                   k=k, res=res, steps=steps, n_experts=n_experts,
                   top_k=top_k, ctx=ctx, vocab=vocab, img=img,
                   patch=patch, n_patches=n_patches,
                   attn_entries=attn_entries)
        arch = tpl["arch_tpl"].format(**fmt)
        bottleneck = tpl.get("bottleneck_tpl", tpl.get("bottleneck", "")).format(**fmt)
        flops = tpl["flops_tpl"].format(**fmt)
        s = {"arch": arch, "bottleneck": bottleneck, "flops": flops,
             "fix": tpl["fix"]}
        problem = f"architecture: {s['arch']}"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"bottleneck: {sd['bottleneck']}", f"flops: {sd['flops']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['bottleneck']}; fix: {sd['fix']}"
