# Models

Data models used in SemanticTest.

## DriftResult

The result of a semantic evaluation.

::: semantictest.core.models.DriftResult
    options:
      show_root_heading: true
      show_source: true

---

## Overview

`DriftResult` is a Pydantic model that represents the result of a semantic evaluation. It contains the similarity score, reasoning, and the original inputs.

## Usage

```python
from semantictest import SemanticJudge

judge = SemanticJudge()
result = judge.evaluate(
    actual="The experiment succeeded",
    expected="The experiment was successful"
)

# Access fields
print(result.score)      # 0.95
print(result.reasoning)  # "Both texts convey..."
print(result.actual)     # "The experiment succeeded"
print(result.expected)   # "The experiment was successful"
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Semantic similarity score (0.0 to 1.0) |
| `reasoning` | `str` | Explanation of the evaluation |
| `actual` | `str` | The actual text that was evaluated |
| `expected` | `str` | The expected text for comparison |

### score

A float value between 0.0 and 1.0 representing semantic similarity:

| Range | Meaning |
|-------|---------|
| 0.9 - 1.0 | Perfect semantic alignment |
| 0.8 - 0.9 | High alignment (minor differences) |
| 0.5 - 0.7 | Moderate alignment (some divergence) |
| 0.3 - 0.4 | Low alignment (significant differences) |
| 0.0 - 0.2 | Minimal alignment (different meanings) |

```python
if result.score > 0.8:
    print("✅ Semantically equivalent")
elif result.score > 0.5:
    print("⚠️ Partial match - review needed")
else:
    print("❌ Semantic drift detected")
```

### reasoning

A human-readable explanation of why the score was assigned:

```python
print(result.reasoning)
# "Both texts describe the experiment's outcome as successful.
#  The first uses 'succeeded' while the second uses 'was successful',
#  which are semantically equivalent expressions."
```

### actual

The actual text that was evaluated (preserved from input):

```python
print(result.actual)
# "The experiment succeeded"
```

### expected

The expected text used for comparison (preserved from input):

```python
print(result.expected)
# "The experiment was successful"
```

---

## Serialization

`DriftResult` is a Pydantic model and supports standard serialization:

### To Dictionary

```python
result_dict = result.model_dump()
# {
#     "score": 0.95,
#     "reasoning": "Both texts...",
#     "actual": "The experiment succeeded",
#     "expected": "The experiment was successful"
# }
```

### To JSON

```python
result_json = result.model_dump_json()
# '{"score": 0.95, "reasoning": "Both texts...", ...}'
```

### From Dictionary

```python
from semantictest.core.models import DriftResult

result = DriftResult(
    score=0.95,
    reasoning="Both texts convey the same meaning",
    actual="The experiment succeeded",
    expected="The experiment was successful"
)
```

---

## Validation

Pydantic validates all fields:

```python
from semantictest.core.models import DriftResult
from pydantic import ValidationError

try:
    # Invalid: score out of range
    result = DriftResult(
        score=1.5,  # Must be 0.0-1.0
        reasoning="test",
        actual="test",
        expected="test"
    )
except ValidationError as e:
    print(e)
```

---

## Type Hints

For type-safe code:

```python
from semantictest import SemanticJudge
from semantictest.core.models import DriftResult
from typing import List

def evaluate_responses(
    judge: SemanticJudge,
    responses: List[str],
    expected: str
) -> List[DriftResult]:
    """Evaluate multiple responses against expected text."""
    results: List[DriftResult] = []
    for response in responses:
        result: DriftResult = judge.evaluate(response, expected)
        results.append(result)
    return results
```

---

## Testing with DriftResult

### Assertions

```python
def test_semantic_match(judge):
    result = judge.evaluate(actual, expected)

    # Simple assertion
    assert result.score > 0.8

    # With message
    assert result.score > 0.8, f"Score too low: {result.reasoning}"
```

### Custom Matchers

```python
def is_semantic_match(result: DriftResult, threshold: float = 0.8) -> bool:
    """Check if result represents a semantic match."""
    return result.score > threshold

def test_with_matcher(judge):
    result = judge.evaluate(actual, expected)
    assert is_semantic_match(result, threshold=0.85)
```

---

## See Also

- [SemanticJudge](semantic-judge.md) - The main evaluation class
- [Core Concepts](../user-guide/concepts.md) - Understanding drift detection
