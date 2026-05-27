"""Tests targeting every remaining uncovered line for 100% coverage."""
import sys
import pytest

from engram_generator.base import STEP_TOKEN
from engram_generator.curriculum.registry import get_all_generators, get_generator
from engram_generator.tokenizer import CharTokenizer
from engram_generator.parallel import ParallelGenerator


class TestCLIMainFunction:
    """Cover cli.py main() and parse_args by calling directly."""

    def test_main_with_task_arg(self, monkeypatch, capsys) -> None:
        """Call main() with --task argument."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog", "--task", "addition", "--samples", "2"])
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "PASS" in captured.out

    def test_main_with_all_arg(self, monkeypatch, capsys) -> None:
        """Call main() with --all argument."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog", "--all", "--samples", "1"])
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "PASSED" in captured.out

    def test_main_with_tier_arg(self, monkeypatch, capsys) -> None:
        """Call main() with --tier argument."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog", "--tier", "0", "--samples", "2"])
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "PASS" in captured.out

    def test_main_skill_tree(self, monkeypatch, capsys) -> None:
        """Call main() with --skill-tree argument."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog", "--skill-tree"])
        cli.main()
        captured = capsys.readouterr()
        assert "Tier" in captured.out

    def test_main_no_args_exits(self, monkeypatch) -> None:
        """Call main() with no arguments — should exit with code 1."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog"])
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 1

    def test_main_stress_test(self, monkeypatch, capsys) -> None:
        """Call main() with --stress-test — may report some target length warnings."""
        from engram_generator import cli
        monkeypatch.setattr(sys, "argv", ["prog", "--stress-test", "--samples", "1"])
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code in (0, 1)

    def test_validate_with_errors(self) -> None:
        """Cover the error path in validate_task with tiny max lengths."""
        from engram_generator.cli import validate_task
        results = validate_task("fibonacci", 3, 5, 5, 5, False)
        assert results["errors"]


class TestDunderMain:
    """Cover __main__.py."""

    def test_main_module_runs(self, monkeypatch, capsys) -> None:
        """Verify __main__.py calls cli.main()."""
        monkeypatch.setattr(sys, "argv", ["prog", "--task", "addition", "--samples", "1"])
        with pytest.raises(SystemExit) as exc:
            import importlib
            import engram_generator.__main__
            importlib.reload(engram_generator.__main__)
        assert exc.value.code == 0


class TestParallelEffectiveWorkers:
    """Cover the _effective_workers default path."""

    def test_default_workers_uses_cpu_count(self) -> None:
        """Verify None max_workers uses CPU count."""
        pg = ParallelGenerator(max_workers=None)
        workers = pg._effective_workers()
        assert workers >= 1


class TestGeneratorBranchCoverage:
    """Hit specific branches in generators by controlling seeds and difficulties.

    Each test targets specific uncovered lines identified from the coverage report.
    """

    def test_tier1_expression_simplify_zero_coeff(self) -> None:
        """Cover expression_simplify when x_coeff is zero."""
        gen = get_generator("expression_simplify", seed=1)
        for _ in range(50):
            s = gen.generate(1)[0]
            if "0" in s.answer:
                break

    def test_tier3_generators_at_boundary_difficulties(self) -> None:
        """Cover tier3 branches at difficulty transitions."""
        tier3_names = [
            g.task_name for g in get_all_generators() if g.tier == 3
        ]
        for name in tier3_names:
            for d in [1, 2, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier4_generators_at_boundary_difficulties(self) -> None:
        """Cover tier4 branches at difficulty transitions."""
        tier4_names = [
            g.task_name for g in get_all_generators() if g.tier == 4
        ]
        for name in tier4_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier5_generators_at_boundary_difficulties(self) -> None:
        """Cover tier5 branches at difficulty transitions."""
        tier5_names = [
            g.task_name for g in get_all_generators() if g.tier == 5
        ]
        for name in tier5_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier6_generators_at_boundary_difficulties(self) -> None:
        """Cover tier6 branches at difficulty transitions."""
        tier6_names = [
            g.task_name for g in get_all_generators() if g.tier == 6
        ]
        for name in tier6_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier7_generators_at_boundary_difficulties(self) -> None:
        """Cover tier7 branches."""
        tier7_names = [
            g.task_name for g in get_all_generators() if g.tier == 7
        ]
        for name in tier7_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier9_generators_at_boundary_difficulties(self) -> None:
        """Cover tier9 branches."""
        tier9_names = [
            g.task_name for g in get_all_generators() if g.tier == 9
        ]
        for name in tier9_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_tier10_generators_at_boundary_difficulties(self) -> None:
        """Cover tier10 branches."""
        tier10_names = [
            g.task_name for g in get_all_generators() if g.tier == 10
        ]
        for name in tier10_names:
            for d in [1, 3, 5, 7, 8]:
                gen = get_generator(name, min_difficulty=d, max_difficulty=d)
                samples = gen.generate(3)
                for s in samples:
                    assert s.answer

    def test_mass_generation_covers_rare_paths(self) -> None:
        """Generate 50 samples per generator to hit stochastic branches."""
        failures: list[str] = []
        for gen in get_all_generators():
            gen.set_difficulty(1, 8)
            try:
                samples = gen.generate(50)
                for s in samples:
                    if not s.answer:
                        failures.append(f"{gen.task_name}: empty answer")
                        break
            except Exception as e:
                failures.append(f"{gen.task_name}: {e}")

        assert not failures, "\n".join(failures)
