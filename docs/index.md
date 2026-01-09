---
title: SemanticTest - Unit Testing for AI Agents
description: Stop your AI from hallucinating in production with one line of code
hide:
  - navigation
---

<style>
.md-typeset h1 {
  display: none;
}
</style>

<div align="center" markdown>

# SemanticTest

## Unit Testing for AI Agents

**Stop your AI from hallucinating in production with one line of code.**

[![Tests](https://github.com/chaitanyakumar-d/semantictest/actions/workflows/tests.yml/badge.svg)](https://github.com/chaitanyakumar-d/semantictest/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/chaitanyakumar-d/semantictest/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/chaitanyakumar-d/semantictest/blob/main/CONTRIBUTING.md)

[Get Started](getting-started/quickstart.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/chaitanyakumar-d/semantictest){ .md-button }

</div>

---

## The Problem

Traditional testing breaks with AI:

```python
# ❌ This fails even when AI is correct
assert ai_response == "The test passed successfully"
# AI says: "The test was successful" → TEST FAILS (but meaning is correct!)
```

AI outputs are **never** identical, even when correct. Your tests shouldn't break on paraphrasing.

## The Solution

```python
from semantictest import SemanticJudge

judge = SemanticJudge()
result = judge.evaluate(
    actual=ai_response,
    expected="The test passed successfully"
)

assert result.score > 0.8  # ✅ Tests meaning, not exact words
```

---

## :star: Key Features

<div class="grid cards" markdown>

- :dart: **Test Meaning, Not Words**

    ---

    Assert on semantic correctness, not string equality. Your AI can paraphrase freely without breaking tests.

- :shield: **Prevent Hallucinations**

    ---

    Catch AI drift before it reaches users. Get actionable insights on why outputs diverged.

- :zap: **Drop-in Replacement**

    ---

    Works seamlessly with pytest, unittest, or any test framework you already use.

- :test_tube: **Deterministic**

    ---

    Reproducible results for reliable CI/CD. Same inputs always yield same outputs.

- :chart_with_upwards_trend: **Actionable Insights**

    ---

    Get detailed explanations for why tests pass or fail, enabling faster debugging.

- :rocket: **100+ LLM Support**

    ---

    Works with OpenAI, Anthropic, Google, Azure, Groq, Ollama, and many more providers.

</div>

---

## :zap: Quick Install

=== "pip"

    ```bash
    pip install semantictest
    ```

=== "From Source"

    ```bash
    git clone https://github.com/chaitanyakumar-d/semantictest.git
    cd semantictest
    pip install -e .
    ```

---

## :bulb: Quick Example

```python
from semantictest import SemanticJudge

# Initialize the judge
judge = SemanticJudge()

# Your AI's output
ai_output = "The experiment succeeded with 95% accuracy"
expected = "The experiment achieved 95% accuracy"

# Test semantic correctness
result = judge.evaluate(ai_output, expected)

if result.score > 0.8:
    print("✓ AI response is semantically correct")
else:
    print(f"✗ AI drifted: {result.reasoning}")
```

---

## :busts_in_silhouette: Who Uses SemanticTest?

| Role | Use Case |
|------|----------|
| **AI Engineers** | Testing LLM applications and agents |
| **QA Teams** | Automated testing of AI features |
| **DevOps** | Monitoring AI systems in production |
| **Researchers** | Evaluating model performance |
| **Startups** | Shipping AI products with confidence |

---

## :link: Supported Providers

SemanticTest supports **100+ LLMs** through [LiteLLM](https://github.com/BerriAI/litellm):

| Provider | Example Models |
|----------|----------------|
| **OpenAI** | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |
| **Anthropic** | `claude-3-5-sonnet-20241022`, `claude-3-opus` |
| **Google** | `gemini/gemini-1.5-pro`, `gemini/gemini-1.5-flash` |
| **Azure** | `azure/gpt-4o`, `azure/gpt-4` |
| **Groq** | `groq/llama-3.1-70b-versatile` |
| **Ollama** | `ollama/llama3.1`, `ollama/mistral` |
| **AWS Bedrock** | `bedrock/anthropic.claude-3-sonnet` |
| **Together AI** | `together_ai/meta-llama/Llama-3-70b-chat-hf` |

[See all providers →](user-guide/providers.md)

---

## :book: Documentation

<div class="grid cards" markdown>

- [:material-clock-fast: **Getting Started**](getting-started/quickstart.md)

    Install and run your first semantic test in minutes.

- [:material-book-open-variant: **User Guide**](user-guide/concepts.md)

    Learn core concepts and best practices.

- [:material-api: **API Reference**](api/semantic-judge.md)

    Complete API documentation with examples.

- [:material-code-tags: **Examples**](examples/basic.md)

    Real-world examples and use cases.

</div>

---

## :heart: Contributing

We welcome contributions! See our [Contributing Guide](contributing/index.md) for details.

```bash
# Clone and setup
git clone https://github.com/chaitanyakumar-d/semantictest.git
cd semantictest
pip install -e ".[dev]"

# Run tests
pytest
```

---

## :page_facing_up: License

SemanticTest is licensed under the [Apache License 2.0](https://github.com/chaitanyakumar-d/semantictest/blob/main/LICENSE).
