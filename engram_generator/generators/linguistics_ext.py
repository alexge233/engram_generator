"""Extended linguistics generators -- syllable counting, IPA transcription,
morphological analysis, word frequency (Zipf's law), language entropy,
edit distance.

6 generators across tiers 3-5, deepening the linguistics domain.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# 1. Syllable count  (tier 3)
# ===================================================================

@register
class SyllableCountGenerator(StepGenerator):
    """Count syllables in an English word by vowel-group heuristic.

    Counts consecutive vowel groups (a, e, i, o, u, y-as-vowel),
    adjusts for silent-e and common diphthongs.

    Difficulty scaling:
        Difficulty 1-3: 1-2 syllable words.
        Difficulty 4-6: 3-4 syllable words.
        Difficulty 7-8: 5+ syllable words with silent-e.

    Prerequisites:
        counting.
    """

    _WORDS: list[dict] = [
        {"word": "cat", "syllables": 1, "groups": ["a"]},
        {"word": "dog", "syllables": 1, "groups": ["o"]},
        {"word": "apple", "syllables": 2, "groups": ["a", "e(silent-e adj)"]},
        {"word": "banana", "syllables": 3, "groups": ["a", "a", "a"]},
        {"word": "table", "syllables": 2, "groups": ["a", "e(silent-e adj)"]},
        {"word": "computer", "syllables": 3, "groups": ["o", "u", "er"]},
        {"word": "elephant", "syllables": 3, "groups": ["e", "e", "a"]},
        {"word": "beautiful", "syllables": 3, "groups": ["eau", "i", "u"]},
        {"word": "information", "syllables": 4, "groups": ["i", "o", "a", "io"]},
        {"word": "university", "syllables": 5, "groups": ["u", "i", "e", "i", "y"]},
        {"word": "communication", "syllables": 5, "groups": ["o", "u", "i", "a", "io"]},
        {"word": "extraordinary", "syllables": 6, "groups": ["e", "ao", "i", "a", "y", "adj"]},
        {"word": "simple", "syllables": 2, "groups": ["i", "e(silent-e adj)"]},
        {"word": "create", "syllables": 2, "groups": ["ea", "e(silent-e adj)"]},
        {"word": "machine", "syllables": 2, "groups": ["a", "i-e(silent-e adj)"]},
        {"word": "orange", "syllables": 2, "groups": ["o", "a-e(silent-e adj)"]},
        {"word": "fire", "syllables": 1, "groups": ["i-e(silent-e adj)"]},
        {"word": "calculate", "syllables": 3, "groups": ["a", "u", "a-e(silent-e adj)"]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "syllable_count"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "count syllables in English word"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a syllable counting problem.

        Selects a word with appropriate syllable count for the
        difficulty level.

        Args:
            difficulty: Controls word complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            candidates = [w for w in self._WORDS if w["syllables"] <= 2]
        elif difficulty <= 6:
            candidates = [w for w in self._WORDS if 3 <= w["syllables"] <= 4]
        else:
            candidates = [w for w in self._WORDS if w["syllables"] >= 4]

        if not candidates:
            candidates = self._WORDS

        word_entry = self._rng.choice(candidates)
        desc = f"count syllables: '{word_entry['word']}'"
        return desc, {
            "word": word_entry["word"],
            "syllables": word_entry["syllables"],
            "groups": word_entry["groups"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"word: {sd['word']}",
            f"vowel groups: {', '.join(sd['groups'])}",
            f"count = {sd['syllables']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the syllable count.

        Args:
            sd: Solution data.

        Returns:
            Syllable count as a string.
        """
        return str(sd["syllables"])


# ===================================================================
# 2. IPA transcription  (tier 4)
# ===================================================================

@register
class IPATranscriptionGenerator(StepGenerator):
    """Convert simple English words to IPA transcription.

    Uses a lookup table of 10+ common English words with their IPA
    transcriptions. Template-based matching.

    Difficulty scaling:
        Difficulty 1-3: simple CVC words (cat, dog, sun).
        Difficulty 4-6: multi-syllable words.
        Difficulty 7-8: words with silent letters or irregular spellings.

    Prerequisites:
        comparison.
    """

    _WORDS: list[dict] = [
        {"word": "cat", "ipa": "/k ae t/", "notes": "short a", "level": 1},
        {"word": "dog", "ipa": "/d aw g/", "notes": "open o", "level": 1},
        {"word": "sun", "ipa": "/s uh n/", "notes": "short u", "level": 1},
        {"word": "fish", "ipa": "/f ih sh/", "notes": "sh digraph", "level": 1},
        {"word": "bed", "ipa": "/b eh d/", "notes": "short e", "level": 1},
        {"word": "happy", "ipa": "/h ae p iy/", "notes": "y as vowel", "level": 2},
        {"word": "water", "ipa": "/w ao t er/", "notes": "long o, schwa", "level": 2},
        {"word": "teacher", "ipa": "/t iy ch er/", "notes": "ch digraph, schwa", "level": 2},
        {"word": "bottle", "ipa": "/b aa t l/", "notes": "syllabic l", "level": 2},
        {"word": "phone", "ipa": "/f ow n/", "notes": "ph = f, silent e", "level": 3},
        {"word": "knight", "ipa": "/n ay t/", "notes": "silent k, gh", "level": 3},
        {"word": "through", "ipa": "/th r uw/", "notes": "th fricative, silent gh", "level": 3},
        {"word": "thought", "ipa": "/th ao t/", "notes": "th fricative, silent gh", "level": 3},
        {"word": "enough", "ipa": "/ih n uh f/", "notes": "gh = f", "level": 3},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ipa_transcription"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "convert English word to IPA transcription"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IPA transcription problem.

        Selects a word with appropriate complexity for the difficulty.

        Args:
            difficulty: Controls word complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            max_level = 1
        elif difficulty <= 6:
            max_level = 2
        else:
            max_level = 3

        candidates = [w for w in self._WORDS if w["level"] <= max_level]
        word_entry = self._rng.choice(candidates)
        desc = f"IPA transcription of '{word_entry['word']}'"
        return desc, {
            "word": word_entry["word"],
            "ipa": word_entry["ipa"],
            "notes": word_entry["notes"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"word: {sd['word']}",
            f"apply rules: {sd['notes']}",
            f"IPA: {sd['ipa']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the IPA transcription.

        Args:
            sd: Solution data.

        Returns:
            IPA string.
        """
        return sd["ipa"]


# ===================================================================
# 3. Morphological analysis  (tier 4)
# ===================================================================

@register
class MorphologicalAnalysisGenerator(StepGenerator):
    """Perform full morphological parse of an English word.

    Identifies each morpheme as prefix, root, or suffix and classifies
    as derivational or inflectional.

    Difficulty scaling:
        Difficulty 1-3: 2 morphemes (root + one affix).
        Difficulty 4-6: 3 morphemes (prefix + root + suffix).
        Difficulty 7-8: 4+ morphemes with multiple affixes.

    Prerequisites:
        counting.
    """

    _WORDS: list[dict] = [
        {
            "word": "teachers", "morphemes": ["teach", "er", "s"],
            "types": ["root", "derivational suffix", "inflectional suffix"],
            "count": 3,
        },
        {
            "word": "unhappy", "morphemes": ["un", "happy"],
            "types": ["derivational prefix", "root"],
            "count": 2,
        },
        {
            "word": "unkindness", "morphemes": ["un", "kind", "ness"],
            "types": ["derivational prefix", "root", "derivational suffix"],
            "count": 3,
        },
        {
            "word": "replaying", "morphemes": ["re", "play", "ing"],
            "types": ["derivational prefix", "root", "inflectional suffix"],
            "count": 3,
        },
        {
            "word": "disagreements", "morphemes": ["dis", "agree", "ment", "s"],
            "types": ["derivational prefix", "root", "derivational suffix", "inflectional suffix"],
            "count": 4,
        },
        {
            "word": "unbelievable", "morphemes": ["un", "believe", "able"],
            "types": ["derivational prefix", "root", "derivational suffix"],
            "count": 3,
        },
        {
            "word": "walked", "morphemes": ["walk", "ed"],
            "types": ["root", "inflectional suffix"],
            "count": 2,
        },
        {
            "word": "preschools", "morphemes": ["pre", "school", "s"],
            "types": ["derivational prefix", "root", "inflectional suffix"],
            "count": 3,
        },
        {
            "word": "misunderstandings", "morphemes": ["mis", "under", "stand", "ing", "s"],
            "types": ["derivational prefix", "derivational prefix", "root",
                      "inflectional suffix", "inflectional suffix"],
            "count": 5,
        },
        {
            "word": "impossibility", "morphemes": ["im", "possible", "ity"],
            "types": ["derivational prefix", "root", "derivational suffix"],
            "count": 3,
        },
        {
            "word": "reusable", "morphemes": ["re", "use", "able"],
            "types": ["derivational prefix", "root", "derivational suffix"],
            "count": 3,
        },
        {
            "word": "unlocked", "morphemes": ["un", "lock", "ed"],
            "types": ["derivational prefix", "root", "inflectional suffix"],
            "count": 3,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "morphological_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "morphological parse: identify and classify morphemes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a morphological analysis problem.

        Selects a word with appropriate morpheme count for the
        difficulty level.

        Args:
            difficulty: Controls word complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            candidates = [w for w in self._WORDS if w["count"] <= 2]
        elif difficulty <= 6:
            candidates = [w for w in self._WORDS if w["count"] == 3]
        else:
            candidates = [w for w in self._WORDS if w["count"] >= 4]

        if not candidates:
            candidates = self._WORDS

        word_entry = self._rng.choice(candidates)
        desc = f"morphological analysis: '{word_entry['word']}'"
        return desc, {
            "word": word_entry["word"],
            "morphemes": word_entry["morphemes"],
            "types": word_entry["types"],
            "count": word_entry["count"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"word: {sd['word']}"]
        parse_parts = []
        for morph, mtype in zip(sd["morphemes"], sd["types"]):
            parse_parts.append(f"{morph} ({mtype})")
        steps.append("parse: " + " + ".join(parse_parts))
        steps.append(f"total morphemes: {sd['count']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the morphological parse.

        Args:
            sd: Solution data.

        Returns:
            Parse string with morpheme classifications.
        """
        parts = [f"{m}={t}" for m, t in zip(sd["morphemes"], sd["types"])]
        return "; ".join(parts)


# ===================================================================
# 4. Word frequency / Zipf's law  (tier 4)
# ===================================================================

@register
class WordFrequencyGenerator(StepGenerator):
    """Verify Zipf's law and compute the exponent from word frequencies.

    Zipf's law: f(r) ~ C / r^s where r is rank, f is frequency, s is
    the exponent. Given frequencies of ranked words, compute s from
    the top-2 words: s = log(f1/f2) / log(2/1).

    Difficulty scaling:
        Difficulty 1-3: 3 words, verify proportionality.
        Difficulty 4-6: 5 words, compute exponent s.
        Difficulty 7-8: 8 words, compute s and predict f(r) for new rank.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "word_frequency"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "verify Zipf's law and compute exponent"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Zipf's law problem.

        Creates ranked word frequencies following an approximate Zipf
        distribution, then asks for verification and exponent computation.

        Args:
            difficulty: Controls number of words and tasks.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_words = 3
            predict = False
        elif difficulty <= 6:
            n_words = 5
            predict = False
        else:
            n_words = 8
            predict = True

        # Generate Zipfian frequencies
        s = round(self._rng.uniform(0.8, 1.2), 2)
        c = self._rng.randint(1000, 10000)
        freqs = [round(c / (r ** s)) for r in range(1, n_words + 1)]

        # Compute s from top-2 words
        s_computed = round(math.log(freqs[0] / freqs[1]) / math.log(2), 4)

        ranked_str = ", ".join(
            f"rank {i + 1}: {f}" for i, f in enumerate(freqs)
        )
        desc = f"word frequencies: {ranked_str}; compute Zipf exponent s"

        sd: dict = {
            "freqs": freqs, "n_words": n_words, "s_true": s,
            "c": c, "s_computed": s_computed, "predict": predict,
        }

        if predict:
            pred_rank = n_words + self._rng.randint(1, 5)
            pred_freq = round(c / (pred_rank ** s_computed), 4)
            desc += f"; predict frequency for rank {pred_rank}"
            sd["pred_rank"] = pred_rank
            sd["pred_freq"] = pred_freq

        return desc, sd

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"Zipf: f(r) = C/r^s",
            f"f(1) = {sd['freqs'][0]}, f(2) = {sd['freqs'][1]}",
            f"s = log({sd['freqs'][0]}/{sd['freqs'][1]})/log(2) = {sd['s_computed']}",
        ]
        if sd["predict"]:
            steps.append(
                f"f({sd['pred_rank']}) = {sd['freqs'][0]}/{sd['pred_rank']}^{sd['s_computed']} = {sd['pred_freq']}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Zipf exponent and optional prediction.

        Args:
            sd: Solution data.

        Returns:
            Result string.
        """
        ans = f"s = {sd['s_computed']}"
        if sd["predict"]:
            ans += f", f({sd['pred_rank']}) = {sd['pred_freq']}"
        return ans


# ===================================================================
# 5. Language entropy  (tier 5)
# ===================================================================

@register
class LanguageEntropyGenerator(StepGenerator):
    """Compute character-level Shannon entropy of a text.

    H = -sum_c p(c) * log2(p(c)) where p(c) is the relative frequency
    of character c in the text.

    Difficulty scaling:
        Difficulty 1-3: 2-3 distinct characters.
        Difficulty 4-6: 4-6 distinct characters.
        Difficulty 7-8: full lowercase alphabet subset (8+ chars).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "language_entropy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute character-level Shannon entropy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a language entropy problem.

        Creates a short text with controlled character distribution,
        then computes character frequencies and Shannon entropy.

        Args:
            difficulty: Controls number of distinct characters.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_chars = self._rng.randint(2, 3)
        elif difficulty <= 6:
            n_chars = self._rng.randint(4, 6)
        else:
            n_chars = self._rng.randint(7, 10)

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        chars = list(self._rng.sample(list(alphabet), n_chars))
        # Generate counts for each character
        total = self._rng.randint(10, 30)
        counts: dict[str, int] = {}
        remaining = total
        for i, c in enumerate(chars):
            if i == len(chars) - 1:
                counts[c] = remaining
            else:
                counts[c] = self._rng.randint(1, max(1, remaining - (len(chars) - i - 1)))
                remaining -= counts[c]

        # Compute entropy
        entropy = 0.0
        freq_strs: list[str] = []
        for c in sorted(counts.keys()):
            p = counts[c] / total
            if p > 0:
                entropy -= p * math.log2(p)
                freq_strs.append(f"p({c})={round(p, 4)}")
        entropy = round(entropy, 4)

        # Build the text from counts
        text_chars: list[str] = []
        for c in sorted(counts.keys()):
            text_chars.extend([c] * counts[c])
        self._rng.shuffle(text_chars)
        text = "".join(text_chars)

        desc = f"text: '{text}'; compute Shannon entropy H"
        return desc, {
            "text": text, "counts": counts, "total": total,
            "freq_strs": freq_strs, "entropy": entropy,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        count_str = ", ".join(
            f"{c}:{sd['counts'][c]}" for c in sorted(sd["counts"].keys())
        )
        steps = [
            f"total chars = {sd['total']}",
            f"counts: {count_str}",
            f"frequencies: {', '.join(sd['freq_strs'])}",
            f"H = -sum p(c)*log2(p(c)) = {sd['entropy']} bits",
        ]
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the Shannon entropy.

        Args:
            sd: Solution data.

        Returns:
            Entropy value.
        """
        return f"H = {sd['entropy']} bits"


# ===================================================================
# 6. Edit distance (Levenshtein)  (tier 4)
# ===================================================================

@register
class EditDistanceLinguisticGenerator(StepGenerator):
    """Compute Levenshtein edit distance between two words.

    Uses dynamic programming to find the minimum number of insertions,
    deletions, and substitutions to transform one word into another.

    Difficulty scaling:
        Difficulty 1-3: words of length 3-4.
        Difficulty 4-6: words of length 4-6.
        Difficulty 7-8: words of length 6-8, show operations.

    Prerequisites:
        comparison.
    """

    _WORD_PAIRS: list[dict] = [
        {"a": "cat", "b": "car", "dist": 1, "ops": ["sub t->r"]},
        {"a": "dog", "b": "dot", "dist": 1, "ops": ["sub g->t"]},
        {"a": "kitten", "b": "sitting", "dist": 3, "ops": ["sub k->s", "sub e->i", "ins g"]},
        {"a": "book", "b": "back", "dist": 2, "ops": ["sub o->a", "sub o->c"]},
        {"a": "sunday", "b": "saturday", "dist": 3, "ops": ["ins a", "ins t", "sub n->r"]},
        {"a": "horse", "b": "house", "dist": 1, "ops": ["sub r->u"]},
        {"a": "flaw", "b": "lawn", "dist": 2, "ops": ["del f", "ins n"]},
        {"a": "gumbo", "b": "gambol", "dist": 2, "ops": ["sub u->a", "ins l"]},
        {"a": "abc", "b": "def", "dist": 3, "ops": ["sub a->d", "sub b->e", "sub c->f"]},
        {"a": "pale", "b": "apple", "dist": 3, "ops": ["ins p", "del l", "ins l", "ins e"]},
        {"a": "table", "b": "label", "dist": 3, "ops": ["sub t->l", "sub b->b", "sub l->e", "sub e->l"]},
        {"a": "rain", "b": "train", "dist": 1, "ops": ["ins t"]},
        {"a": "algorithm", "b": "altruistic", "dist": 6,
         "ops": ["sub g->t", "sub o->r", "sub r->u", "sub i->i", "sub t->s", "sub h->t", "ins i", "sub m->c"]},
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "edit_distance_linguistic"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Levenshtein edit distance"

    def _levenshtein(self, s1: str, s2: str) -> tuple[int, list[list[int]]]:
        """Compute Levenshtein distance with DP table.

        Args:
            s1: Source string.
            s2: Target string.

        Returns:
            Tuple of (distance, dp_table).
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # delete
                        dp[i][j - 1],      # insert
                        dp[i - 1][j - 1],  # substitute
                    )
        return dp[m][n], dp

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an edit distance problem.

        Selects a word pair with appropriate length for the difficulty,
        then computes the Levenshtein distance via DP.

        Args:
            difficulty: Controls word length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            candidates = [p for p in self._WORD_PAIRS if max(len(p["a"]), len(p["b"])) <= 4]
        elif difficulty <= 6:
            candidates = [p for p in self._WORD_PAIRS if 4 <= max(len(p["a"]), len(p["b"])) <= 6]
        else:
            candidates = [p for p in self._WORD_PAIRS if max(len(p["a"]), len(p["b"])) >= 5]

        if not candidates:
            candidates = self._WORD_PAIRS

        pair = self._rng.choice(candidates)
        dist, dp = self._levenshtein(pair["a"], pair["b"])

        desc = f"edit distance: '{pair['a']}' -> '{pair['b']}'"
        return desc, {
            "a": pair["a"], "b": pair["b"],
            "dist": dist, "ops": pair["ops"],
            "dp_row0": dp[0] if len(dp[0]) <= 8 else dp[0][:8],
            "dp_last": dp[-1] if len(dp[-1]) <= 8 else dp[-1][:8],
            "show_ops": difficulty > 5,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"source: '{sd['a']}' (len={len(sd['a'])})",
            f"target: '{sd['b']}' (len={len(sd['b'])})",
            f"DP row 0: {sd['dp_row0']}",
            f"DP last row: {sd['dp_last']}",
        ]
        if sd["show_ops"]:
            steps.append(f"operations: {', '.join(sd['ops'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the edit distance.

        Args:
            sd: Solution data.

        Returns:
            Distance as a string.
        """
        return f"distance = {sd['dist']}"
