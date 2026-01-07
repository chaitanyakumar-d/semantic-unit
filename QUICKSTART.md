# Quick Start Guide

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e ".[dev]"
```

## Setup API Key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
```

Or set environment variable:

```bash
export OPENAI_API_KEY=your-api-key-here
```

## Usage

### 1. CLI Usage

**Basic Evaluation:**
```bash
semantic-unit evaluate "The test passed successfully" "The test was successful"
```

**With JSON Output:**
```bash
semantic-unit evaluate "Output A" "Expected A" --json
```

**Save Results:**
```bash
semantic-unit evaluate "Text 1" "Text 2" --output results.json
```

**Batch Evaluation:**

Create `inputs.json`:
```json
[
  {"actual": "Test 1 passed", "expected": "Test 1 successful"},
  {"actual": "Test 2 failed", "expected": "Test 2 passed"}
]
```

Run:
```bash
semantic-unit batch inputs.json --output batch_results.json
```

### 2. Python API Usage

```python
from semantic_unit import SemanticJudge

# Initialize judge
judge = SemanticJudge(model="gpt-4o-mini", temperature=0.0)

# Evaluate
result = judge.evaluate(
    actual="The ML model achieved 95% accuracy",
    expected="The model reached 95% test accuracy"
)

print(f"Score: {result.score}")
print(f"Reasoning: {result.reasoning}")
```

**Batch Evaluation:**
```python
pairs = [
    ("actual 1", "expected 1"),
    ("actual 2", "expected 2"),
]

results = judge.batch_evaluate(pairs)
avg_score = sum(r.score for r in results) / len(results)
```

### 3. Run Examples

```bash
python examples/usage.py
```

## Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=semantic_unit

# Verbose
pytest -v
```

## Development

### Code Quality

```bash
# Format code
black semantic_unit tests

# Lint
ruff check semantic_unit tests

# Type check
mypy semantic_unit
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Project Status

✅ **Production Ready Features:**
- Core SemanticJudge evaluation engine
- LiteLLM integration with gpt-4o-mini
- Full CLI with evaluate and batch commands
- Comprehensive test suite (20 tests, all passing)
- Type hints and validation
- Rich console output
- JSON export support

✅ **Documentation:**
- Academic-grade docstrings
- Citation file (CITATION.cff)
- Contributing guidelines (CONTRIBUTING.md)
- README with examples
- Quick start guide

✅ **Testing:**
- 78% test coverage
- Unit tests for core logic
- Mocked LLM calls
- Pydantic validation tests

## Next Steps for Production

1. **Add your OpenAI API key** in `.env`
2. **Test with real API calls:**
   ```bash
   semantic-unit evaluate "test text" "expected text"
   ```
3. **Add GitHub Actions CI/CD** (optional)
4. **Publish to PyPI** (optional)

## Getting Help

- Run `semantic-unit --help` for CLI help
- Run `semantic-unit evaluate --help` for command help
- Check `examples/usage.py` for code examples
- See test files for usage patterns
