# Testing Integration

Learn how to integrate SemanticTest with your testing framework.

## pytest Integration

### Basic Setup

```python
# conftest.py
import pytest
from semantictest import SemanticJudge

@pytest.fixture(scope="session")
def judge():
    """Create a shared SemanticJudge instance."""
    return SemanticJudge(
        model="gpt-4o-mini",
        temperature=0.0  # Deterministic for CI
    )
```

### Writing Tests

```python
# test_ai.py
def test_ai_response(judge):
    """Test that AI responds correctly."""
    response = get_ai_response("What is 2+2?")
    expected = "The answer is 4"

    result = judge.evaluate(response, expected)

    assert result.score > 0.8, f"AI drift: {result.reasoning}"
```

### Custom Assertions

```python
# conftest.py
import pytest
from semantictest import SemanticJudge

@pytest.fixture(scope="session")
def judge():
    return SemanticJudge(temperature=0.0)

def assert_semantic_match(judge, actual, expected, threshold=0.8):
    """Custom assertion helper."""
    result = judge.evaluate(actual, expected)
    assert result.score > threshold, (
        f"Semantic mismatch (score: {result.score})\n"
        f"Actual: {actual}\n"
        f"Expected: {expected}\n"
        f"Reasoning: {result.reasoning}"
    )

@pytest.fixture
def semantic_assert(judge):
    """Provide semantic assertion in tests."""
    def _assert(actual, expected, threshold=0.8):
        assert_semantic_match(judge, actual, expected, threshold)
    return _assert
```

Usage:

```python
def test_chatbot(semantic_assert):
    response = chatbot.ask("What's your return policy?")
    semantic_assert(response, "We accept returns within 30 days")
```

### Parametrized Tests

```python
import pytest

TEST_CASES = [
    ("2+2 is 4", "The sum of 2 and 2 is 4", 0.9),
    ("Hello world", "Hi there, world", 0.7),
    ("Python is great", "I love Python", 0.6),
]

@pytest.mark.parametrize("actual,expected,min_score", TEST_CASES)
def test_semantic_similarity(judge, actual, expected, min_score):
    result = judge.evaluate(actual, expected)
    assert result.score >= min_score
```

### Test Markers

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "semantic: mark test as semantic evaluation"
    )

# test_ai.py
@pytest.mark.semantic
def test_ai_summary(judge):
    summary = ai.summarize(document)
    result = judge.evaluate(summary, expected_summary)
    assert result.score > 0.85
```

Run only semantic tests:

```bash
pytest -m semantic
```

---

## unittest Integration

```python
import unittest
from semantictest import SemanticJudge

class SemanticTestCase(unittest.TestCase):
    """Base class for semantic tests."""

    @classmethod
    def setUpClass(cls):
        cls.judge = SemanticJudge(temperature=0.0)

    def assertSemantic(self, actual, expected, threshold=0.8, msg=None):
        """Assert semantic similarity."""
        result = self.judge.evaluate(actual, expected)
        if result.score <= threshold:
            self.fail(
                msg or f"Semantic mismatch: {result.score} <= {threshold}\n"
                       f"Reasoning: {result.reasoning}"
            )

class TestAIChatbot(SemanticTestCase):

    def test_greeting(self):
        response = chatbot.greet("John")
        self.assertSemantic(response, "Hello John, how can I help you?")

    def test_factual_response(self):
        response = chatbot.ask("What is Python?")
        self.assertSemantic(
            response,
            "Python is a programming language",
            threshold=0.7
        )

if __name__ == "__main__":
    unittest.main()
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/semantic-tests.yml
name: Semantic Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run semantic tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pytest tests/semantic/ -v
```

### GitLab CI

```yaml
# .gitlab-ci.yml
semantic-tests:
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pytest tests/semantic/ -v
  variables:
    OPENAI_API_KEY: $OPENAI_API_KEY
```

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  semantic-test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: pip install -e ".[dev]"
      - run:
          name: Run semantic tests
          command: pytest tests/semantic/ -v

workflows:
  test:
    jobs:
      - semantic-test
```

---

## Best Practices for CI/CD

### 1. Use Deterministic Settings

```python
# Always use temperature=0 in CI
judge = SemanticJudge(
    model="gpt-4o-mini",
    temperature=0.0
)
```

### 2. Cache API Responses (Optional)

```python
# conftest.py
import pytest
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path(".semantic_cache")

@pytest.fixture(scope="session")
def cached_judge():
    """Judge with response caching for faster CI."""
    CACHE_DIR.mkdir(exist_ok=True)
    return CachedJudge()

class CachedJudge:
    def __init__(self):
        self.judge = SemanticJudge(temperature=0.0)

    def evaluate(self, actual, expected):
        cache_key = hashlib.md5(
            f"{actual}:{expected}".encode()
        ).hexdigest()
        cache_file = CACHE_DIR / f"{cache_key}.json"

        if cache_file.exists():
            return json.loads(cache_file.read_text())

        result = self.judge.evaluate(actual, expected)
        cache_file.write_text(json.dumps({
            "score": result.score,
            "reasoning": result.reasoning
        }))
        return result
```

### 3. Set Reasonable Timeouts

```python
import pytest

@pytest.mark.timeout(30)  # 30 second timeout per test
def test_ai_response(judge):
    result = judge.evaluate(response, expected)
    assert result.score > 0.8
```

### 4. Handle Rate Limits

```python
import time
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=60))
def evaluate_with_retry(judge, actual, expected):
    return judge.evaluate(actual, expected)
```

### 5. Use Appropriate Models

```python
import os

def get_judge():
    """Get appropriate judge for environment."""
    if os.getenv("CI"):
        # Use cheaper model in CI
        return SemanticJudge(model="gpt-4o-mini")
    else:
        # Use better model locally
        return SemanticJudge(model="gpt-4o")
```

---

## Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── semantic/             # Semantic tests
│   ├── __init__.py
│   ├── test_chatbot.py
│   ├── test_rag.py
│   └── test_agents.py
├── unit/                 # Traditional unit tests
│   └── ...
└── integration/          # Integration tests
    └── ...
```

---

## Running Tests

```bash
# All tests
pytest

# Only semantic tests
pytest tests/semantic/

# With coverage
pytest --cov=semantictest tests/

# Verbose output
pytest -v tests/semantic/

# Stop on first failure
pytest -x tests/semantic/
```

## Next Steps

- [Best Practices](best-practices.md) - More testing tips
- [Examples](../examples/pytest.md) - Complete pytest examples
- [API Reference](../api/semantic-judge.md) - Full API docs
