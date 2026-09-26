# Contributing to Darivs Trust

Darivs Trust is an early-stage prototype. Small, focused contributions are welcome.

## Setup

Tested with Python 3.12.
git clone https://github.com/arvened/darivs-trust.git
cd darivs-trust
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pytest --cov=src

## Project layout

- src/connectors/base.py: shared interface, data model, errors and cache
- src/connectors/ukraine.py: prototype connector for the Ukrainian registry (ЄДРПОУ)
- src/connectors/poland.py: prototype connector for the Polish registry (KRS)
- tests/: automated tests (mocked registry responses)

## Making changes

1. Fork the repository and create a branch.
2. Keep changes small and focused. Add or update tests for what you change.
3. Tests must not call live registries. Use mocked responses.
4. Use clear commit messages, for example feat:, fix:, docs:, test:, refactor:, ci:.
5. Open a pull request against main. The GitHub Actions tests must pass.

## Use of generative AI

AI coding assistants are allowed, but you must understand and be able to explain everything you submit. If a commit adds AI-generated code, say so in the commit message: name the model (and version) and summarise the prompt, for example:

    test: add KRS timeout tests

    Generated with Claude (claude-opus-5-5). Prompt: "Write pytest tests
    for PolandConnector timeout handling using mocked httpx responses."
    Reviewed and corrected by hand.

## Reporting issues

Use GitHub Issues. Please include what you did, what you expected, what happened, and your Python version.

## Please do not

- Commit secrets, .env files or personal data taken from registries.
- Describe connector features as working unless they have been verified against the real registry.

## Security

Please do not report security problems in a public issue. Contact the maintainer at hello@arvend.io.