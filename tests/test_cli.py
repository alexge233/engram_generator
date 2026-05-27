"""Tests for the CLI validation tool."""
import subprocess
import sys

import pytest


class TestCLIValidation:
    """Tests for the engram-validate CLI tool."""

    def _run_cli(self, args: list[str]) -> subprocess.CompletedProcess:
        """Run the CLI tool with given arguments.

        Args:
            args: Command-line arguments.

        Returns:
            CompletedProcess with stdout/stderr captured.
        """
        cmd = [
            "/home/tons/code/py/engram_model/.venv/bin/python",
            "-m", "engram_generator",
        ] + args
        return subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
        )

    def test_single_task_validation(self) -> None:
        """Verify CLI validates a single task without error."""
        result = self._run_cli(["--task", "addition", "--samples", "10"])
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_tier_validation(self) -> None:
        """Verify CLI validates an entire tier."""
        result = self._run_cli(["--tier", "0", "--samples", "5"])
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_all_validation(self) -> None:
        """Verify CLI validates all generators."""
        result = self._run_cli(["--all", "--samples", "3"])
        assert "PASS" in result.stdout or "ALL PASSED" in result.stdout

    def test_skill_tree_display(self) -> None:
        """Verify CLI prints skill tree structure."""
        result = self._run_cli(["--skill-tree"])
        assert result.returncode == 0
        assert "Tier" in result.stdout
        assert "addition" in result.stdout

    def test_verbose_output(self) -> None:
        """Verify verbose mode shows sample details."""
        result = self._run_cli(["--task", "addition", "--samples", "3", "-v"])
        assert result.returncode == 0
        assert "Input:" in result.stdout
        assert "Target:" in result.stdout

    def test_difficulty_override(self) -> None:
        """Verify difficulty override is applied."""
        result = self._run_cli([
            "--task", "addition", "--samples", "5", "--difficulty", "5",
        ])
        assert result.returncode == 0
        assert "PASS" in result.stdout

    def test_no_args_exits_with_message(self) -> None:
        """Verify running without arguments provides guidance."""
        result = self._run_cli([])
        assert result.returncode == 1
        assert "Specify" in result.stdout or "specify" in result.stdout.lower()
