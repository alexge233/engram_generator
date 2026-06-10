"""Extended tier 10 generators (batch 2) -- deeper self-architecture tasks.

6 generators for self-improvement proposals, compute budget allocation,
evaluation metric design, data augmentation strategy, objective function
critique, and architecture ablation design. All tier 10.
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


# ── 1. Self-improvement proposal (tier 10) ────────────────────────


@register
class SelfImprovementProposeGenerator(StepGenerator):
    """Propose an architectural modification to address a model weakness.

    Given a specific weakness observed in a model (e.g., fails on length
    generalisation, poor calibration), proposes a concrete architectural
    change with justification.

    Input format:
        ``model weakness: fails on length generalisation. propose fix``

    Target format:
        ``weakness: fails on sequences longer than training length <step>
        root cause: absolute positional encoding cannot extrapolate <step>
        proposal: replace absolute PE with ALiBi (linear bias) <step>
        mechanism: attention score decays linearly with distance,
        no learned positions <step> expected improvement: handles
        sequences 2-4x training length without retraining``

    Difficulty scaling:
        Difficulty 1-3: well-known fixes (PE, normalisation).
        Difficulty 4-6: architectural changes (attention variants).
        Difficulty 7-8: novel compositions of techniques.

    Prerequisites:
        architecture_analysis.
    """

    _WEAKNESSES = [
        {
            "weakness": "fails on sequences longer than training length",
            "root_cause": "absolute positional encoding cannot extrapolate beyond trained positions",
            "proposal": "replace absolute PE with ALiBi (linear attention bias)",
            "mechanism": "attention score decays linearly with distance; no learned positions needed",
            "expected": "handles sequences 2-4x training length without retraining",
        },
        {
            "weakness": "poor calibration: confident on wrong answers",
            "root_cause": "cross-entropy loss encourages overconfident predictions",
            "proposal": "add label smoothing (epsilon=0.1) and temperature scaling at inference",
            "mechanism": "smoothing prevents logit saturation; temperature rescales to calibrated probabilities",
            "expected": "expected calibration error (ECE) decreases by 30-50%",
        },
        {
            "weakness": "catastrophic forgetting when fine-tuning on new tasks",
            "root_cause": "unconstrained gradient updates overwrite previously learned features",
            "proposal": "use elastic weight consolidation (EWC) or LoRA for parameter-efficient tuning",
            "mechanism": "EWC penalises changes to important weights; LoRA adds low-rank adapters without modifying base",
            "expected": "retains >95% of prior task accuracy while learning new task",
        },
        {
            "weakness": "attention entropy collapses in deep layers (all heads attend to same tokens)",
            "root_cause": "residual stream dominates; deep heads learn redundant patterns",
            "proposal": "add head diversity loss: penalise pairwise cosine similarity of attention patterns",
            "mechanism": "auxiliary loss term: L_div = sum_ij cos(A_i, A_j) / (h*(h-1)), added with weight 0.01",
            "expected": "attention entropy increases by 20-40%, downstream accuracy improves 1-3%",
        },
        {
            "weakness": "slow convergence on sparse reward tasks",
            "root_cause": "gradient signal from reward is too infrequent for credit assignment",
            "proposal": "add auxiliary prediction head for next-state prediction (self-supervised signal)",
            "mechanism": "dense self-supervised gradients keep representations useful between reward signals",
            "expected": "sample efficiency improves 2-5x on sparse reward benchmarks",
        },
        {
            "weakness": "model size grows linearly with number of tasks",
            "root_cause": "separate parameters per task with no sharing",
            "proposal": "use mixture of experts (MoE) with shared routing and task-specific expert subsets",
            "mechanism": "top-k routing selects 2 of N experts per token; experts are shared across tasks",
            "expected": "parameter efficiency improves 4-8x while maintaining per-task accuracy",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "self_improvement_propose"

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
            difficulty: Controls weakness complexity.

        Returns:
            Natural language description.
        """
        return "propose architectural modification to address model weakness"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a self-improvement proposal problem.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (weakness_description, solution_data).
        """
        pool = self._WEAKNESSES[:max(2, min(len(self._WEAKNESSES), 1 + difficulty))]
        scenario = self._rng.choice(pool)
        d_model = self._rng.choice([256, 512, 768, 1024])
        layers = self._rng.randint(6, 24)
        problem = (f"weakness: {scenario['weakness']} "
                   f"(model: d={d_model}, L={layers})")
        return problem, dict(scenario)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate proposal reasoning steps.

        Args:
            data: Solution data with root cause and proposal.

        Returns:
            Steps showing analysis and proposed fix.
        """
        return [
            f"root cause: {data['root_cause']}",
            f"proposal: {data['proposal']}",
            f"mechanism: {data['mechanism']}",
            f"expected improvement: {data['expected']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the proposed modification.

        Args:
            data: Solution data.

        Returns:
            Proposal string.
        """
        return data["proposal"]


# ── 2. Compute budget allocation (tier 10) ────────────────────────


@register
class ComputeBudgetAllocateGenerator(StepGenerator):
    """Allocate a fixed compute budget between model size, data, and steps.

    Given a total compute budget in FLOPs, uses the Chinchilla scaling
    laws (L ~ N^{-0.076} * D^{-0.095}) to determine optimal allocation
    between model parameters (N), data tokens (D), and training steps.

    Input format:
        ``allocate C FLOPs optimally between model size and data``

    Target format:
        ``budget: 10^20 FLOPs <step>
        scaling law: L ~ N^{-0.076} * D^{-0.095} <step>
        constraint: C = 6*N*D (approximate) <step>
        optimal ratio: D/N ~ 0.076/0.095 ~ 0.8 <step>
        solve: N = sqrt(C / (6 * 0.8)) <step>
        N = 1.44e9 params, D = 1.15e10 tokens``

    Difficulty scaling:
        Difficulty 1-3: simple budget, round numbers.
        Difficulty 4-6: larger budgets, verify ratio.
        Difficulty 7-8: compare two budget allocations.

    Prerequisites:
        scaling_prediction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "compute_budget_allocate"

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
            difficulty: Controls budget size.

        Returns:
            Natural language description.
        """
        return "allocate compute budget optimally between model size and data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a compute budget allocation problem.

        Uses the approximation C = 6*N*D and the Chinchilla optimal
        ratio D/N = alpha_N / alpha_D where alpha_N=0.076, alpha_D=0.095.

        Args:
            difficulty: Controls budget magnitude.

        Returns:
            Tuple of (budget_description, solution_data).
        """
        exponent = self._rng.randint(17, 21) + difficulty
        coefficient = self._rng.choice([1.0, 2.0, 5.0])
        budget_flops = coefficient * (10 ** exponent)

        alpha_n = 0.076
        alpha_d = 0.095
        ratio = _r4(alpha_n / alpha_d)

        # C = 6*N*D and D = ratio * N => C = 6 * ratio * N^2
        n_optimal = _r4(math.sqrt(budget_flops / (6.0 * ratio)))
        d_optimal = _r4(ratio * n_optimal)

        # Compute expected loss at this allocation
        loss = _r4(n_optimal ** (-alpha_n) * d_optimal ** (-alpha_d))

        problem = f"budget: {coefficient:.0f}e{exponent} FLOPs"
        return problem, {
            "budget_flops": budget_flops,
            "exponent": exponent,
            "coefficient": coefficient,
            "alpha_n": alpha_n,
            "alpha_d": alpha_d,
            "ratio": ratio,
            "n_optimal": n_optimal,
            "d_optimal": d_optimal,
            "loss": loss,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate budget allocation reasoning steps.

        Args:
            data: Solution data with optimal allocation.

        Returns:
            Steps showing scaling law application.
        """
        return [
            f"scaling law: L ~ N^{{-{data['alpha_n']}}} * D^{{-{data['alpha_d']}}}",
            f"constraint: C = 6*N*D = {data['coefficient']:.0f}e{data['exponent']}",
            f"optimal D/N ratio: {data['alpha_n']}/{data['alpha_d']} = {data['ratio']}",
            f"N_opt = sqrt(C / (6 * {data['ratio']})) = {data['n_optimal']:.4e}",
            f"D_opt = {data['ratio']} * N = {data['d_optimal']:.4e}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the optimal allocation.

        Args:
            data: Solution data.

        Returns:
            Allocation string.
        """
        return f"N={data['n_optimal']:.4e}, D={data['d_optimal']:.4e}"


# ── 3. Evaluation metric design (tier 10) ─────────────────────────


@register
class EvaluationMetricDesignGenerator(StepGenerator):
    """Design an evaluation metric for a specific model capability.

    Given a capability to evaluate (reasoning depth, generalisation,
    robustness, calibration), designs a concrete metric with definition,
    measurement procedure, and interpretation.

    Input format:
        ``design evaluation metric for reasoning depth``

    Target format:
        ``capability: reasoning depth <step>
        definition: fraction of multi-step problems solved correctly
        as a function of number of reasoning steps required <step>
        measurement: generate problems requiring 1-10 steps, plot
        accuracy vs steps <step> metric: area under the accuracy-vs-steps
        curve (AUC_depth) <step> interpretation: higher AUC_depth
        means model maintains accuracy on deeper reasoning chains``

    Difficulty scaling:
        Difficulty 1-3: simple accuracy-based metrics.
        Difficulty 4-6: distribution-aware metrics.
        Difficulty 7-8: multi-faceted composite metrics.

    Prerequisites:
        training_diagnosis.
    """

    _CAPABILITIES = [
        {
            "capability": "reasoning depth",
            "definition": "fraction of multi-step problems solved vs number of steps required",
            "measurement": "generate problems requiring 1..K steps, measure accuracy at each K",
            "metric": "AUC_depth = area under accuracy-vs-steps curve, normalised to [0,1]",
            "interpretation": "higher AUC_depth means model sustains accuracy on deeper reasoning",
        },
        {
            "capability": "length generalisation",
            "definition": "accuracy on sequences of length L relative to training length L_train",
            "measurement": "evaluate on L = {1x, 2x, 4x, 8x} * L_train, record accuracy at each",
            "metric": "half-life L_50 = length at which accuracy drops to 50% of L_train performance",
            "interpretation": "larger L_50 means better extrapolation beyond training distribution",
        },
        {
            "capability": "calibration",
            "definition": "agreement between predicted confidence and empirical accuracy",
            "measurement": "bin predictions by confidence, compute |accuracy - confidence| per bin",
            "metric": "ECE = sum(|acc_bin - conf_bin| * n_bin/N) over B bins",
            "interpretation": "lower ECE means predictions are better calibrated",
        },
        {
            "capability": "robustness to input perturbation",
            "definition": "accuracy retention when inputs are perturbed by noise of magnitude epsilon",
            "measurement": "add Gaussian noise with sigma = {0.01, 0.05, 0.1, 0.5} to inputs",
            "metric": "robustness score = min(epsilon) where accuracy drops below 90% of clean accuracy",
            "interpretation": "higher robustness score means model tolerates more perturbation",
        },
        {
            "capability": "compositional generalisation",
            "definition": "accuracy on novel compositions of known primitives",
            "measurement": "train on primitives A,B,C; test on compositions AB, BC, ABC",
            "metric": "composition gap = accuracy(primitives) - accuracy(compositions)",
            "interpretation": "smaller gap means model composes primitives effectively",
        },
        {
            "capability": "sample efficiency",
            "definition": "performance as a function of training examples seen",
            "measurement": "train with {100, 1K, 10K, 100K} examples, measure final accuracy",
            "metric": "learning rate = slope of accuracy vs log(n_samples) in linear region",
            "interpretation": "steeper learning rate means model extracts more from each example",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "evaluation_metric_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls capability complexity.

        Returns:
            Natural language description.
        """
        return "design an evaluation metric for a model capability"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an evaluation metric design problem.

        Args:
            difficulty: Controls capability pool.

        Returns:
            Tuple of (capability_description, solution_data).
        """
        pool = self._CAPABILITIES[:max(2, min(len(self._CAPABILITIES), 1 + difficulty))]
        cap = self._rng.choice(pool)
        problem = f"capability to evaluate: {cap['capability']}"
        return problem, dict(cap)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate metric design steps.

        Args:
            data: Solution data with metric definition.

        Returns:
            Steps showing design process.
        """
        return [
            f"definition: {data['definition']}",
            f"measurement: {data['measurement']}",
            f"metric: {data['metric']}",
            f"interpretation: {data['interpretation']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the designed metric.

        Args:
            data: Solution data.

        Returns:
            Metric description.
        """
        return data["metric"]


# ── 4. Data augmentation strategy (tier 10) ───────────────────────


@register
class DataAugmentationStrategyGenerator(StepGenerator):
    """Design a data augmentation strategy to cover a training gap.

    Given a description of what is underrepresented in the training
    distribution, designs a concrete augmentation strategy with
    generation method, diversity controls, and validation approach.

    Input format:
        ``design augmentation for underrepresented distribution``

    Target format:
        ``gap: model fails on negated statements <step>
        diagnosis: training data has 3x more affirmative than negated <step>
        strategy: for each affirmative example, generate negation
        using template: 'X is Y' -> 'X is not Y' <step>
        diversity: vary negation words (not, never, no, neither) <step>
        validation: check augmented distribution is balanced to within 10%``

    Difficulty scaling:
        Difficulty 1-3: simple balancing strategies.
        Difficulty 4-6: compositional augmentation.
        Difficulty 7-8: adversarial augmentation.

    Prerequisites:
        training_diagnosis.
    """

    _GAPS = [
        {
            "gap": "model fails on negated logical statements",
            "diagnosis": "training data has 3x more affirmative than negated examples",
            "strategy": "template-based negation: 'X is Y' -> 'X is not Y', vary negation words",
            "diversity": "use {not, never, no, neither, nor}; apply to 50% of affirmative examples",
            "validation": "check negated fraction is between 40-60% of total",
        },
        {
            "gap": "model struggles with multi-digit arithmetic beyond 4 digits",
            "diagnosis": "95% of training arithmetic uses 1-3 digit numbers",
            "strategy": "generate uniform random arithmetic with digit counts 1-8 weighted equally",
            "diversity": "balance across operations (+, -, *, /); include carry/borrow cases",
            "validation": "verify accuracy is within 5% across all digit counts 1-8",
        },
        {
            "gap": "model misclassifies rare classes (< 1% of training data)",
            "diagnosis": "class imbalance: top 3 classes have 80% of examples",
            "strategy": "oversample rare classes using SMOTE-like interpolation in embedding space",
            "diversity": "interpolate between k=5 nearest neighbours; add Gaussian noise sigma=0.05",
            "validation": "augmented dataset has each class within 2x of mean class frequency",
        },
        {
            "gap": "model fails on paraphrased instructions",
            "diagnosis": "instructions are templated with low linguistic diversity",
            "strategy": "back-translate instructions through 3 languages (DE, FR, ZH) and back",
            "diversity": "keep all paraphrases that preserve semantic equivalence (verified by entailment model)",
            "validation": "measure accuracy on held-out paraphrase test set; target > 90% of original",
        },
        {
            "gap": "model overfits to specific input orderings",
            "diagnosis": "set-valued inputs always presented in sorted order during training",
            "strategy": "randomly permute input elements for each training example",
            "diversity": "generate k=5 random permutations per example during each epoch",
            "validation": "test on reversed and shuffled orderings; accuracy gap < 3%",
        },
        {
            "gap": "model cannot handle missing or incomplete inputs",
            "diagnosis": "training data has no missing values; real data has 5-15% missing",
            "strategy": "randomly mask 5-20% of input features during training with [MASK] token",
            "diversity": "vary masking rate per example; mask contiguous and random spans",
            "validation": "test with 10% masking; accuracy should be within 5% of complete input",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "data_augmentation_strategy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["training_diagnosis"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls gap complexity.

        Returns:
            Natural language description.
        """
        return "design data augmentation strategy for a training gap"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a data augmentation strategy problem.

        Args:
            difficulty: Controls gap pool.

        Returns:
            Tuple of (gap_description, solution_data).
        """
        pool = self._GAPS[:max(2, min(len(self._GAPS), 1 + difficulty))]
        gap = self._rng.choice(pool)
        problem = f"gap: {gap['gap']}; diagnosis: {gap['diagnosis']}"
        return problem, dict(gap)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate augmentation strategy steps.

        Args:
            data: Solution data with strategy details.

        Returns:
            Steps showing diagnosis, strategy, and validation.
        """
        return [
            f"gap: {data['gap'][:60]}",
            f"strategy: {data['strategy'][:60]}",
            f"validation: {data['validation'][:60]}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the augmentation strategy.

        Args:
            data: Solution data.

        Returns:
            Strategy summary.
        """
        return data["strategy"]


# ── 5. Objective function critique (tier 10) ──────────────────────


@register
class ObjectiveFunctionCritiqueGenerator(StepGenerator):
    """Identify failure modes in a given loss function and suggest fixes.

    Given a loss function formulation, identifies potential failure modes
    such as gradient vanishing, mode collapse, reward hacking, or
    training instability. Suggests concrete modifications.

    Input format:
        ``critique this loss function``

    Target format:
        ``loss: L = -E[log p(y|x)] + beta * KL(q||p) <step>
        failure mode 1: if beta too large, KL dominates and model
        ignores reconstruction <step>
        failure mode 2: posterior collapse: q converges to prior,
        latent is unused <step>
        fix: use beta-annealing: start beta=0, linearly increase
        to 1 over K steps <step> alternative: use free-bits:
        KL >= lambda per dimension``

    Difficulty scaling:
        Difficulty 1-3: single clear failure mode.
        Difficulty 4-6: two interacting failure modes.
        Difficulty 7-8: subtle failure modes requiring analysis.

    Prerequisites:
        loss_design.
    """

    _LOSSES = [
        {
            "loss_formula": "L = -E[log p(y|x)] + beta * KL(q(z|x) || p(z))",
            "name": "VAE ELBO",
            "failure_modes": [
                "beta too large: KL dominates, model ignores reconstruction",
                "posterior collapse: q converges to prior, latent z is unused",
            ],
            "fix": "beta-annealing: start beta=0, linearly increase to 1 over warmup steps",
            "alternative": "free-bits: enforce KL >= lambda per latent dimension",
        },
        {
            "loss_formula": "L = E[log D(x)] + E[log(1-D(G(z)))]",
            "name": "GAN minimax",
            "failure_modes": [
                "mode collapse: generator produces limited variety of outputs",
                "vanishing gradients: when D is too strong, G gets no useful gradient",
            ],
            "fix": "use Wasserstein distance with gradient penalty instead of JS divergence",
            "alternative": "add diversity loss: penalise low pairwise distance in generator outputs",
        },
        {
            "loss_formula": "L = MSE(y, y_hat) + lambda * ||W||_2^2",
            "name": "ridge regression",
            "failure_modes": [
                "lambda too large: underfits by shrinking all weights toward zero",
                "lambda too small: overfits, regularisation has no effect",
            ],
            "fix": "cross-validate lambda on held-out set; use log-scale grid search",
            "alternative": "use elastic net: combine L1 and L2 for sparse + shrinkage",
        },
        {
            "loss_formula": "L = -sum(r_t * log pi(a_t|s_t))",
            "name": "REINFORCE policy gradient",
            "failure_modes": [
                "high variance: raw returns make gradient estimates noisy",
                "reward hacking: agent exploits loopholes in reward signal",
            ],
            "fix": "subtract learned baseline b(s) to reduce variance: L = -sum((r_t - b(s_t)) * log pi)",
            "alternative": "use PPO: clip probability ratio to prevent large policy updates",
        },
        {
            "loss_formula": "L = CE(y, softmax(z/T)) where T is temperature",
            "name": "knowledge distillation",
            "failure_modes": [
                "T too high: soft targets become uniform, no information transferred",
                "T too low: soft targets are identical to hard labels, no benefit from teacher",
            ],
            "fix": "tune T in {2, 4, 8, 16} by validation accuracy; typically T=4 works well",
            "alternative": "use feature distillation: match intermediate representations, not just outputs",
        },
        {
            "loss_formula": "L = alpha * L_task + (1-alpha) * L_aux",
            "name": "multi-task with fixed weights",
            "failure_modes": [
                "gradient dominance: one loss has much larger gradients, dominates updates",
                "conflicting gradients: tasks push parameters in opposite directions",
            ],
            "fix": "use GradNorm to dynamically balance gradient magnitudes across tasks",
            "alternative": "use PCGrad: project conflicting gradients to resolve interference",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "objective_function_critique"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["loss_design"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls loss complexity.

        Returns:
            Natural language description.
        """
        return "critique this loss function and identify failure modes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an objective function critique problem.

        Args:
            difficulty: Controls loss pool.

        Returns:
            Tuple of (loss_formula, solution_data).
        """
        pool = self._LOSSES[:max(2, min(len(self._LOSSES), 1 + difficulty))]
        loss = self._rng.choice(pool)
        problem = f"loss: {loss['loss_formula']} ({loss['name']})"
        return problem, dict(loss)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate critique reasoning steps.

        Args:
            data: Solution data with failure modes and fixes.

        Returns:
            Steps showing failure mode analysis and proposed fixes.
        """
        steps = [f"loss: {data['loss_formula'][:60]}"]
        for i, fm in enumerate(data["failure_modes"][:2]):
            steps.append(f"mode {i + 1}: {fm[:50]}")
        steps.append(f"fix: {data['fix'][:60]}")
        steps.append(f"alternative: {data['alternative']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the primary fix.

        Args:
            data: Solution data.

        Returns:
            Fix description.
        """
        return data["fix"]


# ── 6. Architecture ablation design (tier 10) ────────────────────


@register
class ArchitectureAblationDesignGenerator(StepGenerator):
    """Design an ablation study for a neural architecture.

    Given an architecture with multiple components, designs what to
    remove or replace, what to measure, proper controls, and baselines
    to establish the contribution of each component.

    Input format:
        ``design ablation study for this architecture``

    Target format:
        ``architecture: transformer with RoPE + GQA + SwiGLU FFN <step>
        component 1 (RoPE): replace with learned absolute PE <step>
        component 2 (GQA): replace with standard MHA <step>
        component 3 (SwiGLU): replace with standard FFN (ReLU) <step>
        measurements: validation loss, throughput (tokens/sec), memory <step>
        controls: same total params, same training data and schedule <step>
        baselines: full model vs each single-component ablation``

    Difficulty scaling:
        Difficulty 1-3: 2-component ablation.
        Difficulty 4-6: 3-component ablation with interactions.
        Difficulty 7-8: 4+ components, combinatorial ablation.

    Prerequisites:
        architecture_analysis.
    """

    _ARCHITECTURES = [
        {
            "name": "transformer with RoPE + GQA + SwiGLU FFN",
            "components": [
                {"name": "RoPE", "ablation": "replace with learned absolute PE",
                 "rationale": "isolate benefit of rotary position encoding"},
                {"name": "GQA", "ablation": "replace with standard MHA (same d_model)",
                 "rationale": "measure KV-cache savings vs accuracy trade-off"},
                {"name": "SwiGLU FFN", "ablation": "replace with ReLU FFN (same hidden dim)",
                 "rationale": "quantify gated activation benefit"},
            ],
            "measurements": "validation loss, throughput (tokens/sec), peak memory (GB)",
            "controls": "same total parameters, identical data, schedule, and hyperparameters",
        },
        {
            "name": "vision transformer with patch embedding + cls token + layer scale",
            "components": [
                {"name": "patch embedding", "ablation": "replace with conv stem (3 conv layers)",
                 "rationale": "compare linear projection vs learned hierarchical features"},
                {"name": "cls token", "ablation": "replace with global average pooling",
                 "rationale": "measure cls token necessity for classification"},
                {"name": "layer scale", "ablation": "remove (set scale=1.0 for all layers)",
                 "rationale": "quantify training stability contribution"},
            ],
            "measurements": "top-1 accuracy, training stability (loss variance), convergence speed",
            "controls": "same model size, same augmentation, same training epochs",
        },
        {
            "name": "recurrent model with memory + halting + gating",
            "components": [
                {"name": "external memory", "ablation": "remove memory read/write, use only hidden state",
                 "rationale": "measure explicit memory contribution"},
                {"name": "adaptive halting", "ablation": "replace with fixed iteration count",
                 "rationale": "isolate benefit of dynamic compute allocation"},
                {"name": "gating mechanism", "ablation": "remove gates, use direct addition",
                 "rationale": "quantify selective information flow benefit"},
            ],
            "measurements": "task accuracy, average iterations used, gate entropy",
            "controls": "same parameter budget, same training data and optimiser",
        },
        {
            "name": "diffusion model with U-Net + time embedding + self-attention",
            "components": [
                {"name": "self-attention in U-Net", "ablation": "remove attention blocks, keep only convolutions",
                 "rationale": "measure long-range dependency modelling benefit"},
                {"name": "sinusoidal time embedding", "ablation": "replace with learned time embedding",
                 "rationale": "compare inductive bias of sinusoidal vs learned"},
                {"name": "skip connections", "ablation": "remove U-Net skip connections",
                 "rationale": "isolate multi-scale feature reuse contribution"},
            ],
            "measurements": "FID score, sample diversity (recall), training convergence (steps to FID < 50)",
            "controls": "same number of parameters, same noise schedule, same dataset",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "architecture_ablation_design"

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
            difficulty: Controls architecture complexity.

        Returns:
            Natural language description.
        """
        return "design an ablation study for this architecture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ablation study design problem.

        Args:
            difficulty: Controls architecture pool.

        Returns:
            Tuple of (architecture_description, solution_data).
        """
        pool = self._ARCHITECTURES[:max(2, min(len(self._ARCHITECTURES), 1 + difficulty))]
        arch = self._rng.choice(pool)
        problem = f"architecture: {arch['name']}"
        return problem, dict(arch)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ablation design steps.

        Args:
            data: Solution data with components and measurements.

        Returns:
            Steps showing each ablation and experimental controls.
        """
        steps = [f"model: {data['name']}"]
        for comp in data["components"][:3]:
            steps.append(f"ablate: {comp['name']}")
        steps.append(f"runs: {1 + len(data['components'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the ablation study summary.

        Args:
            data: Solution data.

        Returns:
            Summary of ablation design.
        """
        names = [c["name"] for c in data["components"]]
        return f"ablate: {', '.join(names)}; measure: {data['measurements']}"
