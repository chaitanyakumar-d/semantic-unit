# Semantic Unit: Deterministic Evaluation Standard

A modern, deterministic evaluation framework for semantic units, providing standardized quality assurance and testing capabilities.

## Overview

Semantic Unit provides a robust framework for evaluating and testing semantic components with deterministic, reproducible results. Built with modern Python best practices, it offers a comprehensive CLI and programmatic API for quality assurance workflows.

## Features

- 🎯 **Deterministic Evaluation**: Consistent, reproducible evaluation results
- 🚀 **Modern CLI**: Built with Typer and Rich for excellent user experience
- 📊 **Structured Output**: Pydantic-based data validation and serialization
- 🔌 **LLM Integration**: Powered by LiteLLM for flexible model support
- ⚙️ **Configurable**: Environment-based configuration with python-dotenv
- 🧪 **Well-Tested**: Comprehensive test suite with pytest

## Installation

### From PyPI (when published)

```bash
pip install semantic-unit
```

### From Source

```bash
git clone https://github.com/yourusername/semantic-unit.git
cd semantic-unit
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### CLI Usage

```bash
# Run semantic unit evaluation
semantic-unit evaluate --input data.json

# Check version
semantic-unit --version

# Get help
semantic-unit --help
```

### Python API

```python
from semantic_unit.core import Evaluator

# Initialize evaluator
evaluator = Evaluator()

# Run evaluation
result = evaluator.evaluate(data)
print(result)
```

## Project Structure

```
semantic-unit/
├── semantic_unit/
│   ├── core/          # Core evaluation logic
│   ├── cli/           # Command-line interface
│   └── __init__.py
├── tests/             # Test suite
├── pyproject.toml     # Project configuration
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Requirements

- Python 3.9+
- litellm
- typer
- rich
- pydantic
- python-dotenv

## Configuration

Create a `.env` file in your project root:

```env
# Example configuration
SEMANTIC_UNIT_API_KEY=your-api-key
SEMANTIC_UNIT_MODEL=gpt-4
SEMANTIC_UNIT_DEBUG=false
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/semantic-unit.git
cd semantic-unit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=semantic_unit

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black semantic_unit tests

# Lint code
ruff check semantic_unit tests

# Type checking
mypy semantic_unit
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Built with modern Python tools:
- [LiteLLM](https://github.com/BerriAI/litellm) - Universal LLM API
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment management

## Contact

- GitHub: [https://github.com/yourusername/semantic-unit](https://github.com/yourusername/semantic-unit)
- Issues: [https://github.com/yourusername/semantic-unit/issues](https://github.com/yourusername/semantic-unit/issues)

## Roadmap

- [ ] Core evaluation engine implementation
- [ ] Comprehensive CLI commands
- [ ] Extended LLM provider support
- [ ] Documentation site
- [ ] Example gallery
- [ ] Plugin system
- [ ] Performance benchmarks
