"""
Core evaluation logic for SemanticTest.

This package contains the core functionality for deterministic evaluation
of semantic units.
"""

from semantictest.core.engine import SemanticJudge
from semantictest.core.models import DriftResult

__all__ = [
    "SemanticJudge",
    "DriftResult",
]
