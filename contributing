# Contributing to Darivs Trust

Thank you for interest in contributing! This guide explains the development workflow.

---

## 🚀 Getting Started

### Fork & Clone

```bash
git clone https://github.com/arvened/darivs-trust.git
cd darivs-trust
```

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

### Running Tests Locally

```bash
# Run all tests
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_connectors.py::TestUkraineConnector -v
```

---

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/connector-name
```

Branch naming:
- `feature/` - New feature
- `fix/` - Bug fix
- `docs/` - Documentation
- `test/` - Tests

### 2. Write Code

Follow code style guidelines (PEP 8):

```python
def verify_ngo(
    registration_number: str,
    country_code: str
) -> NGOData:
    """
    Verify NGO in registry.
    
    Args:
        registration_number: Registry ID
        country_code: ISO 3166-1 alpha-2
        
    Returns:
        NGOData: Verified NGO data
    """
    # Implementation
    pass
```

### 3. Write Tests Simultaneously

```python
@pytest.mark.asyncio
async def test_verify_ngo_success():
    """Test successful NGO verification"""
    connector = UkraineConnector()
    result = await connector.verify("44874584")
    assert result.status == "active"
```

### 4. Format Code

```bash
# Format with black
black src tests

# Sort imports with isort
isort src tests

# Lint with flake8
flake8 src tests

# Type check with mypy
mypy src
```

### 5. Run Tests

```bash
# All tests
pytest -v

# Coverage report
pytest --cov=src --cov-report=html --cov-fail-under=60
```

### 6. Commit with Clear Messages

```bash
git commit -m "feat: add Ukraine registry connector

- Implement EDRPOU verification
- Add caching for registry responses
- Handle timeout edge cases
- Add 15+ unit tests (60% coverage)"
```

Commit types:
- `feat:` - New feature
- `fix:` - Bug fix
- `test:` - Tests
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `chore:` - Dependencies, tooling

### 7. Create Pull Request

```bash
git push origin feature/connector-name
```

**PR Template:**
```markdown
## Feature: [Feature Name]
- Describe changes
- Reference issue #XXX

## Testing
- [ ] Unit tests added
- [ ] Coverage 60%+
- [ ] All tests passing

## Checklist
- [ ] Code formatted (black)
- [ ] Imports sorted (isort)
- [ ] Type hints added (mypy)
- [ ] Documentation updated
```

---

## 🧪 Testing Requirements

### Minimum Coverage

- **60%** overall code coverage (NLnet requirement)
- Every public function tested
- Both happy-path and error cases

### Test Structure

```
tests/
├── test_connectors.py     # Connector tests
├── test_verification.py   # Verification tests
├── test_api.py           # API endpoint tests
├── conftest.py           # Global fixtures
└── fixtures/
    └── sample_data.py    # Test data
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Coverage report
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_connectors.py::TestUkraineConnector -v

# Watch mode
ptw
```

---

## 📚 Documentation

### Update README.md

When adding new features:
- Add to overview
- Add code example
- Add to roadmap

### Add Docstrings

All public functions must have docstrings:

```python
def verify(self, registration_number: str) -> NGOData:
    """
    Verify NGO in registry.
    
    Args:
        registration_number: Registry ID (8 digits for Ukraine)
        
    Returns:
        NGOData: Organization data
        
    Raises:
        RegistryNotFoundError: NGO not found
        RegistryTimeoutError: API timeout
        VerificationError: Other errors
    """
    pass
```

### Add Comments

Comment complex logic:

```python
# Calculate checksum for EDRPOU validation
checksum = sum(int(digit) for digit in registration_number)
if checksum % 11 != 0:
    raise VerificationError("Invalid checksum")
```

---

## 🔄 Release Process

### Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH-STAGE`

- `0.1.0-alpha` - Alpha release
- `0.1.0-beta` - Beta release
- `0.1.0` - Stable release

### Creating Release

```bash
# Tag release
git tag -a v0.1.0 -m "Release v0.1.0"

# Push tag
git push origin v0.1.0
```

### Update CHANGELOG

```markdown
## [0.1.0] - 2026-07-28

### Added
- Ukraine ЄДРПОУ connector
- Poland KRS connector
- Unified registry interface
- 60%+ test coverage

### Fixed
- Timeout handling for slow registries
```

---

## 📋 Code Style Guide

### Python (PEP 8)

```python
# Imports: sorted alphabetically
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

import httpx
import pytest

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Classes: PascalCase
class UkraineConnector:
    pass

# Functions/Methods: snake_case
async def verify_ngo():
    pass

# Variables: snake_case
registration_number = "44874584"

# Line length: max 120 characters
# Indentation: 4 spaces
# Blank lines: 2 between classes, 1 between methods
```

### Type Hints

Always use type hints:

```python
# ✅ Good
async def verify(
    self,
    registration_number: str
) -> NGOData:
    pass

# ❌ Bad
async def verify(self, registration_number):
    pass
```

---

## 🚨 Pre-commit Checks

Run before committing:

```bash
# Format
black src tests
isort src tests

# Lint
flake8 src tests

# Type check
mypy src

# Tests
pytest --cov=src --cov-fail-under=60

# Security
bandit -r src
```

---

## 📞 Questions?

- Open GitHub Issue
- Email: hello@arvend.io
- NLnet: michiel@NLnet.nl

---

## 🙏 Thank You!

Your contributions help make Darivs Trust better for everyone.
