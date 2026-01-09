# Basic Usage Examples

Simple examples to get started with SemanticTest.

## Simple Evaluation

The most basic use case - comparing two texts:

```python
from semantictest import SemanticJudge

# Create a judge
judge = SemanticJudge()

# Evaluate similarity
result = judge.evaluate(
    actual="The sky is blue today",
    expected="Today the sky has a blue color"
)

print(f"Score: {result.score}")      # 0.95
print(f"Reasoning: {result.reasoning}")
```

## Checking AI Responses

Test that your AI gives correct answers:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

def check_ai_response(ai_response: str, expected: str) -> bool:
    """Check if AI response matches expected meaning."""
    result = judge.evaluate(ai_response, expected)
    return result.score > 0.8

# Example usage
response = your_ai_model.generate("What is 2+2?")
is_correct = check_ai_response(response, "The answer is 4")

if is_correct:
    print("✅ AI response is correct")
else:
    print("❌ AI response is incorrect")
```

## Detecting Hallucinations

Catch when AI makes up information:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

# Ground truth
expected = "Python was created by Guido van Rossum in 1991"

# AI responses to test
ai_responses = [
    "Python was created by Guido van Rossum",  # Good
    "Python was developed by Guido in the early 1990s",  # Good
    "Python was invented by Bill Gates in 2000",  # Hallucination!
]

for response in ai_responses:
    result = judge.evaluate(response, expected)

    if result.score > 0.7:
        print(f"✅ Correct: {response}")
    else:
        print(f"❌ Hallucination: {response}")
        print(f"   Reasoning: {result.reasoning}")
```

## Using Different Models

Choose the right model for your needs:

```python
from semantictest import SemanticJudge

# Fast and cheap (good for development)
judge_fast = SemanticJudge(model="gpt-4o-mini")

# High quality (good for production)
judge_quality = SemanticJudge(model="gpt-4o")

# Free local model
judge_local = SemanticJudge(model="ollama/llama3.1")

# All work the same way
result = judge_fast.evaluate("text", "expected")
```

## Batch Processing

Evaluate multiple test cases efficiently:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

# Multiple test cases
test_cases = [
    {
        "actual": "Revenue increased by 15%",
        "expected": "Revenue grew 15%"
    },
    {
        "actual": "The server is running",
        "expected": "The server is operational"
    },
    {
        "actual": "Error: connection failed",
        "expected": "Successfully connected"
    }
]

# Batch evaluate
results = judge.batch_evaluate(test_cases)

# Check results
for i, result in enumerate(results):
    status = "✅" if result.score > 0.8 else "❌"
    print(f"{status} Test {i+1}: Score={result.score:.2f}")
```

## Setting Thresholds

Choose appropriate thresholds for your use case:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

result = judge.evaluate(ai_response, expected)

# Strict threshold (medical/legal)
if result.score > 0.95:
    print("✅ Very high confidence")

# Standard threshold
elif result.score > 0.8:
    print("✅ Good match")

# Lenient threshold (creative content)
elif result.score > 0.6:
    print("⚠️ Partial match - review recommended")

else:
    print("❌ Significant mismatch")
```

## Working with the Result Object

Extract information from `DriftResult`:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()
result = judge.evaluate(
    actual="The meeting is at 3pm",
    expected="The meeting starts at 3:00 PM"
)

# Access all fields
print(f"Score: {result.score}")
print(f"Reasoning: {result.reasoning}")
print(f"Actual text: {result.actual}")
print(f"Expected text: {result.expected}")

# Convert to dictionary
result_dict = result.model_dump()
print(result_dict)

# Convert to JSON
result_json = result.model_dump_json()
print(result_json)
```

## Fine-tuning Validation

Verify that model fine-tuning maintains quality:

```python
from semantictest import SemanticJudge

judge = SemanticJudge()

def validate_fine_tuning(base_model, fine_tuned_model, test_prompts):
    """Compare base and fine-tuned model responses."""

    degradations = []

    for prompt in test_prompts:
        base_response = base_model.generate(prompt)
        tuned_response = fine_tuned_model.generate(prompt)

        result = judge.evaluate(tuned_response, base_response)

        if result.score < 0.8:
            degradations.append({
                "prompt": prompt,
                "score": result.score,
                "reasoning": result.reasoning
            })

    if degradations:
        print(f"⚠️ Found {len(degradations)} degraded responses")
        for d in degradations:
            print(f"  - {d['prompt'][:50]}... (score: {d['score']:.2f})")
    else:
        print("✅ Fine-tuning maintained quality")

    return len(degradations) == 0

# Usage
is_valid = validate_fine_tuning(
    base_model=gpt_base,
    fine_tuned_model=gpt_tuned,
    test_prompts=test_suite
)
```

## CLI Examples

Use from the command line:

```bash
# Quick check
semantictest evaluate "AI said this" "Should say this"

# With specific model
semantictest evaluate "text" "expected" --model gpt-4o

# Get JSON output
semantictest evaluate "text" "expected" --json

# Batch processing
semantictest batch test_cases.json --output results.json
```

## Error Handling

Handle potential errors gracefully:

```python
from semantictest import SemanticJudge
from litellm import APIError, RateLimitError

judge = SemanticJudge()

def safe_evaluate(actual: str, expected: str) -> dict:
    """Evaluate with error handling."""
    try:
        result = judge.evaluate(actual, expected)
        return {
            "success": True,
            "score": result.score,
            "reasoning": result.reasoning
        }
    except RateLimitError:
        return {
            "success": False,
            "error": "Rate limited - please wait and retry"
        }
    except APIError as e:
        return {
            "success": False,
            "error": f"API error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

# Usage
result = safe_evaluate(ai_response, expected)
if result["success"]:
    print(f"Score: {result['score']}")
else:
    print(f"Error: {result['error']}")
```

## Next Steps

- [Pytest Integration](pytest.md) - Use with your test suite
- [Production Monitoring](monitoring.md) - Monitor AI in production
- [RAG Validation](rag.md) - Test RAG pipelines
