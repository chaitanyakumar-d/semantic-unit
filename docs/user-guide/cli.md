# CLI Reference

SemanticTest provides a command-line interface for quick evaluations and batch processing.

## Installation

The CLI is installed automatically with the package:

```bash
pip install semantictest
semantictest --help
```

## Commands

### `evaluate`

Evaluate semantic similarity between two texts.

```bash
semantictest evaluate "actual text" "expected text"
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--model` | `-m` | LLM model to use | `gpt-4o-mini` |
| `--threshold` | `-t` | Pass/fail threshold | `0.8` |
| `--verbose` | `-v` | Show detailed output | `False` |
| `--json` | `-j` | Output as JSON | `False` |

#### Examples

```bash
# Basic evaluation
semantictest evaluate "The sky is blue" "The sky has a blue color"

# With specific model
semantictest evaluate "text" "expected" --model gpt-4o

# With threshold
semantictest evaluate "text" "expected" --threshold 0.9

# JSON output
semantictest evaluate "text" "expected" --json

# Verbose output
semantictest evaluate "text" "expected" --verbose
```

#### Output

```
┌─────────────────────────────────────────────────────────────┐
│ Semantic Evaluation Result                                   │
├─────────────────────────────────────────────────────────────┤
│ Score: 0.95                                                  │
│ Status: ✅ PASS (threshold: 0.8)                            │
│ Reasoning: Both texts convey the same factual meaning...    │
└─────────────────────────────────────────────────────────────┘
```

---

### `batch`

Evaluate multiple test cases from a JSON file.

```bash
semantictest batch test_cases.json
```

#### Input Format

Create a JSON file with test cases:

```json
[
  {
    "actual": "The experiment achieved 95% accuracy",
    "expected": "The experiment was 95% accurate"
  },
  {
    "actual": "Response time was under 2 seconds",
    "expected": "Response took less than 2 seconds"
  },
  {
    "actual": "Python is a programming language",
    "expected": "Python is a snake species"
  }
]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | stdout |
| `--model` | `-m` | LLM model to use | `gpt-4o-mini` |
| `--threshold` | `-t` | Pass/fail threshold | `0.8` |
| `--format` | `-f` | Output format (table/json) | `table` |

#### Examples

```bash
# Basic batch processing
semantictest batch test_cases.json

# Save results to file
semantictest batch test_cases.json --output results.json

# With specific model
semantictest batch test_cases.json --model gpt-4o

# JSON output format
semantictest batch test_cases.json --format json
```

#### Output

```
┌─────────────────────────────────────────────────────────────┐
│ Batch Evaluation Results                                     │
├─────┬───────┬────────┬──────────────────────────────────────┤
│ #   │ Score │ Status │ Summary                              │
├─────┼───────┼────────┼──────────────────────────────────────┤
│ 1   │ 0.95  │ ✅     │ Same factual content                 │
│ 2   │ 0.92  │ ✅     │ Equivalent meaning                   │
│ 3   │ 0.15  │ ❌     │ Different topics entirely            │
├─────┴───────┴────────┴──────────────────────────────────────┤
│ Summary: 2/3 passed (66.7%)                                  │
└─────────────────────────────────────────────────────────────┘
```

---

### `version`

Display version information.

```bash
semantictest --version
```

---

### `help`

Get help on any command.

```bash
semantictest --help
semantictest evaluate --help
semantictest batch --help
```

---

## Environment Variables

The CLI respects these environment variables:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key |
| `AZURE_API_KEY` | Azure OpenAI API key |
| `AZURE_API_BASE` | Azure OpenAI endpoint |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success (all tests passed) |
| `1` | Failure (some tests failed) |
| `2` | Error (configuration/runtime error) |

---

## Scripting Examples

### CI/CD Integration

```bash
#!/bin/bash
# ci-test.sh

# Run batch tests
semantictest batch tests/semantic_tests.json \
  --threshold 0.85 \
  --output results.json \
  --format json

# Check exit code
if [ $? -eq 0 ]; then
  echo "All semantic tests passed!"
else
  echo "Some semantic tests failed!"
  exit 1
fi
```

### Quick Validation Script

```bash
#!/bin/bash
# validate.sh

ACTUAL="$1"
EXPECTED="$2"
THRESHOLD="${3:-0.8}"

result=$(semantictest evaluate "$ACTUAL" "$EXPECTED" \
  --threshold "$THRESHOLD" \
  --json)

score=$(echo "$result" | jq -r '.score')
echo "Semantic similarity score: $score"
```

### Automated Testing

```bash
# Run with different models
for model in "gpt-4o-mini" "gpt-4o" "claude-3-5-sonnet-20241022"; do
  echo "Testing with $model..."
  semantictest batch tests.json --model "$model" --output "results_${model}.json"
done
```

---

## Tips

!!! tip "Use JSON output for scripting"
    The `--json` flag provides machine-readable output for automation.

!!! tip "Set model via environment"
    You can also configure defaults via environment variables in your shell profile.

!!! tip "Pipe from other commands"
    ```bash
    echo '{"actual": "text", "expected": "text"}' | semantictest evaluate --stdin
    ```

## Next Steps

- [Testing Integration](testing.md) - Use with pytest
- [Best Practices](best-practices.md) - CLI usage patterns
- [API Reference](../api/cli.md) - Detailed CLI API
