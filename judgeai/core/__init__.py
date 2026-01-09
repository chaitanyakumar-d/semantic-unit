"""
Core evaluation logic for JudgeAI.

This package contains the core functionality for LLM-based semantic
evaluation of AI outputs.
"""

from judgeai.core.engine import SemanticJudge
from judgeai.core.models import DriftResult

__all__ = [
    "SemanticJudge",
    "DriftResult",
]
