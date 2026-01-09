# Installation

This guide covers all the ways to install SemanticTest.

## Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Operating System**: Linux, macOS, or Windows

## Quick Install

The easiest way to install SemanticTest is via pip:

```bash
pip install semantictest
```

## Installation Options

=== "pip (Recommended)"

    ```bash
    pip install semantictest
    ```

=== "From Source"

    ```bash
    git clone https://github.com/chaitanyakumar-d/semantictest.git
    cd semantictest
    pip install -e .
    ```

=== "Development"

    For contributors and developers:

    ```bash
    git clone https://github.com/chaitanyakumar-d/semantictest.git
    cd semantictest
    pip install -e ".[dev]"
    ```

=== "Poetry"

    ```bash
    poetry add semantictest
    ```

=== "Conda"

    ```bash
    # First install pip in your conda environment
    conda install pip
    pip install semantictest
    ```

## Verify Installation

After installation, verify everything works:

```python
from semantictest import SemanticJudge

print("SemanticTest installed successfully!")
print(f"Available providers: {SemanticJudge.list_supported_models()}")
```

Or use the CLI:

```bash
semantictest --version
```

## Dependencies

SemanticTest automatically installs these dependencies:

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

??? question "ImportError: No module named 'semantictest'"

    Make sure you installed the package in your active Python environment:

    ```bash
    # Check which Python you're using
    which python

    # Install in the correct environment
    pip install semantictest
    ```

??? question "Permission denied during installation"

    Use `--user` flag or a virtual environment:

    ```bash
    # Option 1: User install
    pip install --user semantictest

    # Option 2: Virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    pip install semantictest
    ```

??? question "Outdated pip"

    Upgrade pip first:

    ```bash
    pip install --upgrade pip
    pip install semantictest
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
    pip install semantictest
    ```

=== "conda"

    ```bash
    # Create environment
    conda create -n semantictest python=3.11

    # Activate
    conda activate semantictest

    # Install
    pip install semantictest
    ```

=== "poetry"

    ```bash
    # Initialize project
    poetry init

    # Add dependency
    poetry add semantictest

    # Enter shell
    poetry shell
    ```

## Next Steps

After installation, proceed to:

1. [Configuration](configuration.md) - Set up your API keys
2. [Quick Start](quickstart.md) - Write your first semantic test
