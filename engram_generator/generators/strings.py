"""String and pattern manipulation generators.

9 generators across tiers 0-3.
"""
import re

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register

@register
class StringReverseGenerator(StepGenerator):
    """Reverse a string."""

    @property
    def task_name(self) -> str:
        return "string_reverse"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "reverse the string"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(3 + difficulty * 2, 20)
        chars = [chr(self._rng.randint(ord('a'), ord('z'))) for _ in range(length)]
        s = "".join(chars)
        return f"reverse: {s}", {"s": s, "reversed": s[::-1]}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"read right to left"]

    def _create_answer(self, sd: dict) -> str:
        return sd["reversed"]


@register
class CharacterCountGenerator(StepGenerator):
    """Count occurrences of a character in a string."""

    @property
    def task_name(self) -> str:
        return "character_count"

    @property
    def tier(self) -> int:
        return 0

    def task_description(self, difficulty: int) -> str:
        return "count character occurrences"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(5 + difficulty * 3, 30)
        chars = [chr(self._rng.randint(ord('a'), ord('e'))) for _ in range(length)]
        s = "".join(chars)
        target = self._rng.choice(chars)
        count = s.count(target)
        return f"count '{target}' in '{s}'", {"s": s, "target": target, "count": count}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"scan: found {sd['count']} occurrences of '{sd['target']}'"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["count"])


@register
class PalindromeCheckGenerator(StepGenerator):
    """Check if a string is a palindrome."""

    @property
    def task_name(self) -> str:
        return "palindrome_check"

    @property
    def tier(self) -> int:
        return 0

    @property
    def prerequisites(self) -> list[str]:
        return ["string_reverse"]

    def task_description(self, difficulty: int) -> str:
        return "check palindrome"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(3 + difficulty, 12)
        if self._rng.random() < 0.5:
            half = [chr(self._rng.randint(ord('a'), ord('z'))) for _ in range(length // 2)]
            s = "".join(half) + ("".join(half[::-1]) if length % 2 == 0 else
                chr(self._rng.randint(ord('a'), ord('z'))) + "".join(half[::-1]))
            is_pal = True
        else:
            s = "".join(chr(self._rng.randint(ord('a'), ord('z'))) for _ in range(length))
            is_pal = s == s[::-1]
        return f"is '{s}' a palindrome?", {"s": s, "is_palindrome": is_pal}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"reversed: '{sd['s'][::-1]}'", f"match: {sd['is_palindrome']}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["is_palindrome"] else "NO"


@register
class SubstringFindGenerator(StepGenerator):
    """Find the index of a substring."""

    @property
    def task_name(self) -> str:
        return "substring_find"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["character_count"]

    def task_description(self, difficulty: int) -> str:
        return "find substring index"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(8 + difficulty * 3, 30)
        s = "".join(chr(self._rng.randint(ord('a'), ord('f'))) for _ in range(length))
        pat_len = min(2 + difficulty // 2, 5)
        start = self._rng.randint(0, max(0, length - pat_len))
        pattern = s[start:start + pat_len]
        idx = s.find(pattern)
        return f"find '{pattern}' in '{s}'", {"s": s, "pattern": pattern, "index": idx}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"scan from left", f"found at index {sd['index']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["index"])


@register
class AnagramCheckGenerator(StepGenerator):
    """Check if two strings are anagrams."""

    @property
    def task_name(self) -> str:
        return "anagram_check"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["character_count"]

    def task_description(self, difficulty: int) -> str:
        return "check anagram"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(4 + difficulty, 10)
        chars = [chr(self._rng.randint(ord('a'), ord('h'))) for _ in range(length)]
        s1 = "".join(chars)
        if self._rng.random() < 0.5:
            shuffled = chars[:]
            self._rng.shuffle(shuffled)
            s2 = "".join(shuffled)
            is_anagram = True
        else:
            s2 = "".join(chr(self._rng.randint(ord('a'), ord('h'))) for _ in range(length))
            is_anagram = sorted(s1) == sorted(s2)
        return f"are '{s1}' and '{s2}' anagrams?", {"s1": s1, "s2": s2, "is_anagram": is_anagram}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"sorted '{sd['s1']}' = {''.join(sorted(sd['s1']))}", f"sorted '{sd['s2']}' = {''.join(sorted(sd['s2']))}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["is_anagram"] else "NO"


@register
class PatternContinueGenerator(StepGenerator):
    """Identify a pattern and predict the next element."""

    @property
    def task_name(self) -> str:
        return "pattern_continue"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "continue the pattern"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        mode = self._rng.choice(["arithmetic", "geometric", "square", "triangular"])

        if mode == "arithmetic":
            start = self._rng.randint(1, 10 * difficulty)
            step = self._rng.randint(1, 5 * difficulty)
            seq = [start + i * step for i in range(n)]
            nxt = start + n * step
            rule = f"add {step}"
        elif mode == "geometric":
            start = self._rng.randint(1, 5)
            ratio = self._rng.randint(2, 4)
            seq = [start * ratio ** i for i in range(n)]
            nxt = start * ratio ** n
            rule = f"multiply by {ratio}"
        elif mode == "square":
            seq = [i * i for i in range(1, n + 1)]
            nxt = (n + 1) ** 2
            rule = "n^2"
        else:
            seq = [i * (i + 1) // 2 for i in range(1, n + 1)]
            nxt = (n + 1) * (n + 2) // 2
            rule = "triangular numbers"

        seq_str = ", ".join(str(x) for x in seq) + ", ?"
        return seq_str, {"seq": seq, "next": nxt, "rule": rule}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"pattern: {sd['rule']}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["next"])


@register
class HammingDistanceGenerator(StepGenerator):
    """Compute Hamming distance between two strings."""

    @property
    def task_name(self) -> str:
        return "hamming_distance"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["character_count"]

    def task_description(self, difficulty: int) -> str:
        return "find Hamming distance"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        length = min(4 + difficulty * 2, 16)
        s1 = "".join(str(self._rng.randint(0, 1)) for _ in range(length))
        s2 = list(s1)
        flips = self._rng.randint(0, length)
        positions = self._rng.sample(range(length), min(flips, length))
        for p in positions:
            s2[p] = "1" if s2[p] == "0" else "0"
        s2 = "".join(s2)
        dist = sum(a != b for a, b in zip(s1, s2))
        return f"hamming('{s1}', '{s2}')", {"s1": s1, "s2": s2, "dist": dist}

    def _create_steps(self, sd: dict) -> list[str]:
        diffs = [i for i, (a, b) in enumerate(zip(sd["s1"], sd["s2"])) if a != b]
        return [f"differ at positions: {diffs}"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["dist"])


@register
class StringEncodeDecodeGenerator(StepGenerator):
    """Run-length encode or decode a string."""

    @property
    def task_name(self) -> str:
        return "string_encode_decode"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["character_count"]

    def task_description(self, difficulty: int) -> str:
        return "run-length encode/decode"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["encode", "decode"])
        if mode == "encode":
            groups = self._rng.randint(2, min(3 + difficulty, 8))
            raw = ""
            for _ in range(groups):
                c = chr(self._rng.randint(ord('a'), ord('e')))
                n = self._rng.randint(1, min(2 + difficulty, 6))
                raw += c * n
            encoded = ""
            i = 0
            while i < len(raw):
                c = raw[i]
                count = 1
                while i + count < len(raw) and raw[i + count] == c:
                    count += 1
                encoded += f"{count}{c}"
                i += count
            return f"encode: {raw}", {"raw": raw, "encoded": encoded, "mode": "encode"}
        else:
            groups = self._rng.randint(2, min(3 + difficulty, 8))
            encoded = ""
            decoded = ""
            for _ in range(groups):
                c = chr(self._rng.randint(ord('a'), ord('e')))
                n = self._rng.randint(1, min(2 + difficulty, 5))
                encoded += f"{n}{c}"
                decoded += c * n
            return f"decode: {encoded}", {"raw": decoded, "encoded": encoded, "mode": "decode"}

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "encode":
            return [f"'{sd['raw']}' -> '{sd['encoded']}'"]
        return [f"'{sd['encoded']}' -> '{sd['raw']}'"]

    def _create_answer(self, sd: dict) -> str:
        if sd["mode"] == "encode":
            return sd["encoded"]
        return sd["raw"]


@register
class RegexMatchGenerator(StepGenerator):
    """Determine if a string matches a simple regex pattern."""

    @property
    def task_name(self) -> str:
        return "regex_match"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["pattern_continue", "boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        return "check regex match"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        import re
        patterns = [
            (r"^[a-z]+$", "one or more lowercase letters"),
            (r"^\d{3}$", "exactly 3 digits"),
            (r"^[aeiou]", "starts with vowel"),
            (r".*[0-9].*", "contains a digit"),
            (r"^.{5}$", "exactly 5 characters"),
            (r"^[a-z]{2}\d{2}$", "2 letters then 2 digits"),
        ]
        pattern, desc = self._rng.choice(patterns[:min(len(patterns), difficulty + 2)])

        if self._rng.random() < 0.5:
            if "lowercase" in desc:
                s = "".join(chr(self._rng.randint(ord('a'), ord('z'))) for _ in range(5))
            elif "3 digits" in desc:
                s = "".join(str(self._rng.randint(0, 9)) for _ in range(3))
            elif "vowel" in desc:
                s = self._rng.choice("aeiou") + "bc"
            elif "contains a digit" in desc:
                s = "ab3cd"
            elif "5 characters" in desc:
                s = "abcde"
            else:
                s = "ab12"
        else:
            s = "".join(chr(self._rng.randint(ord('A'), ord('Z'))) for _ in range(4))

        match = bool(re.match(pattern, s))
        return (
            f"does '{s}' match /{pattern}/?",
            {"s": s, "pattern": pattern, "desc": desc, "match": match},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"pattern: {sd['desc']}", f"test '{sd['s']}': {sd['match']}"]

    def _create_answer(self, sd: dict) -> str:
        return "YES" if sd["match"] else "NO"
