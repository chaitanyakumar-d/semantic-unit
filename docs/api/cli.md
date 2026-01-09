# CLI API Reference

Complete reference for the JudgeAI command-line interface.

## Overview

```bash
judgeai [OPTIONS] COMMAND [ARGS]
```

## Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

---

## Commands

### evaluate

Evaluate semantic similarity between two texts.

```bash
judgeai evaluate ACTUAL EXPECTED [OPTIONS]
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `ACTUAL` | Yes | The actual text to evaluate |
| `EXPECTED` | Yes | The expected text to compare against |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--model` | `-m` | TEXT | `gpt-4o-mini` | LLM model to use |
| `--threshold` | `-t` | FLOAT | `0.8` | Pass/fail threshold |
| `--verbose` | `-v` | FLAG | `False` | Show detailed output |
| `--json` | `-j` | FLAG | `False` | Output as JSON |

#### Examples

```bash
# Basic evaluation
judgeai evaluate "The sky is blue" "The sky has a blue color"

# With specific model
judgeai evaluate "text" "expected" --model gpt-4o

# JSON output for scripting
judgeai evaluate "text" "expected" --json

# Verbose output
judgeai evaluate "text" "expected" --verbose

# With custom threshold
judgeai evaluate "text" "expected" --threshold 0.9
```

#### Output Format

**Standard Output:**
```
┌─────────────────────────────────────────────────────────────┐
│ Semantic Evaluation Result                                   │
├─────────────────────────────────────────────────────────────┤
│ Score: 0.95                                                  │
│ Status: ✅ PASS (threshold: 0.8)                            │
│ Reasoning: Both texts convey the same factual meaning...    │
└─────────────────────────────────────────────────────────────┘
```

**JSON Output (`--json`):**
```json
{
  "score": 0.95,
  "reasoning": "Both texts convey the same factual meaning about the sky being blue.",
  "actual": "The sky is blue",
  "expected": "The sky has a blue color",
  "passed": true,
  "threshold": 0.8
}
```

#### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Evaluation passed (score > threshold) |
| `1` | Evaluation failed (score <= threshold) |
| `2` | Error occurred |

---

### batch

Evaluate multiple test cases from a JSON file.

```bash
judgeai batch FILE [OPTIONS]
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `FILE` | Yes | Path to JSON file with test cases |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | PATH | stdout | Output file path |
| `--model` | `-m` | TEXT | `gpt-4o-mini` | LLM model to use |
| `--threshold` | `-t` | FLOAT | `0.8` | Pass/fail threshold |
| `--format` | `-f` | TEXT | `table` | Output format (table/json) |

#### Input File Format

```json
[
  {
    "actual": "First actual text",
    "expected": "First expected text"
  },
  {
    "actual": "Second actual text",
    "expected": "Second expected text"
  }
]
```

#### Examples

```bash
# Basic batch processing
judgeai batch test_cases.json

# Save results to file
judgeai batch test_cases.json --output results.json

# JSON output format
judgeai batch test_cases.json --format json

# With custom model and threshold
judgeai batch test_cases.json --model gpt-4o --threshold 0.85
```

#### Output Format

**Table Output (default):**
```
┌─────────────────────────────────────────────────────────────┐
│ Batch Evaluation Results                                     │
├─────┬───────┬────────┬──────────────────────────────────────┤
│ #   │ Score │ Status │ Summary                              │
├─────┼───────┼────────┼──────────────────────────────────────┤
│ 1   │ 0.95  │ ✅     │ Same factual content                 │
│ 2   │ 0.42  │ ❌     │ Different topics                     │
│ 3   │ 0.88  │ ✅     │ Equivalent meaning                   │
├─────┴───────┴────────┴──────────────────────────────────────┤
│ Summary: 2/3 passed (66.7%)                                  │
└─────────────────────────────────────────────────────────────┘
```

**JSON Output (`--format json`):**
```json
{
  "results": [
    {
      "index": 1,
      "score": 0.95,
      "passed": true,
      "reasoning": "Same factual content"
    },
    {
      "index": 2,
      "score": 0.42,
      "passed": false,
      "reasoning": "Different topics"
    }
  ],
  "summary": {
    "total": 3,
    "passed": 2,
    "failed": 1,
    "pass_rate": 0.667
  }
}
```

#### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All tests passed |
| `1` | Some tests failed |
| `2` | Error occurred |

---

## Environment Variables

The CLI uses these environment variables:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key |
| `AZURE_API_KEY` | Azure OpenAI API key |
| `AZURE_API_BASE` | Azure OpenAI endpoint |
| `TOGETHER_API_KEY` | Together AI API key |

---

## Shell Completion

### Bash

```bash
# Add to ~/.bashrc
eval "$(_JUDGEAI_COMPLETE=bash_source judgeai)"
```

### Zsh

```bash
# Add to ~/.zshrc
eval "$(_JUDGEAI_COMPLETE=zsh_source judgeai)"
```

### Fish

```bash
# Add to ~/.config/fish/config.fish
_JUDGEAI_COMPLETE=fish_source judgeai | source
```

---

## Scripting Examples

### CI/CD Script

```bash
#!/bin/bash
set -e

# Run semantic tests
judgeai batch tests/semantic_tests.json \
  --threshold 0.85 \
  --format json \
  --output results.json

# Check results
passed=$(jq '.summary.passed' results.json)
total=$(jq '.summary.total' results.json)

echo "Passed: $passed / $total"

if [ "$passed" -ne "$total" ]; then
  echo "Some semantic tests failed!"
  exit 1
fi
```

### Quick Validation

```bash
#!/bin/bash
# validate.sh - Quick semantic validation

ACTUAL="$1"
EXPECTED="$2"

result=$(judgeai evaluate "$ACTUAL" "$EXPECTED" --json)
score=$(echo "$result" | jq -r '.score')

echo "Semantic similarity: $score"
[ "$(echo "$score > 0.8" | bc)" -eq 1 ]
```

### Batch Processing with Progress

```bash
#!/bin/bash
# Process multiple files

for file in tests/*.json; do
  echo "Processing: $file"
  judgeai batch "$file" --output "results/$(basename $file)"
done

echo "All batches complete!"
```

---

## See Also

- [CLI User Guide](../user-guide/cli.md) - User-friendly CLI guide
- [Testing Integration](../user-guide/testing.md) - CI/CD integration
- [SemanticJudge API](semantic-judge.md) - Python API reference
