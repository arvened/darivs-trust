# Darivs Trust

[![Tests](https://github.com/arvened/darivs-trust/actions/workflows/tests.yml/badge.svg)](https://github.com/arvened/darivs-trust/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Open-source verification layer for NGO registry data (Ukraine, Poland).

## Project status

Pre-grant proof of concept. Early stage, not production-ready.

An application (ID 2026-06-3b1, €35,000) has been submitted to the NLnet NGI Zero Commons Fund and is under review. No funding has been awarded. The work listed under "Planned" would only be funded if the application is approved, and dates depend on the project start date confirmed by NLnet.

Disclosure: the maintainer, Eduard Arbitman, is a co-founder and the director of Charity Fund "Glory of Ukraine", which is named as a candidate pilot partner. A pilot with that foundation would not count as independent adoption.

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

## Use of generative AI

The prototype code, the tests and most of the documentation in this repository were generated with Claude (Anthropic) under the direction of Eduard Arbitman. His part was defining the requirements and architecture, reviewing and testing the generated output, finding and correcting errors, and deciding what goes into the repository. He is responsible for its content.

This follows the NLnet policy on generative AI. If the project is funded, AI assistants may still be used as tools, but the funded work will be done and understood by the human team, and every commit that adds AI-generated code will name the model and summarise the prompt in its commit message.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Questions and bug reports: GitHub Issues.

## License

MIT, see [LICENSE](LICENSE).