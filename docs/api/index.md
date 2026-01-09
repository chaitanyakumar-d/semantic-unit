# API Reference

Complete API documentation for JudgeAI.

## Overview

JudgeAI provides a simple, focused API:

| Class/Module | Purpose |
|-------------|---------|
| [`SemanticJudge`](semantic-judge.md) | Core evaluation class |
| [`DriftResult`](models.md) | Evaluation result model |
| [CLI](cli.md) | Command-line interface |

## Quick Reference

### SemanticJudge

```python
from judgeai import SemanticJudge

# Initialize
judge = SemanticJudge(
    model="gpt-4o-mini",    # LLM model
    temperature=0.0,        # Sampling temperature
    max_tokens=500,         # Response limit
    api_key=None,           # Optional API key
    api_base=None           # Optional custom endpoint
)

# Single evaluation
result = judge.evaluate(actual="...", expected="...")

# Batch evaluation
results = judge.batch_evaluate([
    {"actual": "...", "expected": "..."},
    {"actual": "...", "expected": "..."},
])

# List supported models
providers = SemanticJudge.list_supported_models()
```

### DriftResult

```python
result = judge.evaluate(actual, expected)

result.score      # float: 0.0 to 1.0
result.reasoning  # str: Explanation
result.actual     # str: Input actual text
result.expected   # str: Input expected text
```

### CLI

```bash
# Evaluate
judgeai evaluate "actual" "expected"

# Batch
judgeai batch tests.json --output results.json

# Help
judgeai --help
```

## Detailed Documentation

<div class="grid cards" markdown>

- [:material-scale-balance: **SemanticJudge**](semantic-judge.md)

    The core class for semantic evaluation. Full API reference with all methods and parameters.

- [:material-database: **Models**](models.md)

    Data models including `DriftResult` and configuration types.

- [:material-console: **CLI**](cli.md)

    Command-line interface documentation and examples.

</div>

## Import Patterns

```python
# Recommended: Import main class
from judgeai import SemanticJudge

# Import models
from judgeai.core.models import DriftResult

# Import everything (not recommended)
from judgeai import *
```

## Type Hints

JudgeAI is fully typed. Use with mypy:

```python
from judgeai import SemanticJudge
from judgeai.core.models import DriftResult

def test_response(judge: SemanticJudge) -> None:
    result: DriftResult = judge.evaluate("actual", "expected")
    score: float = result.score
    reasoning: str = result.reasoning
```

## Next Steps

- [SemanticJudge](semantic-judge.md) - Full class documentation
- [Models](models.md) - Data model reference
- [CLI](cli.md) - Command-line reference
