"""Deep learning specific task generators.

12 generators across tiers 3-6 covering ReLU derivative, batch
normalisation forward pass, dropout, 2D convolution, max pooling,
embedding lookup, GELU activation, cross-attention, gradient clipping,
learning rate warmup, loss landscape analysis, and weight decay update.
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


def _fm(mat: list[list[float]]) -> str:
    """Format a matrix as a compact string.

    Args:
        mat: 2D list of floats.

    Returns:
        Bracket-enclosed semicolon-separated rows.
    """
    rows = [",".join(str(v) for v in row) for row in mat]
    return "[" + ";".join(rows) + "]"


# ===================================================================
# 1. ReLU Derivative (tier 4)
# ===================================================================

@register
class ReluDerivativeGenerator(StepGenerator):
    """Compute element-wise ReLU derivative for a vector.

    ReLU(x) = max(0, x). Derivative is 0 for x < 0, 1 for x > 0,
    and undefined at x = 0 (treated as 0 by convention).

    Difficulty scaling:
        Difficulty 1-3: 3-element vector with integer values.
        Difficulty 4-6: 4-element vector with decimal values.
        Difficulty 7-8: 5-element vector, also compute ReLU output.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "relu_derivative"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute element-wise ReLU derivative"

    def _vec_size(self, difficulty: int) -> int:
        """Map difficulty to vector size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Vector size (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input vector and compute ReLU derivatives.

        Args:
            difficulty: Controls vector size and value type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._vec_size(difficulty)
        if difficulty <= 3:
            x = [self._rng.randint(-5, 5) for _ in range(n)]
            x = [float(v) for v in x]
        else:
            x = [round(self._rng.uniform(-3.0, 3.0), 2) for _ in range(n)]

        relu_out = [round(max(0.0, v), 4) for v in x]
        deriv = [1.0 if v > 0 else 0.0 for v in x]

        problem = f"ReLU'(x), x={_fv(x)}"
        return problem, {
            "x": x, "relu_out": relu_out, "deriv": deriv,
            "show_relu": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element derivative computation steps.

        Args:
            data: Solution data with input and derivatives.

        Returns:
            Steps showing each element's derivative.
        """
        steps: list[str] = []
        if data["show_relu"]:
            steps.append(f"ReLU(x)={_fv(data['relu_out'])}")
        for i, xi in enumerate(data["x"]):
            sign = ">" if xi > 0 else ("<" if xi < 0 else "=")
            steps.append(f"x_{i}={xi} {sign} 0 -> d={data['deriv'][i]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the derivative vector.

        Args:
            data: Solution data.

        Returns:
            String representation of derivative vector.
        """
        return _fv(data["deriv"])


# ===================================================================
# 2. Batch Normalisation Forward (tier 5)
# ===================================================================

@register
class BatchNormForwardGenerator(StepGenerator):
    """Compute batch normalisation forward pass.

    mu = mean(x), var = mean((x-mu)^2), x_hat = (x-mu)/sqrt(var+eps),
    y = gamma*x_hat + beta. Operates over a mini-batch of values.

    Difficulty scaling:
        Difficulty 1-3: 3-element batch, gamma=1, beta=0.
        Difficulty 4-6: 4-element batch, non-trivial gamma/beta.
        Difficulty 7-8: 5-element batch, non-trivial gamma/beta.

    Prerequisites:
        arithmetic_mean.
    """

    _EPS = 1e-5

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "batch_norm_forward"

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
            difficulty: Controls batch size.

        Returns:
            Short task description.
        """
        return "compute batch normalisation forward pass"

    def _batch_size(self, difficulty: int) -> int:
        """Map difficulty to batch size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Batch size (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate batch data and compute normalised output.

        Args:
            difficulty: Controls batch size and affine params.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._batch_size(difficulty)
        x = [round(self._rng.uniform(-3.0, 6.0), 2) for _ in range(n)]

        if difficulty <= 3:
            gamma = 1.0
            beta = 0.0
        else:
            gamma = round(self._rng.uniform(0.5, 2.0), 2)
            beta = round(self._rng.uniform(-1.0, 1.0), 2)

        mu = round(sum(x) / n, 4)
        var = round(sum((xi - mu) ** 2 for xi in x) / n, 4)
        sigma = round(math.sqrt(var + self._EPS), 4)
        x_hat = [round((xi - mu) / sigma, 4) for xi in x]
        y = [round(gamma * xh + beta, 4) for xh in x_hat]

        x_str = ",".join(str(v) for v in x)
        problem = (
            f"BN(x), x=[{x_str}], \\gamma={gamma}, \\beta={beta}"
        )
        return problem, {
            "x": x, "gamma": gamma, "beta": beta, "n": n,
            "mu": mu, "var": var, "sigma": sigma,
            "x_hat": x_hat, "y": y,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean, variance, normalisation, and affine steps.

        Args:
            data: Solution data with intermediates.

        Returns:
            Steps showing mu, var, sigma, and each y_i.
        """
        steps: list[str] = []
        x_sum = "+".join(str(v) for v in data["x"])
        steps.append(f"\\mu=({x_sum})/{data['n']}={data['mu']}")
        steps.append(f"\\sigma^2={data['var']}")
        steps.append(
            f"\\sigma=\\sqrt{{{data['var']}+{self._EPS}}}={data['sigma']}"
        )
        for i in range(data["n"]):
            steps.append(
                f"y_{i}={data['gamma']}*{data['x_hat'][i]}+{data['beta']}"
                f"={data['y'][i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the normalised output vector.

        Args:
            data: Solution data.

        Returns:
            String representation of output vector.
        """
        return _fv(data["y"])


# ===================================================================
# 3. Dropout Forward (tier 4)
# ===================================================================

@register
class DropoutForwardGenerator(StepGenerator):
    """Compute dropout forward pass with inverted scaling.

    Given input x, binary mask m, and drop probability p:
    y = x * m / (1 - p). Scaling by 1/(1-p) maintains expected value.

    Difficulty scaling:
        Difficulty 1-3: 3-element vector, p=0.5.
        Difficulty 4-6: 4-element vector, p in {0.1, 0.2, 0.3}.
        Difficulty 7-8: 5-element vector, p in {0.1, 0.2, 0.5}.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dropout_forward"

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
            difficulty: Controls vector size.

        Returns:
            Short task description.
        """
        return "compute dropout forward pass with inverted scaling"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input, mask, and compute dropout output.

        Args:
            difficulty: Controls vector size and drop probability.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n = 3
            p = 0.5
        elif difficulty <= 6:
            n = 4
            p = self._rng.choice([0.1, 0.2, 0.3])
        else:
            n = 5
            p = self._rng.choice([0.1, 0.2, 0.5])

        x = [round(self._rng.uniform(-2.0, 3.0), 2) for _ in range(n)]
        mask = [self._rng.choice([0, 1]) for _ in range(n)]
        scale = round(1.0 / (1.0 - p), 4)
        y = [round(x[i] * mask[i] * scale, 4) for i in range(n)]

        problem = f"dropout(x), x={_fv(x)}, mask={mask}, p={p}"
        return problem, {
            "x": x, "mask": mask, "p": p, "scale": scale, "y": y,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element dropout computation steps.

        Args:
            data: Solution data with input, mask, and output.

        Returns:
            Steps showing scale factor and each element.
        """
        steps: list[str] = [f"scale=1/(1-{data['p']})={data['scale']}"]
        for i in range(len(data["x"])):
            steps.append(
                f"y_{i}={data['x'][i]}*{data['mask'][i]}*{data['scale']}"
                f"={data['y'][i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the dropout output vector.

        Args:
            data: Solution data.

        Returns:
            String representation of output vector.
        """
        return _fv(data["y"])


# ===================================================================
# 4. Conv2D Forward (tier 5)
# ===================================================================

@register
class Conv2dForwardGenerator(StepGenerator):
    """Compute 2D convolution: slide kernel over input.

    y[i,j] = sum_m sum_n K[m,n] * X[i+m, j+n]. Uses a 3x3 kernel
    on a small input (valid convolution, no padding).

    Difficulty scaling:
        Difficulty 1-3: 3x3 input, 2x2 kernel (output 2x2).
        Difficulty 4-6: 4x4 input, 3x3 kernel (output 2x2).
        Difficulty 7-8: 5x5 input, 3x3 kernel (output 3x3).

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conv2d_forward"

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
            difficulty: Controls input and kernel size.

        Returns:
            Short task description.
        """
        return "compute 2D convolution (valid, no padding)"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to input size and kernel size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (input_size, kernel_size).
        """
        if difficulty <= 3:
            return 3, 2
        if difficulty <= 6:
            return 4, 3
        return 5, 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input matrix, kernel, and compute convolution.

        Args:
            difficulty: Controls matrix dimensions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        in_size, k_size = self._config(difficulty)
        out_size = in_size - k_size + 1

        inp = [[self._rng.randint(0, 5) for _ in range(in_size)]
               for _ in range(in_size)]
        kernel = [[self._rng.randint(-2, 2) for _ in range(k_size)]
                  for _ in range(k_size)]

        output = []
        for i in range(out_size):
            row = []
            for j in range(out_size):
                val = 0
                for m in range(k_size):
                    for n in range(k_size):
                        val += kernel[m][n] * inp[i + m][j + n]
                row.append(val)
            output.append(row)

        problem = f"conv2d, X={_fm(inp)}, K={_fm(kernel)}"
        return problem, {
            "inp": inp, "kernel": kernel, "output": output,
            "in_size": in_size, "k_size": k_size, "out_size": out_size,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-position convolution steps.

        Args:
            data: Solution data with input, kernel, and output.

        Returns:
            Steps showing each output element computation.
        """
        steps: list[str] = [
            f"input {data['in_size']}x{data['in_size']}, "
            f"kernel {data['k_size']}x{data['k_size']}, "
            f"output {data['out_size']}x{data['out_size']}"
        ]
        for i in range(data["out_size"]):
            for j in range(data["out_size"]):
                steps.append(f"y[{i},{j}]={data['output'][i][j]}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the convolution output matrix.

        Args:
            data: Solution data.

        Returns:
            String representation of output matrix.
        """
        return _fm(data["output"])


# ===================================================================
# 5. Max Pooling Forward (tier 4)
# ===================================================================

@register
class MaxpoolForwardGenerator(StepGenerator):
    """Compute 2x2 max pooling on a small input matrix.

    Takes the maximum of each non-overlapping 2x2 block and records
    which position contributed (argmax).

    Difficulty scaling:
        Difficulty 1-3: 4x4 input (output 2x2).
        Difficulty 4-6: 4x4 input with decimal values.
        Difficulty 7-8: 6x6 input (output 3x3).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "maxpool_forward"

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
            difficulty: Controls input size.

        Returns:
            Short task description.
        """
        return "compute 2x2 max pooling"

    def _input_size(self, difficulty: int) -> int:
        """Map difficulty to input matrix size.

        Args:
            difficulty: Difficulty level.

        Returns:
            Input size (4 or 6).
        """
        if difficulty <= 6:
            return 4
        return 6

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input matrix and compute max pooling.

        Args:
            difficulty: Controls input size and value type.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        size = self._input_size(difficulty)
        out_size = size // 2

        if difficulty <= 3:
            inp = [[self._rng.randint(0, 9) for _ in range(size)]
                   for _ in range(size)]
        else:
            inp = [[round(self._rng.uniform(0.0, 9.0), 2)
                    for _ in range(size)] for _ in range(size)]

        output = []
        positions = []
        for i in range(out_size):
            row_out = []
            row_pos = []
            for j in range(out_size):
                block = []
                for di in range(2):
                    for dj in range(2):
                        block.append(
                            (inp[2 * i + di][2 * j + dj], 2 * i + di, 2 * j + dj)
                        )
                best = max(block, key=lambda t: t[0])
                row_out.append(round(best[0], 4))
                row_pos.append((best[1], best[2]))
            output.append(row_out)
            positions.append(row_pos)

        problem = f"maxpool2x2, X={_fm(inp)}"
        return problem, {
            "inp": inp, "output": output, "positions": positions,
            "out_size": out_size,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-block max pooling steps.

        Args:
            data: Solution data with input, output, and positions.

        Returns:
            Steps showing each block's max and position.
        """
        steps: list[str] = []
        for i in range(data["out_size"]):
            for j in range(data["out_size"]):
                pos = data["positions"][i][j]
                steps.append(
                    f"block[{i},{j}]: max={data['output'][i][j]} "
                    f"at ({pos[0]},{pos[1]})"
                )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the pooled output matrix.

        Args:
            data: Solution data.

        Returns:
            String representation of pooled output.
        """
        return _fm(data["output"])


# ===================================================================
# 6. Embedding Lookup (tier 3)
# ===================================================================

@register
class EmbeddingLookupGenerator(StepGenerator):
    """Look up token embeddings from an embedding matrix.

    Given embedding matrix E of shape (V, d) and a sequence of token
    IDs, retrieve E[token_id] for each token.

    Difficulty scaling:
        Difficulty 1-3: V=4, d=2, sequence length 2.
        Difficulty 4-6: V=6, d=3, sequence length 3.
        Difficulty 7-8: V=8, d=3, sequence length 4.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "embedding_lookup"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vocabulary and embedding size.

        Returns:
            Short task description.
        """
        return "look up token embeddings from embedding matrix"

    def _config(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to vocab size, embed dim, and sequence length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (vocab_size, embed_dim, seq_len).
        """
        if difficulty <= 3:
            return 4, 2, 2
        if difficulty <= 6:
            return 6, 3, 3
        return 8, 3, 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate embedding matrix and token sequence.

        Args:
            difficulty: Controls dimensions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        vocab, dim, seq_len = self._config(difficulty)
        emb = [[round(self._rng.uniform(-1.0, 1.0), 2)
                for _ in range(dim)] for _ in range(vocab)]
        tokens = [self._rng.randint(0, vocab - 1) for _ in range(seq_len)]
        output = [emb[t] for t in tokens]

        problem = f"E[tokens], E={_fm(emb)}, tokens={tokens}"
        return problem, {
            "emb": emb, "tokens": tokens, "output": output,
            "vocab": vocab, "dim": dim,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-token lookup steps.

        Args:
            data: Solution data with embeddings and tokens.

        Returns:
            Steps showing each token's embedding.
        """
        steps: list[str] = [
            f"E: {data['vocab']}x{data['dim']} embedding matrix"
        ]
        for i, t in enumerate(data["tokens"]):
            steps.append(f"token {t} -> E[{t}]={_fv(data['output'][i])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the looked-up embedding sequence.

        Args:
            data: Solution data.

        Returns:
            String representation of embedding sequence.
        """
        return _fm(data["output"])


# ===================================================================
# 7. GELU Compute (tier 5)
# ===================================================================

@register
class GeluComputeGenerator(StepGenerator):
    """Compute GELU activation using the tanh approximation.

    GELU(x) = 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3))).

    Difficulty scaling:
        Difficulty 1-3: 3-element vector with values in [-1, 1].
        Difficulty 4-6: 4-element vector with values in [-3, 3].
        Difficulty 7-8: 5-element vector with values in [-5, 5].

    Prerequisites:
        sigmoid_eval.
    """

    _SQRT_2_PI = round(math.sqrt(2.0 / math.pi), 4)
    _COEFF = 0.044715

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gelu_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sigmoid_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size and range.

        Returns:
            Short task description.
        """
        return "compute GELU activation (tanh approximation)"

    def _config(self, difficulty: int) -> tuple[int, float, float]:
        """Map difficulty to vector size and value range.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (size, lo, hi).
        """
        if difficulty <= 3:
            return 3, -1.0, 1.0
        if difficulty <= 6:
            return 4, -3.0, 3.0
        return 5, -5.0, 5.0

    def _gelu_one(self, x: float) -> tuple[float, float, float]:
        """Compute GELU for a single value with intermediates.

        Args:
            x: Input value.

        Returns:
            Tuple of (inner, tanh_val, gelu_val).
        """
        inner = round(self._SQRT_2_PI * (x + self._COEFF * x ** 3), 4)
        tanh_val = round(math.tanh(inner), 4)
        gelu_val = round(0.5 * x * (1.0 + tanh_val), 4)
        return inner, tanh_val, gelu_val

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input vector and compute GELU values.

        Args:
            difficulty: Controls vector size and range.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, lo, hi = self._config(difficulty)
        x = [round(self._rng.uniform(lo, hi), 2) for _ in range(n)]
        results = [self._gelu_one(xi) for xi in x]
        gelu_out = [r[2] for r in results]

        problem = f"GELU(x), x={_fv(x)}"
        return problem, {
            "x": x, "results": results, "gelu_out": gelu_out,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-element GELU computation steps.

        Args:
            data: Solution data with intermediates and output.

        Returns:
            Steps showing inner, tanh, and GELU for each element.
        """
        steps: list[str] = [
            f"sqrt(2/pi)={self._SQRT_2_PI}, c={self._COEFF}"
        ]
        for i, (xi, (inner, tanh_val, gelu_val)) in enumerate(
            zip(data["x"], data["results"])
        ):
            steps.append(
                f"x_{i}={xi}: inner={inner}, tanh={tanh_val}, "
                f"GELU={gelu_val}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the GELU output vector.

        Args:
            data: Solution data.

        Returns:
            String representation of GELU output.
        """
        return _fv(data["gelu_out"])


# ===================================================================
# 8. Cross-Attention (tier 6)
# ===================================================================

@register
class CrossAttentionGenerator(StepGenerator):
    """Compute cross-attention: Q from decoder, K and V from encoder.

    attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V.
    Q has decoder sequence length, K/V have encoder sequence length.

    Difficulty scaling:
        Difficulty 1-3: Q 1x2, K/V 2x2.
        Difficulty 4-6: Q 2x2, K/V 2x2.
        Difficulty 7-8: Q 2x2, K/V 3x2.

    Prerequisites:
        attention_score.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cross_attention"

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
            difficulty: Controls sequence lengths.

        Returns:
            Short task description.
        """
        return "compute cross-attention (Q from decoder, K/V from encoder)"

    def _config(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to decoder len, encoder len, d_k.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (dec_len, enc_len, d_k).
        """
        if difficulty <= 3:
            return 1, 2, 2
        if difficulty <= 6:
            return 2, 2, 2
        return 2, 3, 2

    def _dot(self, a: list[float], b: list[float]) -> float:
        """Compute dot product of two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Dot product rounded to 4 dp.
        """
        return round(sum(a[i] * b[i] for i in range(len(a))), 4)

    def _softmax(self, logits: list[float]) -> list[float]:
        """Compute softmax of a vector.

        Args:
            logits: Input values.

        Returns:
            Softmax probabilities rounded to 4 dp.
        """
        mx = max(logits)
        exps = [math.exp(v - mx) for v in logits]
        total = sum(exps)
        return [round(e / total, 4) for e in exps]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Q, K, V and compute cross-attention.

        Args:
            difficulty: Controls sequence lengths.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dec_len, enc_len, d_k = self._config(difficulty)
        scale = round(math.sqrt(d_k), 4)

        q = [[round(self._rng.uniform(-1.0, 1.0), 2)
              for _ in range(d_k)] for _ in range(dec_len)]
        k = [[round(self._rng.uniform(-1.0, 1.0), 2)
              for _ in range(d_k)] for _ in range(enc_len)]
        v = [[round(self._rng.uniform(-1.0, 1.0), 2)
              for _ in range(d_k)] for _ in range(enc_len)]

        # Compute scores: Q * K^T / sqrt(d_k)
        scores = []
        for i in range(dec_len):
            row = []
            for j in range(enc_len):
                dot = self._dot(q[i], k[j])
                row.append(round(dot / scale, 4))
            scores.append(row)

        # Softmax per row
        weights = [self._softmax(row) for row in scores]

        # Weighted sum of V
        output = []
        for i in range(dec_len):
            out_row = [0.0] * d_k
            for j in range(enc_len):
                for d in range(d_k):
                    out_row[d] += weights[i][j] * v[j][d]
            output.append([round(val, 4) for val in out_row])

        problem = f"cross-attn, Q={_fm(q)}, K={_fm(k)}, V={_fm(v)}"
        return problem, {
            "q": q, "k": k, "v": v, "d_k": d_k, "scale": scale,
            "scores": scores, "weights": weights, "output": output,
            "dec_len": dec_len, "enc_len": enc_len,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cross-attention computation steps.

        Args:
            data: Solution data with scores, weights, and output.

        Returns:
            Steps showing scores, softmax, and weighted sum.
        """
        steps: list[str] = [f"d_k={data['d_k']}, scale={data['scale']}"]
        steps.append(f"scores={_fm(data['scores'])}")
        steps.append(f"weights={_fm(data['weights'])}")
        steps.append(f"output={_fm(data['output'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cross-attention output.

        Args:
            data: Solution data.

        Returns:
            String representation of attention output.
        """
        return _fm(data["output"])


# ===================================================================
# 9. Gradient Clipping (tier 5)
# ===================================================================

@register
class GradientClippingGenerator(StepGenerator):
    """Compute gradient clipping by global norm.

    If ||g|| > max_norm: g_clipped = g * max_norm / ||g||.
    Otherwise g_clipped = g.

    Difficulty scaling:
        Difficulty 1-3: 2D gradient, integer values.
        Difficulty 4-6: 3D gradient, decimal values.
        Difficulty 7-8: 4D gradient, decimal values.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gradient_clipping"

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
            difficulty: Controls gradient dimension.

        Returns:
            Short task description.
        """
        return "compute gradient clipping by global norm"

    def _dim(self, difficulty: int) -> int:
        """Map difficulty to gradient dimension.

        Args:
            difficulty: Difficulty level.

        Returns:
            Gradient dimension (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate gradient vector and compute clipped version.

        Args:
            difficulty: Controls gradient dimension.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim = self._dim(difficulty)
        max_norm = round(self._rng.uniform(1.0, 5.0), 2)

        if difficulty <= 3:
            grad = [float(self._rng.randint(-5, 5)) for _ in range(dim)]
        else:
            grad = [round(self._rng.uniform(-5.0, 5.0), 2)
                    for _ in range(dim)]

        norm = round(math.sqrt(sum(g ** 2 for g in grad)), 4)
        clipped = norm > max_norm
        if clipped:
            scale = round(max_norm / norm, 4)
            g_clipped = [round(g * scale, 4) for g in grad]
        else:
            scale = 1.0
            g_clipped = [round(g, 4) for g in grad]

        problem = (
            f"clip(g, max\\_norm={max_norm}), g={_fv(grad)}"
        )
        return problem, {
            "grad": grad, "max_norm": max_norm, "norm": norm,
            "clipped": clipped, "scale": scale, "g_clipped": g_clipped,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gradient norm and clipping steps.

        Args:
            data: Solution data with gradient and clipped result.

        Returns:
            Steps showing norm check and clipping.
        """
        steps: list[str] = [f"||g||={data['norm']}"]
        if data["clipped"]:
            steps.append(
                f"||g||={data['norm']} > {data['max_norm']}: clip"
            )
            steps.append(f"scale={data['max_norm']}/{data['norm']}={data['scale']}")
            steps.append(f"g_clipped={_fv(data['g_clipped'])}")
        else:
            steps.append(
                f"||g||={data['norm']} <= {data['max_norm']}: no clip"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the clipped gradient vector.

        Args:
            data: Solution data.

        Returns:
            String representation of clipped gradient.
        """
        return _fv(data["g_clipped"])


# ===================================================================
# 10. Learning Rate Warmup (tier 4)
# ===================================================================

@register
class LearningRateWarmupGenerator(StepGenerator):
    """Compute linear learning rate warmup.

    lr = base_lr * step / warmup_steps for step < warmup_steps.
    After warmup, lr = base_lr.

    Difficulty scaling:
        Difficulty 1-3: warmup_steps=10, compute at 1-2 steps.
        Difficulty 4-6: warmup_steps=100, compute at 3 steps.
        Difficulty 7-8: warmup_steps=1000, compute at 4 steps.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "learning_rate_warmup"

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
            difficulty: Controls warmup steps.

        Returns:
            Short task description.
        """
        return "compute linear learning rate warmup"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate warmup parameters and compute LR at steps.

        Args:
            difficulty: Controls warmup_steps and number of query steps.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        base_lr = self._rng.choice([0.001, 0.0005, 0.0001])

        if difficulty <= 3:
            warmup_steps = 10
            n_query = 2
        elif difficulty <= 6:
            warmup_steps = 100
            n_query = 3
        else:
            warmup_steps = 1000
            n_query = 4

        query_steps = sorted(
            self._rng.sample(range(1, warmup_steps), min(n_query, warmup_steps - 1))
        )
        results = []
        for s in query_steps:
            lr = round(base_lr * s / warmup_steps, 4)
            results.append((s, lr))

        problem = (
            f"lr\\_warmup, base\\_lr={base_lr}, "
            f"warmup\\_steps={warmup_steps}"
        )
        return problem, {
            "base_lr": base_lr, "warmup_steps": warmup_steps,
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
            f"base_lr={data['base_lr']}, warmup={data['warmup_steps']}"
        ]
        for step, lr in data["results"]:
            steps.append(
                f"step {step}: lr={data['base_lr']}*{step}"
                f"/{data['warmup_steps']}={lr}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the LR values at query steps.

        Args:
            data: Solution data.

        Returns:
            String with step:lr pairs.
        """
        parts = [f"step{s}:{lr}" for s, lr in data["results"]]
        return ", ".join(parts)


# ===================================================================
# 11. Loss Landscape Local (tier 6)
# ===================================================================

@register
class LossLandscapeLocalGenerator(StepGenerator):
    """Estimate local gradient and curvature from loss samples.

    Given loss at x-h, x, x+h: gradient = (f(x+h) - f(x-h)) / (2h),
    curvature = (f(x+h) - 2*f(x) + f(x-h)) / h^2.

    Difficulty scaling:
        Difficulty 1-3: integer loss values, h=1.
        Difficulty 4-6: decimal loss values, h=0.1.
        Difficulty 7-8: decimal values, h=0.01, classify stationary point.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loss_landscape_local"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls precision.

        Returns:
            Short task description.
        """
        return "estimate gradient and curvature from loss samples"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate three loss values and compute gradient/curvature.

        Args:
            difficulty: Controls value precision and step size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            h = 1.0
            f_left = float(self._rng.randint(1, 20))
            f_mid = float(self._rng.randint(1, 20))
            f_right = float(self._rng.randint(1, 20))
        elif difficulty <= 6:
            h = 0.1
            f_left = round(self._rng.uniform(0.5, 10.0), 2)
            f_mid = round(self._rng.uniform(0.5, 10.0), 2)
            f_right = round(self._rng.uniform(0.5, 10.0), 2)
        else:
            h = 0.01
            f_left = round(self._rng.uniform(0.5, 10.0), 4)
            f_mid = round(self._rng.uniform(0.5, 10.0), 4)
            f_right = round(self._rng.uniform(0.5, 10.0), 4)

        grad = round((f_right - f_left) / (2 * h), 4)
        curv = round((f_right - 2 * f_mid + f_left) / (h ** 2), 4)

        classify = ""
        if difficulty >= 7:
            if curv > 0:
                classify = "local minimum region"
            elif curv < 0:
                classify = "local maximum region"
            else:
                classify = "inflection region"

        problem = (
            f"f(x-h)={f_left}, f(x)={f_mid}, f(x+h)={f_right}, h={h}"
        )
        return problem, {
            "f_left": f_left, "f_mid": f_mid, "f_right": f_right,
            "h": h, "grad": grad, "curv": curv, "classify": classify,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate gradient and curvature estimation steps.

        Args:
            data: Solution data with loss values and estimates.

        Returns:
            Steps showing gradient and curvature formulas.
        """
        steps: list[str] = [
            f"f(x-h)={data['f_left']}, f(x)={data['f_mid']}, "
            f"f(x+h)={data['f_right']}"
        ]
        steps.append(
            f"grad=({data['f_right']}-{data['f_left']})/(2*{data['h']})"
            f"={data['grad']}"
        )
        steps.append(
            f"curv=({data['f_right']}-2*{data['f_mid']}+{data['f_left']})"
            f"/{data['h']}^2={data['curv']}"
        )
        if data["classify"]:
            steps.append(f"curvature {data['curv']}: {data['classify']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the estimated gradient and curvature.

        Args:
            data: Solution data.

        Returns:
            String with gradient and curvature values.
        """
        ans = f"grad={data['grad']}, curv={data['curv']}"
        if data["classify"]:
            ans += f", {data['classify']}"
        return ans


# ===================================================================
# 12. Weight Decay Update (tier 5)
# ===================================================================

@register
class WeightDecayUpdateGenerator(StepGenerator):
    """Compute weight update with weight decay (decoupled).

    w_new = w - lr * (grad + lambda * w). Shows the effective update
    combining gradient and regularisation terms.

    Difficulty scaling:
        Difficulty 1-3: 2D weight, integer values.
        Difficulty 4-6: 3D weight, decimal values.
        Difficulty 7-8: 4D weight, compare with/without decay.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "weight_decay_update"

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
            difficulty: Controls weight dimension.

        Returns:
            Short task description.
        """
        return "compute weight update with weight decay"

    def _dim(self, difficulty: int) -> int:
        """Map difficulty to weight dimension.

        Args:
            difficulty: Difficulty level.

        Returns:
            Weight dimension (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate weights, gradients, and compute decay update.

        Args:
            difficulty: Controls weight dimension.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim = self._dim(difficulty)
        lr = self._rng.choice([0.01, 0.001, 0.1])
        lam = round(self._rng.uniform(0.001, 0.1), 4)

        if difficulty <= 3:
            w = [float(self._rng.randint(-5, 5)) for _ in range(dim)]
            grad = [float(self._rng.randint(-3, 3)) for _ in range(dim)]
        else:
            w = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]
            grad = [round(self._rng.uniform(-2.0, 2.0), 2) for _ in range(dim)]

        eff_grad = [round(grad[i] + lam * w[i], 4) for i in range(dim)]
        w_new = [round(w[i] - lr * eff_grad[i], 4) for i in range(dim)]

        # Without decay for comparison
        w_no_decay = [round(w[i] - lr * grad[i], 4) for i in range(dim)]

        problem = (
            f"w\\_decay, w={_fv(w)}, grad={_fv(grad)}, "
            f"lr={lr}, \\lambda={lam}"
        )
        return problem, {
            "w": w, "grad": grad, "lr": lr, "lam": lam,
            "eff_grad": eff_grad, "w_new": w_new,
            "w_no_decay": w_no_decay,
            "show_compare": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate weight decay computation steps.

        Args:
            data: Solution data with weights, gradients, and updates.

        Returns:
            Steps showing effective gradient and new weights.
        """
        steps: list[str] = [
            f"lr={data['lr']}, lambda={data['lam']}"
        ]
        steps.append(f"eff_grad=grad+lambda*w={_fv(data['eff_grad'])}")
        steps.append(f"w_new=w-lr*eff_grad={_fv(data['w_new'])}")
        if data["show_compare"]:
            steps.append(f"w_no_decay=w-lr*grad={_fv(data['w_no_decay'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the updated weight vector.

        Args:
            data: Solution data.

        Returns:
            String representation of updated weights.
        """
        return _fv(data["w_new"])
