"""Exhaustive validation system for engram-generator training data.

Generates samples at scale, verifies every arithmetic step
computationally, and exports static lookup tables for human
inspection.

Three tiers of verification:
1. Structural: non-empty problem, steps, answer; no fallbacks
2. Leak detection: answer not in problem text
3. Computational: PythonVerifier on every step containing arithmetic
"""
from engram_generator.validation.result import (
    StepResult,
    SampleResult,
    ValidationReport,
)
from engram_generator.validation.runner import ValidationRunner
from engram_generator.validation.exporter import Exporter

__all__ = [
    "StepResult",
    "SampleResult",
    "ValidationReport",
    "ValidationRunner",
    "Exporter",
]
