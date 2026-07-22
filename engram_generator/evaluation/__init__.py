"""Evaluation tools for reasoning chain comparison.

Provides step-level accuracy, first failure detection, final answer
matching, commutativity-aware normalisation, and Python-based
computational verification as a fallback.

Three evaluation tiers:
1. Step exact match (after normalisation) -- fast, strict
2. ROUGE-L / similarity -- catches near-misses
3. Python verification (fallback) -- computationally verify steps
   that failed tiers 1 and 2
"""
from engram_generator.evaluation.normaliser import OperationNormaliser
from engram_generator.evaluation.reasoning_chain import ReasoningChain
from engram_generator.evaluation.metrics import ReasoningMetrics
from engram_generator.evaluation.python_verifier import PythonVerifier, VerifyResult

__all__ = [
    "OperationNormaliser",
    "ReasoningChain",
    "ReasoningMetrics",
    "PythonVerifier",
    "VerifyResult",
]
