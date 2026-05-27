"""AI/ML curriculum generators -- optimisation, losses, neural net math, RL, and evaluation.

Covers gradient-based optimisation, loss functions, neural network
operations, reinforcement learning fundamentals, information theory,
Markov decision processes, and model evaluation metrics.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class VectorHelper:
    """Utility for generating small float vectors used across AI/ML generators.

    Produces reproducible random vectors with controlled magnitude and
    precision, suitable for demonstrating optimisation and loss computations.

    Attributes:
        _rng: Random number generator shared from the parent generator.
    """

    def __init__(self, rng) -> None:
        """Initialise with a shared random number generator.

        Args:
            rng: A random.Random instance for reproducibility.
        """
        self._rng = rng

    def float_vector(self, size: int, lo: float, hi: float,
                     decimals: int = 2) -> list[float]:
        """Generate a vector of rounded random floats.

        Args:
            size: Number of elements.
            lo: Lower bound (inclusive).
            hi: Upper bound (inclusive).
            decimals: Decimal places for rounding.

        Returns:
            List of rounded floats.
        """
        return [round(self._rng.uniform(lo, hi), decimals) for _ in range(size)]

    def positive_vector(self, size: int, lo: float = 0.1,
                        hi: float = 2.0) -> list[float]:
        """Generate a vector of positive floats.

        Args:
            size: Number of elements.
            lo: Lower bound.
            hi: Upper bound.

        Returns:
            List of positive rounded floats.
        """
        return self.float_vector(size, lo, hi)


class ProbabilityHelper:
    """Utility for generating valid probability distributions.

    Ensures distributions sum to 1.0 and all elements are positive,
    using Dirichlet-style normalisation from uniform draws.

    Attributes:
        _rng: Random number generator shared from the parent generator.
    """

    def __init__(self, rng) -> None:
        """Initialise with a shared random number generator.

        Args:
            rng: A random.Random instance for reproducibility.
        """
        self._rng = rng

    def distribution(self, size: int, min_prob: float = 0.05) -> list[float]:
        """Generate a valid probability distribution summing to 1.0.

        Args:
            size: Number of categories.
            min_prob: Minimum probability per category.

        Returns:
            List of probabilities summing to 1.0.
        """
        raw = [self._rng.uniform(min_prob, 1.0) for _ in range(size)]
        total = sum(raw)
        normed = [round(x / total, 4) for x in raw]
        return self._fix_sum(normed)

    def _fix_sum(self, probs: list[float]) -> list[float]:
        """Adjust the last element so probabilities sum to exactly 1.0.

        Args:
            probs: Probability list that may not sum to exactly 1.0.

        Returns:
            Adjusted list summing to 1.0.
        """
        diff = round(1.0 - sum(probs), 4)
        probs[-1] = round(probs[-1] + diff, 4)
        return probs


@register
class GradientDescentGenerator(StepGenerator):
    """One step of vanilla gradient descent: w' = w - lr * dL/dw.

    Generates a weight vector and gradient vector, then shows the
    element-wise update w_i' = w_i - lr * g_i for each dimension.
    Uses small learning rates (0.01-0.1) and 2-4 element vectors.

    Input format:
        ``perform one step of gradient descent``

    Target format:
        ``w=[0.5,0.3], g=[0.2,-0.1], lr=0.1 <step>
        w_0'=0.5-0.1*0.2=0.48 <step>
        w_1'=0.3-0.1*-0.1=0.31 <step> [0.48,0.31]``

    Difficulty scaling:
        Difficulty 1-3: 2-element vectors, lr=0.1.
        Difficulty 4-6: 3-element vectors, lr=0.01.
        Difficulty 7-8: 4-element vectors, lr=0.001.

    Prerequisites:
        derivative_eval.

    Example:
        >>> gen = GradientDescentGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gradient_descent'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gradient_descent"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size and learning rate.

        Returns:
            Natural language description.
        """
        return "perform one step of gradient descent"

    def _vector_size(self, difficulty: int) -> int:
        """Map difficulty to weight vector dimensionality.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of dimensions (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _learning_rate(self, difficulty: int) -> float:
        """Map difficulty to learning rate.

        Args:
            difficulty: Difficulty level.

        Returns:
            Learning rate value.
        """
        if difficulty <= 3:
            return 0.1
        if difficulty <= 6:
            return 0.01
        return 0.001

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate weight and gradient vectors for one GD step.

        Args:
            difficulty: Controls vector size and learning rate.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        vh = VectorHelper(self._rng)
        n = self._vector_size(difficulty)
        lr = self._learning_rate(difficulty)
        w = vh.float_vector(n, -2.0, 2.0)
        g = vh.float_vector(n, -1.0, 1.0)
        w_new = [round(w[i] - lr * g[i], 4) for i in range(n)]

        w_str = ",".join(str(v) for v in w)
        g_str = ",".join(str(v) for v in g)
        problem = f"w'=w-\\alpha \\nabla L, w=[{w_str}], g=[{g_str}], \\alpha={lr}"
        return problem, {"w": w, "g": g, "lr": lr, "w_new": w_new, "n": n}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element weight update steps.

        Args:
            data: Solution data with weights, gradients, and lr.

        Returns:
            Steps showing each w_i' = w_i - lr * g_i.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            wi = data["w"][i]
            gi = data["g"][i]
            lr = data["lr"]
            wi_new = data["w_new"][i]
            steps.append(f"w_{i}'={wi}-{lr}*{gi}={wi_new}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated weight vector.

        Args:
            data: Solution data.

        Returns:
            String representation of new weights.
        """
        return "[" + ",".join(str(v) for v in data["w_new"]) + "]"


@register
class MomentumSGDGenerator(StepGenerator):
    """SGD with momentum: v = beta*v + grad, w = w - lr*v.

    Generates weight, gradient, and velocity vectors, then shows
    the two-phase update: velocity accumulation followed by the
    weight update. Uses beta=0.9 for momentum coefficient.

    Input format:
        ``compute one step of SGD with momentum``

    Target format:
        ``w=[1.0,0.5], g=[0.3,-0.2], v=[0.1,0.0], lr=0.01, beta=0.9
        <step> v_0=0.9*0.1+0.3=0.39 <step> v_1=0.9*0.0+-0.2=-0.2
        <step> w_0'=1.0-0.01*0.39=0.9961 <step>
        w_1'=0.5-0.01*-0.2=0.502 <step> [0.9961,0.502]``

    Difficulty scaling:
        Difficulty 1-3: 2-element vectors.
        Difficulty 4-6: 3-element vectors.
        Difficulty 7-8: 4-element vectors.

    Prerequisites:
        gradient_descent.

    Example:
        >>> gen = MomentumSGDGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'momentum_sgd'
    """

    _BETA = 0.9
    _LR = 0.01

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "momentum_sgd"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["gradient_descent"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size.

        Returns:
            Natural language description.
        """
        return "compute one step of SGD with momentum"

    def _vector_size(self, difficulty: int) -> int:
        """Map difficulty to vector dimensionality.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of dimensions (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate vectors for one momentum SGD step.

        Args:
            difficulty: Controls vector size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        vh = VectorHelper(self._rng)
        n = self._vector_size(difficulty)
        w = vh.float_vector(n, -2.0, 2.0)
        g = vh.float_vector(n, -1.0, 1.0)
        v = vh.float_vector(n, -0.5, 0.5)

        v_new = [round(self._BETA * v[i] + g[i], 4) for i in range(n)]
        w_new = [round(w[i] - self._LR * v_new[i], 4) for i in range(n)]

        w_s = ",".join(str(x) for x in w)
        g_s = ",".join(str(x) for x in g)
        v_s = ",".join(str(x) for x in v)
        problem = (
            f"v=\\beta v+g, w'=w-\\alpha v, "
            f"w=[{w_s}], g=[{g_s}], v=[{v_s}], "
            f"\\alpha={self._LR}, \\beta={self._BETA}"
        )
        return problem, {
            "w": w, "g": g, "v": v, "v_new": v_new,
            "w_new": w_new, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate velocity and weight update steps.

        Args:
            data: Solution data with all vectors.

        Returns:
            Steps showing v update then w update per element.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            vi = data["v"][i]
            gi = data["g"][i]
            vi_new = data["v_new"][i]
            steps.append(f"v_{i}={self._BETA}*{vi}+{gi}={vi_new}")
        for i in range(data["n"]):
            wi = data["w"][i]
            vi_new = data["v_new"][i]
            wi_new = data["w_new"][i]
            steps.append(f"w_{i}'={wi}-{self._LR}*{vi_new}={wi_new}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated weight vector.

        Args:
            data: Solution data.

        Returns:
            String representation of new weights.
        """
        return "[" + ",".join(str(v) for v in data["w_new"]) + "]"


@register
class AdamOptimizerGenerator(StepGenerator):
    """One step of Adam optimiser with bias correction.

    Shows the full Adam update: first moment (m), second moment (v),
    bias-corrected estimates, and the final weight update. Uses
    standard hyperparameters beta1=0.9, beta2=0.999, eps=1e-8.

    Input format:
        ``compute one step of Adam optimiser``

    Target format:
        ``g=0.5, m=0.1, v=0.01, t=3 <step>
        m=0.9*0.1+(1-0.9)*0.5=0.14 <step>
        v=0.999*0.01+(1-0.999)*0.25=0.01024 <step>
        m_hat=0.14/(1-0.9^3)=0.5185 <step>
        v_hat=0.01024/(1-0.999^3)=3.424 <step>
        w'=w-0.001*0.5185/(sqrt(3.424)+1e-8)``

    Difficulty scaling:
        Difficulty 1-3: 1 weight (scalar).
        Difficulty 4-6: 2 weights.
        Difficulty 7-8: 3 weights.

    Prerequisites:
        momentum_sgd.

    Example:
        >>> gen = AdamOptimizerGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'adam_step'
    """

    _BETA1 = 0.9
    _BETA2 = 0.999
    _EPS = 1e-8
    _LR = 0.001

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "adam_step"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["momentum_sgd"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of weights.

        Returns:
            Natural language description.
        """
        return "compute one step of Adam optimiser"

    def _num_weights(self, difficulty: int) -> int:
        """Map difficulty to number of scalar weights.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of weights (1-3).
        """
        if difficulty <= 3:
            return 1
        if difficulty <= 6:
            return 2
        return 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Adam optimiser state for one update step.

        Args:
            difficulty: Controls number of weights.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        vh = VectorHelper(self._rng)
        n = self._num_weights(difficulty)
        t = self._rng.randint(1, 10)
        w = vh.float_vector(n, -2.0, 2.0)
        g = vh.float_vector(n, -1.0, 1.0)
        m = vh.float_vector(n, -0.3, 0.3)
        v = vh.positive_vector(n, 0.001, 0.1)

        results = self._compute_updates(w, g, m, v, t, n)
        problem = self._format_problem(w, g, m, v, t)
        results["n"] = n
        return problem, results

    def _compute_updates(self, w: list[float], g: list[float],
                         m: list[float], v: list[float],
                         t: int, n: int) -> dict:
        """Compute all Adam intermediate values.

        Args:
            w: Current weights.
            g: Gradients.
            m: First moment estimates.
            v: Second moment estimates.
            t: Time step.
            n: Number of weights.

        Returns:
            Dict with all intermediate and final values.
        """
        m_new = [round(self._BETA1 * m[i] + (1 - self._BETA1) * g[i], 4) for i in range(n)]
        v_new = [round(self._BETA2 * v[i] + (1 - self._BETA2) * g[i] ** 2, 6) for i in range(n)]
        bc1 = round(1 - self._BETA1 ** t, 6)
        bc2 = round(1 - self._BETA2 ** t, 6)
        m_hat = [round(m_new[i] / bc1, 4) for i in range(n)]
        v_hat = [round(v_new[i] / bc2, 6) for i in range(n)]
        w_new = [round(w[i] - self._LR * m_hat[i] / (math.sqrt(v_hat[i]) + self._EPS), 4) for i in range(n)]
        return {
            "w": w, "g": g, "m": m, "v": v, "t": t,
            "m_new": m_new, "v_new": v_new,
            "bc1": bc1, "bc2": bc2,
            "m_hat": m_hat, "v_hat": v_hat, "w_new": w_new,
        }

    def _format_problem(self, w: list[float], g: list[float],
                        m: list[float], v: list[float], t: int) -> str:
        """Format the problem statement in LaTeX.

        Args:
            w: Current weights.
            g: Gradients.
            m: First moment estimates.
            v: Second moment estimates.
            t: Time step.

        Returns:
            LaTeX-formatted problem string.
        """
        w_s = ",".join(str(x) for x in w)
        g_s = ",".join(str(x) for x in g)
        m_s = ",".join(str(x) for x in m)
        v_s = ",".join(str(x) for x in v)
        return (
            f"Adam: w=[{w_s}], g=[{g_s}], m=[{m_s}], v=[{v_s}], "
            f"t={t}, \\beta_1={self._BETA1}, \\beta_2={self._BETA2}"
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate moment update, bias correction, and weight steps.

        Args:
            data: Solution data with all intermediates.

        Returns:
            Steps showing m, v, bias correction, and weight update.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            steps.append(
                f"m_{i}={self._BETA1}*{data['m'][i]}+"
                f"{1 - self._BETA1}*{data['g'][i]}={data['m_new'][i]}"
            )
        for i in range(data["n"]):
            g_sq = round(data["g"][i] ** 2, 4)
            steps.append(
                f"v_{i}={self._BETA2}*{data['v'][i]}+"
                f"{1 - self._BETA2}*{g_sq}={data['v_new'][i]}"
            )
        steps.append(f"bc1=1-{self._BETA1}^{data['t']}={data['bc1']}")
        steps.append(f"bc2=1-{self._BETA2}^{data['t']}={data['bc2']}")
        for i in range(data["n"]):
            steps.append(
                f"\\hat{{m}}_{i}={data['m_new'][i]}/{data['bc1']}="
                f"{data['m_hat'][i]}"
            )
        for i in range(data["n"]):
            steps.append(
                f"\\hat{{v}}_{i}={data['v_new'][i]}/{data['bc2']}="
                f"{data['v_hat'][i]}"
            )
        for i in range(data["n"]):
            steps.append(f"w_{i}'={data['w_new'][i]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated weight vector.

        Args:
            data: Solution data.

        Returns:
            String representation of new weights.
        """
        return "[" + ",".join(str(v) for v in data["w_new"]) + "]"


@register
class LearningRateDecayGenerator(StepGenerator):
    """Compute learning rate at step t for various decay schedules.

    Supports cosine annealing, step decay, and exponential decay.
    Shows formula substitution and numerical evaluation.

    Input format:
        ``compute learning rate at step t``

    Target format:
        ``\\alpha_t = \\alpha_0 \\cdot \\gamma^t, \\alpha_0=0.01,
        \\gamma=0.95, t=10 <step> 0.01*0.95^{10} <step>
        0.01*0.5987=0.005987 <step> 0.005987``

    Difficulty scaling:
        Difficulty 1-3: exponential decay (simple power).
        Difficulty 4-6: step decay (floor division).
        Difficulty 7-8: cosine annealing (trig computation).

    Prerequisites:
        exponentiation, multiplication.

    Example:
        >>> gen = LearningRateDecayGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lr_decay'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lr_decay"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls schedule type.

        Returns:
            Natural language description.
        """
        return "compute learning rate at step t"

    def _schedule_type(self, difficulty: int) -> str:
        """Map difficulty to decay schedule type.

        Args:
            difficulty: Difficulty level.

        Returns:
            Schedule name string.
        """
        if difficulty <= 3:
            return "exponential"
        if difficulty <= 6:
            return "step"
        return "cosine"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a learning rate decay computation.

        Args:
            difficulty: Controls schedule type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        schedule = self._schedule_type(difficulty)
        lr_0 = self._rng.choice([0.1, 0.01, 0.001])
        t = self._rng.randint(5, 50)

        if schedule == "exponential":
            return self._exponential_problem(lr_0, t)
        if schedule == "step":
            return self._step_problem(lr_0, t)
        return self._cosine_problem(lr_0, t)

    def _exponential_problem(self, lr_0: float, t: int) -> tuple[str, dict]:
        """Generate exponential decay problem.

        Args:
            lr_0: Initial learning rate.
            t: Current step.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        gamma = self._rng.choice([0.9, 0.95, 0.99])
        decay_factor = round(gamma ** t, 6)
        lr_t = round(lr_0 * decay_factor, 6)
        problem = (
            f"\\alpha_t = \\alpha_0 \\cdot \\gamma^t, "
            f"\\alpha_0={lr_0}, \\gamma={gamma}, t={t}"
        )
        return problem, {
            "schedule": "exponential", "lr_0": lr_0,
            "gamma": gamma, "t": t,
            "decay_factor": decay_factor, "lr_t": lr_t,
        }

    def _step_problem(self, lr_0: float, t: int) -> tuple[str, dict]:
        """Generate step decay problem.

        Args:
            lr_0: Initial learning rate.
            t: Current step.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        step_size = self._rng.choice([10, 20, 30])
        gamma = self._rng.choice([0.1, 0.5])
        num_drops = t // step_size
        decay_factor = round(gamma ** num_drops, 6)
        lr_t = round(lr_0 * decay_factor, 6)
        problem = (
            f"\\alpha_t = \\alpha_0 \\cdot \\gamma^{{\\lfloor t/s \\rfloor}}, "
            f"\\alpha_0={lr_0}, \\gamma={gamma}, s={step_size}, t={t}"
        )
        return problem, {
            "schedule": "step", "lr_0": lr_0,
            "gamma": gamma, "step_size": step_size, "t": t,
            "num_drops": num_drops, "decay_factor": decay_factor,
            "lr_t": lr_t,
        }

    def _cosine_problem(self, lr_0: float, t: int) -> tuple[str, dict]:
        """Generate cosine annealing problem.

        Args:
            lr_0: Initial learning rate.
            t: Current step.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        t_max = self._rng.choice([100, 200])
        cos_val = round(math.cos(math.pi * t / t_max), 4)
        lr_t = round(0.5 * lr_0 * (1 + cos_val), 6)
        problem = (
            f"\\alpha_t = \\frac{{1}}{{2}}\\alpha_0(1+\\cos(\\pi t/T)), "
            f"\\alpha_0={lr_0}, T={t_max}, t={t}"
        )
        return problem, {
            "schedule": "cosine", "lr_0": lr_0,
            "t_max": t_max, "t": t,
            "cos_val": cos_val, "lr_t": lr_t,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate schedule-specific computation steps.

        Args:
            data: Solution data with schedule parameters.

        Returns:
            Steps showing formula evaluation.
        """
        schedule = data["schedule"]
        if schedule == "exponential":
            return self._exponential_steps(data)
        if schedule == "step":
            return self._step_steps(data)
        return self._cosine_steps(data)

    def _exponential_steps(self, data: dict) -> list[str]:
        """Generate steps for exponential decay.

        Args:
            data: Solution data.

        Returns:
            Steps showing power computation and multiplication.
        """
        return [
            f"{data['gamma']}^{{{data['t']}}}={data['decay_factor']}",
            f"{data['lr_0']}*{data['decay_factor']}={data['lr_t']}",
        ]

    def _step_steps(self, data: dict) -> list[str]:
        """Generate steps for step decay.

        Args:
            data: Solution data.

        Returns:
            Steps showing floor division and power.
        """
        return [
            f"\\lfloor {data['t']}/{data['step_size']} \\rfloor={data['num_drops']}",
            f"{data['gamma']}^{{{data['num_drops']}}}={data['decay_factor']}",
            f"{data['lr_0']}*{data['decay_factor']}={data['lr_t']}",
        ]

    def _cosine_steps(self, data: dict) -> list[str]:
        """Generate steps for cosine annealing.

        Args:
            data: Solution data.

        Returns:
            Steps showing cosine evaluation and scaling.
        """
        ratio = round(data["t"] / data["t_max"], 4)
        return [
            f"\\pi*{data['t']}/{data['t_max']}={round(math.pi * ratio, 4)}",
            f"\\cos({round(math.pi * ratio, 4)})={data['cos_val']}",
            f"0.5*{data['lr_0']}*(1+{data['cos_val']})={data['lr_t']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the decayed learning rate.

        Args:
            data: Solution data.

        Returns:
            String representation of lr_t.
        """
        return str(data["lr_t"])


@register
class MSELossGenerator(StepGenerator):
    """Compute mean squared error: MSE = (1/n) * sum((y_i - yhat_i)^2).

    Generates true values and predictions, shows each squared error
    term, and computes the mean. Uses 2-4 element vectors with
    simple integer or single-decimal values.

    Input format:
        ``compute mean squared error``

    Target format:
        ``MSE(y,\\hat{y}), y=[1,3,5], \\hat{y}=[1.2,2.8,5.5] <step>
        (1-1.2)^2=0.04 <step> (3-2.8)^2=0.04 <step>
        (5-5.5)^2=0.25 <step> (0.04+0.04+0.25)/3=0.11 <step> 0.11``

    Difficulty scaling:
        Difficulty 1-3: 2-element vectors, integer targets.
        Difficulty 4-6: 3-element vectors, float targets.
        Difficulty 7-8: 4-element vectors, float targets.

    Prerequisites:
        mean, exponentiation.

    Example:
        >>> gen = MSELossGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mse_loss'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mse_loss"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size.

        Returns:
            Natural language description.
        """
        return "compute mean squared error"

    def _vector_size(self, difficulty: int) -> int:
        """Map difficulty to number of data points.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of elements (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate true values and predictions for MSE.

        Args:
            difficulty: Controls vector size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._vector_size(difficulty)
        y = [self._rng.randint(1, 10) for _ in range(n)]
        y_hat = [round(y[i] + self._rng.uniform(-1.0, 1.0), 1) for i in range(n)]
        sq_errors = [round((y[i] - y_hat[i]) ** 2, 4) for i in range(n)]
        mse = round(sum(sq_errors) / n, 4)

        y_s = ",".join(str(v) for v in y)
        yh_s = ",".join(str(v) for v in y_hat)
        problem = f"MSE(y,\\hat{{y}}), y=[{y_s}], \\hat{{y}}=[{yh_s}]"
        return problem, {
            "y": y, "y_hat": y_hat,
            "sq_errors": sq_errors, "mse": mse, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element squared error and mean computation.

        Args:
            data: Solution data with true/predicted values.

        Returns:
            Steps showing each (y_i - yhat_i)^2 and the mean.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            yi = data["y"][i]
            yhi = data["y_hat"][i]
            sq = data["sq_errors"][i]
            steps.append(f"({yi}-{yhi})^2={sq}")
        steps.append(f"({'+'.join(str(e) for e in data['sq_errors'])})/{data['n']}={data['mse']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the MSE value.

        Args:
            data: Solution data.

        Returns:
            String representation of MSE.
        """
        return str(data["mse"])


@register
class BinaryCrossEntropyGenerator(StepGenerator):
    """Binary cross-entropy: BCE = -[y*log(p) + (1-y)*log(1-p)].

    Generates binary labels and predicted probabilities, shows the
    log computation for each sample, and averages.

    Input format:
        ``compute binary cross entropy loss``

    Target format:
        ``BCE, y=[1,0,1], p=[0.9,0.2,0.8] <step>
        -[1*log(0.9)+(1-1)*log(0.1)]=-(-0.1054)=0.1054 <step>
        -[0*log(0.2)+(1-0)*log(0.8)]=-(-0.2231)=0.2231 <step>
        ... <step> mean=0.1643 <step> 0.1643``

    Difficulty scaling:
        Difficulty 1-3: 2 samples.
        Difficulty 4-6: 3 samples.
        Difficulty 7-8: 4 samples.

    Prerequisites:
        cross_entropy.

    Example:
        >>> gen = BinaryCrossEntropyGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bce_loss'
    """

    _PROB_VALUES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bce_loss"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cross_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of samples.

        Returns:
            Natural language description.
        """
        return "compute binary cross entropy loss"

    def _num_samples(self, difficulty: int) -> int:
        """Map difficulty to number of binary samples.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of samples (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate binary labels and predictions for BCE.

        Args:
            difficulty: Controls number of samples.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_samples(difficulty)
        y = [self._rng.randint(0, 1) for _ in range(n)]
        p = [self._rng.choice(self._PROB_VALUES) for _ in range(n)]
        losses = self._compute_losses(y, p, n)
        bce = round(sum(losses) / n, 4)

        y_s = ",".join(str(v) for v in y)
        p_s = ",".join(str(v) for v in p)
        problem = f"BCE = -[y\\log p + (1-y)\\log(1-p)], y=[{y_s}], p=[{p_s}]"
        return problem, {"y": y, "p": p, "losses": losses, "bce": bce, "n": n}

    def _compute_losses(self, y: list[int], p: list[float],
                        n: int) -> list[float]:
        """Compute per-sample BCE losses.

        Args:
            y: Binary labels.
            p: Predicted probabilities.
            n: Number of samples.

        Returns:
            List of per-sample loss values.
        """
        losses: list[float] = []
        for i in range(n):
            term1 = y[i] * math.log(p[i]) if p[i] > 0 else 0.0
            term2 = (1 - y[i]) * math.log(1 - p[i]) if (1 - p[i]) > 0 else 0.0
            losses.append(round(-(term1 + term2), 4))
        return losses

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-sample BCE computation steps.

        Args:
            data: Solution data with labels and predictions.

        Returns:
            Steps showing log terms for each sample.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            yi = data["y"][i]
            pi = data["p"][i]
            loss = data["losses"][i]
            log_p = round(math.log(pi), 4) if pi > 0 else "-inf"
            log_1p = round(math.log(1 - pi), 4) if (1 - pi) > 0 else "-inf"
            steps.append(
                f"-[{yi}*\\log({pi})+{1 - yi}*\\log({1 - pi})]="
                f"-[{yi}*{log_p}+{1 - yi}*{log_1p}]={loss}"
            )
        loss_sum = round(sum(data["losses"]), 4)
        steps.append(f"mean={loss_sum}/{data['n']}={data['bce']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the average BCE loss.

        Args:
            data: Solution data.

        Returns:
            String representation of average BCE.
        """
        return str(data["bce"])


@register
class KLDivergenceGenerator(StepGenerator):
    """KL divergence: KL(P||Q) = sum(p_i * log(p_i / q_i)).

    Generates two discrete probability distributions and shows
    per-element computation of p_i * log(p_i / q_i).

    Input format:
        ``compute KL divergence``

    Target format:
        ``KL(P||Q), P=[0.4,0.6], Q=[0.5,0.5] <step>
        0.4*\\log(0.4/0.5)=0.4*(-0.2231)=-0.0893 <step>
        0.6*\\log(0.6/0.5)=0.6*(0.1823)=0.1094 <step>
        sum=-0.0893+0.1094=0.0201 <step> 0.0201``

    Difficulty scaling:
        Difficulty 1-3: 2 categories.
        Difficulty 4-6: 3 categories.
        Difficulty 7-8: 4 categories.

    Prerequisites:
        info_entropy.

    Example:
        >>> gen = KLDivergenceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kl_divergence'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kl_divergence"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of categories.

        Returns:
            Natural language description.
        """
        return "compute KL divergence"

    def _num_categories(self, difficulty: int) -> int:
        """Map difficulty to distribution size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of categories (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two distributions for KL divergence.

        Args:
            difficulty: Controls number of categories.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ph = ProbabilityHelper(self._rng)
        n = self._num_categories(difficulty)
        p = ph.distribution(n)
        q = ph.distribution(n)
        terms = [round(p[i] * math.log(p[i] / q[i]), 4) for i in range(n)]
        kl = round(sum(terms), 4)

        p_s = ",".join(str(v) for v in p)
        q_s = ",".join(str(v) for v in q)
        problem = f"D_{{KL}}(P||Q), P=[{p_s}], Q=[{q_s}]"
        return problem, {"p": p, "q": q, "terms": terms, "kl": kl, "n": n}

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element KL divergence steps.

        Args:
            data: Solution data with distributions and terms.

        Returns:
            Steps showing p_i * log(p_i / q_i) for each i.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            pi = data["p"][i]
            qi = data["q"][i]
            ratio = round(pi / qi, 4)
            log_ratio = round(math.log(ratio), 4)
            term = data["terms"][i]
            steps.append(f"{pi}*\\log({pi}/{qi})={pi}*{log_ratio}={term}")
        term_sum = "+".join(str(t) for t in data["terms"])
        steps.append(f"sum={term_sum}={data['kl']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the KL divergence value.

        Args:
            data: Solution data.

        Returns:
            String representation of KL divergence.
        """
        return str(data["kl"])


@register
class BatchNormGenerator(StepGenerator):
    """Batch normalisation: normalise, then scale and shift.

    Shows the full batch norm pipeline: compute mean, variance,
    normalise (x - mean) / sqrt(var + eps), and apply affine
    transform gamma * x_norm + beta.

    Input format:
        ``apply batch normalisation``

    Target format:
        ``BN(x), x=[2,4,6], \\gamma=1.0, \\beta=0.0 <step>
        mean=(2+4+6)/3=4.0 <step> var=((2-4)^2+(4-4)^2+(6-4)^2)/3=2.6667
        <step> x_0=(2-4)/sqrt(2.6667+1e-5)=-1.2247 <step> ...
        <step> [-1.2247,0.0,1.2247]``

    Difficulty scaling:
        Difficulty 1-3: 3-element batch, gamma=1, beta=0.
        Difficulty 4-6: 4-element batch, gamma=1, beta=0.
        Difficulty 7-8: 4-element batch with non-trivial gamma/beta.

    Prerequisites:
        mean, variance.

    Example:
        >>> gen = BatchNormGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'batch_norm'
    """

    _EPS = 1e-5

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "batch_norm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mean", "variance"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls batch size and affine params.

        Returns:
            Natural language description.
        """
        return "apply batch normalisation"

    def _batch_size(self, difficulty: int) -> int:
        """Map difficulty to batch size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Batch size (3-4).
        """
        if difficulty <= 3:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a batch and affine parameters for batch norm.

        Args:
            difficulty: Controls batch size and affine params.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._batch_size(difficulty)
        x = [self._rng.randint(1, 20) for _ in range(n)]
        gamma = round(self._rng.uniform(0.5, 2.0), 1) if difficulty >= 7 else 1.0
        beta = round(self._rng.uniform(-1.0, 1.0), 1) if difficulty >= 7 else 0.0

        mu = round(sum(x) / n, 4)
        var = round(sum((xi - mu) ** 2 for xi in x) / n, 4)
        denom = round(math.sqrt(var + self._EPS), 4)
        x_norm = [round((xi - mu) / denom, 4) for xi in x]
        y = [round(gamma * xn + beta, 4) for xn in x_norm]

        x_s = ",".join(str(v) for v in x)
        problem = (
            f"BN(x), x=[{x_s}], "
            f"\\gamma={gamma}, \\beta={beta}"
        )
        return problem, {
            "x": x, "gamma": gamma, "beta": beta,
            "mu": mu, "var": var, "denom": denom,
            "x_norm": x_norm, "y": y, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean, variance, normalisation, and affine steps.

        Args:
            data: Solution data with batch and intermediates.

        Returns:
            Steps showing mean, var, each x_norm, and each y.
        """
        steps: list[str] = []
        x_sum = "+".join(str(v) for v in data["x"])
        steps.append(f"\\mu=({x_sum})/{data['n']}={data['mu']}")
        sq_terms = "+".join(
            f"({v}-{data['mu']})^2" for v in data["x"]
        )
        steps.append(f"\\sigma^2=({sq_terms})/{data['n']}={data['var']}")
        steps.append(
            f"\\sqrt{{{data['var']}+{self._EPS}}}={data['denom']}"
        )
        for i in range(data["n"]):
            steps.append(
                f"\\hat{{x}}_{i}=({data['x'][i]}-{data['mu']})/"
                f"{data['denom']}={data['x_norm'][i]}"
            )
        if data["gamma"] != 1.0 or data["beta"] != 0.0:
            for i in range(data["n"]):
                steps.append(
                    f"y_{i}={data['gamma']}*{data['x_norm'][i]}+"
                    f"{data['beta']}={data['y'][i]}"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the normalised (and optionally transformed) output.

        Args:
            data: Solution data.

        Returns:
            String representation of output vector.
        """
        out = data["y"] if (data["gamma"] != 1.0 or data["beta"] != 0.0) else data["x_norm"]
        return "[" + ",".join(str(v) for v in out) + "]"


@register
class DropoutGenerator(StepGenerator):
    """Apply dropout mask and inverted scaling: x * mask / (1 - p).

    Generates an input vector and a binary mask, then shows masking
    and rescaling to maintain expected values during training.

    Input format:
        ``apply dropout to vector``

    Target format:
        ``dropout(x, p=0.3), x=[2.0,1.5,3.0,0.5], mask=[1,0,1,1]
        <step> 2.0*1=2.0 <step> 1.5*0=0.0 <step> 3.0*1=3.0 <step>
        0.5*1=0.5 <step> scale=1/(1-0.3)=1.4286 <step>
        [2.857,0.0,4.286,0.714]``

    Difficulty scaling:
        Difficulty 1-3: 3-element vector, p=0.3.
        Difficulty 4-6: 4-element vector, p=0.4.
        Difficulty 7-8: 5-element vector, p=0.5.

    Prerequisites:
        multiplication, division.

    Example:
        >>> gen = DropoutGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'dropout_compute'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "dropout_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication", "division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size and drop rate.

        Returns:
            Natural language description.
        """
        return "apply dropout to vector"

    def _config(self, difficulty: int) -> tuple[int, float]:
        """Map difficulty to vector size and drop probability.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (vector_size, dropout_probability).
        """
        if difficulty <= 3:
            return 3, 0.3
        if difficulty <= 6:
            return 4, 0.4
        return 5, 0.5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input vector, mask, and dropout parameters.

        Args:
            difficulty: Controls vector size and drop rate.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, p = self._config(difficulty)
        vh = VectorHelper(self._rng)
        x = vh.float_vector(n, 0.5, 5.0, decimals=1)
        mask = [self._rng.choice([0, 1]) for _ in range(n)]
        if all(m == 0 for m in mask):
            mask[0] = 1

        scale = round(1.0 / (1.0 - p), 4)
        masked = [round(x[i] * mask[i], 4) for i in range(n)]
        output = [round(masked[i] * scale, 4) for i in range(n)]

        x_s = ",".join(str(v) for v in x)
        m_s = ",".join(str(v) for v in mask)
        problem = f"\\text{{dropout}}(x, p={p}), x=[{x_s}], mask=[{m_s}]"
        return problem, {
            "x": x, "mask": mask, "p": p, "scale": scale,
            "masked": masked, "output": output, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate masking and scaling steps.

        Args:
            data: Solution data with input, mask, and scale.

        Returns:
            Steps showing each masking then the scaling factor.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            steps.append(
                f"{data['x'][i]}*{data['mask'][i]}={data['masked'][i]}"
            )
        steps.append(
            f"scale=1/(1-{data['p']})={data['scale']}"
        )
        for i in range(data["n"]):
            steps.append(
                f"{data['masked'][i]}*{data['scale']}={data['output'][i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the dropout-scaled output vector.

        Args:
            data: Solution data.

        Returns:
            String representation of output vector.
        """
        return "[" + ",".join(str(v) for v in data["output"]) + "]"


@register
class ConvolutionOutputSizeGenerator(StepGenerator):
    """Compute conv output size: O = (W - K + 2P) / S + 1.

    Shows formula substitution for various input widths, kernel sizes,
    padding, and stride values.

    Input format:
        ``compute convolution output size``

    Target format:
        ``O = (W-K+2P)/S + 1, W=32, K=3, P=1, S=1 <step>
        (32-3+2*1)/1+1 <step> (32-3+2)/1+1 <step>
        31/1+1=32 <step> 32``

    Difficulty scaling:
        Difficulty 1-3: stride=1, no padding.
        Difficulty 4-6: stride=1 or 2, with padding.
        Difficulty 7-8: stride=2, various padding.

    Prerequisites:
        division, addition.

    Example:
        >>> gen = ConvolutionOutputSizeGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'conv_output_size'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "conv_output_size"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "addition"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls stride and padding complexity.

        Returns:
            Natural language description.
        """
        return "compute convolution output size"

    def _params(self, difficulty: int) -> tuple[int, int, int, int]:
        """Generate convolution parameters based on difficulty.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (width, kernel_size, padding, stride).
        """
        w = self._rng.choice([8, 16, 28, 32, 64])
        k = self._rng.choice([3, 5, 7])
        if difficulty <= 3:
            return w, k, 0, 1
        if difficulty <= 6:
            p = self._rng.choice([0, 1, 2])
            s = self._rng.choice([1, 2])
        else:
            p = self._rng.choice([1, 2, 3])
            s = self._rng.choice([2, 3])
        return w, k, p, s

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate convolution parameters and compute output size.

        Args:
            difficulty: Controls stride and padding.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        w, k, p, s = self._params(difficulty)
        numerator = w - k + 2 * p
        output = numerator // s + 1
        problem = f"O=(W-K+2P)/S+1, W={w}, K={k}, P={p}, S={s}"
        return problem, {
            "w": w, "k": k, "p": p, "s": s,
            "numerator": numerator, "output": output,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate formula substitution steps.

        Args:
            data: Solution data with conv parameters.

        Returns:
            Steps showing substitution and arithmetic.
        """
        w, k, p, s = data["w"], data["k"], data["p"], data["s"]
        two_p = 2 * p
        return [
            f"({w}-{k}+2*{p})/{s}+1",
            f"({w}-{k}+{two_p})/{s}+1",
            f"{data['numerator']}/{s}+1",
            f"{data['numerator'] // s}+1={data['output']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the output spatial dimension.

        Args:
            data: Solution data.

        Returns:
            String representation of output size.
        """
        return str(data["output"])


@register
class BellmanEquationGenerator(StepGenerator):
    """Bellman equation: V(s) = R(s) + gamma * max_a sum P(s'|s,a) V(s').

    Uses a simple 2-3 state grid world with known transition
    probabilities and rewards to demonstrate value iteration.

    Input format:
        ``compute value using bellman equation``

    Target format:
        ``V(s_0), R=[1,-1,5], \\gamma=0.9, transitions given <step>
        V(s_0)=1+0.9*max(0.8*V(s_1)+0.2*V(s_0), ...) <step>
        ... <step> V(s_0)=3.6``

    Difficulty scaling:
        Difficulty 1-3: 2 states, 2 actions, gamma=0.9.
        Difficulty 4-6: 3 states, 2 actions.
        Difficulty 7-8: 3 states, 3 actions.

    Prerequisites:
        expected_value, multiplication.

    Example:
        >>> gen = BellmanEquationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bellman_equation'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bellman_equation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expected_value", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of states and actions.

        Returns:
            Natural language description.
        """
        return "compute value using bellman equation"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to number of states and actions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (num_states, num_actions).
        """
        if difficulty <= 3:
            return 2, 2
        if difficulty <= 6:
            return 3, 2
        return 3, 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a simple MDP for Bellman equation evaluation.

        Args:
            difficulty: Controls MDP size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n_states, n_actions = self._config(difficulty)
        gamma = 0.9
        rewards = [self._rng.randint(-2, 5) for _ in range(n_states)]
        v_current = [round(self._rng.uniform(0, 5), 1) for _ in range(n_states)]
        transitions = self._build_transitions(n_states, n_actions)

        action_values = self._compute_action_values(
            rewards, v_current, transitions, gamma, n_states, n_actions,
        )
        best_action = max(range(n_actions), key=lambda a: action_values[a])
        v_new = round(rewards[0] + gamma * action_values[best_action], 4)

        r_s = ",".join(str(r) for r in rewards)
        v_s = ",".join(str(v) for v in v_current)
        problem = (
            f"V(s_0), R=[{r_s}], V_{{curr}}=[{v_s}], \\gamma={gamma}"
        )
        return problem, {
            "rewards": rewards, "v_current": v_current,
            "gamma": gamma, "transitions": transitions,
            "action_values": action_values, "best_action": best_action,
            "v_new": v_new, "n_states": n_states, "n_actions": n_actions,
        }

    def _build_transitions(self, n_states: int,
                           n_actions: int) -> list[list[float]]:
        """Build transition probability tables P(s'|s_0, a).

        Args:
            n_states: Number of states.
            n_actions: Number of actions.

        Returns:
            Nested list [action][next_state] of probabilities.
        """
        transitions: list[list[float]] = []
        for _ in range(n_actions):
            raw = [self._rng.randint(1, 10) for _ in range(n_states)]
            total = sum(raw)
            probs = [round(r / total, 2) for r in raw]
            diff = round(1.0 - sum(probs), 2)
            probs[-1] = round(probs[-1] + diff, 2)
            transitions.append(probs)
        return transitions

    def _compute_action_values(self, rewards: list[int],
                               v_current: list[float],
                               transitions: list[list[float]],
                               gamma: float, n_states: int,
                               n_actions: int) -> list[float]:
        """Compute expected value for each action from state 0.

        Args:
            rewards: Immediate rewards per state.
            v_current: Current value estimates.
            transitions: Transition probabilities.
            gamma: Discount factor.
            n_states: Number of states.
            n_actions: Number of actions.

        Returns:
            List of action values.
        """
        action_values: list[float] = []
        for a in range(n_actions):
            ev = sum(
                transitions[a][s] * v_current[s] for s in range(n_states)
            )
            action_values.append(round(ev, 4))
        return action_values

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Bellman equation evaluation steps.

        Args:
            data: Solution data with MDP parameters.

        Returns:
            Steps showing action value computation and max selection.
        """
        steps: list[str] = []
        for a in range(data["n_actions"]):
            terms = []
            for s in range(data["n_states"]):
                prob = data["transitions"][a][s]
                val = data["v_current"][s]
                terms.append(f"{prob}*{val}")
            ev = data["action_values"][a]
            steps.append(f"Q(s_0,a_{a})={'+'.join(terms)}={ev}")
        best = data["best_action"]
        steps.append(
            f"max_a Q={data['action_values'][best]}"
        )
        steps.append(
            f"V(s_0)={data['rewards'][0]}+"
            f"{data['gamma']}*{data['action_values'][best]}="
            f"{data['v_new']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated value for state 0.

        Args:
            data: Solution data.

        Returns:
            String representation of V(s_0).
        """
        return str(data["v_new"])


@register
class QValueUpdateGenerator(StepGenerator):
    """Q-learning TD update: Q(s,a) += alpha * (R + gamma*max Q(s',a') - Q(s,a)).

    Shows the temporal difference update step by step, including
    the TD target, TD error, and final Q-value update.

    Input format:
        ``perform Q-value update``

    Target format:
        ``Q(s,a)=2.5, R=1, gamma=0.9, max_Q(s')=3.0, alpha=0.1 <step>
        target=1+0.9*3.0=3.7 <step> error=3.7-2.5=1.2 <step>
        Q'=2.5+0.1*1.2=2.62 <step> 2.62``

    Difficulty scaling:
        Difficulty 1-3: single update, alpha=0.1.
        Difficulty 4-6: single update, alpha=0.01.
        Difficulty 7-8: two sequential updates.

    Prerequisites:
        bellman_equation.

    Example:
        >>> gen = QValueUpdateGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'q_value_update'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "q_value_update"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bellman_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls alpha and number of updates.

        Returns:
            Natural language description.
        """
        return "perform Q-value update"

    def _alpha(self, difficulty: int) -> float:
        """Map difficulty to learning rate.

        Args:
            difficulty: Difficulty level.

        Returns:
            Learning rate for Q update.
        """
        if difficulty <= 3:
            return 0.1
        return 0.01

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Q-learning update parameters.

        Args:
            difficulty: Controls alpha and complexity.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        alpha = self._alpha(difficulty)
        gamma = 0.9
        q_old = round(self._rng.uniform(0, 5), 2)
        reward = self._rng.randint(-2, 5)
        max_q_next = round(self._rng.uniform(0, 5), 2)

        target = round(reward + gamma * max_q_next, 4)
        td_error = round(target - q_old, 4)
        q_new = round(q_old + alpha * td_error, 4)

        problem = (
            f"Q(s,a)={q_old}, R={reward}, \\gamma={gamma}, "
            f"\\max_{{a'}} Q(s',a')={max_q_next}, \\alpha={alpha}"
        )
        return problem, {
            "q_old": q_old, "reward": reward, "gamma": gamma,
            "max_q_next": max_q_next, "alpha": alpha,
            "target": target, "td_error": td_error, "q_new": q_new,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate TD target, error, and update steps.

        Args:
            data: Solution data with Q-learning parameters.

        Returns:
            Steps showing target, error, and new Q-value.
        """
        return [
            (
                f"target={data['reward']}+"
                f"{data['gamma']}*{data['max_q_next']}="
                f"{data['target']}"
            ),
            f"TD\\_error={data['target']}-{data['q_old']}={data['td_error']}",
            (
                f"Q'={data['q_old']}+{data['alpha']}*{data['td_error']}="
                f"{data['q_new']}"
            ),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the updated Q-value.

        Args:
            data: Solution data.

        Returns:
            String representation of new Q-value.
        """
        return str(data["q_new"])


@register
class PolicyGradientGenerator(StepGenerator):
    """Policy gradient: compute log pi(a|s) * R for gradient estimation.

    Generates action probabilities from a softmax policy, computes
    the log probability of the selected action, and multiplies
    by the reward for the REINFORCE gradient estimate.

    Input format:
        ``compute policy gradient estimate``

    Target format:
        ``\\pi(a|s)=[0.3,0.5,0.2], a=1, R=3.0 <step>
        \\log \\pi(a_1|s)=\\log(0.5)=-0.6931 <step>
        \\nabla = -0.6931 * 3.0 = -2.0794 <step> -2.0794``

    Difficulty scaling:
        Difficulty 1-3: 2 actions.
        Difficulty 4-6: 3 actions.
        Difficulty 7-8: 4 actions, with baseline subtraction.

    Prerequisites:
        backprop_simple.

    Example:
        >>> gen = PolicyGradientGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'policy_gradient'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "policy_gradient"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["backprop_simple"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of actions.

        Returns:
            Natural language description.
        """
        return "compute policy gradient estimate"

    def _num_actions(self, difficulty: int) -> int:
        """Map difficulty to number of available actions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of actions (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate policy, action, and reward for gradient computation.

        Args:
            difficulty: Controls number of actions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ph = ProbabilityHelper(self._rng)
        n = self._num_actions(difficulty)
        policy = ph.distribution(n, min_prob=0.1)
        action = self._rng.randint(0, n - 1)
        reward = round(self._rng.uniform(-3.0, 5.0), 1)

        baseline = 0.0
        if difficulty >= 7:
            baseline = round(self._rng.uniform(0.0, 2.0), 1)

        log_prob = round(math.log(policy[action]), 4)
        advantage = round(reward - baseline, 4)
        gradient = round(log_prob * advantage, 4)

        pi_s = ",".join(str(v) for v in policy)
        problem = (
            f"\\pi(a|s)=[{pi_s}], a={action}, R={reward}"
        )
        if baseline > 0:
            problem += f", b={baseline}"
        return problem, {
            "policy": policy, "action": action, "reward": reward,
            "baseline": baseline, "log_prob": log_prob,
            "advantage": advantage, "gradient": gradient, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate log probability and gradient multiplication steps.

        Args:
            data: Solution data with policy and reward.

        Returns:
            Steps showing log pi, advantage, and gradient.
        """
        steps: list[str] = []
        a = data["action"]
        prob = data["policy"][a]
        steps.append(
            f"\\log \\pi(a_{a}|s)=\\log({prob})={data['log_prob']}"
        )
        if data["baseline"] > 0:
            steps.append(
                f"A=R-b={data['reward']}-{data['baseline']}="
                f"{data['advantage']}"
            )
        steps.append(
            f"\\nabla={data['log_prob']}*{data['advantage']}="
            f"{data['gradient']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the policy gradient estimate.

        Args:
            data: Solution data.

        Returns:
            String representation of gradient value.
        """
        return str(data["gradient"])


@register
class MutualInformationGenerator(StepGenerator):
    """Mutual information: I(X;Y) = H(X) + H(Y) - H(X,Y).

    Generates a joint distribution over two binary/ternary variables,
    computes marginal entropies and joint entropy, then derives MI.

    Input format:
        ``compute mutual information``

    Target format:
        ``P(X,Y) given <step> H(X)=0.9710 <step> H(Y)=1.0 <step>
        H(X,Y)=1.5 <step> I(X;Y)=0.9710+1.0-1.5=0.4710 <step> 0.4710``

    Difficulty scaling:
        Difficulty 1-3: 2x2 joint table.
        Difficulty 4-6: 2x3 joint table.
        Difficulty 7-8: 3x3 joint table.

    Prerequisites:
        info_entropy.

    Example:
        >>> gen = MutualInformationGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'mutual_information'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "mutual_information"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls joint table dimensions.

        Returns:
            Natural language description.
        """
        return "compute mutual information"

    def _dims(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to joint distribution dimensions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (rows, cols) for joint table.
        """
        if difficulty <= 3:
            return 2, 2
        if difficulty <= 6:
            return 2, 3
        return 3, 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a joint distribution and compute mutual information.

        Args:
            difficulty: Controls joint table size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        rx, ry = self._dims(difficulty)
        joint = self._build_joint(rx, ry)
        px = self._marginal_x(joint, rx, ry)
        py = self._marginal_y(joint, rx, ry)

        hx = round(self._entropy(px), 4)
        hy = round(self._entropy(py), 4)
        flat = [joint[i][j] for i in range(rx) for j in range(ry)]
        hxy = round(self._entropy(flat), 4)
        mi = round(hx + hy - hxy, 4)

        rows = [",".join(str(v) for v in joint[i]) for i in range(rx)]
        table = ";".join(rows)
        problem = f"I(X;Y), P(X,Y)=[{table}]"
        return problem, {
            "joint": joint, "px": px, "py": py,
            "hx": hx, "hy": hy, "hxy": hxy, "mi": mi,
            "rx": rx, "ry": ry,
        }

    def _build_joint(self, rx: int, ry: int) -> list[list[float]]:
        """Build a valid joint probability distribution.

        Args:
            rx: Number of X values.
            ry: Number of Y values.

        Returns:
            2D list of joint probabilities summing to 1.
        """
        raw = [[self._rng.randint(1, 10) for _ in range(ry)] for _ in range(rx)]
        total = sum(sum(row) for row in raw)
        joint = [[round(raw[i][j] / total, 4) for j in range(ry)] for i in range(rx)]
        diff = round(1.0 - sum(sum(row) for row in joint), 4)
        joint[-1][-1] = round(joint[-1][-1] + diff, 4)
        return joint

    def _marginal_x(self, joint: list[list[float]], rx: int,
                    ry: int) -> list[float]:
        """Compute marginal distribution P(X).

        Args:
            joint: Joint probability table.
            rx: Number of X values.
            ry: Number of Y values.

        Returns:
            Marginal probabilities for X.
        """
        return [round(sum(joint[i][j] for j in range(ry)), 4) for i in range(rx)]

    def _marginal_y(self, joint: list[list[float]], rx: int,
                    ry: int) -> list[float]:
        """Compute marginal distribution P(Y).

        Args:
            joint: Joint probability table.
            rx: Number of X values.
            ry: Number of Y values.

        Returns:
            Marginal probabilities for Y.
        """
        return [round(sum(joint[i][j] for i in range(rx)), 4) for j in range(ry)]

    def _entropy(self, probs: list[float]) -> float:
        """Compute Shannon entropy H = -sum(p * log2(p)).

        Args:
            probs: Probability values.

        Returns:
            Entropy in bits.
        """
        return -sum(p * math.log2(p) for p in probs if p > 0)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate entropy computation and MI derivation steps.

        Args:
            data: Solution data with entropies.

        Returns:
            Steps showing H(X), H(Y), H(X,Y), and I(X;Y).
        """
        return [
            f"H(X)={data['hx']} bits",
            f"H(Y)={data['hy']} bits",
            f"H(X,Y)={data['hxy']} bits",
            (
                f"I(X;Y)={data['hx']}+{data['hy']}-{data['hxy']}="
                f"{data['mi']}"
            ),
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mutual information value.

        Args:
            data: Solution data.

        Returns:
            String representation of MI in bits.
        """
        return f"{data['mi']} bits"


@register
class KLFromDistributionsGenerator(StepGenerator):
    """KL divergence between two named discrete distributions.

    Generates two explicit probability distributions (e.g. uniform
    vs. skewed) and computes KL(P||Q) element-wise, reinforcing
    the asymmetry of KL divergence.

    Input format:
        ``compute KL divergence between distributions``

    Target format:
        ``P=[0.25,0.25,0.25,0.25], Q=[0.1,0.2,0.3,0.4] <step>
        0.25*\\log(0.25/0.1)=0.2291 <step> ... <step> 0.1046``

    Difficulty scaling:
        Difficulty 1-3: 2 categories.
        Difficulty 4-6: 3 categories.
        Difficulty 7-8: 4 categories with near-zero probabilities.

    Prerequisites:
        kl_divergence.

    Example:
        >>> gen = KLFromDistributionsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'kl_from_distributions'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "kl_from_distributions"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["kl_divergence"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of categories.

        Returns:
            Natural language description.
        """
        return "compute KL divergence between distributions"

    def _num_categories(self, difficulty: int) -> int:
        """Map difficulty to distribution size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of categories (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two distributions for KL divergence comparison.

        Args:
            difficulty: Controls distribution size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_categories(difficulty)
        p_uniform = [round(1.0 / n, 4)] * n
        diff = round(1.0 - sum(p_uniform), 4)
        p_uniform[-1] = round(p_uniform[-1] + diff, 4)

        ph = ProbabilityHelper(self._rng)
        q = ph.distribution(n, min_prob=0.05)

        terms = [round(p_uniform[i] * math.log(p_uniform[i] / q[i]), 4) for i in range(n)]
        kl = round(sum(terms), 4)

        p_s = ",".join(str(v) for v in p_uniform)
        q_s = ",".join(str(v) for v in q)
        problem = f"D_{{KL}}(P||Q), P=[{p_s}], Q=[{q_s}]"
        return problem, {
            "p": p_uniform, "q": q, "terms": terms,
            "kl": kl, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element KL computation steps.

        Args:
            data: Solution data with distributions and terms.

        Returns:
            Steps showing each term and the sum.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            pi = data["p"][i]
            qi = data["q"][i]
            ratio = round(pi / qi, 4)
            log_r = round(math.log(ratio), 4)
            steps.append(f"{pi}*\\log({ratio})={pi}*{log_r}={data['terms'][i]}")
        steps.append(f"KL={'+'.join(str(t) for t in data['terms'])}={data['kl']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the KL divergence value.

        Args:
            data: Solution data.

        Returns:
            String representation of KL divergence.
        """
        return str(data["kl"])


@register
class MarkovRewardGenerator(StepGenerator):
    """Expected reward for a policy: E[R] = sum pi(a|s) * R(s,a).

    Generates a state with action probabilities and rewards, then
    computes the expected reward under the policy.

    Input format:
        ``compute expected reward for policy``

    Target format:
        ``\\pi(a|s)=[0.6,0.4], R(s,a)=[3,-1] <step>
        0.6*3=1.8 <step> 0.4*-1=-0.4 <step> 1.8+(-0.4)=1.4 <step> 1.4``

    Difficulty scaling:
        Difficulty 1-3: 2 actions, 1 state.
        Difficulty 4-6: 3 actions, 2 states averaged.
        Difficulty 7-8: 4 actions, 2 states.

    Prerequisites:
        markov_chain, expected_value.

    Example:
        >>> gen = MarkovRewardGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'markov_reward'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "markov_reward"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["markov_chain", "expected_value"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of actions.

        Returns:
            Natural language description.
        """
        return "compute expected reward for policy"

    def _num_actions(self, difficulty: int) -> int:
        """Map difficulty to number of actions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of actions (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate policy and reward table for expected reward.

        Args:
            difficulty: Controls number of actions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        ph = ProbabilityHelper(self._rng)
        n = self._num_actions(difficulty)
        policy = ph.distribution(n, min_prob=0.1)
        rewards = [self._rng.randint(-3, 5) for _ in range(n)]

        terms = [round(policy[i] * rewards[i], 4) for i in range(n)]
        expected = round(sum(terms), 4)

        pi_s = ",".join(str(v) for v in policy)
        r_s = ",".join(str(v) for v in rewards)
        problem = (
            f"E[R]=\\sum \\pi(a|s) R(s,a), "
            f"\\pi=[{pi_s}], R=[{r_s}]"
        )
        return problem, {
            "policy": policy, "rewards": rewards,
            "terms": terms, "expected": expected, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-action expected reward computation steps.

        Args:
            data: Solution data with policy and rewards.

        Returns:
            Steps showing each pi_i * R_i and the sum.
        """
        steps: list[str] = []
        for i in range(data["n"]):
            steps.append(
                f"{data['policy'][i]}*{data['rewards'][i]}="
                f"{data['terms'][i]}"
            )
        term_str = "+".join(str(t) for t in data["terms"])
        steps.append(f"E[R]={term_str}={data['expected']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the expected reward.

        Args:
            data: Solution data.

        Returns:
            String representation of expected reward.
        """
        return str(data["expected"])


@register
class DiscountedReturnGenerator(StepGenerator):
    """Discounted return: G_t = R_t + gamma*R_{t+1} + gamma^2*R_{t+2} + ...

    Shows the geometric series of discounted rewards step by step,
    computing each gamma^k * R_{t+k} term and summing.

    Input format:
        ``compute discounted return``

    Target format:
        ``G_t, R=[2,3,-1,4], \\gamma=0.9 <step>
        0.9^0*2=2.0 <step> 0.9^1*3=2.7 <step>
        0.9^2*-1=-0.81 <step> 0.9^3*4=2.916 <step>
        sum=6.806 <step> 6.806``

    Difficulty scaling:
        Difficulty 1-3: 3 rewards, gamma=0.9.
        Difficulty 4-6: 4 rewards, gamma=0.95.
        Difficulty 7-8: 5 rewards, gamma=0.99.

    Prerequisites:
        exponentiation, prefix_scan.

    Example:
        >>> gen = DiscountedReturnGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'discounted_return'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "discounted_return"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "prefix_scan"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls reward sequence length.

        Returns:
            Natural language description.
        """
        return "compute discounted return"

    def _config(self, difficulty: int) -> tuple[int, float]:
        """Map difficulty to sequence length and discount factor.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (num_rewards, gamma).
        """
        if difficulty <= 3:
            return 3, 0.9
        if difficulty <= 6:
            return 4, 0.95
        return 5, 0.99

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reward sequence for discounted return.

        Args:
            difficulty: Controls sequence length and gamma.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, gamma = self._config(difficulty)
        rewards = [self._rng.randint(-3, 5) for _ in range(n)]
        terms = [round(gamma ** k * rewards[k], 4) for k in range(n)]
        total = round(sum(terms), 4)

        r_s = ",".join(str(r) for r in rewards)
        problem = f"G_t=\\sum_{{k=0}}^{{T}} \\gamma^k R_{{t+k}}, R=[{r_s}], \\gamma={gamma}"
        return problem, {
            "rewards": rewards, "gamma": gamma,
            "terms": terms, "total": total, "n": n,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-timestep discounted reward steps.

        Args:
            data: Solution data with rewards and gamma.

        Returns:
            Steps showing gamma^k * R_k for each k.
        """
        steps: list[str] = []
        for k in range(data["n"]):
            gamma_k = round(data["gamma"] ** k, 4)
            steps.append(
                f"{data['gamma']}^{k}*{data['rewards'][k]}="
                f"{gamma_k}*{data['rewards'][k]}={data['terms'][k]}"
            )
        term_str = "+".join(str(t) for t in data["terms"])
        steps.append(f"G_t={term_str}={data['total']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the discounted return value.

        Args:
            data: Solution data.

        Returns:
            String representation of G_t.
        """
        return str(data["total"])


@register
class ConfusionMatrixGenerator(StepGenerator):
    """Compute precision, recall, and F1 from TP/FP/TN/FN counts.

    Generates realistic confusion matrix values and shows the
    computation of each classification metric step by step.

    Input format:
        ``compute metrics from confusion matrix``

    Target format:
        ``TP=80, FP=10, TN=90, FN=20 <step>
        precision=80/(80+10)=0.8889 <step>
        recall=80/(80+20)=0.8 <step>
        F1=2*0.8889*0.8/(0.8889+0.8)=0.8421 <step> 0.8421``

    Difficulty scaling:
        Difficulty 1-3: values 10-100, clean ratios.
        Difficulty 4-6: values 50-500.
        Difficulty 7-8: values 100-1000, messy ratios.

    Prerequisites:
        division.

    Example:
        >>> gen = ConfusionMatrixGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'confusion_matrix'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "confusion_matrix"

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
            difficulty: Controls value ranges.

        Returns:
            Natural language description.
        """
        return "compute metrics from confusion matrix"

    def _value_range(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to confusion matrix value range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (min_value, max_value).
        """
        if difficulty <= 3:
            return 10, 100
        if difficulty <= 6:
            return 50, 500
        return 100, 1000

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate confusion matrix values and compute metrics.

        Args:
            difficulty: Controls value ranges.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lo, hi = self._value_range(difficulty)
        tp = self._rng.randint(lo, hi)
        fp = self._rng.randint(lo // 5, hi // 3)
        tn = self._rng.randint(lo, hi)
        fn = self._rng.randint(lo // 5, hi // 3)

        precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
        recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
        f1 = self._compute_f1(precision, recall)

        problem = f"TP={tp}, FP={fp}, TN={tn}, FN={fn}"
        return problem, {
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "precision": precision, "recall": recall, "f1": f1,
        }

    def _compute_f1(self, precision: float, recall: float) -> float:
        """Compute F1 score from precision and recall.

        Args:
            precision: Precision value.
            recall: Recall value.

        Returns:
            F1 score.
        """
        if precision + recall == 0:
            return 0.0
        return round(2 * precision * recall / (precision + recall), 4)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate precision, recall, and F1 computation steps.

        Args:
            data: Solution data with confusion matrix values.

        Returns:
            Steps showing each metric calculation.
        """
        tp, fp, fn = data["tp"], data["fp"], data["fn"]
        p = data["precision"]
        r = data["recall"]
        return [
            f"precision={tp}/({tp}+{fp})={p}",
            f"recall={tp}/({tp}+{fn})={r}",
            f"F1=2*{p}*{r}/({p}+{r})={data['f1']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the F1 score.

        Args:
            data: Solution data.

        Returns:
            String representation of F1 score.
        """
        return str(data["f1"])


@register
class ROCAUCGenerator(StepGenerator):
    """Compute AUC from sorted predictions using trapezoidal rule.

    Generates prediction scores and true labels, sorts by score,
    computes TPR/FPR at each threshold, and integrates.

    Input format:
        ``compute ROC AUC``

    Target format:
        ``scores=[0.9,0.7,0.4,0.3], labels=[1,1,0,0] <step>
        threshold=0.9: TPR=0.5,FPR=0.0 <step> ... <step> AUC=1.0``

    Difficulty scaling:
        Difficulty 1-3: 4 samples (2 pos, 2 neg).
        Difficulty 4-6: 6 samples (3 pos, 3 neg).
        Difficulty 7-8: 8 samples (4 pos, 4 neg).

    Prerequisites:
        sorting, confusion_matrix.

    Example:
        >>> gen = ROCAUCGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'roc_auc'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "roc_auc"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sorting", "confusion_matrix"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of samples.

        Returns:
            Natural language description.
        """
        return "compute ROC AUC"

    def _num_samples(self, difficulty: int) -> int:
        """Map difficulty to total number of samples.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of samples (4-8).
        """
        if difficulty <= 3:
            return 4
        if difficulty <= 6:
            return 6
        return 8

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate scores and labels for ROC AUC computation.

        Args:
            difficulty: Controls number of samples.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_samples(difficulty)
        n_pos = n // 2
        n_neg = n - n_pos
        labels = [1] * n_pos + [0] * n_neg
        scores = [round(self._rng.uniform(0.1, 0.99), 2) for _ in range(n)]

        paired = list(zip(scores, labels))
        paired.sort(key=lambda x: -x[0])
        sorted_scores = [p[0] for p in paired]
        sorted_labels = [p[1] for p in paired]

        points = self._compute_roc_points(sorted_labels, n_pos, n_neg)
        auc = self._compute_auc(points)

        s_str = ",".join(str(s) for s in sorted_scores)
        l_str = ",".join(str(l) for l in sorted_labels)
        problem = f"scores=[{s_str}], labels=[{l_str}]"
        return problem, {
            "sorted_scores": sorted_scores,
            "sorted_labels": sorted_labels,
            "points": points, "auc": auc,
            "n_pos": n_pos, "n_neg": n_neg,
        }

    def _compute_roc_points(self, sorted_labels: list[int],
                            n_pos: int,
                            n_neg: int) -> list[tuple[float, float]]:
        """Compute (FPR, TPR) points for the ROC curve.

        Args:
            sorted_labels: Labels sorted by descending score.
            n_pos: Total positive count.
            n_neg: Total negative count.

        Returns:
            List of (FPR, TPR) tuples including (0,0) origin.
        """
        points: list[tuple[float, float]] = [(0.0, 0.0)]
        tp = 0
        fp = 0
        for label in sorted_labels:
            if label == 1:
                tp += 1
            else:
                fp += 1
            tpr = round(tp / n_pos, 4) if n_pos > 0 else 0.0
            fpr = round(fp / n_neg, 4) if n_neg > 0 else 0.0
            points.append((fpr, tpr))
        return points

    def _compute_auc(self, points: list[tuple[float, float]]) -> float:
        """Compute area under ROC curve using trapezoidal rule.

        Args:
            points: List of (FPR, TPR) tuples.

        Returns:
            AUC value.
        """
        auc = 0.0
        for i in range(1, len(points)):
            dx = points[i][0] - points[i - 1][0]
            avg_y = (points[i][1] + points[i - 1][1]) / 2
            auc += dx * avg_y
        return round(auc, 4)

    def _create_steps(self, data: dict) -> list[str]:
        """Generate ROC point computation and AUC integration steps.

        Args:
            data: Solution data with ROC points.

        Returns:
            Steps showing each threshold point and final AUC.
        """
        steps: list[str] = []
        points = data["points"]
        for i in range(1, len(points)):
            fpr, tpr = points[i]
            steps.append(f"point_{i}: FPR={fpr}, TPR={tpr}")
        steps.append(f"AUC={data['auc']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the AUC value.

        Args:
            data: Solution data.

        Returns:
            String representation of AUC.
        """
        return str(data["auc"])


@register
class BiasVarianceGenerator(StepGenerator):
    """Bias-variance decomposition: MSE = Bias^2 + Variance + Noise.

    Generates multiple model predictions for the same inputs, computes
    the average prediction, bias, variance, and shows the decomposition.

    Input format:
        ``decompose MSE into bias and variance``

    Target format:
        ``y_true=5.0, predictions=[4.2,5.1,4.8,4.5] <step>
        mean_pred=(4.2+5.1+4.8+4.5)/4=4.65 <step>
        bias=4.65-5.0=-0.35, bias^2=0.1225 <step>
        var=mean((4.2-4.65)^2+...)=0.1163 <step>
        MSE=0.1225+0.1163=0.2388 <step> 0.2388``

    Difficulty scaling:
        Difficulty 1-3: 3 predictions, no noise term.
        Difficulty 4-6: 4 predictions, no noise term.
        Difficulty 7-8: 5 predictions with explicit noise.

    Prerequisites:
        mse_loss, variance.

    Example:
        >>> gen = BiasVarianceGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'bias_variance'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "bias_variance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mse_loss", "variance"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of predictions.

        Returns:
            Natural language description.
        """
        return "decompose MSE into bias and variance"

    def _num_predictions(self, difficulty: int) -> int:
        """Map difficulty to number of model runs.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of predictions (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate true value and multiple predictions for decomposition.

        Args:
            difficulty: Controls number of predictions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._num_predictions(difficulty)
        y_true = round(self._rng.uniform(2.0, 8.0), 1)
        preds = [round(y_true + self._rng.uniform(-1.5, 1.5), 2) for _ in range(n)]

        mean_pred = round(sum(preds) / n, 4)
        bias = round(mean_pred - y_true, 4)
        bias_sq = round(bias ** 2, 4)
        pred_var = round(sum((p - mean_pred) ** 2 for p in preds) / n, 4)

        noise = 0.0
        if difficulty >= 7:
            noise = round(self._rng.uniform(0.01, 0.1), 4)
        mse = round(bias_sq + pred_var + noise, 4)

        p_s = ",".join(str(p) for p in preds)
        problem = f"y_{{true}}={y_true}, predictions=[{p_s}]"
        if noise > 0:
            problem += f", \\sigma^2_{{noise}}={noise}"
        return problem, {
            "y_true": y_true, "preds": preds, "n": n,
            "mean_pred": mean_pred, "bias": bias,
            "bias_sq": bias_sq, "pred_var": pred_var,
            "noise": noise, "mse": mse,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bias, variance, and decomposition steps.

        Args:
            data: Solution data with predictions and components.

        Returns:
            Steps showing mean, bias^2, variance, and total MSE.
        """
        steps: list[str] = []
        pred_sum = "+".join(str(p) for p in data["preds"])
        steps.append(
            f"\\bar{{y}}=({pred_sum})/{data['n']}={data['mean_pred']}"
        )
        steps.append(
            f"bias={data['mean_pred']}-{data['y_true']}={data['bias']}, "
            f"bias^2={data['bias_sq']}"
        )
        var_terms = "+".join(
            f"({p}-{data['mean_pred']})^2" for p in data["preds"]
        )
        steps.append(
            f"var=({var_terms})/{data['n']}={data['pred_var']}"
        )
        if data["noise"] > 0:
            steps.append(
                f"MSE={data['bias_sq']}+{data['pred_var']}+"
                f"{data['noise']}={data['mse']}"
            )
        else:
            steps.append(
                f"MSE={data['bias_sq']}+{data['pred_var']}={data['mse']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total MSE from the decomposition.

        Args:
            data: Solution data.

        Returns:
            String representation of MSE.
        """
        return str(data["mse"])
