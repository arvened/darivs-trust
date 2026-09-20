# Changelog

All notable changes to this project are recorded here. Dates are ISO 8601.

## [Unreleased] - 2026-09-20

### Changed
- Repository layout corrected: code in src/connectors/, tests in tests/.
- Restored src/connectors/base.py (it had been overwritten by a copy of poland.py).
- Retry logic now re-raises the original registry error (reraise=True).
- requirements.txt now lists only the packages the code uses; test packages are in requirements-dev.txt.
- GitHub Actions workflow runs the tests on Python 3.12.
- README, CONTRIBUTING and the v0.1.0-alpha release notes rewritten to match the verified state.

### Removed
- Out-of-scope political_campaign.py and its test file.
- Internal status reports and notes that claimed the work was complete.

### Verified on 2026-09-20
- 43 automated tests pass; 67% line coverage of src/ (mocked registry responses).
- Not verified: behaviour against the live registries.

## [0.1.0-alpha]

Pre-grant prototype snapshot (tag v0.1.0-alpha). Earlier notes about production readiness, 52 tests and 60%+ coverage were not verified and are withdrawn.

### Added
- Prototype connector for the Ukrainian registry (EDRPOU).
- Prototype connector for the Polish registry (KRS).
- BaseConnector interface with a factory method.
- NGOData Pydantic model for standardised registry data.
- Initial test suite (pytest).