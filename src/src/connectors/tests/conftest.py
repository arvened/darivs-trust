"""Pytest Configuration and Global Fixtures"""

import pytest
import asyncio
from datetime import datetime


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_edrpou_number():
    """Sample valid EDRPOU number"""
    return "44874584"


@pytest.fixture
def sample_krs_number():
    """Sample valid KRS number"""
    return "0000012345"


@pytest.fixture
def sample_ngo_data_ukraine():
    """Sample Ukraine NGO data"""
    return {
        "country_code": "UA",
        "registration_number": "44874584",
        "name": "БФ Слава України",
        "legal_name": "Благодійний фонд Слава України",
        "status": "active",
        "registration_date": datetime(2015, 3, 15),
        "address": "вул. Героїв Майдану, 1",
        "city": "Київ",
        "postal_code": "02000",
        "email": "info@slavaukraine.org",
        "phone": "+380441234567",
        "website": "https://slavaukraine.org",
        "verified_at": datetime.utcnow(),
        "registry_id": "44874584",
        "data_source": "EDRPOU",
        "confidence_score": 0.95
    }


@pytest.fixture
def sample_ngo_data_poland():
    """Sample Poland NGO data"""
    return {
        "country_code": "PL",
        "registration_number": "0000012345",
        "name": "Fundacja Polska Pomoc",
        "legal_name": "Fundacja Polska Pomoc dla Ukrainy",
        "status": "active",
        "registration_date": datetime(2015, 6, 20),
        "address": "ul. Warszawska 123",
        "city": "Warszawa",
        "postal_code": "00-001",
        "email": "info@polskiapomoc.pl",
        "phone": "+48221234567",
        "website": "https://polskiapomoc.pl",
        "verified_at": datetime.utcnow(),
        "registry_id": "0000012345",
        "data_source": "KRS",
        "confidence_score": 0.95
    }


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
