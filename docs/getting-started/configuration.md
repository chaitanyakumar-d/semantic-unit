# Configuration

Learn how to configure JudgeAI for your needs.

## API Keys

JudgeAI requires an API key for the LLM provider you want to use.

### Setting API Keys

=== "Environment Variables"

    ```bash
    # OpenAI (default)
    export OPENAI_API_KEY="sk-..."

    # Anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."

    # Google
    export GEMINI_API_KEY="..."

    # Groq
    export GROQ_API_KEY="gsk_..."

    # Azure OpenAI
    export AZURE_API_KEY="..."
    export AZURE_API_BASE="https://your-resource.openai.azure.com"
    ```

=== ".env File"

    Create a `.env` file in your project root:

    ```bash
    # .env
    OPENAI_API_KEY=sk-...
    ANTHROPIC_API_KEY=sk-ant-...
    GEMINI_API_KEY=...
    GROQ_API_KEY=gsk_...
    ```

    JudgeAI automatically loads `.env` files using `python-dotenv`.

=== "Direct Parameter"

    Pass the API key directly (not recommended for production):

    ```python
    judge = SemanticJudge(api_key="sk-...")
    ```

### Provider-Specific Keys

| Provider | Environment Variable | Notes |
|----------|---------------------|-------|
| OpenAI | `OPENAI_API_KEY` | Default provider |
| Anthropic | `ANTHROPIC_API_KEY` | For Claude models |
| Google | `GEMINI_API_KEY` | For Gemini models |
| Azure | `AZURE_API_KEY` + `AZURE_API_BASE` | Requires both |
| Groq | `GROQ_API_KEY` | Fast inference |
| Together AI | `TOGETHER_API_KEY` | Open-source models |
| AWS Bedrock | AWS credentials | Uses boto3 |
| Ollama | None | Local, no key needed |

## Model Configuration

### Selecting a Model

```python
from judgeai import SemanticJudge

# OpenAI (default)
judge = SemanticJudge(model="gpt-4o-mini")

# Anthropic Claude
judge = SemanticJudge(model="claude-3-5-sonnet-20241022")

# Google Gemini
judge = SemanticJudge(model="gemini/gemini-1.5-flash")

# Groq (fast)
judge = SemanticJudge(model="groq/llama-3.1-70b-versatile")

# Local Ollama
judge = SemanticJudge(model="ollama/llama3.1")
```

### Temperature

Control the determinism of evaluations:

```python
# Maximum determinism (recommended for testing)
judge = SemanticJudge(temperature=0.0)

# Some variability
judge = SemanticJudge(temperature=0.3)
```

!!! tip "Use temperature=0 for CI/CD"
    For reproducible CI/CD results, always use `temperature=0.0`.

### Token Limits

Control the response length:

```python
judge = SemanticJudge(max_tokens=500)  # Default
judge = SemanticJudge(max_tokens=1000)  # More detailed reasoning
```

## Custom API Base

For self-hosted models or proxies:

```python
# Custom OpenAI-compatible endpoint
judge = SemanticJudge(
    model="gpt-4",
    api_base="https://your-proxy.com/v1"
)

# Local Ollama
judge = SemanticJudge(
    model="ollama/llama3.1",
    api_base="http://localhost:11434"
)
```

## Full Configuration Example

```python
from judgeai import SemanticJudge

judge = SemanticJudge(
    model="gpt-4o-mini",           # Model to use
    temperature=0.0,               # Deterministic output
    max_tokens=500,                # Response limit
    api_key="sk-...",              # Optional: direct key
    api_base="https://..."         # Optional: custom endpoint
)
```

## Configuration Best Practices

### For Development

```python
# Fast iteration with cheaper model
judge = SemanticJudge(
    model="gpt-4o-mini",
    temperature=0.0
)
```

### For Production Testing

```python
# More capable model for critical tests
judge = SemanticJudge(
    model="gpt-4o",
    temperature=0.0,
    max_tokens=1000
)
```

### For CI/CD

```python
# Deterministic and reproducible
judge = SemanticJudge(
    model="gpt-4o-mini",
    temperature=0.0
)
```

### For Local Development (Free)

```python
# No API costs with Ollama
judge = SemanticJudge(
    model="ollama/llama3.1",
    api_base="http://localhost:11434"
)
```

## Environment-Based Configuration

Use different settings per environment:

```python
import os

def get_judge():
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        return SemanticJudge(model="gpt-4o", temperature=0.0)
    elif env == "ci":
        return SemanticJudge(model="gpt-4o-mini", temperature=0.0)
    else:
        return SemanticJudge(model="ollama/llama3.1")
```

## Listing Available Models

```python
from judgeai import SemanticJudge

# Get all supported providers and models
providers = SemanticJudge.list_supported_models()
for provider, info in providers.items():
    print(f"{provider}: {info['models']}")
```

Output:

```
openai: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']
anthropic: ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', ...]
google: ['gemini/gemini-1.5-pro', 'gemini/gemini-1.5-flash', ...]
...
```

## Next Steps

- [Quick Start](quickstart.md) - Start using JudgeAI
- [LLM Providers](../user-guide/providers.md) - Deep dive into providers
- [API Reference](../api/semantic-judge.md) - Complete API docs
