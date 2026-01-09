# Installation

This guide covers all the ways to install JudgeAI.

## Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Operating System**: Linux, macOS, or Windows

## Quick Install

The easiest way to install JudgeAI is via pip:

```bash
pip install judgeai
```

## Installation Options

=== "pip (Recommended)"

    ```bash
    pip install judgeai
    ```

=== "From Source"

    ```bash
    git clone https://github.com/chaitanyakumar-d/judgeai.git
    cd judgeai
    pip install -e .
    ```

=== "Development"

    For contributors and developers:

    ```bash
    git clone https://github.com/chaitanyakumar-d/judgeai.git
    cd judgeai
    pip install -e ".[dev]"
    ```

=== "Poetry"

    ```bash
    poetry add judgeai
    ```

=== "Conda"

    ```bash
    # First install pip in your conda environment
    conda install pip
    pip install judgeai
    ```

## Verify Installation

After installation, verify everything works:

```python
from judgeai import SemanticJudge

print("JudgeAI installed successfully!")
print(f"Available providers: {SemanticJudge.list_supported_models()}")
```

Or use the CLI:

```bash
judgeai --version
```

## Dependencies

JudgeAI automatically installs these dependencies:

| Package | Purpose |
|---------|---------|
| `litellm` | Universal LLM API (100+ models) |
| `typer` | CLI framework |
| `rich` | Beautiful terminal output |
| `pydantic` | Data validation |
| `python-dotenv` | Environment variable management |

## Development Dependencies

For development, additional packages are installed:

| Package | Purpose |
|---------|---------|
| `pytest` | Testing framework |
| `pytest-cov` | Coverage reporting |
| `black` | Code formatting |
| `ruff` | Fast linting |
| `mypy` | Type checking |
| `pre-commit` | Git hooks |

## Troubleshooting

### Common Issues

??? question "ImportError: No module named 'judgeai'"

    Make sure you installed the package in your active Python environment:

    ```bash
    # Check which Python you're using
    which python

    # Install in the correct environment
    pip install judgeai
    ```

??? question "Permission denied during installation"

    Use `--user` flag or a virtual environment:

    ```bash
    # Option 1: User install
    pip install --user judgeai

    # Option 2: Virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    pip install judgeai
    ```

??? question "Outdated pip"

    Upgrade pip first:

    ```bash
    pip install --upgrade pip
    pip install judgeai
    ```

## Virtual Environment Setup

We recommend using a virtual environment:

=== "venv"

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate (Linux/macOS)
    source venv/bin/activate

    # Activate (Windows)
    venv\Scripts\activate

    # Install
    pip install judgeai
    ```

=== "conda"

    ```bash
    # Create environment
    conda create -n judgeai python=3.11

    # Activate
    conda activate judgeai

    # Install
    pip install judgeai
    ```

=== "poetry"

    ```bash
    # Initialize project
    poetry init

    # Add dependency
    poetry add judgeai

    # Enter shell
    poetry shell
    ```

## Next Steps

After installation, proceed to:

1. [Configuration](configuration.md) - Set up your API keys
2. [Quick Start](quickstart.md) - Write your first semantic test
