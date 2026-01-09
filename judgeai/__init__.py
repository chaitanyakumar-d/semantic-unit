"""
JudgeAI: LLM-as-a-Judge Framework

A modern framework for semantic evaluation of AI outputs using
LLM-based judgment with deterministic, reproducible results.
"""

from judgeai.core import DriftResult, SemanticJudge

__version__ = "0.1.0"
__author__ = "Chaitanya Kumar Dasari"
__license__ = "Apache-2.0"

__all__ = [
    "__version__",
    "SemanticJudge",
    "DriftResult",
]
