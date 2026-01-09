# LLM Providers

SemanticTest supports **100+ LLMs** through [LiteLLM](https://github.com/BerriAI/litellm). This guide covers all supported providers and how to configure them.

## Supported Providers

| Provider | Models | Best For |
|----------|--------|----------|
| [OpenAI](#openai) | GPT-4o, GPT-4, GPT-3.5 | General use, best quality |
| [Anthropic](#anthropic) | Claude 3.5, Claude 3 | Long context, reasoning |
| [Google](#google-gemini) | Gemini 1.5 Pro/Flash | Fast, multimodal |
| [Azure](#azure-openai) | GPT-4o, GPT-4 | Enterprise, compliance |
| [Groq](#groq) | Llama 3.1, Mixtral | Speed, open-source |
| [Ollama](#ollama) | Llama, Mistral | Local, private, free |
| [AWS Bedrock](#aws-bedrock) | Claude, Titan | AWS ecosystem |
| [Together AI](#together-ai) | Llama, Mistral | Open-source models |
| [OpenRouter](#openrouter) | Multiple | Model aggregation |

## OpenAI

The default and most tested provider.

### Setup

```bash
export OPENAI_API_KEY="sk-..."
```

### Usage

```python
from semantictest import SemanticJudge

# Default model
judge = SemanticJudge()

# Specific model
judge = SemanticJudge(model="gpt-4o")
judge = SemanticJudge(model="gpt-4o-mini")  # Cheaper
judge = SemanticJudge(model="gpt-4-turbo")
judge = SemanticJudge(model="gpt-4")
judge = SemanticJudge(model="gpt-3.5-turbo")  # Cheapest
```

### Available Models

| Model | Context | Best For |
|-------|---------|----------|
| `gpt-4o` | 128K | Best quality |
| `gpt-4o-mini` | 128K | Cost-effective ⭐ |
| `gpt-4-turbo` | 128K | High quality |
| `gpt-4` | 8K | Stable |
| `gpt-3.5-turbo` | 16K | Budget |

---

## Anthropic

Claude models excel at reasoning and long-context tasks.

### Setup

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Usage

```python
# Claude 3.5 Sonnet (recommended)
judge = SemanticJudge(model="claude-3-5-sonnet-20241022")

# Claude 3 Opus (most capable)
judge = SemanticJudge(model="claude-3-opus-20240229")

# Claude 3 Haiku (fastest)
judge = SemanticJudge(model="claude-3-haiku-20240307")
```

### Available Models

| Model | Context | Best For |
|-------|---------|----------|
| `claude-3-5-sonnet-20241022` | 200K | Best balance ⭐ |
| `claude-3-opus-20240229` | 200K | Complex reasoning |
| `claude-3-sonnet-20240229` | 200K | General use |
| `claude-3-haiku-20240307` | 200K | Speed |

---

## Google Gemini

Fast and multimodal-capable models.

### Setup

```bash
export GEMINI_API_KEY="..."
```

### Usage

```python
# Note: Prefix with "gemini/"
judge = SemanticJudge(model="gemini/gemini-1.5-pro")
judge = SemanticJudge(model="gemini/gemini-1.5-flash")  # Fast
judge = SemanticJudge(model="gemini/gemini-1.5-flash-8b")  # Cheapest
```

### Available Models

| Model | Context | Best For |
|-------|---------|----------|
| `gemini/gemini-1.5-pro` | 2M | Complex tasks |
| `gemini/gemini-1.5-flash` | 1M | Speed ⭐ |
| `gemini/gemini-1.5-flash-8b` | 1M | Budget |

---

## Azure OpenAI

Enterprise-grade OpenAI models with Azure compliance.

### Setup

```bash
export AZURE_API_KEY="..."
export AZURE_API_BASE="https://your-resource.openai.azure.com"
```

### Usage

```python
# Prefix with "azure/"
judge = SemanticJudge(model="azure/gpt-4o")
judge = SemanticJudge(model="azure/gpt-4")
judge = SemanticJudge(model="azure/gpt-35-turbo")
```

!!! note "Deployment Names"
    Azure uses deployment names. Make sure your deployment name matches the model name, or configure LiteLLM accordingly.

---

## Groq

Extremely fast inference for open-source models.

### Setup

```bash
export GROQ_API_KEY="gsk_..."
```

### Usage

```python
# Prefix with "groq/"
judge = SemanticJudge(model="groq/llama-3.1-70b-versatile")
judge = SemanticJudge(model="groq/llama-3.1-8b-instant")  # Fastest
judge = SemanticJudge(model="groq/mixtral-8x7b-32768")
```

### Available Models

| Model | Speed | Best For |
|-------|-------|----------|
| `groq/llama-3.1-70b-versatile` | Fast | Best quality ⭐ |
| `groq/llama-3.1-8b-instant` | Fastest | Speed |
| `groq/mixtral-8x7b-32768` | Fast | Long context |

---

## Ollama

Run models locally - free, private, and offline.

### Setup

1. Install Ollama: https://ollama.ai
2. Pull a model:

```bash
ollama pull llama3.1
ollama pull mistral
ollama pull codellama
```

### Usage

```python
# Prefix with "ollama/"
judge = SemanticJudge(model="ollama/llama3.1")
judge = SemanticJudge(model="ollama/mistral")

# Custom endpoint
judge = SemanticJudge(
    model="ollama/llama3.1",
    api_base="http://localhost:11434"
)
```

### Available Models

Any model from the [Ollama library](https://ollama.ai/library):

| Model | Size | Best For |
|-------|------|----------|
| `ollama/llama3.1` | 8B | General use ⭐ |
| `ollama/llama3.1:70b` | 70B | High quality |
| `ollama/mistral` | 7B | Fast |
| `ollama/codellama` | 7B | Code |

---

## AWS Bedrock

AWS-hosted models with enterprise security.

### Setup

Configure AWS credentials via:
- Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- AWS CLI (`aws configure`)
- IAM roles (on EC2/Lambda)

### Usage

```python
# Prefix with "bedrock/"
judge = SemanticJudge(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0")
judge = SemanticJudge(model="bedrock/amazon.titan-text-express-v1")
```

---

## Together AI

Access open-source models via API.

### Setup

```bash
export TOGETHER_API_KEY="..."
```

### Usage

```python
# Prefix with "together_ai/"
judge = SemanticJudge(model="together_ai/meta-llama/Llama-3-70b-chat-hf")
judge = SemanticJudge(model="together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1")
```

---

## OpenRouter

Access multiple providers through one API.

### Setup

```bash
export OPENROUTER_API_KEY="..."
```

### Usage

```python
# Prefix with "openrouter/"
judge = SemanticJudge(model="openrouter/openai/gpt-4")
judge = SemanticJudge(model="openrouter/anthropic/claude-3-sonnet")
```

---

## Choosing a Provider

### Decision Matrix

| Need | Recommended |
|------|-------------|
| **Best quality** | OpenAI `gpt-4o` or Anthropic `claude-3-5-sonnet` |
| **Cost-effective** | OpenAI `gpt-4o-mini` or Groq |
| **Speed** | Groq or Gemini Flash |
| **Privacy/Local** | Ollama |
| **Enterprise** | Azure OpenAI or AWS Bedrock |
| **Long context** | Gemini (2M) or Anthropic (200K) |

### Cost Comparison (Approximate)

| Provider | Model | Cost (per 1M tokens) |
|----------|-------|---------------------|
| OpenAI | gpt-4o-mini | ~$0.15 input / $0.60 output |
| OpenAI | gpt-4o | ~$2.50 input / $10 output |
| Anthropic | claude-3-5-sonnet | ~$3 input / $15 output |
| Groq | llama-3.1-70b | ~$0.59 input / $0.79 output |
| Ollama | llama3.1 | **Free** (local) |

---

## Listing All Providers

```python
from semantictest import SemanticJudge

providers = SemanticJudge.list_supported_models()
for name, info in providers.items():
    print(f"{name}:")
    print(f"  Models: {info['models']}")
    print(f"  Env var: {info['env_var']}")
```

---

## Custom Endpoints

For self-hosted models or proxies:

```python
judge = SemanticJudge(
    model="gpt-4",
    api_base="https://your-proxy.example.com/v1"
)
```

## Next Steps

- [CLI Reference](cli.md) - Use providers from the command line
- [Testing Integration](testing.md) - Set up CI/CD with different providers
- [Best Practices](best-practices.md) - Provider selection tips
