# Darivs Trust - NGO Verification Layer
Grant: NLnet NGI Zero Commons Fund (2026-06-3b1) | €35,000 | Application submitted June 2026 — Pending review | Timeline: Phase 1 (Sep 2026 - Dec 2026) | Phase 2+ (2027)

[![NLnet Funded](https://img.shields.io/badge/NLnet-2026--06--3b1-blue)](https://nlnet.nl)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-60%25-brightgreen)](coverage.xml)

**Trust infrastructure for charitable platforms | Verification layer for NGO donations**

---

## 🎯 Overview

Darivs Trust is an open-source verification layer that enables charitable platforms to:

- ✅ **Verify NGO legitimacy** against official registries (Ukraine, Poland, EU)
- ✅ **Track donation flows** with transparent transaction routing
- ✅ **Validate impact reporting** with confidence scoring
- ✅ **Ensure compliance** with GDPR, EU, and Ukraine regulations

Grant application submitted to NLnet NGI Zero Commons Fund.

Grant: 2026-06-3b1 | €35,000 | Status: Pending review | Timeline: Sep 2026 - Aug 2027

**Timeline:** Phase 1 (Sep 2026 - Dec 2026) | Phase 2+ (2027)

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/arvened/darivs-trust.git
cd darivs-trust

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database and registry API keys
```

### Running the Application

```bash
# Start FastAPI server
uvicorn src.api.main:app --reload

# API Documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test module
pytest tests/test_connectors.py -v

# Run with markers
pytest -m "integration" -v
```

---

## 📚 Features (v0.1.0-alpha)

### Registry Connectors

#### Ukraine NGO Registry (ЄДРПОУ)
```python
from src.connectors.ukraine import UkraineConnector

connector = UkraineConnector()
ngo = await connector.verify(registration_number="44874584")
# Returns: {"name": "БФ Слава України", "status": "active", ...}
```

#### Polish NGO Registry (KRS)
```python
from src.connectors.poland import PolandConnector

connector = PolandConnector()
ngo = await connector.verify(registration_number="0000012345")
# Returns: {"name": "Organization Name", "status": "active", ...}
```

#### Unified Interface
```python
from src.connectors.base import RegistryConnector

# Auto-detect country and use appropriate connector
connector = RegistryConnector.for_country("UA")
ngo = await connector.verify("44874584")
```

### Verification Engine

Coming in Week 3-4:
- NGO status verification
- Transaction routing verification
- Impact reporting validation

---

## 🏗️ Project Structure

```
darivs-trust/
├── src/
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract connector class
│   │   ├── ukraine.py        # Ukraine ЄДРПОУ connector
│   │   └── poland.py         # Poland KRS connector
│   ├── verification/
│   │   ├── __init__.py
│   │   ├── ngo_status.py     # NGO verification logic
│   │   ├── transaction_routing.py
│   │   └── impact_reporting.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   └── routes.py         # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ngo.py            # NGO data model
│   │   └── schemas.py        # Pydantic schemas
│   └── database.py           # SQLAlchemy setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_connectors.py    # Connector tests (60%+)
│   ├── test_verification.py
│   ├── test_api.py
│   └── fixtures/
│       └── sample_data.py
├── docs/
│   ├── api.md                # API documentation
│   ├── examples.md           # Code examples
│   ├── registry_api.md       # Registry API details
│   └── setup.md              # Setup guide
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
├── pytest.ini
└── CHANGELOG.md
```

---

## 🔧 Tech Stack

- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **Testing:** pytest, pytest-asyncio, pytest-cov
- **Async:** asyncio, aiohttp
- **CI/CD:** GitHub Actions
- **License:** MIT

---

## 📖 API Endpoints (v0.1.0-alpha)

### Verify NGO

```bash
POST /api/v1/registry/verify

Request:
{
  "country": "UA",
  "registration_number": "44874584"
}

Response:
{
  "id": "ngo-uuid",
  "country": "UA",
  "registration_number": "44874584",
  "name": "БФ Слава України",
  "status": "active",
  "verified_at": "2026-07-15T10:30:00Z",
  "details": {...}
}
```

### Batch Verification

```bash
POST /api/v1/registry/batch-verify

Request:
{
  "verifications": [
    {"country": "UA", "registration_number": "44874584"},
    {"country": "PL", "registration_number": "0000012345"}
  ]
}

Response:
[
  {...},
  {...}
]
```

---

## 🧪 Testing

### Test Coverage

```
tests/
├── test_connectors.py         # 60%+ coverage
│   ├── TestUkraineConnector   # 15+ tests
│   ├── TestPolandConnector    # 15+ tests
│   └── TestBaseConnector      # 10+ tests
├── test_verification.py       # 60%+ coverage
├── test_api.py                # 60%+ coverage
└── fixtures/                  # Sample data
```

### Running Tests

```bash
# All tests
pytest -v

# Coverage report
pytest --cov=src --cov-report=html
# Open: htmlcov/index.html

# Specific test
pytest tests/test_connectors.py::TestUkraineConnector -v

# Watch mode (requires pytest-watch)
ptw
```

---

## 📋 GDPR & Compliance

✅ **GDPR Compliant:**
- Data minimization
- Consent tracking
- Right to erasure
- Data portability
- Encryption in transit

✅ **Ukraine Regulations:**
- ЄДРПОУ registry compliance
- Local data protection laws
- NGO regulations

✅ **EU Regulations:**
- KRS registry compliance
- EU charity directives
- Cross-border compliance

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

### Commit Guidelines

```bash
# Feature
git commit -m "feat: add Ukraine registry connector"

# Test
git commit -m "test: add connector unit tests (60% coverage)"

# Documentation
git commit -m "docs: update API documentation"

# Fix
git commit -m "fix: handle registry timeout edge case"
```

---

## 📞 Support

- **Issues:** GitHub Issues
- **Email:** hello@arvend.io
- **NLnet:** michiel@NLnet.nl

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

Funded by [NLnet Foundation](https://nlnet.nl) through the NGI Zero Commons Fund.

**Grant:** 2026-06-3b1 | €35,000
**Timeline:** Sep 2026 - Aug 2027

---

## 📈 Roadmap

**v0.1.0-alpha (Jul 28):** Registry connectors + unified interface
**v0.1.0-beta (Aug 11):** Verification engine + transaction routing
**v0.1.0 (Aug 25):** Full documentation + examples
**Phase 1 (Sep-Dec 2026):** Production integration + additional features

---

**Status:** 🟢 Active Development
**Last Updated:** 2026-07-15
