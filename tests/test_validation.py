"""Tests for the validation infrastructure."""
import json
import os
import tempfile

import pytest

from engram_generator.validation import (
    StepResult,
    SampleResult,
    ValidationReport,
    ValidationRunner,
    Exporter,
)


class TestStepResult:
    """Tests for StepResult serialisation."""

    def test_to_dict_verified(self):
        """Verified step serialises all fields."""
        sr = StepResult(text="4+5=9", verified=True,
                        expected=9.0, computed=9.0)
        d = sr.to_dict()
        assert d["text"] == "4+5=9"
        assert d["verified"] is True
        assert d["computed"] == 9.0

    def test_to_dict_unparseable(self):
        """Unparseable step omits computed/expected."""
        sr = StepResult(text="visit node 3", verified=None,
                        reason="unparseable")
        d = sr.to_dict()
        assert d["verified"] is None
        assert "computed" not in d
        assert d["reason"] == "unparseable"


class TestSampleResult:
    """Tests for SampleResult serialisation."""

    def test_to_dict(self):
        """Sample result serialises correctly."""
        sr = SampleResult(
            generator="AdditionGenerator", task_name="addition",
            tier=0, difficulty=2, seed=42,
            problem="15 + 36", answer="51", status="all_verified",
            steps=[
                StepResult("5+6=11", True, 11.0, 11.0),
                StepResult("1+3=4", True, 4.0, 4.0),
            ],
        )
        d = sr.to_dict()
        assert d["generator"] == "AdditionGenerator"
        assert d["status"] == "all_verified"
        assert len(d["steps"]) == 2


class TestValidationReport:
    """Tests for report aggregation."""

    def _make_report(self):
        """Create a report with mixed results."""
        report = ValidationReport()
        report.add(SampleResult(
            "GenA", "task_a", 0, 1, 0, "p1", [], "42", "all_verified",
        ))
        report.add(SampleResult(
            "GenA", "task_a", 0, 1, 1, "p2", [], "43", "unverifiable",
        ))
        report.add(SampleResult(
            "GenB", "task_b", 1, 2, 0, "p3",
            [StepResult("1+1=3", False, 3.0, 2.0)],
            "3", "wrong",
        ))
        return report

    def test_total(self):
        """Total counts all samples."""
        report = self._make_report()
        assert report.total == 3

    def test_count_by_status(self):
        """Status counts are correct."""
        report = self._make_report()
        counts = report.count_by_status()
        assert counts["all_verified"] == 1
        assert counts["unverifiable"] == 1
        assert counts["wrong"] == 1

    def test_per_generator_summary(self):
        """Per-generator summary computes correctly."""
        report = self._make_report()
        summary = report.per_generator_summary()
        assert "GenA" in summary
        assert summary["GenA"]["total_samples"] == 2
        assert summary["GenB"]["verified_wrong"] == 1

    def test_per_tier_summary(self):
        """Per-tier summary groups correctly."""
        report = self._make_report()
        summary = report.per_tier_summary()
        assert summary[0]["total_samples"] == 2
        assert summary[1]["wrong_steps"] == 1


class TestValidationRunner:
    """Tests for the validation runner."""

    def test_validate_tier_zero(self):
        """Tier 0 validation runs without crashes."""
        runner = ValidationRunner(seeds_per_difficulty=3)
        report = runner.validate_tier(0)
        assert report.total > 0
        assert all(r.status != "crash" for r in report.results)

    def test_no_fallbacks(self):
        """No samples should fall back at low seed count."""
        runner = ValidationRunner(seeds_per_difficulty=3)
        report = runner.validate_tier(0)
        assert all(r.status != "fallback" for r in report.results)

    def test_no_wrong_tier_zero(self):
        """Tier 0 arithmetic should be verifiably correct."""
        runner = ValidationRunner(seeds_per_difficulty=10)
        report = runner.validate_tier(0)
        wrong = [r for r in report.results if r.status == "wrong"]
        assert len(wrong) == 0, (
            f"Wrong samples: {[(w.generator, w.difficulty, w.seed) for w in wrong[:5]]}"
        )


class TestExporter:
    """Tests for export functionality."""

    def _make_report(self):
        report = ValidationReport()
        report.add(SampleResult(
            "GenA", "task_a", 0, 1, 0, "problem text",
            [StepResult("1+2=3", True, 3.0, 3.0)],
            "3", "all_verified",
        ))
        return report

    def test_export_jsonl(self):
        """JSONL export creates files."""
        report = self._make_report()
        exporter = Exporter(report)
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = exporter.export_jsonl(tmpdir)
            assert len(paths) == 1
            with open(paths[0]) as f:
                line = json.loads(f.readline())
                assert line["generator"] == "GenA"
                assert line["steps"][0]["verified"] is True

    def test_export_summary(self):
        """Summary JSON has expected structure."""
        report = self._make_report()
        exporter = Exporter(report)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = exporter.export_summary(os.path.join(tmpdir, "s.json"))
            with open(path) as f:
                summary = json.load(f)
            assert summary["total_samples"] == 1
            assert "per_generator" in summary

    def test_export_csv(self):
        """CSV export creates readable file."""
        report = self._make_report()
        exporter = Exporter(report)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = exporter.export_csv(os.path.join(tmpdir, "v.csv"))
            with open(path) as f:
                lines = f.readlines()
            assert len(lines) == 2  # header + 1 step


class TestDecimalCap:
    """Tests for the decimal precision cap."""

    def test_cap_applied_to_answer(self):
        """Answers with many decimals are rounded to 4 d.p."""
        from engram_generator.base import StepGenerator
        result = StepGenerator._cap_decimals("3.141592653589793")
        assert result == "3.1416"

    def test_integers_unchanged(self):
        """Integers are not affected."""
        from engram_generator.base import StepGenerator
        assert StepGenerator._cap_decimals("42") == "42"

    def test_short_decimals_unchanged(self):
        """Decimals with <= 4 places are not changed."""
        from engram_generator.base import StepGenerator
        assert StepGenerator._cap_decimals("3.14") == "3.14"
        assert StepGenerator._cap_decimals("1.2345") == "1.2345"

    def test_scientific_notation(self):
        """Scientific notation mantissa is capped."""
        from engram_generator.base import StepGenerator
        result = StepGenerator._cap_decimals("6.67430000e-11")
        assert "e-11" in result
        decimal_part = result.split("e")[0]
        assert len(decimal_part.split(".")[-1]) <= 4


class TestExpandedVerifier:
    """Tests for new PythonVerifier parsers."""

    def setup_method(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from engram_generator.evaluation.python_verifier import (
                PythonVerifier,
            )
            self.v = PythonVerifier(enabled=True)

    def test_sqrt_correct(self):
        """Correct sqrt is valid."""
        r = self.v.verify_step("sqrt(144)=12")
        assert r.valid is True

    def test_sqrt_latex(self):
        """LaTeX sqrt notation works."""
        r = self.v.verify_step("\\sqrt{9}=3")
        assert r.valid is True

    def test_sqrt_wrong(self):
        """Wrong sqrt is invalid."""
        r = self.v.verify_step("sqrt(144)=13")
        assert r.valid is False

    def test_log2_correct(self):
        """Correct log base 2 is valid."""
        r = self.v.verify_step("log2(8)=3")
        assert r.valid is True

    def test_log10_correct(self):
        """Correct log base 10 is valid."""
        r = self.v.verify_step("log(100)=2")
        assert r.valid is True

    def test_ln_correct(self):
        """Correct natural log is valid."""
        import math
        r = self.v.verify_step(f"ln({round(math.e**3, 4)})=3")
        assert r.valid is True

    def test_tolerance_rounding(self):
        """Rounded values within tolerance pass."""
        r = self.v.verify_step("7/3=2.3333")
        assert r.valid is True
