# Best Practices

Tips and patterns for effective semantic testing.

## Choosing Thresholds

### General Guidelines

| Use Case | Threshold | Rationale |
|----------|-----------|-----------|
| Exact factual match | 0.9+ | Critical information must match |
| General correctness | 0.8 | Standard semantic equivalence |
| Topic alignment | 0.7 | Related content, flexible wording |
| Sentiment match | 0.6 | Same general feeling/tone |

### Context-Specific Thresholds

```python
# Strict: Medical/Legal information
def test_medical_info(judge):
    result = judge.evaluate(ai_response, medical_fact)
    assert result.score > 0.95, "Medical info must be exact"

# Standard: Customer support
def test_support_response(judge):
    result = judge.evaluate(ai_response, expected_answer)
    assert result.score > 0.8, "Support response should be accurate"

# Lenient: Creative content
def test_creative_writing(judge):
    result = judge.evaluate(ai_story, theme_description)
    assert result.score > 0.6, "Should match the theme"
```

---

## Writing Good Expected Values

### Be Specific, Not Verbose

```python
# ❌ Too specific (breaks on paraphrasing)
expected = "The function returns a dictionary containing the user's first name, last name, and email address"

# ✅ Focus on key facts
expected = "Returns user info: name and email"
```

### Include Key Facts

```python
# ❌ Missing important details
expected = "The process completed"

# ✅ Include critical facts
expected = "The backup completed successfully in 2.3 seconds with no errors"
```

### Avoid Style Requirements

```python
# ❌ Specifies style
expected = "Please note that the server will be down for maintenance"

# ✅ Focus on content
expected = "Server maintenance downtime notification"
```

---

## Test Organization

### Group by Feature

```python
# test_chatbot_semantic.py

class TestCustomerSupport:
    """Semantic tests for customer support responses."""

    def test_return_policy(self, judge):
        ...

    def test_shipping_info(self, judge):
        ...

class TestProductInfo:
    """Semantic tests for product information."""

    def test_specifications(self, judge):
        ...

    def test_pricing(self, judge):
        ...
```

### Use Descriptive Names

```python
# ❌ Vague
def test_response(judge):
    ...

# ✅ Descriptive
def test_chatbot_returns_accurate_shipping_times(judge):
    ...
```

---

## Handling Flaky Tests

### Use Deterministic Settings

```python
# Always use temperature=0 for reproducibility
judge = SemanticJudge(temperature=0.0)
```

### Add Retries for Network Issues

```python
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def evaluate_with_retry(judge, actual, expected):
    return judge.evaluate(actual, expected)

def test_with_retry(judge):
    result = evaluate_with_retry(judge, response, expected)
    assert result.score > 0.8
```

### Use Appropriate Margins

```python
# ❌ Too tight (flaky)
assert result.score > 0.823

# ✅ Reasonable margin
assert result.score > 0.8
```

---

## Performance Optimization

### Batch Similar Tests

```python
# ❌ Many individual calls
def test_responses(judge):
    for case in test_cases:
        result = judge.evaluate(case["actual"], case["expected"])
        assert result.score > 0.8

# ✅ Batch evaluation
def test_responses_batch(judge):
    results = judge.batch_evaluate(test_cases)
    for result in results:
        assert result.score > 0.8
```

### Use Session-Scoped Fixtures

```python
# ❌ New judge per test (slow)
@pytest.fixture
def judge():
    return SemanticJudge()

# ✅ Shared judge (fast)
@pytest.fixture(scope="session")
def judge():
    return SemanticJudge()
```

### Choose Appropriate Models

```python
import os

@pytest.fixture(scope="session")
def judge():
    if os.getenv("CI"):
        # Fast/cheap for CI
        return SemanticJudge(model="gpt-4o-mini")
    else:
        # Better quality locally
        return SemanticJudge(model="gpt-4o")
```

---

## Error Messages

### Include Context

```python
def test_ai_response(judge):
    result = judge.evaluate(response, expected)

    # ❌ Unhelpful message
    assert result.score > 0.8

    # ✅ Helpful message
    assert result.score > 0.8, (
        f"Semantic mismatch (score: {result.score})\n"
        f"Expected: {expected}\n"
        f"Actual: {response}\n"
        f"Reasoning: {result.reasoning}"
    )
```

### Create Helper Functions

```python
def assert_semantic(judge, actual, expected, threshold=0.8):
    result = judge.evaluate(actual, expected)
    assert result.score > threshold, (
        f"Semantic test failed:\n"
        f"  Score: {result.score} (threshold: {threshold})\n"
        f"  Reasoning: {result.reasoning}\n"
        f"  Actual: {actual[:100]}...\n"
        f"  Expected: {expected[:100]}..."
    )
```

---

## Testing Strategies

### Golden Response Testing

```python
# Store known-good responses
GOLDEN_RESPONSES = {
    "greeting": "Hello! How can I help you today?",
    "farewell": "Goodbye! Have a great day!",
}

def test_greeting_response(judge):
    response = chatbot.respond("hi")
    result = judge.evaluate(response, GOLDEN_RESPONSES["greeting"])
    assert result.score > 0.8
```

### Regression Testing

```python
def test_no_regression(judge):
    """Ensure new model doesn't regress."""
    baseline_responses = load_baseline()
    current_responses = get_current_responses()

    regressions = []
    for prompt, (baseline, current) in zip_responses(baseline_responses, current_responses):
        result = judge.evaluate(current, baseline)
        if result.score < 0.85:
            regressions.append((prompt, result))

    assert not regressions, f"Regressions found: {regressions}"
```

### A/B Testing

```python
def test_model_comparison(judge):
    """Compare two model versions."""
    prompts = load_test_prompts()

    scores_a, scores_b = [], []
    for prompt in prompts:
        response_a = model_a.generate(prompt)
        response_b = model_b.generate(prompt)

        result = judge.evaluate(response_a, response_b)
        scores_a.append(result.score)

    avg_similarity = sum(scores_a) / len(scores_a)
    print(f"Average similarity: {avg_similarity}")
```

---

## Common Pitfalls

### ❌ Testing Exact Output

```python
# Wrong: Testing for exact match defeats the purpose
result = judge.evaluate(response, response)
assert result.score == 1.0
```

### ❌ Too Strict Thresholds

```python
# Wrong: 0.99 is almost never achievable
assert result.score > 0.99
```

### ❌ Ignoring Reasoning

```python
# Wrong: Not using the reasoning
assert result.score > 0.8

# Right: Log or display reasoning on failure
assert result.score > 0.8, f"Failed: {result.reasoning}"
```

### ❌ Non-Deterministic CI

```python
# Wrong: Non-zero temperature causes flaky tests
judge = SemanticJudge(temperature=0.7)

# Right: Zero temperature for reproducibility
judge = SemanticJudge(temperature=0.0)
```

---

## Checklist

Before running semantic tests in CI/CD:

- [ ] Temperature set to 0.0
- [ ] API keys configured as secrets
- [ ] Reasonable thresholds chosen
- [ ] Error messages include context
- [ ] Tests are independent
- [ ] Timeouts configured
- [ ] Rate limiting handled

## Next Steps

- [Examples](../examples/index.md) - Real-world examples
- [API Reference](../api/semantic-judge.md) - Complete API
- [Troubleshooting](../contributing/index.md) - Common issues
