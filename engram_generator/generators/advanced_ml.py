"""Advanced ML curriculum generators -- multi-head attention, normalisation,
positional encoding, beam search, contrastive loss, FLOPs estimation,
learning rate scheduling, and weight initialisation.

Builds on existing AI/ML generators with tier 5-6 tasks requiring
deeper understanding of transformer architecture components and
training infrastructure.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class MatrixHelper:
    """Utility for generating small float matrices used across advanced ML generators.

    Produces reproducible random matrices with controlled magnitude and
    precision, suitable for demonstrating attention and normalisation.

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

    def float_matrix(self, rows: int, cols: int, lo: float, hi: float,
                     decimals: int = 2) -> list[list[float]]:
        """Generate a matrix of rounded random floats.

        Args:
            rows: Number of rows.
            cols: Number of columns.
            lo: Lower bound (inclusive).
            hi: Upper bound (inclusive).
            decimals: Decimal places for rounding.

        Returns:
            2D list of rounded floats.
        """
        return [self.float_vector(cols, lo, hi, decimals) for _ in range(rows)]


@register
class AttentionMultiheadGenerator(StepGenerator):
    """Compute multi-head attention: split Q,K,V into h heads, attend, concat.

    Uses h=2 heads with d_model=4 (d_k=2 per head). For each head,
    computes scaled dot-product attention scores, applies softmax,
    and multiplies by V. Final output concatenates head outputs.

    Input format:
        ``compute multi-head attention with 2 heads``

    Target format:
        ``Q,K,V each [2,4], h=2, d_k=2 <step>
        head_0: scores=Q0*K0^T/sqrt(2) <step> softmax <step> *V0
        <step> head_1: ... <step> concat <step> [result]``

    Difficulty scaling:
        Difficulty 1-3: sequence length 2, d_model=4, h=2.
        Difficulty 4-6: sequence length 2, d_model=4, h=2, varied values.
        Difficulty 7-8: sequence length 3, d_model=4, h=2.

    Prerequisites:
        attention_score.

    Example:
        >>> gen = AttentionMultiheadGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'attention_multihead'
    """

    _NUM_HEADS = 1
    _D_MODEL = 2

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "attention_multihead"

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
            difficulty: Controls sequence length.

        Returns:
            Natural language description.
        """
        return "compute multi-head attention with 2 heads"

    def _seq_len(self, difficulty: int) -> int:
        """Map difficulty to sequence length.

        Args:
            difficulty: Difficulty level.

        Returns:
            Sequence length (2 or 3).
        """
        if difficulty <= 6:
            return 2
        return 3

    def _dot_product(self, a: list[float], b: list[float]) -> float:
        """Compute dot product of two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Rounded dot product.
        """
        return round(sum(a[i] * b[i] for i in range(len(a))), 4)

    def _softmax(self, logits: list[float]) -> list[float]:
        """Compute softmax of a vector.

        Args:
            logits: Input logit values.

        Returns:
            Softmax probabilities rounded to 4 dp.
        """
        max_val = max(logits)
        exps = [math.exp(x - max_val) for x in logits]
        total = sum(exps)
        return [round(e / total, 4) for e in exps]

    def _weighted_sum(self, weights: list[float],
                      vectors: list[list[float]]) -> list[float]:
        """Compute weighted sum of vectors.

        Args:
            weights: Weight per vector.
            vectors: List of vectors to combine.

        Returns:
            Weighted sum vector rounded to 4 dp.
        """
        dim = len(vectors[0])
        result = [0.0] * dim
        for w, vec in zip(weights, vectors):
            for j in range(dim):
                result[j] += w * vec[j]
        return [round(v, 4) for v in result]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Q, K, V matrices and compute multi-head attention.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mh = MatrixHelper(self._rng)
        seq_len = self._seq_len(difficulty)
        d_k = self._D_MODEL // self._NUM_HEADS

        q = mh.float_matrix(seq_len, self._D_MODEL, -1.0, 1.0)
        k = mh.float_matrix(seq_len, self._D_MODEL, -1.0, 1.0)
        v = mh.float_matrix(seq_len, self._D_MODEL, -1.0, 1.0)

        head_outputs = []
        head_details = []
        scale = math.sqrt(d_k)

        for h in range(self._NUM_HEADS):
            q_h = [row[h * d_k:(h + 1) * d_k] for row in q]
            k_h = [row[h * d_k:(h + 1) * d_k] for row in k]
            v_h = [row[h * d_k:(h + 1) * d_k] for row in v]

            scores = []
            for i in range(seq_len):
                row_scores = []
                for j in range(seq_len):
                    dot = self._dot_product(q_h[i], k_h[j])
                    row_scores.append(round(dot / scale, 4))
                scores.append(row_scores)

            attn_weights = [self._softmax(row) for row in scores]
            output = []
            for i in range(seq_len):
                output.append(self._weighted_sum(attn_weights[i], v_h))

            head_outputs.append(output)
            head_details.append({
                "q_h": q_h, "k_h": k_h, "v_h": v_h,
                "scores": scores, "attn_weights": attn_weights,
                "output": output,
            })

        concat = []
        for i in range(seq_len):
            row = []
            for h in range(self._NUM_HEADS):
                row.extend(head_outputs[h][i])
            concat.append(row)

        q_str = self._format_matrix(q)
        k_str = self._format_matrix(k)
        v_str = self._format_matrix(v)
        problem = (
            f"MHA(Q,K,V), h={self._NUM_HEADS}, d_k={d_k}, "
            f"Q={q_str}, K={k_str}, V={v_str}"
        )
        return problem, {
            "q": q, "k": k, "v": v, "seq_len": seq_len,
            "d_k": d_k, "scale": round(scale, 4),
            "head_details": head_details, "concat": concat,
        }

    def _format_matrix(self, mat: list[list[float]]) -> str:
        """Format a matrix as a compact string.

        Args:
            mat: 2D list of floats.

        Returns:
            Compact string representation.
        """
        rows = [",".join(str(v) for v in row) for row in mat]
        return "[" + ";".join(rows) + "]"

    def _format_vector(self, vec: list[float]) -> str:
        """Format a vector as a compact string.

        Args:
            vec: List of floats.

        Returns:
            Compact string representation.
        """
        return "[" + ",".join(str(v) for v in vec) + "]"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-head attention computation steps.

        Args:
            data: Solution data with head details.

        Returns:
            Steps showing each head's scores, softmax, and output.
        """
        steps: list[str] = []
        for h, hd in enumerate(data["head_details"]):
            score_str = self._format_matrix(hd["scores"])
            steps.append(f"head_{h}: scores/sqrt({data['d_k']})={score_str}")
            attn_str = self._format_matrix(hd["attn_weights"])
            steps.append(f"head_{h}: softmax={attn_str}")
            out_str = self._format_matrix(hd["output"])
            steps.append(f"head_{h}: output={out_str}")
        concat_str = self._format_matrix(data["concat"])
        steps.append(f"concat={concat_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the concatenated multi-head attention output.

        Args:
            data: Solution data.

        Returns:
            String representation of concat output.
        """
        return self._format_matrix(data["concat"])


@register
class LayerNormGenerator(StepGenerator):
    """Compute LayerNorm: mu=mean(x), sigma=std(x), y=(x-mu)/sigma*gamma+beta.

    Generates a small input vector, computes mean and standard deviation
    across the feature dimension, normalises, and applies affine transform.

    Input format:
        ``compute layer normalisation``

    Target format:
        ``LN(x), x=[2.0,4.0,6.0], gamma=[1,1,1], beta=[0,0,0]
        <step> mu=4.0 <step> sigma=1.6330 <step>
        y_0=(2.0-4.0)/1.6330*1+0=-1.2247 <step> ... <step> result``

    Difficulty scaling:
        Difficulty 1-3: 3-element vector, gamma=1, beta=0.
        Difficulty 4-6: 4-element vector, gamma=1, beta=0.
        Difficulty 7-8: 4-element vector with non-trivial gamma/beta.

    Prerequisites:
        arithmetic_mean, std_dev.

    Example:
        >>> gen = LayerNormGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'layer_norm'
    """

    _EPS = 1e-5

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "layer_norm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["arithmetic_mean", "std_dev"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vector size and affine params.

        Returns:
            Natural language description.
        """
        return "compute layer normalisation"

    def _vector_size(self, difficulty: int) -> int:
        """Map difficulty to feature dimension.

        Args:
            difficulty: Difficulty level.

        Returns:
            Feature dimension (3 or 4).
        """
        if difficulty <= 3:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate input vector and affine parameters for LayerNorm.

        Args:
            difficulty: Controls vector size and affine params.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        mh = MatrixHelper(self._rng)
        n = self._vector_size(difficulty)
        x = mh.float_vector(n, -3.0, 6.0)
        gamma = mh.float_vector(n, 0.5, 2.0) if difficulty >= 7 else [1.0] * n
        beta = mh.float_vector(n, -1.0, 1.0) if difficulty >= 7 else [0.0] * n

        mu = round(sum(x) / n, 4)
        var = round(sum((xi - mu) ** 2 for xi in x) / n, 4)
        sigma = round(math.sqrt(var + self._EPS), 4)
        x_norm = [round((xi - mu) / sigma, 4) for xi in x]
        y = [round(gamma[i] * x_norm[i] + beta[i], 4) for i in range(n)]

        x_str = ",".join(str(v) for v in x)
        g_str = ",".join(str(v) for v in gamma)
        b_str = ",".join(str(v) for v in beta)
        problem = f"LN(x), x=[{x_str}], \\gamma=[{g_str}], \\beta=[{b_str}]"
        return problem, {
            "x": x, "gamma": gamma, "beta": beta, "n": n,
            "mu": mu, "var": var, "sigma": sigma,
            "x_norm": x_norm, "y": y,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mean, std, normalisation, and affine steps.

        Args:
            data: Solution data with input and intermediates.

        Returns:
            Steps showing mu, sigma, each y_i.
        """
        steps: list[str] = []
        x_sum = "+".join(str(v) for v in data["x"])
        steps.append(f"\\mu=({x_sum})/{data['n']}={data['mu']}")
        sq_terms = "+".join(f"({v}-{data['mu']})^2" for v in data["x"])
        steps.append(f"\\sigma^2=({sq_terms})/{data['n']}={data['var']}")
        steps.append(f"\\sigma=\\sqrt{{{data['var']}+{self._EPS}}}={data['sigma']}")
        for i in range(data["n"]):
            steps.append(
                f"y_{i}=({data['x'][i]}-{data['mu']})/{data['sigma']}"
                f"*{data['gamma'][i]}+{data['beta'][i]}={data['y'][i]}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the normalised output vector.

        Args:
            data: Solution data.

        Returns:
            String representation of output vector.
        """
        return "[" + ",".join(str(v) for v in data["y"]) + "]"


@register
class PositionalEncodingGenerator(StepGenerator):
    """Compute sinusoidal positional encoding for d=4, pos=0..P-1.

    PE(pos,2i) = sin(pos/10000^(2i/d)), PE(pos,2i+1) = cos(...).
    Shows the frequency computation for each dimension pair and
    evaluates sin/cos at each position.

    Input format:
        ``compute positional encoding``

    Target format:
        ``PE(pos,d=4), pos=0..2 <step>
        freq_0=1/10000^(0/4)=1.0 <step> freq_1=1/10000^(2/4)=0.01
        <step> PE(0)=[sin(0),cos(0),sin(0),cos(0)]=[0,1,0,1]
        <step> PE(1)=... <step> result``

    Difficulty scaling:
        Difficulty 1-3: pos=0..1 (2 positions).
        Difficulty 4-6: pos=0..2 (3 positions).
        Difficulty 7-8: pos=0..3 (4 positions).

    Prerequisites:
        sin_cos_eval.

    Example:
        >>> gen = PositionalEncodingGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'positional_encoding'
    """

    _D_MODEL = 4
    _BASE = 10000

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "positional_encoding"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of positions.

        Returns:
            Natural language description.
        """
        return "compute positional encoding"

    def _num_positions(self, difficulty: int) -> int:
        """Map difficulty to number of positions.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of positions (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate positional encodings for all positions.

        Args:
            difficulty: Controls number of positions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num_pos = self._num_positions(difficulty)
        d = self._D_MODEL

        freqs = []
        for i in range(d // 2):
            freq = round(1.0 / (self._BASE ** (2 * i / d)), 4)
            freqs.append(freq)

        encodings = []
        for pos in range(num_pos):
            row = []
            for i in range(d // 2):
                angle = round(pos * freqs[i], 4)
                row.append(round(math.sin(angle), 4))
                row.append(round(math.cos(angle), 4))
            encodings.append(row)

        problem = f"PE(pos, d={d}), pos=0..{num_pos - 1}"
        return problem, {
            "d": d, "num_pos": num_pos,
            "freqs": freqs, "encodings": encodings,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate frequency and per-position encoding steps.

        Args:
            data: Solution data with frequencies and encodings.

        Returns:
            Steps showing frequencies and PE values.
        """
        steps: list[str] = []
        for i, freq in enumerate(data["freqs"]):
            exp = round(2 * i / data["d"], 4)
            steps.append(f"freq_{i}=1/{self._BASE}^{{{exp}}}={freq}")
        for pos in range(data["num_pos"]):
            enc = data["encodings"][pos]
            enc_str = ",".join(str(v) for v in enc)
            steps.append(f"PE({pos})=[{enc_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the full positional encoding matrix.

        Args:
            data: Solution data.

        Returns:
            String representation of encoding matrix.
        """
        rows = []
        for enc in data["encodings"]:
            rows.append(",".join(str(v) for v in enc))
        return "[" + ";".join(rows) + "]"


@register
class BeamSearchStepGenerator(StepGenerator):
    """One step of beam search with beam width k=2.

    Given current beams (partial sequences with scores) and next-token
    log-probabilities, expands each beam, scores all candidates,
    and selects the top-k.

    Input format:
        ``perform one step of beam search``

    Target format:
        ``beams: [("a",−0.5),("b",−0.8)], next_probs given
        <step> expand "a": "a"+"x"=−0.5+(−0.3)=−0.8, ...
        <step> expand "b": ... <step> all candidates sorted
        <step> top-2: ... <step> result``

    Difficulty scaling:
        Difficulty 1-3: 2 beams, 2 next tokens.
        Difficulty 4-6: 2 beams, 3 next tokens.
        Difficulty 7-8: 2 beams, 4 next tokens.

    Prerequisites:
        softmax_eval.

    Example:
        >>> gen = BeamSearchStepGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'beam_search_step'
    """

    _BEAM_WIDTH = 2
    _TOKENS = ["x", "y", "z", "w"]

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "beam_search_step"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["softmax_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls vocabulary size.

        Returns:
            Natural language description.
        """
        return "perform one step of beam search"

    def _num_tokens(self, difficulty: int) -> int:
        """Map difficulty to number of candidate next tokens.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of next tokens (2-4).
        """
        if difficulty <= 3:
            return 2
        if difficulty <= 6:
            return 3
        return 4

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate beam state and next-token probabilities.

        Args:
            difficulty: Controls vocabulary size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        num_tokens = self._num_tokens(difficulty)
        beam_seqs = [chr(ord("a") + i) for i in range(self._BEAM_WIDTH)]
        beam_scores = [round(self._rng.uniform(-2.0, -0.1), 4)
                       for _ in range(self._BEAM_WIDTH)]

        next_log_probs = []
        for _ in range(self._BEAM_WIDTH):
            probs = [round(self._rng.uniform(-3.0, -0.1), 4)
                     for _ in range(num_tokens)]
            next_log_probs.append(probs)

        candidates = []
        for b in range(self._BEAM_WIDTH):
            for t in range(num_tokens):
                new_seq = beam_seqs[b] + self._TOKENS[t]
                new_score = round(beam_scores[b] + next_log_probs[b][t], 4)
                candidates.append((new_seq, new_score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top_k = candidates[:self._BEAM_WIDTH]

        beams_str = ", ".join(
            f"(\"{s}\",{sc})" for s, sc in zip(beam_seqs, beam_scores)
        )
        tokens_str = ",".join(self._TOKENS[:num_tokens])
        problem = (
            f"beam search k={self._BEAM_WIDTH}, "
            f"beams=[{beams_str}], tokens=[{tokens_str}]"
        )
        return problem, {
            "beam_seqs": beam_seqs, "beam_scores": beam_scores,
            "next_log_probs": next_log_probs, "num_tokens": num_tokens,
            "candidates": candidates, "top_k": top_k,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate beam expansion and selection steps.

        Args:
            data: Solution data with beams and candidates.

        Returns:
            Steps showing expansion, scoring, and top-k selection.
        """
        steps: list[str] = []
        for b in range(self._BEAM_WIDTH):
            expansions = []
            for t in range(data["num_tokens"]):
                tok = self._TOKENS[t]
                lp = data["next_log_probs"][b][t]
                new_score = round(data["beam_scores"][b] + lp, 4)
                expansions.append(
                    f"\"{data['beam_seqs'][b]}{tok}\"="
                    f"{data['beam_scores'][b]}+{lp}={new_score}"
                )
            steps.append(f"expand \"{data['beam_seqs'][b]}\": {', '.join(expansions)}")

        sorted_str = ", ".join(
            f"(\"{s}\",{sc})" for s, sc in data["candidates"]
        )
        steps.append(f"all candidates: {sorted_str}")

        top_str = ", ".join(
            f"(\"{s}\",{sc})" for s, sc in data["top_k"]
        )
        steps.append(f"top-{self._BEAM_WIDTH}: {top_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the top-k beams after this step.

        Args:
            data: Solution data.

        Returns:
            String representation of selected beams.
        """
        parts = [f"(\"{s}\",{sc})" for s, sc in data["top_k"]]
        return "[" + ",".join(parts) + "]"


@register
class ContrastiveLossGenerator(StepGenerator):
    """Compute InfoNCE loss: -log(exp(sim(q,k+)/tau) / sum(exp(sim(q,ki)/tau))).

    Generates a query vector, one positive key, and N-1 negative keys.
    Computes cosine similarity for each pair, applies temperature scaling,
    and evaluates the contrastive loss.

    Input format:
        ``compute contrastive loss (InfoNCE)``

    Target format:
        ``q=[...], k+=[...], k-=[...], tau=0.1 <step>
        sim(q,k+)=0.85 <step> sim(q,k0-)=0.3 <step> ...
        <step> numerator=exp(0.85/0.1)=... <step>
        denominator=sum(...) <step> loss=-log(num/den)=... <step> result``

    Difficulty scaling:
        Difficulty 1-3: 2D vectors, 1 negative.
        Difficulty 4-6: 3D vectors, 2 negatives.
        Difficulty 7-8: 3D vectors, 3 negatives.

    Prerequisites:
        cross_entropy.

    Example:
        >>> gen = ContrastiveLossGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'contrastive_loss'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "contrastive_loss"

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
            difficulty: Controls vector dim and number of negatives.

        Returns:
            Natural language description.
        """
        return "compute contrastive loss (InfoNCE)"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to vector dimension and negative count.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (dimension, num_negatives).
        """
        if difficulty <= 3:
            return 2, 1
        if difficulty <= 6:
            return 3, 2
        return 3, 3

    def _cosine_sim(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Cosine similarity rounded to 4 dp.
        """
        dot = sum(a[i] * b[i] for i in range(len(a)))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return round(dot / (norm_a * norm_b), 4)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate query, positive key, and negative keys for InfoNCE.

        Args:
            difficulty: Controls dimensions and negative count.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        dim, num_neg = self._config(difficulty)
        mh = MatrixHelper(self._rng)
        tau = self._rng.choice([0.1, 0.5, 1.0])

        q = mh.float_vector(dim, -1.0, 1.0)
        k_pos = [round(q[i] + self._rng.uniform(-0.3, 0.3), 2)
                 for i in range(dim)]
        k_negs = [mh.float_vector(dim, -1.0, 1.0) for _ in range(num_neg)]

        sim_pos = self._cosine_sim(q, k_pos)
        sim_negs = [self._cosine_sim(q, kn) for kn in k_negs]

        all_sims = [sim_pos] + sim_negs
        exp_terms = [round(math.exp(s / tau), 4) for s in all_sims]
        numerator = exp_terms[0]
        denominator = round(sum(exp_terms), 4)
        loss = round(-math.log(numerator / denominator), 4)

        q_str = ",".join(str(v) for v in q)
        kp_str = ",".join(str(v) for v in k_pos)
        kn_strs = [",".join(str(v) for v in kn) for kn in k_negs]
        neg_part = "; ".join(f"k^-_{i}=[{s}]" for i, s in enumerate(kn_strs))
        problem = (
            f"InfoNCE, q=[{q_str}], k^+=[{kp_str}], "
            f"{neg_part}, \\tau={tau}"
        )
        return problem, {
            "q": q, "k_pos": k_pos, "k_negs": k_negs,
            "tau": tau, "sim_pos": sim_pos, "sim_negs": sim_negs,
            "exp_terms": exp_terms, "numerator": numerator,
            "denominator": denominator, "loss": loss,
            "num_neg": num_neg,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate similarity, exponent, and loss computation steps.

        Args:
            data: Solution data with similarities and loss.

        Returns:
            Steps showing sim, exp, and final loss.
        """
        steps: list[str] = []
        steps.append(f"sim(q,k^+)={data['sim_pos']}")
        for i, sim in enumerate(data["sim_negs"]):
            steps.append(f"sim(q,k^-_{i})={sim}")
        steps.append(
            f"exp({data['sim_pos']}/{data['tau']})={data['exp_terms'][0]}"
        )
        exp_str = "+".join(str(e) for e in data["exp_terms"])
        steps.append(f"denom={exp_str}={data['denominator']}")
        steps.append(
            f"loss=-\\log({data['numerator']}/{data['denominator']})={data['loss']}"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the InfoNCE loss value.

        Args:
            data: Solution data.

        Returns:
            String representation of loss.
        """
        return str(data["loss"])


@register
class TransformerFlopsGenerator(StepGenerator):
    """Estimate FLOPs for one transformer layer.

    Computes: QKV projection = 3*2*n*d^2, attention = 2*n^2*d,
    FFN = 2*2*n*d*4d = 16*n*d^2. Total per layer.

    Input format:
        ``estimate transformer FLOPs``

    Target format:
        ``n=128, d=256, L=6 <step>
        QKV=3*2*128*256^2=... <step> attn=2*128^2*256=...
        <step> FFN=2*2*128*256*1024=... <step>
        per_layer=QKV+attn+FFN <step> total=per_layer*L <step> result``

    Difficulty scaling:
        Difficulty 1-3: n=32, d=64, L=1.
        Difficulty 4-6: n=128, d=256, L=4.
        Difficulty 7-8: n=512, d=512, L=6.

    Prerequisites:
        multiplication.

    Example:
        >>> gen = TransformerFlopsGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'transformer_flops'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "transformer_flops"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls model dimensions.

        Returns:
            Natural language description.
        """
        return "estimate transformer FLOPs"

    def _config(self, difficulty: int) -> tuple[int, int, int]:
        """Map difficulty to sequence length, d_model, and num layers.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (seq_len, d_model, num_layers).
        """
        if difficulty <= 3:
            return 32, 64, 1
        if difficulty <= 6:
            return 128, 256, 4
        return 512, 512, 6

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate transformer dimensions and compute FLOPs.

        Args:
            difficulty: Controls model size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n, d, num_layers = self._config(difficulty)
        d_ff = 4 * d

        qkv_flops = 3 * 2 * n * d * d
        attn_flops = 2 * n * n * d
        ffn_flops = 2 * 2 * n * d * d_ff
        per_layer = qkv_flops + attn_flops + ffn_flops
        total = per_layer * num_layers

        problem = f"transformer FLOPs: n={n}, d={d}, d_{{ff}}={d_ff}, L={num_layers}"
        return problem, {
            "n": n, "d": d, "d_ff": d_ff, "num_layers": num_layers,
            "qkv_flops": qkv_flops, "attn_flops": attn_flops,
            "ffn_flops": ffn_flops, "per_layer": per_layer,
            "total": total,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-component FLOP computation steps.

        Args:
            data: Solution data with model dimensions and FLOPs.

        Returns:
            Steps showing QKV, attention, FFN, and total FLOPs.
        """
        n, d = data["n"], data["d"]
        return [
            f"QKV=3*2*{n}*{d}^2={data['qkv_flops']}",
            f"attn=2*{n}^2*{d}={data['attn_flops']}",
            f"FFN=2*2*{n}*{d}*{data['d_ff']}={data['ffn_flops']}",
            f"per_layer={data['qkv_flops']}+{data['attn_flops']}+{data['ffn_flops']}={data['per_layer']}",
            f"total={data['per_layer']}*{data['num_layers']}={data['total']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the total FLOPs.

        Args:
            data: Solution data.

        Returns:
            String representation of total FLOPs.
        """
        return str(data["total"])


@register
class LRScheduleGenerator(StepGenerator):
    """Compute learning rate at step t with warmup and cosine decay.

    For t < T_w: lr = lr_max * t / T_w (linear warmup).
    For t >= T_w: lr = lr_min + 0.5*(lr_max - lr_min)*(1 + cos(pi*(t-T_w)/(T_max-T_w))).

    Input format:
        ``compute learning rate at step t``

    Target format:
        ``lr_max=0.001, lr_min=1e-6, T_w=100, T_max=1000, t=500
        <step> t>=T_w, use cosine decay <step>
        progress=(500-100)/(1000-100)=0.4444 <step>
        cos(pi*0.4444)=... <step> lr=... <step> result``

    Difficulty scaling:
        Difficulty 1-3: warmup phase (t < T_w).
        Difficulty 4-6: cosine decay phase, round step.
        Difficulty 7-8: cosine decay phase, arbitrary step.

    Prerequisites:
        sin_cos_eval.

    Example:
        >>> gen = LRScheduleGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'lr_schedule'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "lr_schedule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls which phase the step falls in.

        Returns:
            Natural language description.
        """
        return "compute learning rate at step t"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate LR schedule parameters and compute LR at step t.

        Args:
            difficulty: Controls which phase.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        lr_max = self._rng.choice([0.001, 0.0005, 0.0001])
        lr_min = 1e-6
        t_warmup = self._rng.choice([100, 200, 500])
        t_max = self._rng.choice([1000, 2000, 5000])

        if difficulty <= 3:
            t = self._rng.randint(1, t_warmup - 1)
            phase = "warmup"
            lr = round(lr_max * t / t_warmup, 4)
            progress = round(t / t_warmup, 4)
            cos_val = None
        else:
            t = self._rng.randint(t_warmup, t_max)
            phase = "cosine"
            progress = round((t - t_warmup) / (t_max - t_warmup), 4)
            cos_val = round(math.cos(math.pi * progress), 4)
            lr = round(lr_min + 0.5 * (lr_max - lr_min) * (1 + cos_val), 4)

        problem = (
            f"lr(t), lr_{{max}}={lr_max}, lr_{{min}}={lr_min}, "
            f"T_w={t_warmup}, T_{{max}}={t_max}, t={t}"
        )
        return problem, {
            "lr_max": lr_max, "lr_min": lr_min,
            "t_warmup": t_warmup, "t_max": t_max, "t": t,
            "phase": phase, "progress": progress,
            "cos_val": cos_val, "lr": lr,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate phase identification and LR computation steps.

        Args:
            data: Solution data with schedule parameters.

        Returns:
            Steps showing phase, progress, and LR formula.
        """
        steps: list[str] = []
        if data["phase"] == "warmup":
            steps.append(f"t={data['t']} < T_w={data['t_warmup']}: warmup phase")
            steps.append(
                f"lr={data['lr_max']}*{data['t']}/{data['t_warmup']}="
                f"{data['lr']}"
            )
        else:
            steps.append(
                f"t={data['t']} >= T_w={data['t_warmup']}: cosine decay"
            )
            steps.append(
                f"progress=({data['t']}-{data['t_warmup']})"
                f"/({data['t_max']}-{data['t_warmup']})={data['progress']}"
            )
            steps.append(
                f"\\cos(\\pi*{data['progress']})={data['cos_val']}"
            )
            steps.append(
                f"lr={data['lr_min']}+0.5*({data['lr_max']}-{data['lr_min']})"
                f"*(1+{data['cos_val']})={data['lr']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the learning rate at step t.

        Args:
            data: Solution data.

        Returns:
            String representation of learning rate.
        """
        return str(data["lr"])


@register
class WeightInitGenerator(StepGenerator):
    """Compute Xavier and He initialisation variances.

    Xavier: var = 2 / (fan_in + fan_out).
    He: var = 2 / fan_in.
    Shows both computations and the resulting standard deviations.

    Input format:
        ``compute weight initialisation variance``

    Target format:
        ``fan_in=512, fan_out=256 <step>
        Xavier: var=2/(512+256)=0.0026 <step> std=sqrt(0.0026)=0.051
        <step> He: var=2/512=0.0039 <step> std=sqrt(0.0039)=0.0625
        <step> Xavier_var=0.0026, He_var=0.0039``

    Difficulty scaling:
        Difficulty 1-3: small layers (fan_in 32-64).
        Difficulty 4-6: medium layers (fan_in 128-512).
        Difficulty 7-8: large layers (fan_in 512-2048).

    Prerequisites:
        division, square_root.

    Example:
        >>> gen = WeightInitGenerator(min_difficulty=1, max_difficulty=1, seed=42)
        >>> sample = gen.generate(1)[0]
        >>> sample.task_name
        'weight_init'
    """

    @property
    def task_name(self) -> str:
        """Return the task identifier."""
        return "weight_init"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division", "square_root"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls layer dimensions.

        Returns:
            Natural language description.
        """
        return "compute weight initialisation variance"

    def _config(self, difficulty: int) -> tuple[int, int]:
        """Map difficulty to fan_in and fan_out.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (fan_in, fan_out).
        """
        if difficulty <= 3:
            choices = [32, 64]
        elif difficulty <= 6:
            choices = [128, 256, 512]
        else:
            choices = [512, 1024, 2048]
        fan_in = self._rng.choice(choices)
        fan_out = self._rng.choice(choices)
        return fan_in, fan_out

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate layer dimensions and compute init variances.

        Args:
            difficulty: Controls layer size.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        fan_in, fan_out = self._config(difficulty)

        xavier_var = round(2.0 / (fan_in + fan_out), 4)
        xavier_std = round(math.sqrt(xavier_var), 4)
        he_var = round(2.0 / fan_in, 4)
        he_std = round(math.sqrt(he_var), 4)

        problem = f"init variance: fan_{{in}}={fan_in}, fan_{{out}}={fan_out}"
        return problem, {
            "fan_in": fan_in, "fan_out": fan_out,
            "xavier_var": xavier_var, "xavier_std": xavier_std,
            "he_var": he_var, "he_std": he_std,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Xavier and He variance computation steps.

        Args:
            data: Solution data with fan dimensions and variances.

        Returns:
            Steps showing both initialisations.
        """
        fi, fo = data["fan_in"], data["fan_out"]
        return [
            f"Xavier: var=2/({fi}+{fo})={data['xavier_var']}",
            f"Xavier: std=\\sqrt{{{data['xavier_var']}}}={data['xavier_std']}",
            f"He: var=2/{fi}={data['he_var']}",
            f"He: std=\\sqrt{{{data['he_var']}}}={data['he_std']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return both initialisation variances.

        Args:
            data: Solution data.

        Returns:
            String with Xavier and He variances.
        """
        return f"Xavier={data['xavier_var']}, He={data['he_var']}"
