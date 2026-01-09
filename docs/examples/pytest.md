# Pytest Integration Examples

Complete examples for integrating JudgeAI with pytest.

## Basic Setup

### conftest.py

```python
# tests/conftest.py
import pytest
from judgeai import SemanticJudge

@pytest.fixture(scope="session")
def judge():
    """Shared SemanticJudge instance for all tests."""
    return SemanticJudge(
        model="gpt-4o-mini",
        temperature=0.0  # Deterministic for CI
    )

@pytest.fixture
def semantic_assert(judge):
    """Helper for semantic assertions."""
    def _assert(actual, expected, threshold=0.8, msg=None):
        result = judge.evaluate(actual, expected)
        assert result.score > threshold, (
            msg or f"Semantic mismatch:\n"
                   f"  Score: {result.score} (threshold: {threshold})\n"
                   f"  Reasoning: {result.reasoning}\n"
                   f"  Actual: {actual}\n"
                   f"  Expected: {expected}"
        )
        return result
    return _assert
```

## Test Examples

### Simple Tests

```python
# tests/test_basic.py

def test_simple_match(judge):
    """Test basic semantic matching."""
    result = judge.evaluate(
        actual="The sky is blue",
        expected="The sky has a blue color"
    )
    assert result.score > 0.8

def test_with_helper(semantic_assert):
    """Test using the semantic_assert helper."""
    semantic_assert(
        "Python is a programming language",
        "Python is a high-level programming language"
    )

def test_mismatch_detection(judge):
    """Test that mismatches are detected."""
    result = judge.evaluate(
        actual="The cat is black",
        expected="The dog is white"
    )
    assert result.score < 0.5, "Should detect semantic mismatch"
```

### Testing AI Chatbot

```python
# tests/test_chatbot.py
import pytest
from your_app import Chatbot

@pytest.fixture
def chatbot():
    return Chatbot()

class TestChatbotResponses:
    """Test suite for chatbot semantic correctness."""

    def test_greeting(self, judge, chatbot):
        response = chatbot.respond("Hello!")
        result = judge.evaluate(response, "Hello! How can I help you?")
        assert result.score > 0.7

    def test_return_policy(self, judge, chatbot):
        response = chatbot.respond("What's your return policy?")
        expected = "We accept returns within 30 days with a receipt"
        result = judge.evaluate(response, expected)
        assert result.score > 0.8, f"Policy incorrect: {result.reasoning}"

    def test_business_hours(self, judge, chatbot):
        response = chatbot.respond("When are you open?")
        expected = "We're open Monday to Friday, 9 AM to 5 PM"
        result = judge.evaluate(response, expected)
        assert result.score > 0.8

    def test_no_hallucination(self, judge, chatbot):
        """Ensure chatbot doesn't make up information."""
        response = chatbot.respond("What discounts do you offer?")
        # If we don't have discounts, response shouldn't claim we do
        if "discount" in response.lower():
            result = judge.evaluate(
                response,
                "We currently don't offer any discounts"
            )
            assert result.score > 0.5, "Chatbot may be hallucinating discounts"
```

### Parametrized Tests

```python
# tests/test_parametrized.py
import pytest

# Test cases: (actual, expected, min_score, description)
SEMANTIC_TEST_CASES = [
    ("2+2 equals 4", "The sum of 2 and 2 is 4", 0.9, "math"),
    ("Hello world", "Hi there, world!", 0.6, "greeting"),
    ("Python is great", "Python is an excellent language", 0.75, "positive"),
    ("Error occurred", "An error has happened", 0.85, "error message"),
]

@pytest.mark.parametrize(
    "actual,expected,min_score,desc",
    SEMANTIC_TEST_CASES,
    ids=[case[3] for case in SEMANTIC_TEST_CASES]
)
def test_semantic_cases(judge, actual, expected, min_score, desc):
    """Parametrized semantic tests."""
    result = judge.evaluate(actual, expected)
    assert result.score >= min_score, (
        f"Test '{desc}' failed: score {result.score} < {min_score}"
    )
```

### Custom Markers

```python
# tests/conftest.py
import pytest

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "semantic: mark test as semantic evaluation test"
    )
    config.addinivalue_line(
        "markers",
        "slow_semantic: mark test as slow semantic test"
    )

# tests/test_marked.py
import pytest

@pytest.mark.semantic
def test_basic_semantic(judge):
    """Basic semantic test."""
    result = judge.evaluate("Hello", "Hi there")
    assert result.score > 0.5

@pytest.mark.semantic
@pytest.mark.slow_semantic
def test_complex_semantic(judge):
    """Complex semantic test that takes longer."""
    # Long text comparison
    result = judge.evaluate(
        actual="This is a very long response about...",
        expected="This response covers the topic of..."
    )
    assert result.score > 0.7
```

Run marked tests:

```bash
# Only semantic tests
pytest -m semantic

# Exclude slow tests
pytest -m "semantic and not slow_semantic"
```

### Testing with Multiple Models

```python
# tests/test_multi_model.py
import pytest

@pytest.fixture(params=["gpt-4o-mini", "gpt-4o"])
def judge_multi(request):
    """Test with multiple models."""
    from judgeai import SemanticJudge
    return SemanticJudge(model=request.param, temperature=0.0)

def test_across_models(judge_multi):
    """Ensure consistency across models."""
    result = judge_multi.evaluate(
        "The test passed",
        "The test was successful"
    )
    # All models should agree this is similar
    assert result.score > 0.8
```

### Fixtures for Common Test Data

```python
# tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture(scope="session")
def test_cases():
    """Load test cases from JSON file."""
    path = Path(__file__).parent / "data" / "test_cases.json"
    return json.loads(path.read_text())

@pytest.fixture(scope="session")
def golden_responses():
    """Load golden (known-good) responses."""
    return {
        "greeting": "Hello! How can I help you today?",
        "farewell": "Goodbye! Have a great day!",
        "error": "I'm sorry, I don't understand. Could you rephrase?",
    }
```

### Async Tests (for async AI clients)

```python
# tests/test_async.py
import pytest
import asyncio

@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_async_ai_response(judge):
    """Test async AI responses."""
    # Simulate async AI call
    async def get_ai_response():
        await asyncio.sleep(0.1)
        return "The answer is 42"

    response = await get_ai_response()
    result = judge.evaluate(response, "The answer is 42")
    assert result.score > 0.9
```

## Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── data/
│   ├── test_cases.json      # Test data
│   └── golden_responses.json
├── semantic/
│   ├── __init__.py
│   ├── test_chatbot.py
│   ├── test_rag.py
│   └── test_agents.py
├── unit/
│   └── test_models.py
└── integration/
    └── test_api.py
```

## Running Tests

```bash
# All tests
pytest

# Verbose
pytest -v

# With coverage
pytest --cov=your_app

# Only semantic tests
pytest tests/semantic/

# Stop on first failure
pytest -x

# Run specific test
pytest tests/semantic/test_chatbot.py::TestChatbotResponses::test_greeting
```

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest -v --cov
```

## Next Steps

- [Production Monitoring](monitoring.md) - Monitor AI in production
- [Best Practices](../user-guide/best-practices.md) - Testing tips
- [API Reference](../api/semantic-judge.md) - Full API docs
