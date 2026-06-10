"""Deep ML optimization and training dynamics task generators.

10 generators across tiers 4-6 covering SGD with momentum, Adam
optimiser, cosine LR schedule, mixup training, knowledge distillation,
gradient accumulation, normalisation comparison, sparse attention,
model FLOP computation, and loss function comparison.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fv(vec: list[float]) -> str:
    """Format a vector as a compact string.

    Args:
        vec: List of floats.

    Returns:
        Bracket-enclosed comma-separated string.
    """
    return "[" + ",".join(str(v) for v in vec) + "]"


# ===================================================================
# 1. SGD Momentum Step (tier 5)
# ===================================================================

@register
class SGDMomentumStepGenerator(StepGenerator):
    """Compute SGD with momentum velocity accumulation over 3 steps.

    v_t = beta * v_{t-1} + (1 - beta) * grad_t.
    w_t = w_{t-1} - lr * v_t.

    Difficulty scaling:
        Difficulty 1-3: 1D weight, integer gradients.
        Difficulty 4-6: 2D weight, decimal gradients.
        Difficulty 7-8: 3D weight, decimal gradients.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sgd_momentum_step"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute SGD with momentum over 3 steps"

    def _dim(self, difficulty: int) -> int:
        """Map difficulty to weight dimension.

        Args:
            difficulty: Difficulty level.

        Returns:
            Weight dimension (1-3).
        """
        if difficulty <= 3:
            return 1
        if difficulty <= 6:
            return 2
        return 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate weight, gradients, and compute 3 momentum steps.

        Args:
            difficulty: Controls dimension and value type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim = self._dim(difficulty)
        lr = self._rng.choice([0.01, 0.05, 0.1])
        beta = self._rng.choice([0.9, 0.8, 0.95])

        if difficulty <= 3:
            w = [float(self._rng.randint(-3, 3)) for _ in range(dim)]
            grads = [[float(self._rng.randint(-5, 5)) for _ in range(dim)]
                     for _ in range(3)]
        else:
            w = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]
            grads = [[round(self._rng.uniform(-3.0, 3.0), 2)
                      for _ in range(dim)] for _ in range(3)]

        v = [0.0] * dim
        trace = []
        w_curr = list(w)
        for t in range(3):
            v_new = [round(beta * v[i] + (1 - beta) * grads[t][i], 4)
                     for i in range(dim)]
            w_new = [round(w_curr[i] - lr * v_new[i], 4)
                     for i in range(dim)]
            trace.append({"v": list(v_new), "w": list(w_new)})
            v = v_new
            w_curr = w_new

        g_strs = ", ".join(f"g{i+1}={_fv(g)}" for i, g in enumerate(grads))
        problem = (
            f"SGD-M: w0={_fv(w)}, lr={lr}, beta={beta}, {g_strs}"
        )
        return problem, {
            "w0": w, "lr": lr, "beta": beta, "grads": grads,
            "trace": trace, "dim": dim,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-step velocity and weight update steps.

        Args:
            data: Solution data with trace of 3 steps.

        Returns:
            Steps showing velocity and weight at each step.
        """
        steps: list[str] = [
            f"lr={data['lr']}, beta={data['beta']}, w0={_fv(data['w0'])}"
        ]
        for t, entry in enumerate(data["trace"]):
            steps.append(
                f"t={t+1}: v={_fv(entry['v'])}, w={_fv(entry['w'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final weight after 3 steps.

        Args:
            data: Solution data.

        Returns:
            String representation of final weight vector.
        """
        return f"w3={_fv(data['trace'][-1]['w'])}"


# ===================================================================
# 2. Adam Full Step (tier 5)
# ===================================================================

@register
class AdamFullStepGenerator(StepGenerator):
    """Compute one Adam optimiser update step.

    m = b1*m + (1-b1)*g, v = b2*v + (1-b2)*g^2,
    m_hat = m/(1-b1^t), v_hat = v/(1-b2^t),
    w -= lr * m_hat / (sqrt(v_hat) + eps).

    Difficulty scaling:
        Difficulty 1-3: 1D weight, step t=1.
        Difficulty 4-6: 2D weight, step t=2.
        Difficulty 7-8: 2D weight, step t=3.

    Prerequisites:
        division.
    """

    _EPS = 1e-8

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "adam_full_step"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute one Adam optimiser update step"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to dimension and step number.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (dim, step_t).
        """
        if difficulty <= 3:
            return 1, 1
        if difficulty <= 6:
            return 2, 2
        return 2, 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate weight, gradient, and compute Adam update.

        Args:
            difficulty: Controls dimension and step.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim, t = self._config(difficulty)
        lr = self._rng.choice([0.001, 0.01, 0.0001])
        b1, b2 = 0.9, 0.999

        w = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]
        g = [round(self._rng.uniform(-3.0, 3.0), 2) for _ in range(dim)]

        # Previous moments (zero for t=1, random for t>1)
        if t == 1:
            m_prev = [0.0] * dim
            v_prev = [0.0] * dim
        else:
            m_prev = [round(self._rng.uniform(-1.0, 1.0), 4)
                       for _ in range(dim)]
            v_prev = [round(self._rng.uniform(0.01, 1.0), 4)
                       for _ in range(dim)]

        m_new = [round(b1 * m_prev[i] + (1 - b1) * g[i], 4)
                 for i in range(dim)]
        v_new = [round(b2 * v_prev[i] + (1 - b2) * g[i] ** 2, 4)
                 for i in range(dim)]
        m_hat = [round(m_new[i] / (1 - b1 ** t), 4) for i in range(dim)]
        v_hat = [round(v_new[i] / (1 - b2 ** t), 4) for i in range(dim)]
        w_new = [round(w[i] - lr * m_hat[i] / (math.sqrt(v_hat[i]) + self._EPS), 4)
                 for i in range(dim)]

        problem = (
            f"Adam: w={_fv(w)}, g={_fv(g)}, t={t}, lr={lr}"
        )
        return problem, {
            "w": w, "g": g, "t": t, "lr": lr, "b1": b1, "b2": b2,
            "m_prev": m_prev, "v_prev": v_prev,
            "m_new": m_new, "v_new": v_new,
            "m_hat": m_hat, "v_hat": v_hat, "w_new": w_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Adam update computation steps.

        Args:
            data: Solution data with moments and updates.

        Returns:
            Steps showing m, v, bias correction, and weight update.
        """
        return [
            f"m={_fv(data['m_new'])}, v={_fv(data['v_new'])}",
            f"m_hat={_fv(data['m_hat'])}, v_hat={_fv(data['v_hat'])}",
            f"w_new={_fv(data['w_new'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the updated weight vector.

        Args:
            data: Solution data.

        Returns:
            String representation of updated weights.
        """
        return f"w={_fv(data['w_new'])}"


# ===================================================================
# 3. Cosine LR Schedule (tier 4)
# ===================================================================

@register
class CosineLRScheduleGenerator(StepGenerator):
    """Compute cosine annealing learning rate at a given step.

    lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * t / T)).

    Difficulty scaling:
        Difficulty 1-3: Compute at 1 step, T <= 100.
        Difficulty 4-6: Compute at 2 steps, T <= 500.
        Difficulty 7-8: Compute at 3 steps, T <= 1000.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cosine_lr_schedule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute cosine annealing learning rate at given step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate LR schedule parameters and compute LR at steps.

        Args:
            difficulty: Controls number of query steps and T.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lr_max = self._rng.choice([0.001, 0.01, 0.1])
        lr_min = self._rng.choice([0.0, 1e-5, 1e-4])

        if difficulty <= 3:
            total = self._rng.choice([50, 100])
            n_query = 1
        elif difficulty <= 6:
            total = self._rng.choice([200, 500])
            n_query = 2
        else:
            total = self._rng.choice([500, 1000])
            n_query = 3

        query_steps = sorted(
            self._rng.sample(range(0, total + 1), min(n_query, total + 1))
        )
        results = []
        for t in query_steps:
            cos_val = math.cos(math.pi * t / total)
            lr = round(lr_min + 0.5 * (lr_max - lr_min) * (1 + cos_val), 4)
            results.append((t, lr))

        problem = (
            f"cosine\\_lr: lr\\_max={lr_max}, lr\\_min={lr_min}, T={total}"
        )
        return problem, {
            "lr_max": lr_max, "lr_min": lr_min, "total": total,
            "results": results,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-step LR computation steps.

        Args:
            data: Solution data with query steps and results.

        Returns:
            Steps showing LR at each query step.
        """
        steps: list[str] = [
            f"lr_max={data['lr_max']}, lr_min={data['lr_min']}, T={data['total']}"
        ]
        for t, lr in data["results"]:
            cos_val = round(math.cos(math.pi * t / data["total"]), 4)
            steps.append(
                f"t={t}: cos(pi*{t}/{data['total']})={cos_val}, lr={lr}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the LR values at query steps.

        Args:
            data: Solution data.

        Returns:
            String with step:lr pairs.
        """
        parts = [f"t={t}:lr={lr}" for t, lr in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 4. Mixup Training (tier 5)
# ===================================================================

@register
class MixupTrainingGenerator(StepGenerator):
    """Compute mixup data augmentation for a pair of samples.

    x_mix = lambda * x_i + (1 - lambda) * x_j.
    y_mix = lambda * y_i + (1 - lambda) * y_j.

    Difficulty scaling:
        Difficulty 1-3: 2D features, 2-class one-hot labels.
        Difficulty 4-6: 3D features, 3-class one-hot labels.
        Difficulty 7-8: 4D features, 4-class one-hot labels.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mixup_training"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute mixup augmentation for a pair of samples"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to feature dim and number of classes.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (feat_dim, n_classes).
        """
        if difficulty <= 3:
            return 2, 2
        if difficulty <= 6:
            return 3, 3
        return 4, 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two samples and compute their mixup.

        Args:
            difficulty: Controls feature dim and classes.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        feat_dim, n_cls = self._config(difficulty)
        lam = round(self._rng.uniform(0.1, 0.9), 2)

        x_i = [round(self._rng.uniform(-2.0, 3.0), 2) for _ in range(feat_dim)]
        x_j = [round(self._rng.uniform(-2.0, 3.0), 2) for _ in range(feat_dim)]

        cls_i = self._rng.randint(0, n_cls - 1)
        cls_j = self._rng.randint(0, n_cls - 1)
        y_i = [1.0 if k == cls_i else 0.0 for k in range(n_cls)]
        y_j = [1.0 if k == cls_j else 0.0 for k in range(n_cls)]

        x_mix = [round(lam * x_i[d] + (1 - lam) * x_j[d], 4)
                 for d in range(feat_dim)]
        y_mix = [round(lam * y_i[c] + (1 - lam) * y_j[c], 4)
                 for c in range(n_cls)]

        problem = (
            f"mixup: x_i={_fv(x_i)}, x_j={_fv(x_j)}, "
            f"y_i={_fv(y_i)}, y_j={_fv(y_j)}, lam={lam}"
        )
        return problem, {
            "x_i": x_i, "x_j": x_j, "y_i": y_i, "y_j": y_j,
            "lam": lam, "x_mix": x_mix, "y_mix": y_mix,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mixup computation steps.

        Args:
            data: Solution data with mixed samples.

        Returns:
            Steps showing x_mix and y_mix computation.
        """
        return [
            f"lambda={data['lam']}",
            f"x_mix={data['lam']}*{_fv(data['x_i'])}+{round(1-data['lam'],2)}*{_fv(data['x_j'])}={_fv(data['x_mix'])}",
            f"y_mix={data['lam']}*{_fv(data['y_i'])}+{round(1-data['lam'],2)}*{_fv(data['y_j'])}={_fv(data['y_mix'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mixed sample and label.

        Args:
            data: Solution data.

        Returns:
            String representation of mixed x and y.
        """
        return f"x_mix={_fv(data['x_mix'])}, y_mix={_fv(data['y_mix'])}"


# ===================================================================
# 5. Knowledge Distillation (tier 6)
# ===================================================================

@register
class KnowledgeDistillationGenerator(StepGenerator):
    """Compute knowledge distillation loss with soft targets.

    L = alpha * CE(y, p_student) + (1-alpha) * T^2 * KL(soft_teacher, soft_student).
    Soft targets: softmax(logits / T).

    Difficulty scaling:
        Difficulty 1-3: 2-class, T=2.
        Difficulty 4-6: 3-class, T=3.
        Difficulty 7-8: 4-class, T=4.

    Prerequisites:
        cross_entropy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "knowledge_distillation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cross_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute knowledge distillation loss with soft targets"

    def _softmax_t(self, logits: list[float], temp: float) -> list[float]:
        """Compute temperature-scaled softmax.

        Args:
            logits: Raw logit values.
            temp: Temperature parameter.

        Returns:
            Probability distribution rounded to 4 dp.
        """
        scaled = [l / temp for l in logits]
        mx = max(scaled)
        exps = [math.exp(s - mx) for s in scaled]
        total = sum(exps)
        return [round(e / total, 4) for e in exps]

    def _config(self, difficulty: int) -> tuple[int, float]:
        """Map difficulty to number of classes and temperature.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_classes, temperature).
        """
        if difficulty <= 3:
            return 2, 2.0
        if difficulty <= 6:
            return 3, 3.0
        return 4, 4.0

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate logits and compute distillation loss.

        Args:
            difficulty: Controls number of classes and temperature.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_cls, temp = self._config(difficulty)
        alpha = round(self._rng.uniform(0.3, 0.7), 2)

        teacher_logits = [round(self._rng.uniform(-2.0, 3.0), 2)
                          for _ in range(n_cls)]
        student_logits = [round(self._rng.uniform(-2.0, 3.0), 2)
                          for _ in range(n_cls)]
        true_label = self._rng.randint(0, n_cls - 1)

        soft_teacher = self._softmax_t(teacher_logits, temp)
        soft_student = self._softmax_t(student_logits, temp)
        hard_student = self._softmax_t(student_logits, 1.0)

        # Hard CE loss: -log(p_student[true_label])
        ce_hard = round(-math.log(max(hard_student[true_label], 1e-10)), 4)

        # KL divergence: sum p_teacher * log(p_teacher / p_student)
        kl_div = 0.0
        for i in range(n_cls):
            if soft_teacher[i] > 0:
                kl_div += soft_teacher[i] * math.log(
                    max(soft_teacher[i], 1e-10) / max(soft_student[i], 1e-10)
                )
        kl_div = round(kl_div, 4)

        loss = round(alpha * ce_hard + (1 - alpha) * temp ** 2 * kl_div, 4)

        problem = (
            f"KD: teacher={_fv(teacher_logits)}, "
            f"student={_fv(student_logits)}, label={true_label}, "
            f"T={temp}, alpha={alpha}"
        )
        return problem, {
            "teacher_logits": teacher_logits,
            "student_logits": student_logits,
            "true_label": true_label, "temp": temp, "alpha": alpha,
            "soft_teacher": soft_teacher, "soft_student": soft_student,
            "hard_student": hard_student,
            "ce_hard": ce_hard, "kl_div": kl_div, "loss": loss,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate distillation loss computation steps.

        Args:
            data: Solution data with soft targets and losses.

        Returns:
            Steps showing soft targets, CE, KL, and total loss.
        """
        return [
            f"soft_teacher={_fv(data['soft_teacher'])}",
            f"soft_student={_fv(data['soft_student'])}",
            f"CE(hard)=-log({data['hard_student'][data['true_label']]})={data['ce_hard']}",
            f"KL(soft)={data['kl_div']}",
            f"L={data['alpha']}*{data['ce_hard']}+{round(1-data['alpha'],2)}*{data['temp']}^2*{data['kl_div']}={data['loss']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the distillation loss.

        Args:
            data: Solution data.

        Returns:
            Loss value as a string.
        """
        return f"L={data['loss']}"


# ===================================================================
# 6. Gradient Accumulation (tier 4)
# ===================================================================

@register
class GradientAccumulationGenerator(StepGenerator):
    """Compute effective batch size and averaged gradient.

    Effective batch = micro_batch * accumulation_steps.
    Averaged gradient = sum(grads) / accumulation_steps.

    Difficulty scaling:
        Difficulty 1-3: 2 accumulation steps, 1D gradient.
        Difficulty 4-6: 3-4 accumulation steps, 2D gradient.
        Difficulty 7-8: 4-6 accumulation steps, 3D gradient.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gradient_accumulation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute effective batch size and averaged gradient"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to accumulation steps and gradient dim.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (accum_steps, dim).
        """
        if difficulty <= 3:
            return 2, 1
        if difficulty <= 6:
            return self._rng.randint(3, 4), 2
        return self._rng.randint(4, 6), 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate micro-batch gradients and compute effective update.

        Args:
            difficulty: Controls accumulation steps and gradient dim.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        accum, dim = self._config(difficulty)
        micro_batch = self._rng.choice([4, 8, 16, 32])
        lr = self._rng.choice([0.001, 0.01, 0.1])

        grads = [[round(self._rng.uniform(-2.0, 2.0), 2)
                   for _ in range(dim)] for _ in range(accum)]

        eff_batch = micro_batch * accum
        avg_grad = [round(sum(grads[s][d] for s in range(accum)) / accum, 4)
                    for d in range(dim)]
        eff_lr = round(lr * accum, 4)

        g_strs = ", ".join(f"g{i+1}={_fv(g)}" for i, g in enumerate(grads))
        problem = (
            f"grad\\_accum: micro={micro_batch}, steps={accum}, "
            f"lr={lr}, {g_strs}"
        )
        return problem, {
            "micro_batch": micro_batch, "accum": accum, "lr": lr,
            "grads": grads, "eff_batch": eff_batch,
            "avg_grad": avg_grad, "eff_lr": eff_lr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gradient accumulation computation steps.

        Args:
            data: Solution data with gradients and effective values.

        Returns:
            Steps showing effective batch, averaged gradient, and LR.
        """
        return [
            f"eff_batch={data['micro_batch']}*{data['accum']}={data['eff_batch']}",
            f"avg_grad=sum(grads)/{data['accum']}={_fv(data['avg_grad'])}",
            f"eff_lr={data['lr']}*{data['accum']}={data['eff_lr']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the effective batch, averaged gradient, and LR.

        Args:
            data: Solution data.

        Returns:
            String with effective values.
        """
        return (
            f"eff_batch={data['eff_batch']}, "
            f"avg_grad={_fv(data['avg_grad'])}"
        )


# ===================================================================
# 7. Normalisation Comparison (tier 5)
# ===================================================================

@register
class NormalisationComparisonGenerator(StepGenerator):
    """Compute BatchNorm, LayerNorm, and InstanceNorm on a tensor.

    BatchNorm: normalise over batch dimension.
    LayerNorm: normalise over feature dimension.
    InstanceNorm: normalise over spatial dimension.
    Given a [B, C, H] tensor, compute each normalisation.

    Difficulty scaling:
        Difficulty 1-3: [2, 2, 2] tensor.
        Difficulty 4-6: [2, 2, 3] tensor.
        Difficulty 7-8: [2, 3, 3] tensor.

    Prerequisites:
        arithmetic_mean.
    """

    _EPS = 1e-5

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "normalization_comparison"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["arithmetic_mean"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute BatchNorm, LayerNorm, and InstanceNorm"

    def _shape(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to tensor shape [B, C, H].

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (batch, channels, spatial).
        """
        if difficulty <= 3:
            return 2, 2, 2
        if difficulty <= 6:
            return 2, 2, 3
        return 2, 3, 3

    def _norm(self, vals: list[float]) -> list[float]:
        """Normalise a list of values to zero mean, unit variance.

        Args:
            vals: Input values.

        Returns:
            Normalised values rounded to 4 dp.
        """
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        sigma = math.sqrt(var + self._EPS)
        return [round((v - mu) / sigma, 4) for v in vals]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate tensor and compute all three normalisations.

        Args:
            difficulty: Controls tensor shape.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        b, c, h = self._shape(difficulty)
        tensor = [[[round(self._rng.uniform(-2.0, 3.0), 2)
                     for _ in range(h)]
                    for _ in range(c)]
                   for _ in range(b)]

        # LayerNorm: normalise over C*H for each batch element
        ln_result = []
        for bi in range(b):
            flat = [tensor[bi][ci][hi] for ci in range(c) for hi in range(h)]
            normed = self._norm(flat)
            row = []
            idx = 0
            for ci in range(c):
                ch_vals = []
                for hi in range(h):
                    ch_vals.append(normed[idx])
                    idx += 1
                row.append(ch_vals)
            ln_result.append(row)

        # InstanceNorm: normalise over H for each (batch, channel) pair
        in_result = []
        for bi in range(b):
            row = []
            for ci in range(c):
                normed = self._norm(tensor[bi][ci])
                row.append(normed)
            in_result.append(row)

        # BatchNorm: normalise over B for each (channel, spatial) position
        bn_result = [[[0.0] * h for _ in range(c)] for _ in range(b)]
        for ci in range(c):
            for hi in range(h):
                vals = [tensor[bi][ci][hi] for bi in range(b)]
                normed = self._norm(vals)
                for bi in range(b):
                    bn_result[bi][ci][hi] = normed[bi]

        # Format compact: just show first batch element
        t_str = str(tensor)
        problem = f"norm: tensor[{b},{c},{h}]={t_str}"
        return problem, {
            "tensor": tensor, "b": b, "c": c, "h": h,
            "bn": bn_result, "ln": ln_result, "in_": in_result,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate normalisation comparison steps.

        Args:
            data: Solution data with all three normalisations.

        Returns:
            Steps showing first batch element of each normalisation.
        """
        steps: list[str] = [
            f"shape=[{data['b']},{data['c']},{data['h']}]"
        ]
        steps.append(f"BN[0]={data['bn'][0]}")
        steps.append(f"LN[0]={data['ln'][0]}")
        steps.append(f"IN[0]={data['in_'][0]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return first batch element of each normalisation.

        Args:
            data: Solution data.

        Returns:
            String with BN, LN, IN for batch element 0.
        """
        return f"BN[0]={data['bn'][0]}, LN[0]={data['ln'][0]}, IN[0]={data['in_'][0]}"


# ===================================================================
# 8. Sparse Attention (tier 6)
# ===================================================================

@register
class SparseAttentionGenerator(StepGenerator):
    """Compute local and strided sparse attention patterns.

    Local: each position i attends to positions max(0,i-w)..min(n-1,i+w).
    Strided: each position i attends to every s-th position.
    Report which positions each token attends to.

    Difficulty scaling:
        Difficulty 1-3: n=6 tokens, window w=1, stride s=2.
        Difficulty 4-6: n=8 tokens, window w=2, stride s=2.
        Difficulty 7-8: n=10 tokens, window w=2, stride s=3.

    Prerequisites:
        attention_score.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sparse_attention"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["attention_score"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute local and strided sparse attention patterns"

    def _config(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to sequence length, window, and stride.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (n_tokens, window, stride).
        """
        if difficulty <= 3:
            return 6, 1, 2
        if difficulty <= 6:
            return 8, 2, 2
        return 10, 2, 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate attention patterns for local and strided modes.

        Args:
            difficulty: Controls sequence length and pattern params.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, w, s = self._config(difficulty)

        local_pattern = {}
        for i in range(n):
            lo = max(0, i - w)
            hi = min(n - 1, i + w)
            local_pattern[i] = list(range(lo, hi + 1))

        strided_pattern = {}
        for i in range(n):
            positions = list(range(i % s, n, s))
            if i not in positions:
                positions.append(i)
                positions.sort()
            strided_pattern[i] = positions

        local_count = sum(len(v) for v in local_pattern.values())
        strided_count = sum(len(v) for v in strided_pattern.values())
        full_count = n * n

        problem = f"sparse\\_attn: n={n}, window={w}, stride={s}"
        return problem, {
            "n": n, "w": w, "s": s,
            "local": local_pattern, "strided": strided_pattern,
            "local_count": local_count, "strided_count": strided_count,
            "full_count": full_count,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate sparse attention pattern steps.

        Args:
            data: Solution data with patterns and counts.

        Returns:
            Steps showing patterns for first few positions and counts.
        """
        steps: list[str] = []
        show = min(3, data["n"])
        for i in range(show):
            steps.append(
                f"pos {i}: local={data['local'][i]}, "
                f"strided={data['strided'][i]}"
            )
        steps.append(
            f"local entries={data['local_count']}/{data['full_count']}, "
            f"strided entries={data['strided_count']}/{data['full_count']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the sparsity ratios.

        Args:
            data: Solution data.

        Returns:
            String with local and strided sparsity.
        """
        local_ratio = round(data["local_count"] / data["full_count"], 4)
        strided_ratio = round(data["strided_count"] / data["full_count"], 4)
        return (
            f"local_ratio={local_ratio}, strided_ratio={strided_ratio}"
        )


# ===================================================================
# 9. Model FLOPs Compute (tier 5)
# ===================================================================

@register
class ModelFlopsComputeGenerator(StepGenerator):
    """Compute total FLOPs for a simple transformer architecture.

    Dense layer: 2 * in_dim * out_dim.
    Attention: 2 * n^2 * d + 2 * n * d^2.
    Sum FLOPs across layers.

    Difficulty scaling:
        Difficulty 1-3: 1 dense layer only.
        Difficulty 4-6: 1 attention + 1 dense layer.
        Difficulty 7-8: 2 attention + 2 dense layers.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "model_flops_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute total FLOPs for a model architecture"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate architecture and compute total FLOPs.

        Args:
            difficulty: Controls number and type of layers.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        layers = []
        total_flops = 0

        if difficulty <= 3:
            in_d = self._rng.choice([64, 128, 256])
            out_d = self._rng.choice([64, 128, 256])
            flops = 2 * in_d * out_d
            layers.append({"type": "dense", "in": in_d, "out": out_d,
                           "flops": flops})
            total_flops += flops
        elif difficulty <= 6:
            n = self._rng.choice([32, 64, 128])
            d = self._rng.choice([32, 64])
            attn_flops = 2 * n * n * d + 2 * n * d * d
            layers.append({"type": "attn", "n": n, "d": d,
                           "flops": attn_flops})
            total_flops += attn_flops
            in_d = d
            out_d = self._rng.choice([128, 256])
            dense_flops = 2 * in_d * out_d
            layers.append({"type": "dense", "in": in_d, "out": out_d,
                           "flops": dense_flops})
            total_flops += dense_flops
        else:
            n = self._rng.choice([64, 128])
            d = self._rng.choice([64, 128])
            for _ in range(2):
                attn_flops = 2 * n * n * d + 2 * n * d * d
                layers.append({"type": "attn", "n": n, "d": d,
                               "flops": attn_flops})
                total_flops += attn_flops
                ff_in = d
                ff_out = d * 4
                dense_flops = 2 * ff_in * ff_out
                layers.append({"type": "dense", "in": ff_in, "out": ff_out,
                               "flops": dense_flops})
                total_flops += dense_flops

        layer_strs = []
        for la in layers:
            if la["type"] == "attn":
                layer_strs.append(f"attn(n={la['n']},d={la['d']})")
            else:
                layer_strs.append(f"dense({la['in']},{la['out']})")

        problem = f"FLOPs: {', '.join(layer_strs)}"
        return problem, {
            "layers": layers, "total_flops": total_flops,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-layer FLOP computation steps.

        Args:
            data: Solution data with layers and FLOPs.

        Returns:
            Steps showing each layer's FLOP count.
        """
        steps: list[str] = []
        for i, la in enumerate(data["layers"]):
            if la["type"] == "attn":
                steps.append(
                    f"attn: 2*{la['n']}^2*{la['d']}+2*{la['n']}*{la['d']}^2"
                    f"={la['flops']}"
                )
            else:
                steps.append(
                    f"dense: 2*{la['in']}*{la['out']}={la['flops']}"
                )
        steps.append(f"total={data['total_flops']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total FLOPs.

        Args:
            data: Solution data.

        Returns:
            Total FLOPs as a string.
        """
        return f"total_flops={data['total_flops']}"


# ===================================================================
# 10. Loss Function Comparison (tier 5)
# ===================================================================

@register
class LossFunctionComparisonGenerator(StepGenerator):
    """Compute MSE, MAE, and Huber loss for predictions vs targets.

    MSE = mean((y - yhat)^2).
    MAE = mean(|y - yhat|).
    Huber = 0.5*x^2 if |x| < delta else delta*|x| - 0.5*delta^2.

    Difficulty scaling:
        Difficulty 1-3: 3-element vectors, integer values.
        Difficulty 4-6: 4-element vectors, decimal values.
        Difficulty 7-8: 5-element vectors, decimal values.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loss_function_comparison"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute MSE, MAE, and Huber loss"

    def _dim(self, difficulty: int) -> int:
        """Map difficulty to vector dimension.

        Args:
            difficulty: Difficulty level.

        Returns:
            Vector dimension (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate predictions and targets, compute all three losses.

        Args:
            difficulty: Controls vector dimension and value type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._dim(difficulty)
        delta = self._rng.choice([0.5, 1.0, 1.5])

        if difficulty <= 3:
            y = [float(self._rng.randint(-3, 5)) for _ in range(n)]
            yhat = [float(self._rng.randint(-3, 5)) for _ in range(n)]
        else:
            y = [round(self._rng.uniform(-3.0, 5.0), 2) for _ in range(n)]
            yhat = [round(self._rng.uniform(-3.0, 5.0), 2) for _ in range(n)]

        residuals = [round(y[i] - yhat[i], 4) for i in range(n)]
        sq_errors = [round(r ** 2, 4) for r in residuals]
        abs_errors = [round(abs(r), 4) for r in residuals]

        mse = round(sum(sq_errors) / n, 4)
        mae = round(sum(abs_errors) / n, 4)

        huber_terms = []
        for r in residuals:
            a = abs(r)
            if a < delta:
                huber_terms.append(round(0.5 * r ** 2, 4))
            else:
                huber_terms.append(round(delta * a - 0.5 * delta ** 2, 4))
        huber = round(sum(huber_terms) / n, 4)

        problem = (
            f"loss: y={_fv(y)}, yhat={_fv(yhat)}, delta={delta}"
        )
        return problem, {
            "y": y, "yhat": yhat, "delta": delta, "n": n,
            "residuals": residuals, "mse": mse, "mae": mae,
            "huber": huber, "huber_terms": huber_terms,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate loss computation steps.

        Args:
            data: Solution data with residuals and losses.

        Returns:
            Steps showing residuals, MSE, MAE, and Huber.
        """
        return [
            f"residuals={_fv(data['residuals'])}",
            f"MSE=mean(r^2)={data['mse']}",
            f"MAE=mean(|r|)={data['mae']}",
            f"Huber(delta={data['delta']})={data['huber']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return all three loss values.

        Args:
            data: Solution data.

        Returns:
            String with MSE, MAE, and Huber values.
        """
        return f"MSE={data['mse']}, MAE={data['mae']}, Huber={data['huber']}"
