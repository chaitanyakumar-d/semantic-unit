# Quick Start

Get up and running with JudgeAI in 5 minutes.

## Prerequisites

- [x] Python 3.9+ installed
- [x] JudgeAI installed (`pip install judgeai`)
- [x] An LLM API key (OpenAI, Anthropic, etc.)

## Step 1: Set Up Your API Key

Create a `.env` file in your project root:

```bash
# .env
OPENAI_API_KEY=your-openai-api-key-here
```

Or export it directly:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

## Step 2: Your First Semantic Test

Create a file called `test_semantic.py`:

```python
from judgeai import SemanticJudge

# Initialize the judge
judge = SemanticJudge()

# Simulate an AI response
ai_output = "The experiment was successful with 95% accuracy"
expected = "The experiment achieved 95% accuracy"

# Evaluate semantic similarity
result = judge.evaluate(ai_output, expected)

# Check the result
print(f"Score: {result.score}")
print(f"Reasoning: {result.reasoning}")

if result.score > 0.8:
    print("✅ AI response is semantically correct!")
else:
    print("❌ AI response drifted from expected meaning")
```

Run it:

```bash
python test_semantic.py
```

Expected output:

```
Score: 0.95
Reasoning: Both texts convey the same factual content about an experiment achieving 95% accuracy. The difference is purely stylistic ("was successful with" vs "achieved").
✅ AI response is semantically correct!
```

## Step 3: Integrate with pytest

Create `test_ai.py`:

```python
import pytest
from judgeai import SemanticJudge

@pytest.fixture
def judge():
    """Create a SemanticJudge instance for tests."""
    return SemanticJudge()

def test_ai_response_accuracy(judge):
    """Test that AI responses maintain semantic accuracy."""
    ai_response = "Our system processed 1,000 requests in under 2 seconds"
    expected = "The system handled 1000 requests within 2 seconds"

    result = judge.evaluate(ai_response, expected)

    assert result.score > 0.8, f"AI drifted: {result.reasoning}"

def test_ai_factual_correctness(judge):
    """Test that AI doesn't hallucinate facts."""
    ai_response = "Python was created by Guido van Rossum in 1991"
    expected = "Python was created by Guido van Rossum"

    result = judge.evaluate(ai_response, expected)

    assert result.score > 0.7, "AI response contains factual errors"

def test_ai_catches_hallucination(judge):
    """Test that the judge catches actual hallucinations."""
    ai_response = "Python was created by Bill Gates in 2005"
    expected = "Python was created by Guido van Rossum in 1991"

    result = judge.evaluate(ai_response, expected)

    # This should have a LOW score (hallucination detected)
    assert result.score < 0.5, "Judge should catch this hallucination"
```

Run the tests:

```bash
pytest test_ai.py -v
```

## Step 4: Use the CLI

JudgeAI includes a powerful CLI:

```bash
# Quick evaluation
judgeai evaluate "AI said this" "Expected to say this"

# With a specific model
judgeai evaluate "text" "expected" --model gpt-4

# Batch processing
judgeai batch test_cases.json --output results.json
```

## Understanding Results

The `DriftResult` object contains:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Semantic similarity (0.0 to 1.0) |
| `reasoning` | `str` | Explanation of the evaluation |
| `actual` | `str` | The actual text evaluated |
| `expected` | `str` | The expected text |

### Score Guidelines

| Score Range | Meaning |
|-------------|---------|
| **0.9 - 1.0** | Perfect alignment (identical meaning) |
| **0.8 - 0.9** | High alignment (same facts, minor differences) |
| **0.5 - 0.7** | Moderate alignment (overlapping, some divergence) |
| **0.3 - 0.4** | Low alignment (significant discrepancies) |
| **0.0 - 0.2** | Minimal alignment (fundamentally different) |

## Common Patterns

### Testing AI Chatbots

```python
def test_customer_support_response(judge):
    chatbot_response = get_chatbot_response("What's your return policy?")
    expected = "We accept returns within 30 days with a receipt"

    result = judge.evaluate(chatbot_response, expected)
    assert result.score > 0.8, f"Chatbot gave incorrect info: {result.reasoning}"
```

### Validating RAG Outputs

```python
def test_rag_accuracy(judge):
    rag_output = run_rag_query("What is the capital of France?")
    ground_truth = "Paris is the capital of France"

    result = judge.evaluate(rag_output, ground_truth)
    assert result.score > 0.85, "RAG pipeline hallucinated"
```

### Production Monitoring

```python
def monitor_ai_responses(responses, expected_behavior, judge):
    for response in responses:
        result = judge.evaluate(response, expected_behavior)
        if result.score < 0.7:
            alert_team(f"AI drift detected! Score: {result.score}")
            log_incident(result)
```

## Next Steps

- [Configuration](configuration.md) - Learn about all configuration options
- [LLM Providers](../user-guide/providers.md) - Use different AI providers
- [Testing Integration](../user-guide/testing.md) - Advanced pytest patterns
- [API Reference](../api/semantic-judge.md) - Complete API documentation
