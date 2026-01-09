# SemanticJudge

::: semantictest.core.engine.SemanticJudge
    options:
      show_root_heading: true
      show_source: true
      members_order: source

---

## Overview

`SemanticJudge` is the core class for performing semantic evaluations. It uses large language models to compare the meaning of two texts and determine their semantic similarity.

## Basic Usage

```python
from semantictest import SemanticJudge

# Initialize with defaults
judge = SemanticJudge()

# Evaluate semantic similarity
result = judge.evaluate(
    actual="The experiment achieved 95% accuracy",
    expected="The experiment was 95% accurate"
)

print(f"Score: {result.score}")  # 0.95
print(f"Reasoning: {result.reasoning}")
```

## Constructor

```python
SemanticJudge(
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    max_tokens: int = 500,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `"gpt-4o-mini"` | LLM model identifier. Supports 100+ models via LiteLLM. |
| `temperature` | `float` | `0.0` | Sampling temperature. Use 0.0 for deterministic results. |
| `max_tokens` | `int` | `500` | Maximum tokens in the response. |
| `api_key` | `Optional[str]` | `None` | API key. If not provided, uses environment variable. |
| `api_base` | `Optional[str]` | `None` | Custom API endpoint URL. |

### Examples

```python
# Default configuration
judge = SemanticJudge()

# With specific model
judge = SemanticJudge(model="gpt-4o")

# With Anthropic Claude
judge = SemanticJudge(model="claude-3-5-sonnet-20241022")

# With local Ollama
judge = SemanticJudge(
    model="ollama/llama3.1",
    api_base="http://localhost:11434"
)

# With custom settings
judge = SemanticJudge(
    model="gpt-4o",
    temperature=0.0,
    max_tokens=1000,
    api_key="sk-..."
)
```

---

## Methods

### evaluate()

Evaluate the semantic similarity between two texts.

```python
def evaluate(
    self,
    actual: str,
    expected: str
) -> DriftResult
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `actual` | `str` | The actual text (e.g., AI output) |
| `expected` | `str` | The expected text (ground truth) |

#### Returns

`DriftResult` - An object containing:
- `score` (float): Similarity score from 0.0 to 1.0
- `reasoning` (str): Explanation of the evaluation
- `actual` (str): The input actual text
- `expected` (str): The input expected text

#### Example

```python
result = judge.evaluate(
    actual="Python is a programming language",
    expected="Python is a high-level programming language"
)

print(f"Score: {result.score}")
print(f"Reasoning: {result.reasoning}")

if result.score > 0.8:
    print("✅ Semantically equivalent")
else:
    print("❌ Semantic drift detected")
```

---

### batch_evaluate()

Evaluate multiple test cases in a single call.

```python
def batch_evaluate(
    self,
    test_cases: List[Dict[str, str]]
) -> List[DriftResult]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `test_cases` | `List[Dict[str, str]]` | List of dicts with "actual" and "expected" keys |

#### Returns

`List[DriftResult]` - List of evaluation results

#### Example

```python
test_cases = [
    {
        "actual": "The sky is blue",
        "expected": "The sky has a blue color"
    },
    {
        "actual": "Python is fast",
        "expected": "Python is slow"
    },
]

results = judge.batch_evaluate(test_cases)

for i, result in enumerate(results):
    print(f"Test {i+1}: Score={result.score}")
```

---

### list_supported_models()

Get all supported LLM providers and models.

```python
@classmethod
def list_supported_models(cls) -> Dict[str, Dict[str, Any]]
```

#### Returns

`Dict[str, Dict[str, Any]]` - Dictionary of providers with their models and configuration.

#### Example

```python
providers = SemanticJudge.list_supported_models()

for provider, info in providers.items():
    print(f"\n{provider}:")
    print(f"  Models: {info['models']}")
    print(f"  Env var: {info['env_var']}")
```

Output:

```
openai:
  Models: ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']
  Env var: OPENAI_API_KEY

anthropic:
  Models: ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', ...]
  Env var: ANTHROPIC_API_KEY
...
```

---

## Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `model` | `str` | The configured LLM model |
| `temperature` | `float` | The inference temperature |
| `max_tokens` | `int` | Maximum response tokens |
| `system_prompt` | `str` | The evaluation system prompt |

---

## Error Handling

```python
from semantictest import SemanticJudge
from litellm import APIError, RateLimitError

judge = SemanticJudge()

try:
    result = judge.evaluate(actual, expected)
except RateLimitError:
    print("Rate limited - wait and retry")
except APIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Best Practices

### For Testing

```python
# Use deterministic settings
judge = SemanticJudge(
    model="gpt-4o-mini",
    temperature=0.0  # Critical for reproducibility
)
```

### For Production

```python
# Use higher quality model
judge = SemanticJudge(
    model="gpt-4o",
    temperature=0.0,
    max_tokens=1000
)
```

### For Local Development

```python
# Use free local model
judge = SemanticJudge(
    model="ollama/llama3.1",
    api_base="http://localhost:11434"
)
```

---

## See Also

- [DriftResult](models.md) - Result model documentation
- [Configuration](../getting-started/configuration.md) - Configuration guide
- [LLM Providers](../user-guide/providers.md) - Provider setup
