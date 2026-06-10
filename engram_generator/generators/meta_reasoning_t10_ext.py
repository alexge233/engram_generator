"""Extended tier 8-10 meta-reasoning generators -- deeper self-architecture tasks.

8 generators that push the upper tiers toward more depth: architecture search,
curriculum design, loss landscape analysis, transfer learning strategy,
experiment design, proof complexity estimation, debugging strategy, and
benchmark design.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _r4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


class ArchitectureCandidate:
    """Represents a candidate architecture with scored attributes.

    Stores latency, memory, and accuracy estimates for a candidate
    neural architecture, allowing comparison and ranking.

    Attributes:
        name: Architecture identifier.
        latency_ms: Inference latency in milliseconds.
        memory_mb: Memory footprint in megabytes.
        accuracy: Expected accuracy (0-1 scale).
    """

    def __init__(self, name: str, latency_ms: float,
                 memory_mb: float, accuracy: float) -> None:
        """Initialise the architecture candidate.

        Args:
            name: Architecture identifier.
            latency_ms: Inference latency in milliseconds.
            memory_mb: Memory footprint in megabytes.
            accuracy: Expected accuracy (0-1 scale).
        """
        self._name = name
        self._latency_ms = latency_ms
        self._memory_mb = memory_mb
        self._accuracy = accuracy

    @property
    def name(self) -> str:
        """Return the architecture name."""
        return self._name

    @property
    def latency_ms(self) -> float:
        """Return inference latency in milliseconds."""
        return self._latency_ms

    @property
    def memory_mb(self) -> float:
        """Return memory footprint in megabytes."""
        return self._memory_mb

    @property
    def accuracy(self) -> float:
        """Return expected accuracy."""
        return self._accuracy

    def score(self, w_acc: float, w_lat: float, w_mem: float,
              max_lat: float, max_mem: float) -> float:
        """Compute a weighted score for this candidate.

        Args:
            w_acc: Weight for accuracy.
            w_lat: Weight for latency (penalty).
            w_mem: Weight for memory (penalty).
            max_lat: Maximum latency for normalisation.
            max_mem: Maximum memory for normalisation.

        Returns:
            Weighted score (higher is better).
        """
        lat_norm = 1.0 - (self._latency_ms / max_lat) if max_lat > 0 else 0.0
        mem_norm = 1.0 - (self._memory_mb / max_mem) if max_mem > 0 else 0.0
        return _r4(w_acc * self._accuracy + w_lat * lat_norm + w_mem * mem_norm)


class SymptomDatabase:
    """Stores ML training symptoms and their root causes.

    Provides lookup from observed symptom to likely root cause,
    diagnostic checks, and recommended fixes.
    """

    _SYMPTOMS: dict[str, dict] = {
        "nan_loss": {
            "root_cause": "numerical overflow or division by zero",
            "checks": [
                "inspect learning rate (too high?)",
                "check for log(0) or division by zero in loss",
                "verify input data has no NaN/Inf values",
            ],
            "fix": "reduce learning rate, add epsilon to denominators, clip gradients",
        },
        "mode_collapse": {
            "root_cause": "generator produces limited diversity (GAN) or posterior collapses (VAE)",
            "checks": [
                "measure output diversity across batches",
                "check discriminator loss (too strong?)",
                "inspect KL divergence term weight",
            ],
            "fix": "use spectral normalisation, reduce discriminator updates, anneal KL weight",
        },
        "underfitting": {
            "root_cause": "model capacity too low or learning rate too small",
            "checks": [
                "compare train loss to random baseline",
                "check if model can overfit a single batch",
                "verify data pipeline is correct",
            ],
            "fix": "increase model size, increase learning rate, reduce regularisation",
        },
        "overfitting": {
            "root_cause": "model memorises training data instead of generalising",
            "checks": [
                "compare train vs validation loss curves",
                "check for large gap after N epochs",
                "verify data augmentation is applied",
            ],
            "fix": "add dropout, weight decay, data augmentation, or early stopping",
        },
        "gradient_explosion": {
            "root_cause": "unstable gradient magnitudes in deep networks",
            "checks": [
                "monitor gradient norms per layer",
                "check for very large weight values",
                "verify batch normalisation is applied",
            ],
            "fix": "apply gradient clipping, use batch norm, reduce learning rate",
        },
        "slow_convergence": {
            "root_cause": "suboptimal optimiser settings or poor initialisation",
            "checks": [
                "compare convergence to known baselines",
                "check learning rate schedule",
                "verify weight initialisation method",
            ],
            "fix": "use Adam/AdamW, apply learning rate warmup, use Xavier/Kaiming init",
        },
    }

    def random_symptom(self, rng: "random.Random") -> tuple[str, dict]:
        """Select a random training symptom.

        Args:
            rng: Seeded random instance.

        Returns:
            Tuple of (symptom_name, symptom_data).
        """
        key = rng.choice(list(self._SYMPTOMS.keys()))
        return key, self._SYMPTOMS[key]


_SYMPTOM_DB = SymptomDatabase()


@register
class ArchitectureSearchGenerator(StepGenerator):
    """Select the optimal architecture from candidates given task constraints.

    Presents 3-4 candidate architectures with latency, memory, and accuracy
    estimates, plus task constraints. Scores each candidate on a weighted
    combination and selects the best.

    Difficulty scaling:
        Difficulty 1-3: 3 candidates, equal weights.
        Difficulty 4-6: 3 candidates, custom weights.
        Difficulty 7-8: 4 candidates, hard constraint thresholds.
    """

    _ARCH_NAMES = [
        "Transformer", "CNN-ResNet", "MLP-Mixer", "LSTM",
        "GRU", "ConvNeXt", "EfficientNet", "ViT-Small",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "architecture_search"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["architecture_analysis"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "select optimal architecture from candidates given constraints"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an architecture search problem.

        Args:
            difficulty: Controls number of candidates and constraints.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_cands = 3 if difficulty <= 6 else 4
        names = self._rng.sample(self._ARCH_NAMES, n_cands)

        candidates = []
        for name in names:
            lat = _r4(self._rng.uniform(5.0, 100.0))
            mem = _r4(self._rng.uniform(50.0, 2000.0))
            acc = _r4(self._rng.uniform(0.7, 0.98))
            candidates.append(ArchitectureCandidate(name, lat, mem, acc))

        if difficulty <= 3:
            w_acc, w_lat, w_mem = 0.34, 0.33, 0.33
        else:
            w_acc = _r4(self._rng.uniform(0.4, 0.7))
            w_lat = _r4(self._rng.uniform(0.1, 0.3))
            w_mem = _r4(1.0 - w_acc - w_lat)

        max_lat = max(c.latency_ms for c in candidates)
        max_mem = max(c.memory_mb for c in candidates)

        scores = {}
        for c in candidates:
            scores[c.name] = c.score(w_acc, w_lat, w_mem, max_lat, max_mem)

        # Apply hard constraints at high difficulty
        if difficulty >= 7:
            lat_thresh = _r4(self._rng.uniform(30.0, 70.0))
            mem_thresh = _r4(self._rng.uniform(200.0, 1000.0))
            for c in candidates:
                if c.latency_ms > lat_thresh or c.memory_mb > mem_thresh:
                    scores[c.name] = 0.0
        else:
            lat_thresh = None
            mem_thresh = None

        best = max(scores, key=scores.get)

        cand_strs = [
            f"{c.name}: lat={c.latency_ms}ms, mem={c.memory_mb}MB, acc={c.accuracy}"
            for c in candidates
        ]
        problem = f"candidates: {'; '.join(cand_strs)}, weights: acc={w_acc}, lat={w_lat}, mem={w_mem}"
        if lat_thresh is not None:
            problem += f", max_lat={lat_thresh}ms, max_mem={mem_thresh}MB"

        return problem, {
            "candidates": candidates, "scores": scores,
            "best": best, "w_acc": w_acc, "w_lat": w_lat, "w_mem": w_mem,
            "lat_thresh": lat_thresh, "mem_thresh": mem_thresh,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate scoring and selection steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for c in sd["candidates"]:
            steps.append(f"{c.name}: score = {sd['scores'][c.name]}")
        if sd["lat_thresh"] is not None:
            steps.append(
                f"hard constraints: lat<={sd['lat_thresh']}ms, "
                f"mem<={sd['mem_thresh']}MB"
            )
        steps.append(f"best = {sd['best']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the best architecture.

        Args:
            sd: Solution data.

        Returns:
            Best architecture name as a string.
        """
        return sd["best"]


@register
class CurriculumDesignGenerator(StepGenerator):
    """Design a training curriculum by ordering tasks and setting thresholds.

    Given a set of tasks with estimated difficulty and dependencies,
    produces an ordered curriculum with mastery thresholds and
    advancement criteria.

    Difficulty scaling:
        Difficulty 1-3: 3 tasks, linear dependencies.
        Difficulty 4-6: 4 tasks, branching dependencies.
        Difficulty 7-8: 5 tasks, multiple prerequisite chains.
    """

    _TASK_POOL = [
        ("addition", 1), ("multiplication", 2), ("division", 3),
        ("fractions", 4), ("algebra", 5), ("geometry", 3),
        ("statistics", 4), ("calculus", 6), ("proofs", 7),
        ("optimization", 6),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "curriculum_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "design training curriculum with ordering and mastery thresholds"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a curriculum design problem.

        Args:
            difficulty: Controls number of tasks and dependency structure.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_tasks = 3
        elif difficulty <= 6:
            n_tasks = 4
        else:
            n_tasks = 5

        selected = self._rng.sample(self._TASK_POOL, n_tasks)
        # Sort by difficulty to create a natural ordering
        selected.sort(key=lambda x: x[1])

        # Mastery thresholds: higher difficulty tasks need higher threshold
        thresholds = {}
        for name, diff in selected:
            threshold = _r4(min(0.95, 0.7 + 0.05 * diff))
            thresholds[name] = threshold

        # Order: topological sort by difficulty
        order = [name for name, _ in selected]

        # Advancement criterion
        advancement = _r4(self._rng.uniform(0.8, 0.95))

        tasks_str = ", ".join(f"{name}(diff={diff})" for name, diff in selected)
        problem = f"tasks: {tasks_str}, advancement_threshold={advancement}"
        return problem, {
            "selected": selected, "order": order,
            "thresholds": thresholds, "advancement": advancement,
            "n_tasks": n_tasks,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate curriculum reasoning steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"sort by difficulty: {sd['order']}"]
        for name, diff in sd["selected"]:
            steps.append(
                f"{name}: mastery threshold = {sd['thresholds'][name]}"
            )
        steps.append(f"advance when accuracy >= {sd['advancement']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the designed curriculum order.

        Args:
            sd: Solution data.

        Returns:
            Curriculum order as a string.
        """
        return " -> ".join(sd["order"])


@register
class LossLandscapeGenerator(StepGenerator):
    """Analyse loss landscape properties from Hessian eigenvalues.

    Given eigenvalues of the Hessian at a critical point, classifies it
    as a local minimum (all positive), local maximum (all negative),
    or saddle point (mixed signs). Computes condition number.

    Difficulty scaling:
        Difficulty 1-3: 2x2 Hessian (2 eigenvalues).
        Difficulty 4-6: 3x3 Hessian.
        Difficulty 7-8: 4x4 Hessian with near-zero eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loss_landscape"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["loss_design"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "classify critical point from Hessian eigenvalues"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loss landscape analysis problem.

        Args:
            difficulty: Controls Hessian dimension.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
        elif difficulty <= 6:
            n = 3
        else:
            n = 4

        # Generate eigenvalues -- mix of positive and negative for variety
        point_type = self._rng.choice(["minimum", "saddle", "maximum"])
        eigenvalues = self._generate_eigenvalues(n, point_type, difficulty)

        # Classify
        n_pos = sum(1 for e in eigenvalues if e > 0)
        n_neg = sum(1 for e in eigenvalues if e < 0)
        n_zero = sum(1 for e in eigenvalues if e == 0)

        if n_pos == n:
            classification = "local minimum"
        elif n_neg == n:
            classification = "local maximum"
        else:
            classification = "saddle point"

        # Condition number
        abs_eigs = [abs(e) for e in eigenvalues if e != 0]
        if abs_eigs:
            cond = _r4(max(abs_eigs) / min(abs_eigs))
        else:
            cond = float("inf")

        problem = f"Hessian eigenvalues: {eigenvalues}"
        return problem, {
            "eigenvalues": eigenvalues, "n": n,
            "n_pos": n_pos, "n_neg": n_neg, "n_zero": n_zero,
            "classification": classification, "cond": cond,
        }

    def _generate_eigenvalues(self, n: int, point_type: str,
                              difficulty: int) -> list[float]:
        """Generate eigenvalues for a given critical point type.

        Args:
            n: Number of eigenvalues.
            point_type: One of 'minimum', 'maximum', 'saddle'.
            difficulty: Controls eigenvalue range.

        Returns:
            List of eigenvalues.
        """
        if point_type == "minimum":
            eigs = [_r4(self._rng.uniform(0.01, 10.0)) for _ in range(n)]
        elif point_type == "maximum":
            eigs = [_r4(-self._rng.uniform(0.01, 10.0)) for _ in range(n)]
        else:
            eigs = []
            for _ in range(n):
                sign = self._rng.choice([-1, 1])
                eigs.append(_r4(sign * self._rng.uniform(0.01, 10.0)))
            # Ensure at least one positive and one negative
            if all(e > 0 for e in eigs):
                eigs[0] = _r4(-abs(eigs[0]))
            elif all(e < 0 for e in eigs):
                eigs[0] = _r4(abs(eigs[0]))

        if difficulty >= 7 and n >= 3:
            eigs[-1] = _r4(self._rng.uniform(-0.001, 0.001))

        return sorted(eigs)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate analysis steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"eigenvalues: {sd['eigenvalues']}",
            f"positive: {sd['n_pos']}, negative: {sd['n_neg']}, zero: {sd['n_zero']}",
            f"classification: {sd['classification']}",
            f"condition number: {sd['cond']}",
        ]
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the critical point classification.

        Args:
            sd: Solution data.

        Returns:
            Classification and condition number.
        """
        return f"{sd['classification']}, cond={sd['cond']}"


@register
class TransferLearningStrategyGenerator(StepGenerator):
    """Decide what to freeze, finetune, or retrain for transfer learning.

    Given source and target domain descriptions with a similarity metric,
    determines the optimal transfer strategy: freeze backbone, finetune
    specific layers, or retrain from scratch.

    Difficulty scaling:
        Difficulty 1-3: high similarity (freeze most).
        Difficulty 4-6: medium similarity (finetune top layers).
        Difficulty 7-8: low similarity (retrain most or all).
    """

    _DOMAINS = [
        "ImageNet natural images", "medical X-rays", "satellite imagery",
        "handwritten digits", "text documents", "audio spectrograms",
        "molecular structures", "financial time series",
    ]

    _STRATEGIES = {
        "high": {
            "freeze": "all convolutional/attention layers",
            "finetune": "final classification head only",
            "retrain": "none",
            "rationale": "domains are very similar, features transfer well",
        },
        "medium": {
            "freeze": "early layers (generic features)",
            "finetune": "later layers and classification head",
            "retrain": "none",
            "rationale": "partial feature overlap, later layers need adaptation",
        },
        "low": {
            "freeze": "none or first 1-2 layers",
            "finetune": "all layers with reduced learning rate",
            "retrain": "classification head from scratch",
            "rationale": "domain gap is large, most features do not transfer",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "transfer_learning_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["algorithm_design"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "decide transfer learning strategy for domain shift"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transfer learning strategy problem.

        Args:
            difficulty: Controls domain similarity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        source, target = self._rng.sample(self._DOMAINS, 2)
        similarity = _r4(self._rng.uniform(0.0, 1.0))

        if difficulty <= 3:
            similarity = _r4(self._rng.uniform(0.75, 0.95))
            level = "high"
        elif difficulty <= 6:
            similarity = _r4(self._rng.uniform(0.35, 0.74))
            level = "medium"
        else:
            similarity = _r4(self._rng.uniform(0.05, 0.34))
            level = "low"

        strategy = self._STRATEGIES[level]
        n_layers = self._rng.randint(6, 24)

        problem = (
            f"source={source}, target={target}, "
            f"similarity={similarity}, n_layers={n_layers}"
        )
        return problem, {
            "source": source, "target": target,
            "similarity": similarity, "level": level,
            "strategy": strategy, "n_layers": n_layers,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate strategy reasoning steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        s = sd["strategy"]
        return [
            f"domain similarity: {sd['similarity']} ({sd['level']})",
            f"freeze: {s['freeze']}",
            f"finetune: {s['finetune']}",
            f"retrain: {s['retrain']}",
            f"rationale: {s['rationale']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the recommended strategy.

        Args:
            sd: Solution data.

        Returns:
            Strategy summary as a string.
        """
        return f"{sd['level']} similarity: {sd['strategy']['finetune']}"


@register
class ExperimentDesignMLGenerator(StepGenerator):
    """Design an ablation study with variables, controls, and metrics.

    Given a research hypothesis about a model component, identifies
    independent variables, control conditions, evaluation metrics,
    and the appropriate statistical test.

    Difficulty scaling:
        Difficulty 1-3: single variable ablation.
        Difficulty 4-6: two variable ablation with interaction.
        Difficulty 7-8: full factorial design with multiple metrics.
    """

    _COMPONENTS = [
        ("attention mechanism", "with vs without attention", "paired t-test"),
        ("residual connections", "with vs without skip connections", "paired t-test"),
        ("dropout rate", "0.0, 0.1, 0.3, 0.5", "one-way ANOVA"),
        ("learning rate schedule", "constant, cosine, linear warmup", "one-way ANOVA"),
        ("normalisation type", "batch norm, layer norm, none", "one-way ANOVA"),
        ("activation function", "ReLU, GELU, SiLU", "one-way ANOVA"),
    ]

    _METRICS = ["accuracy", "loss", "F1-score", "training time", "convergence speed"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "experiment_design_ml"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hypothesis_design"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "design ablation study for model component"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an experiment design problem.

        Args:
            difficulty: Controls design complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_vars = 1
        elif difficulty <= 6:
            n_vars = 2
        else:
            n_vars = 2

        components = self._rng.sample(self._COMPONENTS, n_vars)
        metrics = self._rng.sample(self._METRICS, min(2 + difficulty // 3, 4))
        n_seeds = self._rng.randint(3, 5)

        variables = []
        for comp_name, levels, test in components:
            variables.append({
                "name": comp_name, "levels": levels, "test": test,
            })

        # Compute number of runs
        if n_vars == 1:
            n_levels = len(variables[0]["levels"].split(","))
            n_runs = n_levels * n_seeds
            stat_test = variables[0]["test"]
        else:
            levels_1 = len(variables[0]["levels"].split(","))
            levels_2 = len(variables[1]["levels"].split(","))
            n_runs = levels_1 * levels_2 * n_seeds
            stat_test = "two-way ANOVA"

        vars_str = "; ".join(v["name"] for v in variables)
        problem = f"ablation variables: {vars_str}, seeds={n_seeds}"
        return problem, {
            "variables": variables, "metrics": metrics,
            "n_seeds": n_seeds, "n_runs": n_runs,
            "stat_test": stat_test, "n_vars": n_vars,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate experiment design steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for v in sd["variables"]:
            steps.append(f"IV: {v['name']} levels=[{v['levels']}]")
        steps.append(f"metrics: {', '.join(sd['metrics'])}")
        steps.append(f"total runs: {sd['n_runs']} ({sd['n_seeds']} seeds each)")
        steps.append(f"statistical test: {sd['stat_test']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the experiment design summary.

        Args:
            sd: Solution data.

        Returns:
            Design summary as a string.
        """
        return f"{sd['n_runs']} runs, test={sd['stat_test']}"


@register
class ProofComplexityGenerator(StepGenerator):
    """Estimate proof complexity by counting lemmas, depth, and key insight.

    Given a theorem statement, identifies required lemmas, estimates
    the proof depth (number of logical steps), and pinpoints the key
    insight that makes the proof work.

    Difficulty scaling:
        Difficulty 1-3: simple proofs (2 lemmas, depth 3-4).
        Difficulty 4-6: moderate proofs (3 lemmas, depth 5-7).
        Difficulty 7-8: complex proofs (4+ lemmas, depth 8+).
    """

    _THEOREMS = {
        "triangle_inequality": {
            "statement": "|a+b| <= |a|+|b|",
            "lemmas": ["abs_nonneg", "square_both_sides"],
            "depth": 4,
            "key_insight": "squaring eliminates absolute values",
        },
        "am_gm_2": {
            "statement": "(a+b)/2 >= sqrt(ab) for a,b >= 0",
            "lemmas": ["nonneg_square", "expand_difference"],
            "depth": 3,
            "key_insight": "(a-b)^2 >= 0 rearranges to the result",
        },
        "euclid_primes": {
            "statement": "there are infinitely many primes",
            "lemmas": ["contradiction_assume_finite", "product_plus_one", "divisibility"],
            "depth": 6,
            "key_insight": "P=p1*p2*...*pn+1 is not divisible by any pi",
        },
        "sqrt2_irrational": {
            "statement": "sqrt(2) is irrational",
            "lemmas": ["contradiction_assume_rational", "even_square", "infinite_descent"],
            "depth": 7,
            "key_insight": "both p and q must be even, contradicting coprimality",
        },
        "cantor_diagonal": {
            "statement": "reals are uncountable",
            "lemmas": [
                "bijection_assumption", "diagonal_construction",
                "digit_differs", "contradiction",
            ],
            "depth": 8,
            "key_insight": "diagonal element differs from every listed element",
        },
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "proof_complexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["verify_proof"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "estimate proof complexity: lemmas, depth, key insight"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a proof complexity estimation problem.

        Args:
            difficulty: Controls theorem complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            candidates = ["triangle_inequality", "am_gm_2"]
        elif difficulty <= 6:
            candidates = ["euclid_primes", "sqrt2_irrational"]
        else:
            candidates = ["cantor_diagonal", "sqrt2_irrational", "euclid_primes"]

        name = self._rng.choice(candidates)
        thm = self._THEOREMS[name]
        n_lemmas = len(thm["lemmas"])

        problem = f"theorem: {thm['statement']}"
        return problem, {
            "name": name, "statement": thm["statement"],
            "lemmas": thm["lemmas"], "n_lemmas": n_lemmas,
            "depth": thm["depth"], "key_insight": thm["key_insight"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate complexity estimation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"required lemmas ({sd['n_lemmas']}): {', '.join(sd['lemmas'])}",
            f"proof depth: {sd['depth']} logical steps",
            f"key insight: {sd['key_insight']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the complexity estimate.

        Args:
            sd: Solution data.

        Returns:
            Complexity summary as a string.
        """
        return (
            f"lemmas={sd['n_lemmas']}, depth={sd['depth']}, "
            f"insight: {sd['key_insight']}"
        )


@register
class DebuggingStrategyGenerator(StepGenerator):
    """Diagnose ML training failures from observed symptoms.

    Given a training symptom (NaN loss, mode collapse, underfitting, etc.),
    identifies the root cause, lists diagnostic checks, and recommends
    a fix. Follows a decision tree approach.

    Difficulty scaling:
        Difficulty 1-3: common symptoms (NaN, underfitting).
        Difficulty 4-6: medium symptoms (overfitting, slow convergence).
        Difficulty 7-8: complex symptoms (mode collapse, gradient explosion).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "debugging_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 8

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["error_detection"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "diagnose training failure and recommend fix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a debugging strategy problem.

        Args:
            difficulty: Controls symptom complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            pool = ["nan_loss", "underfitting"]
        elif difficulty <= 6:
            pool = ["overfitting", "slow_convergence"]
        else:
            pool = ["mode_collapse", "gradient_explosion"]

        symptom_name = self._rng.choice(pool)
        symptom_data = _SYMPTOM_DB._SYMPTOMS[symptom_name]

        # Add random context
        lr = _r4(self._rng.uniform(0.0001, 0.1))
        epochs = self._rng.randint(5, 200)
        batch_size = self._rng.choice([16, 32, 64, 128])

        problem = (
            f"symptom: {symptom_name.replace('_', ' ')}, "
            f"lr={lr}, epochs={epochs}, batch_size={batch_size}"
        )
        return problem, {
            "symptom": symptom_name, "data": symptom_data,
            "lr": lr, "epochs": epochs, "batch_size": batch_size,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate diagnostic steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        d = sd["data"]
        steps = [f"root cause: {d['root_cause']}"]
        for check in d["checks"]:
            steps.append(f"check: {check}")
        steps.append(f"fix: {d['fix']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the diagnosis and fix.

        Args:
            sd: Solution data.

        Returns:
            Root cause and fix as a string.
        """
        return sd["data"]["fix"]


@register
class BenchmarkDesignGenerator(StepGenerator):
    """Design an evaluation benchmark with tasks, metrics, and baselines.

    Given a capability to evaluate, selects appropriate tasks, defines
    difficulty distribution, chooses metrics, establishes baselines,
    and determines statistical significance criteria.

    Difficulty scaling:
        Difficulty 1-3: 3 tasks, single metric.
        Difficulty 4-6: 4-5 tasks, multiple metrics.
        Difficulty 7-8: 6+ tasks, full statistical framework.
    """

    _CAPABILITIES = [
        "arithmetic reasoning", "logical deduction", "spatial reasoning",
        "language understanding", "code generation", "scientific reasoning",
        "multi-step planning", "analogical reasoning",
    ]

    _TASK_TEMPLATES = {
        "arithmetic reasoning": [
            "addition", "multiplication", "word problems",
            "fraction arithmetic", "equation solving", "estimation",
        ],
        "logical deduction": [
            "syllogisms", "truth tables", "constraint satisfaction",
            "propositional logic", "predicate logic", "puzzle solving",
        ],
        "spatial reasoning": [
            "rotation", "reflection", "path finding",
            "area computation", "volume computation", "coordinate geometry",
        ],
        "language understanding": [
            "sentiment analysis", "paraphrase detection", "NLI",
            "reading comprehension", "summarisation", "coreference",
        ],
        "code generation": [
            "function completion", "bug fixing", "test generation",
            "API usage", "algorithm implementation", "refactoring",
        ],
        "scientific reasoning": [
            "hypothesis testing", "experimental design", "data interpretation",
            "causal reasoning", "dimensional analysis", "unit conversion",
        ],
        "multi-step planning": [
            "task decomposition", "scheduling", "resource allocation",
            "dependency ordering", "constraint planning", "goal reasoning",
        ],
        "analogical reasoning": [
            "word analogies", "visual analogies", "relational mapping",
            "proportional reasoning", "structural alignment", "transfer",
        ],
    }

    _METRICS = [
        "accuracy", "exact match", "F1-score", "BLEU",
        "pass@k", "mean reciprocal rank",
    ]

    _BASELINES = [
        "random", "majority class", "GPT-2 small", "T5-base",
        "human performance", "retrieval-based",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "benchmark_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 9

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["method_selection"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "design evaluation benchmark with tasks, metrics, and baselines"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a benchmark design problem.

        Args:
            difficulty: Controls benchmark scope.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        capability = self._rng.choice(self._CAPABILITIES)
        all_tasks = self._TASK_TEMPLATES.get(capability, self._TASK_TEMPLATES["arithmetic reasoning"])

        if difficulty <= 3:
            n_tasks = 3
            n_metrics = 1
        elif difficulty <= 6:
            n_tasks = min(len(all_tasks), self._rng.randint(4, 5))
            n_metrics = 2
        else:
            n_tasks = min(len(all_tasks), self._rng.randint(5, 6))
            n_metrics = 3

        tasks = self._rng.sample(all_tasks, n_tasks)
        metrics = self._rng.sample(self._METRICS, n_metrics)
        baselines = self._rng.sample(self._BASELINES, min(3, 2 + difficulty // 3))

        # Difficulty distribution: easy/medium/hard percentages
        easy_pct = self._rng.randint(20, 40)
        hard_pct = self._rng.randint(15, 30)
        med_pct = 100 - easy_pct - hard_pct

        # Statistical significance
        alpha = self._rng.choice([0.01, 0.05])
        n_samples = self._rng.choice([100, 200, 500, 1000]) * max(1, difficulty)

        problem = f"evaluate: {capability}, budget={n_samples} samples"
        return problem, {
            "capability": capability, "tasks": tasks,
            "metrics": metrics, "baselines": baselines,
            "easy_pct": easy_pct, "med_pct": med_pct, "hard_pct": hard_pct,
            "alpha": alpha, "n_samples": n_samples, "n_tasks": n_tasks,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate benchmark design steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"tasks ({sd['n_tasks']}): {', '.join(sd['tasks'])}",
            f"difficulty split: easy={sd['easy_pct']}%, med={sd['med_pct']}%, hard={sd['hard_pct']}%",
            f"metrics: {', '.join(sd['metrics'])}",
            f"baselines: {', '.join(sd['baselines'])}",
            f"significance: alpha={sd['alpha']}, n={sd['n_samples']}",
        ]
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the benchmark design summary.

        Args:
            sd: Solution data.

        Returns:
            Benchmark summary as a string.
        """
        return (
            f"{sd['n_tasks']} tasks, "
            f"metrics=[{', '.join(sd['metrics'])}], "
            f"alpha={sd['alpha']}"
        )
