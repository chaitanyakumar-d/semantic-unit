# User Guide

Welcome to the JudgeAI User Guide. This section covers everything you need to know to use JudgeAI effectively.

## Overview

JudgeAI provides a **semantic evaluation framework** for testing AI outputs. Instead of comparing strings character-by-character, it evaluates whether two texts convey the same **meaning**.

## Sections

<div class="grid cards" markdown>

- [:material-brain: **Core Concepts**](concepts.md)

    Understand semantic evaluation, drift detection, and how the judge works.

- [:material-cloud: **LLM Providers**](providers.md)

    Configure and use different LLM providers (OpenAI, Anthropic, Google, etc.).

- [:material-console: **CLI Reference**](cli.md)

    Use JudgeAI from the command line.

- [:material-test-tube: **Testing Integration**](testing.md)

    Integrate with pytest, unittest, and CI/CD pipelines.

- [:material-check-all: **Best Practices**](best-practices.md)

    Tips and patterns for effective semantic testing.

</div>

## Key Concepts Preview

### Semantic Evaluation

Traditional testing compares strings exactly:

```python
# Fails if AI paraphrases
assert response == "The answer is 42"
```

Semantic evaluation compares meaning:

```python
result = judge.evaluate(response, "The answer is 42")
assert result.score > 0.8  # Passes if meaning matches
```

### The SemanticJudge

The `SemanticJudge` is the core class that performs semantic evaluations:

```python
from judgeai import SemanticJudge

judge = SemanticJudge(model="gpt-4o-mini")
result = judge.evaluate(actual="...", expected="...")
```

### Drift Detection

"Drift" refers to when AI outputs deviate from expected behavior. The judge quantifies this drift with a score from 0.0 (completely different) to 1.0 (identical meaning).

## Quick Reference

| Task | Solution |
|------|----------|
| Basic evaluation | `judge.evaluate(actual, expected)` |
| Batch evaluation | `judge.batch_evaluate(test_cases)` |
| Change model | `SemanticJudge(model="claude-3-5-sonnet-20241022")` |
| CLI evaluation | `judgeai evaluate "text" "expected"` |

## Next Steps

Start with [Core Concepts](concepts.md) to understand how JudgeAI works, or jump to [LLM Providers](providers.md) to configure your preferred AI provider.
