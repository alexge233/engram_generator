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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        proofs = [
            {
                "claim": "n^2 > 2n for n >= 3",
                "steps": ["base: 3^2=9 > 6=2*3", "assume k^2 > 2k",
                           "(k+1)^2 = k^2+2k+1 > 2k+2k+1 > 2(k+1)"],
                "valid": True, "reason": "all steps follow",
            },
            {
                "claim": "sum 1..n = n(n+1)/2",
                "steps": ["base: 1 = 1*2/2", "assume sum 1..k = k(k+1)/2",
                           "sum 1..k+1 = k(k+1)/2 + k+1 = (k+1)(k+2)/2"],
                "valid": True, "reason": "correct induction",
            },
            {
                "claim": "2^n > n^2 for n >= 1",
                "steps": ["base: 2^1=2 > 1=1^2", "assume 2^k > k^2",
                           "2^{k+1} = 2*2^k > 2k^2"],
                "valid": False, "reason": "2k^2 >= (k+1)^2 only for k>=3, base case fails at n=2",
            },
            {
                "claim": "all horses are the same colour",
                "steps": ["base: 1 horse trivially same colour",
                           "assume any k horses same colour",
                           "for k+1: first k same colour, last k same colour, overlap => all same"],
                "valid": False, "reason": "overlap is empty when k=1, induction step fails",
            },
        ]
        idx = self._rng.randint(0, len(proofs) - 1)
        proof = proofs[idx]
        step_str = "; ".join(proof["steps"])
        problem = f"claim: {proof['claim']}; proof: {step_str}"
        return problem, proof

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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        formulas = [
            {"formula": "v = d/t", "lhs": "m/s", "rhs": "m/s", "consistent": True},
            {"formula": "F = ma", "lhs": "kg*m/s^2", "rhs": "kg*m/s^2", "consistent": True},
            {"formula": "E = mc^2", "lhs": "kg*m^2/s^2", "rhs": "kg*(m/s)^2", "consistent": True},
            {"formula": "v = d*t", "lhs": "m/s", "rhs": "m*s", "consistent": False},
            {"formula": "F = m/a", "lhs": "kg*m/s^2", "rhs": "kg/(m/s^2)", "consistent": False},
            {"formula": "P = F*v", "lhs": "kg*m^2/s^3", "rhs": "kg*m/s^2*m/s", "consistent": True},
        ]
        f = self._rng.choice(formulas)
        problem = f"is {f['formula']} dimensionally consistent? LHS=[{f['lhs']}] RHS=[{f['rhs']}]"
        return problem, f

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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        patterns = [
            {
                "concrete": "find shortest route between cities A and E through B,C,D",
                "abstract": "shortest path in weighted graph",
                "category": "graph_traversal",
            },
            {
                "concrete": "maximise profit given weight limit and item values",
                "abstract": "0/1 knapsack optimisation",
                "category": "dynamic_programming",
            },
            {
                "concrete": "find if a word can be built from magazine letter cutouts",
                "abstract": "multiset subset check",
                "category": "counting",
            },
            {
                "concrete": "schedule non-overlapping meetings to maximise attendance",
                "abstract": "interval scheduling maximisation",
                "category": "greedy",
            },
        ]
        p = self._rng.choice(patterns)
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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        duals = [
            {
                "primal": "find minimum spanning tree",
                "dual": "find maximum weight cut",
                "domain": "graph theory",
            },
            {
                "primal": "minimise cost subject to constraints",
                "dual": "maximise lower bound from constraints",
                "domain": "linear programming",
            },
            {
                "primal": "find shortest path",
                "dual": "find maximum flow (by max-flow min-cut)",
                "domain": "network flow",
            },
        ]
        d = self._rng.choice(duals)
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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {
                "operation": "mean pooling a sequence of embeddings",
                "preserves": "average magnitude and direction",
                "loses": "positional order, individual token identity",
            },
            {
                "operation": "PCA reducing 100D to 10D",
                "preserves": "top 10 variance components",
                "loses": "90 minor variance directions, possible nonlinear structure",
            },
            {
                "operation": "quantising fp32 weights to int8",
                "preserves": "approximate magnitude and sign",
                "loses": "precision within quantisation bins, outlier fidelity",
            },
            {
                "operation": "hashing a string to 32 bits",
                "preserves": "identity (with collision probability)",
                "loses": "content, length, structure, reversibility",
            },
        ]
        s = self._rng.choice(scenarios)
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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cases = [
            {
                "algorithm": "x_{n+1} = x_n/2",
                "converges": True,
                "limit": "0",
                "reason": "contraction mapping, ratio=0.5 < 1",
            },
            {
                "algorithm": "x_{n+1} = 2x_n",
                "converges": False,
                "limit": "diverges",
                "reason": "expansion, ratio=2 > 1",
            },
            {
                "algorithm": "x_{n+1} = (x_n + a/x_n)/2",
                "converges": True,
                "limit": "sqrt(a)",
                "reason": "Newton's method for sqrt, quadratic convergence",
            },
            {
                "algorithm": "x_{n+1} = cos(x_n)",
                "converges": True,
                "limit": "0.7391 (Dottie number)",
                "reason": "|cos'(x)| = |sin(x)| < 1 near fixed point",
            },
        ]
        c = self._rng.choice(cases)
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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {
                "symptom": "train loss 0.01, val loss 2.5, 100M params on 10K samples",
                "diagnosis": "severe overfitting due to param/data ratio",
                "strategy": "L2 weight decay + dropout + data augmentation",
                "reason": "reduce effective capacity and increase data diversity",
            },
            {
                "symptom": "attention concentrating on single token for all inputs",
                "diagnosis": "attention collapse",
                "strategy": "attention entropy regularisation + multi-head diversity loss",
                "reason": "penalise low-entropy attention distributions",
            },
            {
                "symptom": "loss decreasing but generated text is repetitive",
                "diagnosis": "mode collapse in generation",
                "strategy": "nucleus sampling + repetition penalty + unlikelihood training",
                "reason": "diversify output distribution during both training and inference",
            },
        ]
        s = self._rng.choice(scenarios)
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

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        scenarios = [
            {
                "arch": "transformer with seq_len=8192, d_model=512, 12 layers",
                "bottleneck": "self-attention (O(n^2) in seq_len)",
                "flops": "8192^2 * 512 * 12 = 412B per layer",
                "fix": "sparse attention, linear attention, or sliding window",
            },
            {
                "arch": "MLP with 1B params, batch_size=1",
                "bottleneck": "memory bandwidth (not compute-bound at batch 1)",
                "flops": "1B params * 2 = 2 GFLOPS, but 4GB memory transfer",
                "fix": "increase batch size to amortise memory transfer",
            },
            {
                "arch": "engram with 16 iterations, 8 layers per iteration",
                "bottleneck": "sequential iteration dependency (can't parallelise)",
                "flops": "16 * 8L forward = 128 layer passes",
                "fix": "reduce iterations via better halting, or wider per-iteration compute",
            },
        ]
        s = self._rng.choice(scenarios)
        problem = f"architecture: {s['arch']}"
        return problem, s

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"bottleneck: {sd['bottleneck']}", f"flops: {sd['flops']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['bottleneck']}; fix: {sd['fix']}"
