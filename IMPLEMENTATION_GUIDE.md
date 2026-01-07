# Implementation Guide for Enhancements

## 1. GitHub Actions CI/CD Workflows

### Step 1: Create GitHub Repository
```bash
cd /home/chay/projects/semantic-unit
git init
git add .
git commit -m "Initial commit: Semantic Unit framework"
git branch -M main
git remote add origin https://github.com/yourusername/semantic-unit.git
git push -u origin main
```

### Step 2: Add CI/CD Workflows

Already created at `.github/workflows/tests.yml` - just push to GitHub and it will:
- Run tests on every push/PR
- Test on Linux, Windows, macOS
- Test Python 3.9, 3.10, 3.11, 3.12
- Upload coverage to Codecov

### Step 3: Add GitHub Secrets
In GitHub repository settings → Secrets → Actions, add:
- `OPENAI_API_KEY` (for integration tests)
- `PYPI_API_TOKEN` (for publishing)

**Status**: ✅ Files already created, just push to GitHub

---

## 2. Publish to PyPI

### Step 1: Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Verify email
3. Set up 2FA

### Step 2: Create API Token
1. Account Settings → API tokens → "Add API token"
2. Scope: "Entire account" or specific project
3. Copy token (starts with `pypi-...`)

### Step 3: Build Package
```bash
cd /home/chay/projects/semantic-unit
source venv/bin/activate
pip install build twine
python -m build
```

### Step 4: Upload to TestPyPI (Practice)
```bash
python -m twine upload --repository testpypi dist/*
```

### Step 5: Upload to Real PyPI
```bash
python -m twine upload dist/*
```

### Step 6: Automated Publishing
The workflow at `.github/workflows/publish.yml` already exists.
- Create a GitHub Release
- Workflow automatically publishes to PyPI

**Quick Command**:
```bash
# Add to your Makefile (already exists)
make build    # Build package
make publish  # Upload to PyPI
```

---

## 3. Add More Evaluation Metrics

### New Metrics to Add

Create `semantic_unit/core/metrics.py`:

```python
"""Additional evaluation metrics for semantic analysis."""

from typing import Dict, Any
import numpy as np
from semantic_unit.core.models import DriftResult


class MetricsCalculator:
    """Calculate additional evaluation metrics."""
    
    @staticmethod
    def factual_consistency_score(result: DriftResult) -> float:
        """Extract factual consistency from reasoning."""
        # Parse reasoning for factual keywords
        reasoning_lower = result.reasoning.lower()
        if "identical" in reasoning_lower or "same facts" in reasoning_lower:
            return 1.0
        elif "factual discrepancies" in reasoning_lower:
            return 0.3
        return result.score
    
    @staticmethod
    def confidence_interval(scores: list[float]) -> Dict[str, float]:
        """Calculate confidence interval for batch results."""
        mean = np.mean(scores)
        std = np.std(scores)
        return {
            "mean": mean,
            "std": std,
            "ci_lower": mean - 1.96 * std,
            "ci_upper": mean + 1.96 * std
        }
    
    @staticmethod
    def drift_magnitude(result: DriftResult) -> str:
        """Categorize drift magnitude."""
        if result.score >= 0.9:
            return "minimal"
        elif result.score >= 0.7:
            return "moderate"
        elif result.score >= 0.5:
            return "significant"
        else:
            return "severe"
```

### Add to SemanticJudge
```python
# In semantic_unit/core/engine.py, add method:

def evaluate_with_metrics(self, actual: str, expected: str) -> Dict[str, Any]:
    """Evaluate with additional metrics."""
    result = self.evaluate(actual, expected)
    
    return {
        "result": result,
        "drift_magnitude": MetricsCalculator.drift_magnitude(result),
        "factual_consistency": MetricsCalculator.factual_consistency_score(result),
    }
```

**Steps**:
1. Create the metrics.py file
2. Add tests for new metrics
3. Update CLI to show metrics
4. Document in README

---

## 4. Performance Benchmarks

### Create Benchmark Suite

Create `benchmarks/benchmark.py`:

```python
"""Performance benchmarks for Semantic Unit."""

import time
from semantic_unit import SemanticJudge

def benchmark_single_evaluation():
    """Benchmark single evaluation."""
    judge = SemanticJudge()
    
    start = time.time()
    result = judge.evaluate(
        "The test passed successfully",
        "The test was successful"
    )
    latency = time.time() - start
    
    print(f"Single Evaluation Latency: {latency:.2f}s")
    return latency

def benchmark_batch_evaluation():
    """Benchmark batch evaluation."""
    judge = SemanticJudge()
    
    pairs = [("text1", "expected1")] * 10
    
    start = time.time()
    results = judge.batch_evaluate(pairs)
    total_time = time.time() - start
    
    print(f"Batch (10) Latency: {total_time:.2f}s")
    print(f"Per-item: {total_time/10:.2f}s")
    return total_time

if __name__ == "__main__":
    print("Running benchmarks...")
    benchmark_single_evaluation()
    benchmark_batch_evaluation()
```

### Compare Against Baselines

Create `benchmarks/comparison.py`:

```python
"""Compare against baseline methods."""

from semantic_unit import SemanticJudge
import difflib

def baseline_exact_match(actual: str, expected: str) -> float:
    """Exact string matching."""
    return 1.0 if actual == expected else 0.0

def baseline_fuzzy_match(actual: str, expected: str) -> float:
    """Fuzzy string matching."""
    return difflib.SequenceMatcher(None, actual, expected).ratio()

def semantic_unit_match(actual: str, expected: str) -> float:
    """Semantic Unit evaluation."""
    judge = SemanticJudge()
    result = judge.evaluate(actual, expected)
    return result.score

# Run comparison on test dataset
```

**Steps**:
1. Create benchmarks/ directory
2. Add benchmark scripts
3. Document results in README
4. Add to CI/CD for regression testing

---

## 5. Integration Tests with Real API

### Create Integration Tests

Create `tests/integration/test_real_api.py`:

```python
"""Integration tests with real API calls."""

import pytest
import os
from semantic_unit import SemanticJudge

# Skip if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="No API key available"
)

@pytest.mark.integration
def test_real_evaluation():
    """Test with real API call."""
    judge = SemanticJudge(model="gpt-4o-mini")
    
    result = judge.evaluate(
        actual="The experiment was successful",
        expected="The experiment succeeded"
    )
    
    assert 0.0 <= result.score <= 1.0
    assert len(result.reasoning) > 10
    assert result.model == "gpt-4o-mini"
    assert result.score > 0.7  # Should be high similarity

@pytest.mark.integration
def test_real_different_meanings():
    """Test with actually different meanings."""
    judge = SemanticJudge()
    
    result = judge.evaluate(
        actual="The test failed",
        expected="The test passed"
    )
    
    assert result.score < 0.5  # Should detect difference

@pytest.mark.integration
def test_real_batch():
    """Test batch with real API."""
    judge = SemanticJudge()
    
    pairs = [
        ("successful test", "test passed"),
        ("failed test", "test succeeded"),
    ]
    
    results = judge.batch_evaluate(pairs)
    
    assert len(results) == 2
    assert results[0].score > results[1].score
```

### Update pytest config in pyproject.toml:

```toml
[tool.pytest.ini_options]
markers = [
    "integration: Integration tests with real API (deselect with '-m \"not integration\"')",
]
```

### Run Integration Tests
```bash
# Run only integration tests
pytest -m integration

# Run all except integration
pytest -m "not integration"

# Run with API key
OPENAI_API_KEY=your-key pytest -m integration
```

**Steps**:
1. Create tests/integration/ directory
2. Add integration test files
3. Update CI/CD to run integration tests with secrets
4. Document how to run

---

## 6. Documentation Website

### Option A: GitHub Pages with MkDocs

#### Install MkDocs
```bash
pip install mkdocs mkdocs-material mkdocstrings[python]
```

#### Create mkdocs.yml
```yaml
site_name: Semantic Unit
site_description: Deterministic Evaluation Standard
site_author: Chaitanya Kumar Dasari
site_url: https://yourusername.github.io/semantic-unit

theme:
  name: material
  palette:
    primary: indigo
    accent: blue
  features:
    - navigation.sections
    - toc.integrate

nav:
  - Home: index.md
  - Quick Start: quickstart.md
  - CLI Reference: cli.md
  - API Reference: api.md
  - Examples: examples.md
  - Contributing: contributing.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - codehilite
```

#### Create docs/ structure
```bash
mkdir -p docs
# Convert your markdown files to docs/
cp README.md docs/index.md
cp QUICKSTART.md docs/quickstart.md
cp CONTRIBUTING.md docs/contributing.md
```

#### Build and Deploy
```bash
mkdocs build
mkdocs gh-deploy  # Deploys to GitHub Pages
```

### Option B: ReadTheDocs (Sphinx)

#### Setup Sphinx
```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
cd docs
sphinx-quickstart
```

#### Configure docs/conf.py (already exists)

#### Build docs
```bash
cd docs
make html
```

#### Connect to ReadTheDocs
1. Go to https://readthedocs.org
2. Import repository
3. Builds automatically on push

### Option C: Simple GitHub Pages

Create `docs/index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Semantic Unit Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
</head>
<body>
    <h1>Semantic Unit</h1>
    <p>Deterministic Evaluation Standard for AI Testing</p>
    <!-- Add your content -->
</body>
</html>
```

Enable GitHub Pages in repository settings → Pages → Source: docs folder

**Steps**:
1. Choose documentation platform
2. Set up configuration
3. Build documentation
4. Deploy to hosting platform
5. Add link to README

---

## Quick Start Implementation Order

### Week 1: Essential
1. ✅ Push to GitHub
2. ✅ Verify CI/CD runs
3. Add integration tests

### Week 2: Publishing
4. Build and test PyPI upload
5. Create first release
6. Publish to PyPI

### Week 3: Enhancement
7. Add new metrics
8. Create benchmarks
9. Document performance

### Week 4: Documentation
10. Set up documentation site
11. Write tutorials
12. Add API examples

---

## Commands Cheat Sheet

```bash
# GitHub
git push origin main

# Build & Publish
python -m build
twine upload dist/*

# Run integration tests
pytest -m integration -v

# Build docs (MkDocs)
mkdocs serve  # Local preview
mkdocs gh-deploy  # Deploy

# Build docs (Sphinx)
cd docs && make html

# Benchmarks
python benchmarks/benchmark.py

# Format & Check
black semantic_unit tests
ruff check semantic_unit
mypy semantic_unit
```

---

## Need Help With Specific Step?

Let me know which enhancement you want to implement first, and I can:
1. Create the actual files
2. Write the code
3. Set up the configuration
4. Test it works

**What do you want to tackle first?** 🚀
