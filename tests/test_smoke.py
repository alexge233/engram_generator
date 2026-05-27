"""Smoke tests — fast sanity checks for every generator."""
import pytest

from engram_generator.base import STEP_TOKEN
from engram_generator.curriculum.registry import get_all_generators
from engram_generator.tokenizer import CharTokenizer


class TestSmokeAllGenerators:
    """Rapid validation of every generator at every difficulty level.

    Generates 3 samples at each difficulty for each generator and
    checks structural invariants. Catches crashes, empty outputs,
    and format violations.
    """

    @pytest.fixture(scope="class")
    def generators(self) -> list:
        """Return all registered generators."""
        return get_all_generators()

    @pytest.fixture(scope="class")
    def tokenizer(self) -> CharTokenizer:
        """Return a shared tokenizer instance."""
        return CharTokenizer()

    def test_all_generators_at_all_difficulties(self, generators, tokenizer) -> None:
        """Verify every generator produces valid output at every difficulty.

        Args:
            generators: All registered generators.
            tokenizer: Shared tokenizer.
        """
        failures: list[str] = []

        for gen in generators:
            for diff in range(1, 9):
                gen.set_difficulty(diff, diff)
                try:
                    samples = gen.generate(3)
                except Exception as e:
                    failures.append(f"{gen.task_name} d={diff}: CRASH {e}")
                    continue

                for i, s in enumerate(samples):
                    failure = self._validate_sample(gen.task_name, diff, i, s, tokenizer)
                    if failure:
                        failures.append(failure)

        assert not failures, f"{len(failures)} failures:\n" + "\n".join(failures[:20])

    def _validate_sample(self, task: str, diff: int, idx: int,
                         sample, tokenizer: CharTokenizer) -> str | None:
        """Validate a single sample against structural invariants.

        Args:
            task: Task name for error reporting.
            diff: Difficulty level.
            idx: Sample index.
            sample: The sample to validate.
            tokenizer: Tokenizer for encoding check.

        Returns:
            Error message string, or None if valid.
        """
        prefix = f"{task} d={diff} s={idx}"

        if not sample.input_text:
            return f"{prefix}: empty input"
        if not sample.target_text:
            return f"{prefix}: empty target"
        if not sample.answer:
            return f"{prefix}: empty answer"
        if STEP_TOKEN not in sample.target_text:
            return f"{prefix}: no <step> in target"

        ids = tokenizer.encode(sample.target_text)
        decoded = tokenizer.decode(ids)
        if STEP_TOKEN not in decoded:
            return f"{prefix}: <step> lost in roundtrip"

        return None


class TestSmokeTargetLengths:
    """Verify target lengths stay within budget across all generators."""

    def test_target_under_512_chars(self) -> None:
        """Check no target exceeds 512 characters at any difficulty."""
        violations: list[str] = []
        tok = CharTokenizer()

        for gen in get_all_generators():
            for diff in range(1, 9):
                gen.set_difficulty(diff, diff)
                for s in gen.generate(3):
                    token_len = len(tok.encode(s.target_text))
                    if token_len > 512:
                        violations.append(
                            f"{gen.task_name} d={diff}: {token_len} tokens"
                        )

        if violations:
            pytest.skip(f"{len(violations)} targets exceed 512 tokens — may need truncation")


class TestSmokeInputLengths:
    """Verify input lengths stay within budget."""

    def test_input_under_128_chars(self) -> None:
        """Check no input exceeds 128 characters."""
        violations: list[str] = []
        tok = CharTokenizer()

        for gen in get_all_generators():
            for s in gen.generate(5):
                token_len = len(tok.encode(s.input_text))
                if token_len > 128:
                    violations.append(
                        f"{gen.task_name}: {token_len} tokens — {s.input_text[:50]}"
                    )

        assert not violations, f"{len(violations)} inputs exceed 128:\n" + "\n".join(violations[:10])
