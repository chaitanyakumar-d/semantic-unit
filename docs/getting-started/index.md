# Getting Started

Welcome to JudgeAI! This section will help you get up and running quickly.

## What is JudgeAI?

JudgeAI is a modern testing framework that brings **unit testing to AI agents**. Instead of testing for exact string matches (which fail on AI outputs), it tests for **semantic meaning**.

```python
# Traditional testing (breaks with AI)
assert ai_response == "The test passed"  # ❌ Fails on paraphrasing

# JudgeAI testing
result = judge.evaluate(ai_response, "The test passed")
assert result.score > 0.8  # ✅ Tests meaning, not words
```

## Quick Navigation

<div class="grid cards" markdown>

- [:material-download: **Installation**](installation.md)

    Install JudgeAI via pip or from source.

- [:material-rocket-launch: **Quick Start**](quickstart.md)

    Write your first semantic test in 5 minutes.

- [:material-cog: **Configuration**](configuration.md)

    Configure API keys, models, and settings.

</div>

## Prerequisites

Before you begin, make sure you have:

- **Python 3.9 or higher**
- **An API key** for at least one LLM provider (OpenAI, Anthropic, Google, etc.)
- Basic familiarity with Python and testing

## Installation Preview

```bash
pip install judgeai
```

Then set your API key:

```bash
export OPENAI_API_KEY="your-key-here"
```

And you're ready to go!

```python
from judgeai import SemanticJudge

judge = SemanticJudge()
result = judge.evaluate("AI output", "Expected meaning")
print(f"Score: {result.score}")
```

Continue to [Installation](installation.md) for detailed setup instructions.
