# Darivs Trust

[![Tests](https://github.com/arvened/darivs-trust/actions/workflows/tests.yml/badge.svg)](https://github.com/arvened/darivs-trust/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Open-source verification layer for NGO registry data (Ukraine, Poland).

## Project status

Pre-grant proof of concept. Early stage, not production-ready.

An application (ID 2026-06-3b1, €35,000) has been submitted to the NLnet NGI Zero Commons Fund and is under review. No funding has been awarded. The work listed under "Planned" would only be funded if the application is approved, and dates depend on the project start date confirmed by NLnet.

Disclosure: the maintainer is also the founder of a Ukrainian charitable foundation that is a candidate pilot partner. A pilot with that foundation would not be counted as independent adoption.

Parts of the code were drafted with AI coding assistants (Claude). The maintainer is responsible for the repository.

## What exists today

- Shared connector interface: BaseConnector, the NGOData model, error classes and an in-memory cache (`src/connectors/base.py`)
- Prototype connector for the Ukrainian registry, ЄДРПОУ (`src/connectors/ukraine.py`)
- Prototype connector for the Polish registry, KRS (`src/connectors/poland.py`)
- Retries with backoff, batch verification and a factory: BaseConnector.for_country("UA") or "PL"
- 43 automated tests (pytest), run on every push with GitHub Actions
- Line coverage of src/: 67%, measured on 2026-09-20 with pytest --cov=src

## Known limitations

- The tests use mocked registry responses. The connectors have not been verified against the live registries yet, and the registry API addresses in the code are unconfirmed and may be wrong or outdated.
- The retry logic also retries permanent errors such as "not found".
- The code and tests use datetime.utcnow(), which is deprecated in Python 3.12.

## Planned (not implemented)

- Verification against the live registries, with confirmed API endpoints
- REST API (FastAPI) for single and batch verification
- Verification engine (status checks, confidence scoring)
- Transaction routing verification and impact reporting validation
- Data protection: privacy policy, record of processing activities and a legal review before any live processing
- Independent security audit

## Quick start

Tested with Python 3.12.
git clone https://github.com/arvened/darivs-trust.git
cd darivs-trust
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pytest --cov=src

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Questions and bug reports: GitHub Issues.

## License

MIT, see [LICENSE](LICENSE).