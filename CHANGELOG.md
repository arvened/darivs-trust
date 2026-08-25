# Changelog

## [0.1.0-alpha] - 2026-07-12

### Added
- Ukraine ЄДРПОУ NGO registry connector (async, cached, retry)
- Poland KRS NGO registry connector (async, cached, retry)
- Unified BaseConnector interface with factory pattern
- NGOData Pydantic model for standardized registry data
- 52 comprehensive tests (60%+ code coverage)
- pytest configuration and fixtures
- GitHub Actions CI/CD pipeline
- Complete README and contributing guidelines
- Project status report and documentation

### Features
- Async/await support for all registry operations
- Automatic retry mechanism with exponential backoff
- In-memory caching with TTL management
- Comprehensive error handling (5 exception types)
- Multi-Python version support (3.9-3.12)
- Type hints and full docstrings

### Status
Week 1-2 complete. Ready for Week 3-4 (Verification Engine development).
