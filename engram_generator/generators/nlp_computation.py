"""NLP computation task generators.

4 generators covering TF-IDF scoring, n-gram probability estimation,
BLEU score computation, and perplexity calculation.
"""
import math
from collections import Counter

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _f(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ===================================================================
# 1. TF-IDF (tier 5)
# ===================================================================

@register
class TfIdfGenerator(StepGenerator):
    """Compute TF-IDF for a query term across a document collection.

    TF = count(t, d) / |d|. IDF = log(N / df(t)). TF-IDF = TF * IDF.
    Given a small document collection (3-5 docs), compute TF-IDF for
    a query term in each document.

    Difficulty scaling:
        Difficulty 1-3: 3 short docs (3-5 words), simple vocabulary.
        Difficulty 4-6: 4 docs (4-7 words), term appears in some.
        Difficulty 7-8: 5 docs (5-8 words), compute for 2 terms.

    Prerequisites:
        logarithm.
    """

    _VOCAB = [
        "cat", "dog", "bird", "fish", "tree",
        "sky", "rain", "sun", "book", "code",
        "data", "math", "word", "text", "page",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tf_idf"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute TF-IDF for query terms across documents"
        return "compute TF-IDF for a query term"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate document collection and compute TF-IDF.

        Args:
            difficulty: Controls collection size and complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_docs = 3
            doc_len_range = (3, 5)
        elif difficulty <= 6:
            n_docs = 4
            doc_len_range = (4, 7)
        else:
            n_docs = 5
            doc_len_range = (5, 8)

        docs = self._generate_docs(n_docs, doc_len_range)
        query_term = self._pick_query_term(docs)
        results = self._compute_tfidf(docs, query_term)

        docs_str = "; ".join(" ".join(d) for d in docs)
        problem = (
            f"\\text{{TF-IDF}}: docs=[{docs_str}], "
            f"term='{query_term}'"
        )
        return problem, {
            "docs": docs, "query_term": query_term,
            "n_docs": n_docs, **results,
        }

    def _generate_docs(self, n_docs: int,
                       len_range: tuple[int, int]) -> list[list[str]]:
        """Generate a small document collection.

        Args:
            n_docs: Number of documents.
            len_range: Tuple of (min_len, max_len) for each document.

        Returns:
            List of documents, each a list of word strings.
        """
        docs = []
        for _ in range(n_docs):
            length = self._rng.randint(len_range[0], len_range[1])
            doc = [self._rng.choice(self._VOCAB) for _ in range(length)]
            docs.append(doc)
        return docs

    def _pick_query_term(self, docs: list[list[str]]) -> str:
        """Pick a query term that appears in at least one document.

        Args:
            docs: Document collection.

        Returns:
            A word that appears in some documents.
        """
        all_words = [w for d in docs for w in d]
        return self._rng.choice(all_words)

    def _compute_tfidf(self, docs: list[list[str]],
                       term: str) -> dict:
        """Compute TF, IDF, and TF-IDF for a term.

        Args:
            docs: Document collection.
            term: Query term.

        Returns:
            Dict with tf_list, df, idf, and tfidf_list.
        """
        n = len(docs)
        tf_list = []
        for doc in docs:
            count = doc.count(term)
            tf = round(count / len(doc), 4) if len(doc) > 0 else 0.0
            tf_list.append(tf)

        df = sum(1 for doc in docs if term in doc)
        df = max(df, 1)
        idf = round(math.log(n / df), 4)
        tfidf_list = [round(tf * idf, 4) for tf in tf_list]

        return {
            "tf_list": tf_list, "df": df, "idf": idf,
            "tfidf_list": tfidf_list,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate TF-IDF computation steps.

        Args:
            data: Solution data with documents and metrics.

        Returns:
            List of step strings.
        """
        steps = [f"term = '{data['query_term']}', N = {data['n_docs']}"]
        for i, doc in enumerate(data["docs"]):
            count = doc.count(data["query_term"])
            steps.append(
                f"doc{i}: TF = {count}/{len(doc)} = {_f(data['tf_list'][i])}"
            )
        steps.append(
            f"df = {data['df']}, "
            f"IDF = ln({data['n_docs']}/{data['df']}) = {_f(data['idf'])}"
        )
        for i in range(data["n_docs"]):
            steps.append(
                f"doc{i}: TF-IDF = {_f(data['tf_list'][i])}*"
                f"{_f(data['idf'])} = {_f(data['tfidf_list'][i])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the TF-IDF scores.

        Args:
            data: Solution data.

        Returns:
            TF-IDF scores per document.
        """
        scores = ", ".join(
            f"d{i}={_f(v)}" for i, v in enumerate(data["tfidf_list"])
        )
        return f"TF-IDF: [{scores}]"


# ===================================================================
# 2. N-gram Probability (tier 5)
# ===================================================================

@register
class NgramProbabilityGenerator(StepGenerator):
    """Compute bigram probability from a corpus.

    P(w_n | w_{n-1}) = count(w_{n-1}, w_n) / count(w_{n-1}).
    With Laplace smoothing at high difficulty:
    P(w_n | w_{n-1}) = (count(w_{n-1}, w_n) + 1) / (count(w_{n-1}) + V).

    Difficulty scaling:
        Difficulty 1-3: small corpus (6-8 words), no smoothing.
        Difficulty 4-6: medium corpus (8-12 words), no smoothing.
        Difficulty 7-8: medium corpus with Laplace smoothing.

    Prerequisites:
        division.
    """

    _WORDS = [
        "the", "cat", "sat", "on", "mat",
        "dog", "ran", "big", "red", "box",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ngram_probability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute bigram probability with Laplace smoothing"
        return "compute bigram probability from corpus"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate corpus and compute bigram probability.

        Args:
            difficulty: Controls corpus size and smoothing.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            corpus_len = self._rng.randint(6, 8)
        else:
            corpus_len = self._rng.randint(8, 12)

        corpus = [self._rng.choice(self._WORDS) for _ in range(corpus_len)]
        bigrams = list(zip(corpus[:-1], corpus[1:]))

        w1, w2 = self._rng.choice(bigrams)
        bigram_count = sum(1 for b in bigrams if b == (w1, w2))
        unigram_count = sum(1 for w in corpus[:-1] if w == w1)

        use_smoothing = difficulty >= 7
        vocab = list(set(corpus))
        v_size = len(vocab)

        if use_smoothing:
            prob = round((bigram_count + 1) / (unigram_count + v_size), 4)
        else:
            prob = round(bigram_count / unigram_count, 4) if unigram_count > 0 else 0.0

        corpus_str = " ".join(corpus)
        problem = (
            f"\\text{{Bigram}}: corpus='{corpus_str}', "
            f"P({w2}|{w1})"
        )
        if use_smoothing:
            problem += f", Laplace, V={v_size}"

        return problem, {
            "corpus": corpus, "w1": w1, "w2": w2,
            "bigram_count": bigram_count,
            "unigram_count": unigram_count,
            "v_size": v_size, "prob": prob,
            "use_smoothing": use_smoothing,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate bigram probability computation steps.

        Args:
            data: Solution data with corpus and counts.

        Returns:
            List of step strings.
        """
        steps = [
            f"bigram = ({data['w1']}, {data['w2']})",
            f"count({data['w1']}, {data['w2']}) = {data['bigram_count']}",
            f"count({data['w1']}) = {data['unigram_count']}",
        ]
        if data["use_smoothing"]:
            steps.append(f"V = {data['v_size']}")
            steps.append(
                f"P({data['w2']}|{data['w1']}) = "
                f"({data['bigram_count']}+1)/({data['unigram_count']}+{data['v_size']}) "
                f"= {_f(data['prob'])}"
            )
        else:
            steps.append(
                f"P({data['w2']}|{data['w1']}) = "
                f"{data['bigram_count']}/{data['unigram_count']} "
                f"= {_f(data['prob'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the bigram probability.

        Args:
            data: Solution data.

        Returns:
            Probability value.
        """
        return f"P({data['w2']}|{data['w1']}) = {_f(data['prob'])}"


# ===================================================================
# 3. BLEU Score (tier 5)
# ===================================================================

@register
class BleuScoreGenerator(StepGenerator):
    """Compute BLEU score with modified precision and brevity penalty.

    Modified precision clips n-gram count to max reference count.
    Brevity penalty BP = exp(1 - r/c) if c < r, else 1.
    Compute BLEU-1 and BLEU-2.

    Difficulty scaling:
        Difficulty 1-3: 4-6 word sentences, BLEU-1 only.
        Difficulty 4-6: 5-8 word sentences, BLEU-1 and BLEU-2.
        Difficulty 7-8: 6-10 word sentences, BLEU-1 and BLEU-2 with BP.

    Prerequisites:
        multiplication.
    """

    _WORDS = [
        "the", "cat", "is", "on", "a", "mat",
        "dog", "big", "red", "small", "sits", "runs",
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bleu_score"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 4:
            return "compute BLEU-1 and BLEU-2 scores"
        return "compute BLEU-1 score"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate candidate and reference sentences, compute BLEU.

        Args:
            difficulty: Controls sentence length and n-gram order.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            cand_len = self._rng.randint(4, 6)
            ref_len = self._rng.randint(4, 6)
        elif difficulty <= 6:
            cand_len = self._rng.randint(5, 8)
            ref_len = self._rng.randint(5, 8)
        else:
            cand_len = self._rng.randint(6, 10)
            ref_len = self._rng.randint(6, 10)

        candidate = [self._rng.choice(self._WORDS) for _ in range(cand_len)]
        reference = [self._rng.choice(self._WORDS) for _ in range(ref_len)]

        p1, p1_clip, p1_total = self._modified_precision(candidate, reference, 1)
        compute_bleu2 = difficulty >= 4
        p2 = 0.0
        p2_clip = 0
        p2_total = 0
        if compute_bleu2:
            p2, p2_clip, p2_total = self._modified_precision(candidate, reference, 2)

        c = len(candidate)
        r = len(reference)
        if c < r:
            bp = round(math.exp(1 - r / c), 4)
        else:
            bp = 1.0

        bleu1 = round(bp * p1, 4)
        bleu2 = round(bp * math.sqrt(p1 * p2), 4) if compute_bleu2 and p2 > 0 else 0.0

        cand_str = " ".join(candidate)
        ref_str = " ".join(reference)
        problem = (
            f"\\text{{BLEU}}: cand='{cand_str}', "
            f"ref='{ref_str}'"
        )
        return problem, {
            "candidate": candidate, "reference": reference,
            "p1": p1, "p1_clip": p1_clip, "p1_total": p1_total,
            "p2": p2, "p2_clip": p2_clip, "p2_total": p2_total,
            "c": c, "r": r, "bp": bp,
            "bleu1": bleu1, "bleu2": bleu2,
            "compute_bleu2": compute_bleu2,
        }

    def _modified_precision(self, candidate: list[str],
                            reference: list[str],
                            n: int) -> tuple[float, int, int]:
        """Compute modified n-gram precision.

        Args:
            candidate: Candidate sentence tokens.
            reference: Reference sentence tokens.
            n: N-gram order.

        Returns:
            Tuple of (precision, clipped_count, total_count).
        """
        cand_ngrams = self._get_ngrams(candidate, n)
        ref_ngrams = self._get_ngrams(reference, n)

        cand_counts = Counter(cand_ngrams)
        ref_counts = Counter(ref_ngrams)

        clipped = 0
        for ng, count in cand_counts.items():
            clipped += min(count, ref_counts.get(ng, 0))

        total = len(cand_ngrams)
        precision = round(clipped / total, 4) if total > 0 else 0.0
        return precision, clipped, total

    def _get_ngrams(self, tokens: list[str], n: int) -> list[tuple]:
        """Extract n-grams from a token list.

        Args:
            tokens: List of word strings.
            n: N-gram order.

        Returns:
            List of n-gram tuples.
        """
        return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BLEU score computation steps.

        Args:
            data: Solution data with sentences and metrics.

        Returns:
            List of step strings.
        """
        steps = [
            f"candidate ({data['c']} words), reference ({data['r']} words)",
            f"1-gram: clipped={data['p1_clip']}/{data['p1_total']}, "
            f"P1={_f(data['p1'])}",
        ]
        if data["compute_bleu2"]:
            steps.append(
                f"2-gram: clipped={data['p2_clip']}/{data['p2_total']}, "
                f"P2={_f(data['p2'])}"
            )
        if data["c"] < data["r"]:
            steps.append(
                f"BP = exp(1-{data['r']}/{data['c']}) = {_f(data['bp'])}"
            )
        else:
            steps.append("BP = 1 (c >= r)")
        steps.append(f"BLEU-1 = {_f(data['bp'])}*{_f(data['p1'])} = {_f(data['bleu1'])}")
        if data["compute_bleu2"]:
            geo = round(math.sqrt(data["p1"] * data["p2"]), 4) if data["p2"] > 0 else 0.0
            steps.append(
                f"BLEU-2 = {_f(data['bp'])}*sqrt({_f(data['p1'])}*{_f(data['p2'])}) "
                f"= {_f(data['bleu2'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the BLEU scores.

        Args:
            data: Solution data.

        Returns:
            BLEU-1 and optionally BLEU-2.
        """
        ans = f"BLEU-1 = {_f(data['bleu1'])}"
        if data["compute_bleu2"]:
            ans += f", BLEU-2 = {_f(data['bleu2'])}"
        return ans


# ===================================================================
# 4. Perplexity (tier 5)
# ===================================================================

@register
class PerplexityGenerator(StepGenerator):
    """Compute perplexity: PP = exp(-1/N * sum(log P(w_i))).

    Given word probabilities from a language model, compute the
    perplexity. Lower perplexity indicates a better model.

    Difficulty scaling:
        Difficulty 1-3: 3-4 words with simple probabilities.
        Difficulty 4-6: 5-6 words with varied probabilities.
        Difficulty 7-8: 7-8 words, compare two models.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "perplexity"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute and compare perplexity of two models"
        return "compute language model perplexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate word probabilities and compute perplexity.

        Args:
            difficulty: Controls number of words and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(3, 4)
        elif difficulty <= 6:
            n = self._rng.randint(5, 6)
        else:
            n = self._rng.randint(7, 8)

        probs = [round(self._rng.uniform(0.05, 0.9), 2) for _ in range(n)]
        log_probs = [round(math.log(p), 4) for p in probs]
        avg_log = round(sum(log_probs) / n, 4)
        pp = round(math.exp(-avg_log), 4)

        probs_str = ",".join(str(p) for p in probs)
        problem = f"\\text{{PP}} = \\exp(-\\frac{{1}}{{N}}\\sum \\log P(w_i)), P=[{probs_str}]"

        data = {
            "n": n, "probs": probs,
            "log_probs": log_probs, "avg_log": avg_log, "pp": pp,
            "compare": difficulty >= 7,
        }

        if difficulty >= 7:
            probs2 = [round(self._rng.uniform(0.05, 0.9), 2) for _ in range(n)]
            log_probs2 = [round(math.log(p), 4) for p in probs2]
            avg_log2 = round(sum(log_probs2) / n, 4)
            pp2 = round(math.exp(-avg_log2), 4)
            data["probs2"] = probs2
            data["log_probs2"] = log_probs2
            data["avg_log2"] = avg_log2
            data["pp2"] = pp2

        return problem, data

    def _create_steps(self, data: dict) -> list[str]:
        """Generate perplexity computation steps.

        Args:
            data: Solution data with probabilities.

        Returns:
            List of step strings.
        """
        steps = [f"N = {data['n']}"]
        for i in range(data["n"]):
            steps.append(
                f"log P(w_{i}) = log({data['probs'][i]}) = {_f(data['log_probs'][i])}"
            )
        log_sum = round(sum(data["log_probs"]), 4)
        steps.append(f"sum log P = {_f(log_sum)}")
        steps.append(f"avg log P = {_f(log_sum)}/{data['n']} = {_f(data['avg_log'])}")
        steps.append(f"PP = exp(-{_f(data['avg_log'])}) = {_f(data['pp'])}")

        if data["compare"]:
            log_sum2 = round(sum(data["log_probs2"]), 4)
            avg2 = data["avg_log2"]
            steps.append(f"Model 2: avg log P = {_f(avg2)}")
            steps.append(f"Model 2: PP = {_f(data['pp2'])}")
            better = "Model 1" if data["pp"] < data["pp2"] else "Model 2"
            steps.append(f"better = {better} (lower PP)")

        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the perplexity value.

        Args:
            data: Solution data.

        Returns:
            Perplexity value and optionally comparison.
        """
        ans = f"PP = {_f(data['pp'])}"
        if data["compare"]:
            ans += f", PP2 = {_f(data['pp2'])}"
        return ans
