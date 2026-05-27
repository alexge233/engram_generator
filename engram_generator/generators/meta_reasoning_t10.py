"""Tier 10 generators — self-architecture and model design.

Unlocks when Tier 0-9 tasks are mastered. These tasks require the model
to reason about computation itself: gradient flow, information capacity,
loss function design, scaling laws, architectural complexity, and
proposing improvements to computational mechanisms.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class ComputationGraph:
    """Represents a simple computation graph for gradient analysis.

    Stores a sequence of operations applied to an input variable,
    enabling forward evaluation and backward gradient computation
    via the chain rule.

    Example:
        >>> g = ComputationGraph("x", [("multiply", 3), ("add", 2), ("square", 0)])
        >>> g.forward(1)
        25
        >>> g.format_forward(1)
        'x=1 -> 3*1=3 -> 3+2=5 -> 5^2=25'
    """

    def __init__(self, variable: str,
                 operations: list[tuple[str, int]]) -> None:
        """Initialise the computation graph.

        Args:
            variable: Name of the input variable.
            operations: List of (operation_name, parameter) tuples.
        """
        self._variable = variable
        self._operations = operations

    @property
    def variable(self) -> str:
        """Return the input variable name."""
        return self._variable

    @property
    def operations(self) -> list[tuple[str, int]]:
        """Return the operation list."""
        return self._operations

    def forward(self, x: int) -> int:
        """Evaluate the computation graph at a given input.

        Args:
            x: Input value.

        Returns:
            Output value after all operations.
        """
        val = x
        for op, param in self._operations:
            val = self._apply_op(val, op, param)
        return val

    def _apply_op(self, val: int, op: str, param: int) -> int:
        """Apply a single operation.

        Args:
            val: Current value.
            op: Operation name.
            param: Operation parameter.

        Returns:
            Result after applying the operation.
        """
        if op == "multiply":
            return val * param
        if op == "add":
            return val + param
        if op == "square":
            return val * val
        return val

    def format_forward(self, x: int) -> str:
        """Format the forward pass as a step-by-step trace.

        Args:
            x: Input value.

        Returns:
            Trace string showing each operation result.
        """
        parts = [f"{self._variable}={x}"]
        val = x
        for op, param in self._operations:
            prev = val
            val = self._apply_op(val, op, param)
            parts.append(self._format_op_step(prev, op, param, val))
        return " -> ".join(parts)

    def _format_op_step(self, prev: int, op: str,
                        param: int, result: int) -> str:
        """Format a single operation step.

        Args:
            prev: Value before the operation.
            op: Operation name.
            param: Operation parameter.
            result: Value after the operation.

        Returns:
            Formatted step string.
        """
        if op == "multiply":
            return f"{param}*{prev}={result}"
        if op == "add":
            return f"{prev}+{param}={result}"
        if op == "square":
            return f"{prev}^2={result}"
        return f"{prev}->{result}"

    def backward_steps(self, x: int) -> list[str]:
        """Compute backward pass gradient steps via chain rule.

        Args:
            x: Input value for forward pass.

        Returns:
            List of gradient computation steps.
        """
        intermediates = self._compute_intermediates(x)
        return self._chain_rule_steps(intermediates)

    def _compute_intermediates(self, x: int) -> list[tuple[str, int, int, int]]:
        """Compute intermediate values during forward pass.

        Args:
            x: Input value.

        Returns:
            List of (operation, param, input_value, output_value) tuples.
        """
        val = x
        intermediates: list[tuple[str, int, int, int]] = []
        for op, param in self._operations:
            out = self._apply_op(val, op, param)
            intermediates.append((op, param, val, out))
            val = out
        return intermediates

    def _chain_rule_steps(self,
                          intermediates: list[tuple[str, int, int, int]]) -> list[str]:
        """Generate chain rule gradient steps from intermediates.

        Args:
            intermediates: Forward pass intermediate values.

        Returns:
            List of gradient step strings.
        """
        steps: list[str] = []
        grad = 1
        for op, param, inp, out in reversed(intermediates):
            local_grad = self._local_gradient(op, param, inp)
            steps.append(f"d/d({inp})[{op}] = {local_grad}, chain: {grad}*{local_grad}={grad * local_grad}")
            grad *= local_grad
        steps.append(f"final gradient = {grad}")
        return steps

    def _local_gradient(self, op: str, param: int, inp: int) -> int:
        """Compute the local gradient for an operation.

        Args:
            op: Operation name.
            param: Operation parameter.
            inp: Input value to the operation.

        Returns:
            Local gradient value.
        """
        if op == "multiply":
            return param
        if op == "add":
            return 1
        if op == "square":
            return 2 * inp
        return 1

    def total_gradient(self, x: int) -> int:
        """Compute the total gradient of output with respect to input.

        Args:
            x: Input value.

        Returns:
            Total gradient value.
        """
        grad = 1
        val = x
        for op, param in self._operations:
            local = self._local_gradient_with_param(op, param, val)
            grad *= local
            val = self._apply_op(val, op, param)
        return grad

    def _local_gradient_with_param(self, op: str, param: int,
                                   val: int) -> int:
        """Compute local gradient using both operation and parameter.

        Args:
            op: Operation name.
            param: Operation parameter.
            val: Current input value.

        Returns:
            Local gradient value.
        """
        if op == "multiply":
            return param
        if op == "add":
            return 1
        if op == "square":
            return 2 * val
        return 1


class ScalingLawModel:
    """Predicts performance using simple power-law scaling.

    Implements the relationship accuracy = C * N^alpha where
    N is the parameter count and C, alpha are fit from data.

    Example:
        >>> m = ScalingLawModel(1.0, 0.5)
        >>> m.predict(100)
        10.0
    """

    def __init__(self, coefficient: float, exponent: float) -> None:
        """Initialise the scaling law model.

        Args:
            coefficient: Multiplicative constant C.
            exponent: Power law exponent alpha.
        """
        self._coefficient = coefficient
        self._exponent = exponent

    @property
    def coefficient(self) -> float:
        """Return the multiplicative constant."""
        return self._coefficient

    @property
    def exponent(self) -> float:
        """Return the power law exponent."""
        return self._exponent

    def predict(self, n: int) -> float:
        """Predict performance at parameter count n.

        Args:
            n: Number of parameters.

        Returns:
            Predicted accuracy/performance metric.
        """
        return self._coefficient * (n ** self._exponent)

    def format_prediction(self, n: int) -> str:
        """Format a prediction with the scaling formula.

        Args:
            n: Number of parameters.

        Returns:
            Formatted prediction string.
        """
        result = self.predict(n)
        return f"{self._coefficient}*{n}^{self._exponent} = {result:.2f}"


@register
class GradientAnalysisGenerator(StepGenerator):
    """Trace gradient through a simple computation graph.

    Presents a computation graph of the form f(x) = (ax+b)^2 or
    similar compositions, and asks the model to compute the gradient
    of the output with respect to the input using the chain rule.

    Input format:
        ``compute gradient of loss with respect to parameter``

    Target format:
        ``f(x) = (3x+2)^2, x=1 <step> forward: x=1 -> 3*1=3 ->
        3+2=5 -> 5^2=25 <step> backward: d/d(5)[square]=10,
        chain: 1*10=10 <step> d/d(3)[add]=1, chain: 10*1=10 <step>
        d/d(1)[multiply]=3, chain: 10*3=30 <step> gradient = 30
        <step> 30``

    Difficulty scaling:
        Difficulty 1-2: f(x) = ax+b (linear, gradient = a).
        Difficulty 3-4: f(x) = (ax+b)^2 (chain through square).
        Difficulty 5-6: f(x) = (ax^2+b) (chain through square and multiply).
        Difficulty 7-8: f(x) = ((ax+b)^2 + c)^2 (nested squares).

    Prerequisites:
        chain_rule, derivative_eval.

    Example:
        >>> gen = GradientAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'gradient_analysis'
    """

    _GRAPH_TYPES = {
        1: "linear", 2: "linear",
        3: "square_linear", 4: "square_linear",
        5: "square_input", 6: "square_input",
        7: "nested_square", 8: "nested_square",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "gradient_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["chain_rule", "derivative_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls computation graph complexity.

        Returns:
            Natural language description.
        """
        return "compute gradient of loss with respect to parameter"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a gradient analysis problem.

        Args:
            difficulty: Controls graph complexity.

        Returns:
            Tuple of (computation_description, solution_data).
        """
        graph_type = self._rng.choice(list(self._GRAPH_TYPES.values()))
        a = self._rng.randint(2, 4 + difficulty)
        b = self._rng.randint(1, 3 + difficulty)
        x = self._rng.randint(1, 3)
        graph = self._build_graph(graph_type, a, b)
        output = graph.forward(x)
        gradient = graph.total_gradient(x)
        formula = self._format_formula(graph_type, a, b)
        problem = f"f(x) = {formula}, x={x}"
        return problem, {
            "graph": graph, "x": x, "output": output,
            "gradient": gradient, "formula": formula,
            "graph_type": graph_type, "a": a, "b": b,
        }

    def _build_graph(self, graph_type: str, a: int,
                     b: int) -> ComputationGraph:
        """Build a computation graph for the given type.

        Args:
            graph_type: Graph structure identifier.
            a: Multiplicative parameter.
            b: Additive parameter.

        Returns:
            Configured ComputationGraph instance.
        """
        if graph_type == "linear":
            return ComputationGraph("x", [("multiply", a), ("add", b)])
        if graph_type == "square_linear":
            return ComputationGraph("x", [("multiply", a), ("add", b), ("square", 0)])
        if graph_type == "square_input":
            return ComputationGraph("x", [("square", 0), ("multiply", a), ("add", b)])
        return ComputationGraph("x", [("multiply", a), ("add", b), ("square", 0)])

    def _format_formula(self, graph_type: str, a: int, b: int) -> str:
        """Format the computation as a mathematical formula.

        Args:
            graph_type: Graph structure identifier.
            a: Multiplicative parameter.
            b: Additive parameter.

        Returns:
            LaTeX-style formula string.
        """
        if graph_type == "linear":
            return f"{a}x+{b}"
        if graph_type == "square_linear":
            return f"({a}x+{b})^2"
        if graph_type == "square_input":
            return f"{a}x^2+{b}"
        return f"(({a}x+{b})^2)"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate forward and backward pass steps.

        Args:
            data: Solution data with graph and gradient info.

        Returns:
            Steps showing forward pass, backward chain rule, and result.
        """
        graph = data["graph"]
        x = data["x"]
        steps: list[str] = [f"forward: {graph.format_forward(x)}"]
        backward = graph.backward_steps(x)
        steps.extend(backward)
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the computed gradient.

        Args:
            data: Solution data.

        Returns:
            Gradient value as a string.
        """
        return str(data["gradient"])


@register
class CapacityBoundGenerator(StepGenerator):
    """Estimate the information capacity of a system.

    Given a system specification (parameters, bits, vocabulary size,
    sequence length), computes the maximum information that can be
    stored or represented.

    Input format:
        ``estimate maximum information storable``

    Target format:
        ``system: 1000 parameters, 16 bits each <step>
        total bits = 1000 * 16 = 16000 <step>
        equivalent to 2^16000 distinct states <step> 16000 bits``

    Difficulty scaling:
        Difficulty 1-2: N parameters of B bits -> N*B bits.
        Difficulty 3-4: vocabulary V, length L -> L*log2(V) bits.
        Difficulty 5-6: binary tree of depth D -> 2^D leaves.
        Difficulty 7-8: hash table with N buckets, K items -> collision bound.

    Prerequisites:
        info_entropy, exponentiation.

    Example:
        >>> gen = CapacityBoundGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'capacity_bound'
    """

    _CAPACITY_TYPES = {
        1: "parameter_bits", 2: "parameter_bits",
        3: "vocabulary_sequence", 4: "vocabulary_sequence",
        5: "binary_tree", 6: "binary_tree",
        7: "hash_collision", 8: "hash_collision",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "capacity_bound"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["info_entropy", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which capacity model is used.

        Returns:
            Natural language description.
        """
        return "estimate maximum information storable"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a capacity estimation problem.

        Args:
            difficulty: Controls capacity model.

        Returns:
            Tuple of (system_description, solution_data).
        """
        cap_type = self._rng.choice(list(self._CAPACITY_TYPES.values()))
        builder = self._get_builder(cap_type)
        return builder(difficulty)

    def _get_builder(self, cap_type: str):
        """Return the builder method for the given capacity type.

        Args:
            cap_type: Capacity type identifier.

        Returns:
            Builder method.
        """
        builders = {
            "parameter_bits": self._build_parameter_bits,
            "vocabulary_sequence": self._build_vocabulary_sequence,
            "binary_tree": self._build_binary_tree,
            "hash_collision": self._build_hash_collision,
        }
        return builders[cap_type]

    def _build_parameter_bits(self, difficulty: int) -> tuple[str, dict]:
        """Build a parameter-bits capacity problem.

        Args:
            difficulty: Controls parameter count.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n_params = self._rng.choice([100, 500, 1000, 5000]) * difficulty
        bits_per = self._rng.choice([8, 16, 32])
        total_bits = n_params * bits_per
        problem = f"system: {n_params} parameters, {bits_per} bits each"
        return problem, {
            "cap_type": "parameter_bits",
            "n_params": n_params, "bits_per": bits_per,
            "total_bits": total_bits,
            "explanation": f"total bits = {n_params} * {bits_per} = {total_bits}",
            "capacity": f"{total_bits} bits",
        }

    def _build_vocabulary_sequence(self, difficulty: int) -> tuple[str, dict]:
        """Build a vocabulary-sequence capacity problem.

        Args:
            difficulty: Controls vocabulary size and sequence length.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        vocab = self._rng.choice([256, 1024, 4096, 32000])
        seq_len = self._rng.randint(8, 16) * difficulty
        bits_per_token = math.log2(vocab)
        total_bits = seq_len * bits_per_token
        problem = f"system: vocabulary {vocab}, sequence length {seq_len}"
        return problem, {
            "cap_type": "vocabulary_sequence",
            "vocab": vocab, "seq_len": seq_len,
            "bits_per_token": bits_per_token, "total_bits": total_bits,
            "explanation": (
                f"bits per token = log2({vocab}) = {bits_per_token:.1f}, "
                f"total = {seq_len} * {bits_per_token:.1f} = {total_bits:.1f}"
            ),
            "capacity": f"{total_bits:.1f} bits",
        }

    def _build_binary_tree(self, difficulty: int) -> tuple[str, dict]:
        """Build a binary tree capacity problem.

        Args:
            difficulty: Controls tree depth.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        depth = self._rng.randint(3, 5) + difficulty
        leaves = 2 ** depth
        bits = depth
        problem = f"system: binary tree of depth {depth}"
        return problem, {
            "cap_type": "binary_tree",
            "depth": depth, "leaves": leaves, "bits": bits,
            "explanation": (
                f"leaves = 2^{depth} = {leaves}, "
                f"each path encodes {depth} bits"
            ),
            "capacity": f"{leaves} leaves ({depth} bits per path)",
        }

    def _build_hash_collision(self, difficulty: int) -> tuple[str, dict]:
        """Build a hash collision bound problem.

        Args:
            difficulty: Controls table size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n_buckets = self._rng.choice([16, 64, 256, 1024]) * difficulty
        threshold = int(math.sqrt(n_buckets))
        problem = f"system: hash table with {n_buckets} buckets"
        return problem, {
            "cap_type": "hash_collision",
            "n_buckets": n_buckets, "threshold": threshold,
            "explanation": (
                f"birthday bound: collision likely after sqrt({n_buckets}) "
                f"= {threshold} insertions"
            ),
            "capacity": f"~{threshold} items before likely collision",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate capacity analysis steps.

        Args:
            data: Solution data with capacity computation.

        Returns:
            Steps showing the capacity derivation.
        """
        return [
            data["explanation"],
            f"capacity: {data['capacity']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the capacity bound.

        Args:
            data: Solution data.

        Returns:
            Capacity string.
        """
        return data["capacity"]


@register
class LossDesignGenerator(StepGenerator):
    """Design a loss function to achieve a stated behaviour.

    Presents a desired model behaviour and asks for a mathematical
    loss function that would encourage it. Uses well-known loss
    components: MSE, cross-entropy, regularisation, and KL divergence.

    Input format:
        ``design loss function that penalizes long sequences``

    Target format:
        ``desired: penalize sequences longer than T steps <step>
        base loss: cross-entropy on output tokens <step>
        penalty term: lambda * max(0, n_steps - T) <step>
        combined: L = CE + lambda * max(0, n_steps - T) <step>
        L = CE + lambda * max(0, n_steps - T)``

    Difficulty scaling:
        Difficulty 1-2: add length penalty to base loss.
        Difficulty 3-4: add L2 regularisation to prevent overfitting.
        Difficulty 5-6: add KL divergence for distribution matching.
        Difficulty 7-8: multi-objective with weighted sum.

    Prerequisites:
        cross_entropy.

    Example:
        >>> gen = LossDesignGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'loss_design'
    """

    _LOSS_TYPES = {
        1: "length_penalty", 2: "length_penalty",
        3: "l2_regularisation", 4: "l2_regularisation",
        5: "kl_divergence", 6: "kl_divergence",
        7: "multi_objective", 8: "multi_objective",
    }

    _BEHAVIOURS: dict[str, str] = {
        "length_penalty": "penalize sequences longer than T steps",
        "l2_regularisation": "prevent overfitting by limiting weight magnitude",
        "kl_divergence": "keep output distribution close to target distribution",
        "multi_objective": "balance accuracy, efficiency, and regularisation",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "loss_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["cross_entropy"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which loss type is requested.

        Returns:
            Natural language description.
        """
        loss_type = self._rng.choice(list(self._BEHAVIOURS.keys()))
        behaviour = self._BEHAVIOURS[loss_type]
        return f"design loss function that would {behaviour}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loss design problem.

        Args:
            difficulty: Controls loss complexity.

        Returns:
            Tuple of (behaviour_description, solution_data).
        """
        loss_type = self._rng.choice(list(self._BEHAVIOURS.keys()))
        behaviour = self._BEHAVIOURS[loss_type]
        builder = self._get_builder(loss_type)
        return builder(difficulty, behaviour)

    def _get_builder(self, loss_type: str):
        """Return the builder method for the given loss type.

        Args:
            loss_type: Loss type identifier.

        Returns:
            Builder method.
        """
        builders = {
            "length_penalty": self._build_length_penalty,
            "l2_regularisation": self._build_l2_regularisation,
            "kl_divergence": self._build_kl_divergence,
            "multi_objective": self._build_multi_objective,
        }
        return builders.get(loss_type, self._build_generic_loss)

    def _build_generic_loss(self, difficulty: int,
                            behaviour: str) -> tuple[str, dict]:
        """Build a generic loss design problem for extended loss types.

        Args:
            difficulty: Controls parameter values.
            behaviour: Desired behaviour description.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        alpha = round(self._rng.uniform(0.01, 1.0), 2)
        problem = f"desired: {behaviour}"
        return problem, {
            "base_loss": "cross-entropy on primary task",
            "penalty": f"{behaviour} (weight={alpha})",
            "formula": f"L = CE(y, y_hat) + {alpha} * auxiliary_term",
        }

    def _build_length_penalty(self, difficulty: int,
                              behaviour: str) -> tuple[str, dict]:
        """Build a length penalty loss design.

        Args:
            difficulty: Controls parameter values.
            behaviour: Desired behaviour description.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        threshold = self._rng.randint(5, 15)
        lam = round(self._rng.uniform(0.01, 0.1), 2)
        problem = f"desired: {behaviour}"
        formula = f"L = CE + {lam} * max(0, n_steps - {threshold})"
        return problem, {
            "loss_type": "length_penalty",
            "base_loss": "cross-entropy on output tokens",
            "penalty": f"{lam} * max(0, n_steps - {threshold})",
            "formula": formula, "behaviour": behaviour,
        }

    def _build_l2_regularisation(self, difficulty: int,
                                 behaviour: str) -> tuple[str, dict]:
        """Build an L2 regularisation loss design.

        Args:
            difficulty: Controls parameter values.
            behaviour: Desired behaviour description.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        lam = round(self._rng.uniform(0.0001, 0.01), 4)
        problem = f"desired: {behaviour}"
        formula = f"L = CE + {lam} * sum(w_i^2)"
        return problem, {
            "loss_type": "l2_regularisation",
            "base_loss": "cross-entropy on output tokens",
            "penalty": f"{lam} * sum(w_i^2) over all weights",
            "formula": formula, "behaviour": behaviour,
        }

    def _build_kl_divergence(self, difficulty: int,
                             behaviour: str) -> tuple[str, dict]:
        """Build a KL divergence loss design.

        Args:
            difficulty: Controls parameter values.
            behaviour: Desired behaviour description.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        beta = round(self._rng.uniform(0.1, 1.0), 2)
        problem = f"desired: {behaviour}"
        formula = f"L = CE + {beta} * KL(p || q)"
        return problem, {
            "loss_type": "kl_divergence",
            "base_loss": "cross-entropy on output tokens",
            "penalty": f"{beta} * KL(p_model || p_target)",
            "formula": formula, "behaviour": behaviour,
        }

    def _build_multi_objective(self, difficulty: int,
                               behaviour: str) -> tuple[str, dict]:
        """Build a multi-objective loss design.

        Args:
            difficulty: Controls parameter values.
            behaviour: Desired behaviour description.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        alpha = round(self._rng.uniform(0.5, 1.0), 2)
        beta = round(self._rng.uniform(0.01, 0.1), 2)
        gamma = round(self._rng.uniform(0.001, 0.01), 3)
        problem = f"desired: {behaviour}"
        formula = f"L = {alpha}*CE + {beta}*len_penalty + {gamma}*L2"
        return problem, {
            "loss_type": "multi_objective",
            "base_loss": f"{alpha} * cross-entropy",
            "penalty": f"{beta} * length_penalty + {gamma} * L2_regularisation",
            "formula": formula, "behaviour": behaviour,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate loss design reasoning steps.

        Args:
            data: Solution data with loss components.

        Returns:
            Steps showing base loss, penalty term, and combined formula.
        """
        return [
            f"base loss: {data['base_loss']}",
            f"penalty term: {data['penalty']}",
            f"combined: {data['formula']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the designed loss formula.

        Args:
            data: Solution data.

        Returns:
            Loss formula string.
        """
        return data["formula"]


@register
class ScalingPredictionGenerator(StepGenerator):
    """Predict performance at different model scales using scaling laws.

    Given observed performance at known parameter counts, uses
    power-law scaling to predict accuracy at a new scale. The model
    must identify the scaling exponent and extrapolate.

    Input format:
        ``predict accuracy if we double the parameters``

    Target format:
        ``observed: N=1000 -> acc=50.0, N=2000 -> acc=57.4 <step>
        fit scaling law: acc = C * N^alpha <step>
        alpha = log(57.4/50.0) / log(2000/1000) = 0.20 <step>
        C = 50.0 / 1000^0.20 = 12.55 <step>
        predict N=4000: 12.55 * 4000^0.20 = 65.9 <step> 65.9``

    Difficulty scaling:
        Difficulty 1-2: doubling parameters (simple extrapolation).
        Difficulty 3-4: 4x scale with three data points.
        Difficulty 5-6: 10x scale, model must interpolate.
        Difficulty 7-8: diminishing returns prediction.

    Prerequisites:
        exponentiation, polynomial_eval.

    Example:
        >>> gen = ScalingPredictionGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'scaling_prediction'
    """

    _SCALE_FACTORS = {
        1: 2, 2: 2, 3: 4, 4: 4, 5: 10, 6: 10, 7: 5, 8: 8,
    }

    _BASE_SIZES = {
        1: 1000, 2: 2000, 3: 1000, 4: 5000,
        5: 1000, 6: 10000, 7: 10000, 8: 50000,
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "scaling_prediction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation", "polynomial_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls scale factor.

        Returns:
            Natural language description.
        """
        factor = self._rng.choice(list(self._SCALE_FACTORS.values()))
        return f"predict accuracy if we scale parameters by {factor}x"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scaling prediction problem.

        Args:
            difficulty: Controls base size and scale factor.

        Returns:
            Tuple of (observations_string, solution_data).
        """
        base_n = self._rng.choice(list(self._BASE_SIZES.values()))
        factor = self._rng.choice(list(self._SCALE_FACTORS.values()))
        alpha = round(self._rng.uniform(0.1, 0.3), 2)
        c = round(self._rng.uniform(5.0, 20.0), 2)
        model = ScalingLawModel(c, alpha)
        acc1 = round(model.predict(base_n), 1)
        n2 = base_n * 2
        acc2 = round(model.predict(n2), 1)
        target_n = base_n * factor
        target_acc = round(model.predict(target_n), 1)
        problem = f"observed: N={base_n} -> acc={acc1}, N={n2} -> acc={acc2}"
        return problem, {
            "base_n": base_n, "n2": n2, "target_n": target_n,
            "acc1": acc1, "acc2": acc2, "target_acc": target_acc,
            "alpha": alpha, "c": c, "factor": factor,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate scaling law derivation and prediction steps.

        Args:
            data: Solution data with scaling parameters.

        Returns:
            Steps showing fitting and extrapolation.
        """
        ratio_acc = data["acc2"] / data["acc1"] if data["acc1"] != 0 else 1
        ratio_n = data["n2"] / data["base_n"]
        computed_alpha = round(math.log(ratio_acc) / math.log(ratio_n), 2) if ratio_n > 0 and ratio_acc > 0 else 0
        return [
            "fit scaling law: acc = C * N^alpha",
            f"alpha = log({data['acc2']}/{data['acc1']}) / log({data['n2']}/{data['base_n']}) = {computed_alpha}",
            f"C = {data['acc1']} / {data['base_n']}^{computed_alpha}",
            f"predict N={data['target_n']}: {data['target_acc']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the predicted accuracy.

        Args:
            data: Solution data.

        Returns:
            Predicted accuracy as a string.
        """
        return str(data["target_acc"])


@register
class ArchitectureAnalysisGenerator(StepGenerator):
    """Analyse the computational complexity of a neural mechanism.

    Presents a simple operation (matrix multiply, attention, convolution)
    and asks the model to identify the dominant computational terms and
    state the Big-O complexity.

    Input format:
        ``what is the time complexity of this operation``

    Target format:
        ``operation: matrix multiply A(n x k) * B(k x m) <step>
        each output element requires k multiplications and k-1 additions
        <step> n*m output elements <step> total: n*m*k multiplications
        <step> O(nmk)``

    Difficulty scaling:
        Difficulty 1-2: matrix multiply (n x k) * (k x m) -> O(nmk).
        Difficulty 3-4: self-attention on sequence of length n -> O(n^2 d).
        Difficulty 5-6: 1D convolution with kernel k on length n -> O(nk).
        Difficulty 7-8: multi-head attention with h heads -> O(n^2 d).

    Prerequisites:
        matrix_multiply, multiplication.

    Example:
        >>> gen = ArchitectureAnalysisGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'architecture_analysis'
    """

    _OPERATION_TYPES = {
        1: "matrix_multiply", 2: "matrix_multiply",
        3: "self_attention", 4: "self_attention",
        5: "convolution_1d", 6: "convolution_1d",
        7: "multi_head_attention", 8: "multi_head_attention",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "architecture_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which operation is analysed.

        Returns:
            Natural language description.
        """
        return "what is the time complexity of this operation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an architecture analysis problem.

        Args:
            difficulty: Controls operation type.

        Returns:
            Tuple of (operation_description, solution_data).
        """
        op_type = self._rng.choice(list(self._OPERATION_TYPES.values()))
        builder = self._get_builder(op_type)
        return builder(difficulty)

    def _get_builder(self, op_type: str):
        """Return the builder method for the given operation type.

        Args:
            op_type: Operation type identifier.

        Returns:
            Builder method.
        """
        builders = {
            "matrix_multiply": self._build_matrix_multiply,
            "self_attention": self._build_self_attention,
            "convolution_1d": self._build_convolution,
            "multi_head_attention": self._build_multi_head,
        }
        return builders[op_type]

    def _build_matrix_multiply(self, difficulty: int) -> tuple[str, dict]:
        """Build a matrix multiplication complexity problem.

        Args:
            difficulty: Controls matrix dimensions.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n = self._rng.randint(2, 5) * (1 + difficulty)
        k = self._rng.randint(2, 5) * (1 + difficulty)
        m = self._rng.randint(2, 5) * (1 + difficulty)
        problem = f"operation: matrix multiply A({n} x {k}) * B({k} x {m})"
        total_ops = n * m * k
        return problem, {
            "op_type": "matrix_multiply",
            "dimensions": f"({n} x {k}) * ({k} x {m})",
            "analysis": [
                f"each output element requires {k} multiplications and {k - 1} additions",
                f"{n}*{m} = {n * m} output elements",
                f"total: {n}*{m}*{k} = {total_ops} multiplications",
            ],
            "complexity": "O(nmk)",
            "total_ops": total_ops,
        }

    def _build_self_attention(self, difficulty: int) -> tuple[str, dict]:
        """Build a self-attention complexity problem.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        seq_len = self._rng.randint(8, 32) * difficulty
        d_model = self._rng.choice([64, 128, 256, 512])
        problem = f"operation: self-attention on sequence length {seq_len}, d_model={d_model}"
        qk_ops = seq_len * seq_len * d_model
        return problem, {
            "op_type": "self_attention",
            "dimensions": f"seq_len={seq_len}, d_model={d_model}",
            "analysis": [
                f"Q*K^T: ({seq_len} x {d_model}) * ({d_model} x {seq_len}) = O({seq_len}^2 * {d_model})",
                f"softmax: O({seq_len}^2) per row, {seq_len} rows",
                f"attention*V: ({seq_len} x {seq_len}) * ({seq_len} x {d_model})",
                f"dominant term: {seq_len}^2 * {d_model} = {qk_ops}",
            ],
            "complexity": "O(n^2 d)",
            "total_ops": qk_ops,
        }

    def _build_convolution(self, difficulty: int) -> tuple[str, dict]:
        """Build a 1D convolution complexity problem.

        Args:
            difficulty: Controls input size.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        n = self._rng.randint(16, 64) * difficulty
        k = self._rng.choice([3, 5, 7])
        problem = f"operation: 1D convolution, input length {n}, kernel size {k}"
        total_ops = n * k
        return problem, {
            "op_type": "convolution_1d",
            "dimensions": f"n={n}, k={k}",
            "analysis": [
                f"each output position requires {k} multiply-accumulate ops",
                f"{n} output positions (with padding)",
                f"total: {n}*{k} = {total_ops} operations",
            ],
            "complexity": "O(nk)",
            "total_ops": total_ops,
        }

    def _build_multi_head(self, difficulty: int) -> tuple[str, dict]:
        """Build a multi-head attention complexity problem.

        Args:
            difficulty: Controls dimensions.

        Returns:
            Tuple of (problem_string, solution_data).
        """
        seq_len = self._rng.randint(8, 32) * difficulty
        d_model = self._rng.choice([256, 512])
        n_heads = self._rng.choice([4, 8])
        d_head = d_model // n_heads
        problem = (
            f"operation: multi-head attention, {n_heads} heads, "
            f"seq_len={seq_len}, d_model={d_model}"
        )
        per_head = seq_len * seq_len * d_head
        total_ops = per_head * n_heads
        return problem, {
            "op_type": "multi_head_attention",
            "dimensions": f"h={n_heads}, n={seq_len}, d={d_model}, d_h={d_head}",
            "analysis": [
                f"per head: Q*K^T is ({seq_len} x {d_head}) * ({d_head} x {seq_len})",
                f"per head cost: {seq_len}^2 * {d_head} = {per_head}",
                f"{n_heads} heads in parallel: {n_heads} * {per_head} = {total_ops}",
                f"note: {n_heads} * {d_head} = {d_model}, so total = O(n^2 * d_model)",
            ],
            "complexity": "O(n^2 d)",
            "total_ops": total_ops,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate complexity analysis steps.

        Args:
            data: Solution data with operation analysis.

        Returns:
            Steps showing the analysis and complexity conclusion.
        """
        steps = data["analysis"][:]
        steps.append(f"complexity: {data['complexity']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the complexity class.

        Args:
            data: Solution data.

        Returns:
            Big-O complexity string.
        """
        return data["complexity"]


@register
class SuccessorDesignGenerator(StepGenerator):
    """Propose an architectural improvement for a stated limitation.

    Presents a model limitation and asks for an architectural
    modification that addresses it. Uses well-known improvements
    from the deep learning literature.

    Input format:
        ``this model fails on sequences longer than N. propose a fix``

    Target format:
        ``limitation: attention scales as O(n^2) for sequence length n
        <step> bottleneck: full pairwise attention matrix <step>
        proposal: use linear attention (kernel approximation) <step>
        new complexity: O(n) instead of O(n^2) <step>
        trade-off: reduced expressiveness for long-range dependencies
        <step> linear attention: O(n)``

    Difficulty scaling:
        Difficulty 1-2: fixed iterations -> adaptive halting.
        Difficulty 3-4: vanishing gradients -> residual connections.
        Difficulty 5-6: quadratic attention -> linear attention.
        Difficulty 7-8: fixed capacity -> mixture of experts.

    Prerequisites:
        architecture_analysis, algorithm_improvement.

    Example:
        >>> gen = SuccessorDesignGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'successor_design'
    """

    _LIMITATION_TYPES = {
        1: "fixed_iterations", 2: "fixed_iterations",
        3: "vanishing_gradient", 4: "vanishing_gradient",
        5: "quadratic_attention", 6: "quadratic_attention",
        7: "fixed_capacity", 8: "fixed_capacity",
    }

    _LIMITATIONS: dict[str, str] = {
        "fixed_iterations": "model uses fixed number of processing steps regardless of input complexity",
        "vanishing_gradient": "gradient signal vanishes in deep networks (>20 layers)",
        "quadratic_attention": "attention scales as O(n^2) for sequence length n",
        "fixed_capacity": "model capacity is fixed regardless of input difficulty",
    }

    _BOTTLENECKS: dict[str, str] = {
        "fixed_iterations": "all inputs get same compute budget",
        "vanishing_gradient": "gradient magnitude decreases exponentially with depth",
        "quadratic_attention": "full pairwise attention matrix requires n^2 memory and compute",
        "fixed_capacity": "single set of parameters handles all inputs equally",
    }

    _PROPOSALS: dict[str, str] = {
        "fixed_iterations": "use adaptive halting (e.g. ACT): learn a halt probability per step",
        "vanishing_gradient": "add residual connections: output = layer(x) + x",
        "quadratic_attention": "use linear attention via kernel approximation",
        "fixed_capacity": "use mixture of experts: route inputs to specialised sub-networks",
    }

    _NEW_PROPERTIES: dict[str, str] = {
        "fixed_iterations": "compute adapts to input complexity, easy inputs exit early",
        "vanishing_gradient": "gradient flows directly through skip connections regardless of depth",
        "quadratic_attention": "O(n) instead of O(n^2) for sequence length n",
        "fixed_capacity": "effective capacity scales with number of experts without proportional compute increase",
    }

    _TRADEOFFS: dict[str, str] = {
        "fixed_iterations": "harder to parallelise variable-length computation",
        "vanishing_gradient": "increased memory for storing activations at each layer",
        "quadratic_attention": "reduced expressiveness for long-range pairwise dependencies",
        "fixed_capacity": "load balancing across experts requires auxiliary loss",
    }

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "successor_design"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 10

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["architecture_analysis", "algorithm_improvement"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which limitation is addressed.

        Returns:
            Natural language description.
        """
        lim_type = self._rng.choice(list(self._LIMITATIONS.keys()))
        limitation = self._LIMITATIONS[lim_type]
        return f"this model has a problem: {limitation}. propose a fix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a successor design problem.

        Args:
            difficulty: Controls limitation type.

        Returns:
            Tuple of (limitation_description, solution_data).
        """
        lim_type = self._rng.choice(list(self._LIMITATIONS.keys()))
        limitation = self._LIMITATIONS[lim_type]
        bottleneck = self._BOTTLENECKS[lim_type]
        proposal = self._PROPOSALS[lim_type]
        new_prop = self._NEW_PROPERTIES[lim_type]
        tradeoff = self._TRADEOFFS[lim_type]
        problem = f"limitation: {limitation}"
        return problem, {
            "lim_type": lim_type, "limitation": limitation,
            "bottleneck": bottleneck, "proposal": proposal,
            "new_property": new_prop, "tradeoff": tradeoff,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate architectural improvement reasoning steps.

        Args:
            data: Solution data with limitation and proposal.

        Returns:
            Steps showing bottleneck analysis, proposal, and trade-offs.
        """
        return [
            f"bottleneck: {data['bottleneck']}",
            f"proposal: {data['proposal']}",
            f"improvement: {data['new_property']}",
            f"trade-off: {data['tradeoff']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the proposed improvement.

        Args:
            data: Solution data.

        Returns:
            Proposal string.
        """
        return data["proposal"]
