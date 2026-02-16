# Contributing to GuardSQL Agent

Thank you for your interest in contributing to GuardSQL Agent!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/guardsql-agent/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Logs if applicable

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear use case
   - Proposed solution
   - Alternative approaches considered

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Update documentation
7. Commit with clear messages
8. Push to your fork
9. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where applicable
- Add docstrings for functions and classes
- Keep functions small and focused
- Write meaningful variable names

### Testing

- Add unit tests for new features
- Ensure existing tests pass
- Aim for >80% code coverage
- Test edge cases

### Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update TEST_QUERIES.md for new query types
- Keep documentation clear and concise

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/guardsql-agent.git
cd guardsql-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests
pytest
```

## Questions?

Feel free to ask questions in:
- GitHub Issues
- Pull Request comments
- Discussions

Thank you for contributing! 🙏
