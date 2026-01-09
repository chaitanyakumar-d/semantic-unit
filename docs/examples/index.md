# Examples

Real-world examples and use cases for SemanticTest.

## Overview

This section contains practical examples showing how to use SemanticTest in various scenarios.

<div class="grid cards" markdown>

- [:material-code-tags: **Basic Usage**](basic.md)

    Simple examples to get started with semantic evaluation.

- [:material-test-tube: **Pytest Integration**](pytest.md)

    Complete pytest setup with fixtures, markers, and patterns.

- [:material-monitor: **Production Monitoring**](monitoring.md)

    Monitor AI systems in production for semantic drift.

- [:material-database-search: **RAG Validation**](rag.md)

    Validate retrieval-augmented generation pipelines.

</div>

## Quick Examples

### Basic Evaluation

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

result = judge.evaluate(
    actual="The experiment achieved 95% accuracy",
    expected="The experiment was 95% accurate"
)

print(f"Score: {result.score}")  # 0.95
```

### Testing AI Chatbot

```python
def test_chatbot_response(judge):
    response = chatbot.ask("What's your return policy?")
    expected = "We accept returns within 30 days"

    result = judge.evaluate(response, expected)
    assert result.score > 0.8, f"Chatbot drifted: {result.reasoning}"
```

### Batch Evaluation

```python
test_cases = [
    {"actual": "Response 1", "expected": "Expected 1"},
    {"actual": "Response 2", "expected": "Expected 2"},
]

results = judge.batch_evaluate(test_cases)
```

### CLI Usage

```bash
semantictest evaluate "AI output" "Expected output"
semantictest batch tests.json --output results.json
```

## Use Cases

| Use Case | Example Page |
|----------|--------------|
| Unit testing AI | [Basic Usage](basic.md) |
| pytest integration | [Pytest Integration](pytest.md) |
| Production monitoring | [Production Monitoring](monitoring.md) |
| RAG validation | [RAG Validation](rag.md) |
| Fine-tuning validation | [Basic Usage](basic.md#fine-tuning-validation) |
| A/B testing models | [Production Monitoring](monitoring.md#ab-testing) |

## Next Steps

Start with [Basic Usage](basic.md) to learn the fundamentals, then explore specific use cases relevant to your project.
