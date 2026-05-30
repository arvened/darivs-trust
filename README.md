# Darivs Trust

Open-source verification layer for charitable transactions and NGO authenticity.

## What is Darivs Trust?

Darivs Trust enables donors and civil society organisations to independently 
verify that charitable donations reached their intended recipients and that 
NGOs are legitimate registered entities.

When a donation is made, Darivs Trust automatically verifies:
- ✅ NGO registration status (public registries Ukraine + EU)
- ✅ Transaction routing (did funds reach the declared recipient?)
- ✅ Impact reporting (was the declared goal achieved?)

Each verified transaction produces a cryptographically signed public receipt — 
verifiable by anyone, without trusting a central authority.

## Why Darivs Trust?

Charitable fraud costs the sector billions annually. Existing solutions are:
- Centralised (require trusting a third party)
- US-focused (not applicable to EU/Ukraine NGOs)
- Blockchain-dependent (exclude mainstream donors)

Darivs Trust is blockchain-free, works with standard bank transfers, 
and connects to existing NGO registries across EU and Ukraine.

## Core Features (Roadmap)

- [ ] NGO registry connector (Ukraine ЄДРПОУ + Polish KRS)
- [ ] Transaction verification engine
- [ ] Cryptographic audit trail (signed receipts)
- [ ] Public verification API (REST)
- [ ] JavaScript SDK
- [ ] Python SDK
- [ ] GDPR-compliant donor privacy layer

## Tech Stack

- Language: Python 3.9+
- Framework: FastAPI
- Database: PostgreSQL
- Testing: pytest (target: 60%+ coverage)
- CI/CD: GitHub Actions
- License: MIT

## Pilot Partners

- Covent Tech Sp. z o.o. (Poland) — EU deployment partner
- БФ "Слава України" (Ukraine, ЄДРПОУ 44874584) — pilot tester

## Development Timeline

| Phase | Period | Deliverables |
|-------|--------|--------------|
| 1 | Sep–Dec 2026 | Verification engine, NGO registry connectors |
| 2 | Jan–Apr 2027 | Cryptographic signing, SDK, API docs |
| 3 | May–Aug 2027 | Security audit, v1.0.0 release, live pilot |

## Installation

```bash
pip install darivs-trust
