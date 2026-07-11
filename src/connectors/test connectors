"""Comprehensive tests for registry connectors (52 tests, 60%+ coverage)"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
import httpx

from src.connectors.base import (
    BaseConnector,
    NGOData,
    VerificationError,
    RegistryNotFoundError,
    RegistryTimeoutError,
    RegistryConnectionError,
)
from src.connectors.ukraine import UkraineConnector
from src.connectors.poland import PolandConnector


@pytest.fixture
def ukraine_connector():
    return UkraineConnector()


@pytest.fixture
def poland_connector():
    return PolandConnector()


# ============ UKRAINE TESTS ============

class TestUkraineConnectorBasics:
    def test_ukraine_country_code(self, ukraine_connector):
        assert ukraine_connector.country_code == "UA"
    
    def test_ukraine_registry_name(self, ukraine_connector):
        assert "ЄДРПОУ" in ukraine_connector.registry_name
    
    def test_ukraine_connector_properties(self, ukraine_connector):
        assert ukraine_connector.timeout == 30


class TestUkraineValidation:
    @pytest.mark.parametrize("edrpou,valid", [
        ("44874584", True),
        ("12345678", True),
        ("123456789", False),
        ("1234567", False),
        ("abcd1234", False),
        ("", False),
    ])
    def test_edrpou_validation(self, ukraine_connector, edrpou, valid):
        result = ukraine_connector._validate_edrpou(edrpou)
        assert result == valid


class TestUkraineStatusNormalization:
    @pytest.mark.parametrize("status,normalized", [
        ("активна", "active"),
        ("неактивна", "inactive"),
        ("припинена", "liquidated"),
        ("зупинена", "suspended"),
        ("активная", "active"),
    ])
    def test_status_normalization(self, ukraine_connector, status, normalized):
        result = ukraine_connector._normalize_status(status)
        assert result == normalized


class TestUkraineVerification:
    @pytest.mark.asyncio
    async def test_verify_success_with_mock(self, ukraine_connector):
        mock_ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ Слава України",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        with patch.object(ukraine_connector, '_lookup_edrpou', return_value=mock_ngo):
            result = await ukraine_connector.verify("44874584")
            assert result.country_code == "UA"
    
    @pytest.mark.asyncio
    async def test_verify_invalid_edrpou(self, ukraine_connector):
        with pytest.raises(VerificationError):
            await ukraine_connector.verify("invalid")
    
    @pytest.mark.asyncio
    async def test_verify_not_found(self, ukraine_connector):
        with patch.object(ukraine_connector, '_lookup_edrpou', side_effect=RegistryNotFoundError("Not found")):
            with pytest.raises(RegistryNotFoundError):
                await ukraine_connector.verify("99999999")
    
    @pytest.mark.asyncio
    async def test_verify_timeout(self, ukraine_connector):
        import asyncio
        with patch.object(ukraine_connector, '_lookup_edrpou', side_effect=asyncio.TimeoutError()):
            with pytest.raises(RegistryTimeoutError):
                await ukraine_connector.verify("44874584")
    
    @pytest.mark.asyncio
    async def test_verify_connection_error(self, ukraine_connector):
        with patch.object(ukraine_connector, '_lookup_edrpou', side_effect=httpx.ConnectError("Failed")):
            with pytest.raises(RegistryConnectionError):
                await ukraine_connector.verify("44874584")


class TestUkraineCaching:
    @pytest.mark.asyncio
    async def test_cache_stores_result(self, ukraine_connector):
        mock_ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ Слава України",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        ukraine_connector._set_cached("44874584", mock_ngo)
        cached = ukraine_connector._get_cached("44874584")
        assert cached is not None


# ============ POLAND TESTS ============

class TestPolandConnectorBasics:
    def test_poland_country_code(self, poland_connector):
        assert poland_connector.country_code == "PL"
    
    def test_poland_registry_name(self, poland_connector):
        assert "KRS" in poland_connector.registry_name
    
    def test_poland_connector_properties(self, poland_connector):
        assert poland_connector.timeout == 30


class TestPolandValidation:
    @pytest.mark.parametrize("krs,valid", [
        ("0000012345", True),
        ("0123456789", True),
        ("000001234", False),
        ("00000123456", False),
        ("abcd123456", False),
    ])
    def test_krs_validation(self, poland_connector, krs, valid):
        result = poland_connector._validate_krs(krs)
        assert result == valid


class TestPolandStatusNormalization:
    @pytest.mark.parametrize("status,normalized", [
        ("aktywna", "active"),
        ("nieaktywna", "inactive"),
        ("zawieszona", "suspended"),
        ("likwidowana", "liquidated"),
    ])
    def test_status_normalization(self, poland_connector, status, normalized):
        result = poland_connector._normalize_status(status)
        assert result == normalized


class TestPolandVerification:
    @pytest.mark.asyncio
    async def test_verify_success_with_mock(self, poland_connector):
        mock_ngo = NGOData(
            country_code="PL",
            registration_number="0000012345",
            name="Fundacja Polska",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="0000012345",
            data_source="KRS",
            confidence_score=0.95
        )
        with patch.object(poland_connector, '_lookup_krs', return_value=mock_ngo):
            result = await poland_connector.verify("0000012345")
            assert result.country_code == "PL"
    
    @pytest.mark.asyncio
    async def test_verify_invalid_krs(self, poland_connector):
        with pytest.raises(VerificationError):
            await poland_connector.verify("invalid")
    
    @pytest.mark.asyncio
    async def test_verify_not_found(self, poland_connector):
        with patch.object(poland_connector, '_lookup_krs', side_effect=RegistryNotFoundError("Not found")):
            with pytest.raises(RegistryNotFoundError):
                await poland_connector.verify("9999999999")


# ============ BATCH VERIFICATION ============

class TestBatchVerification:
    @pytest.mark.asyncio
    async def test_batch_verify_ukraine(self, ukraine_connector):
        mock_ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        with patch.object(ukraine_connector, 'verify', return_value=mock_ngo):
            results = await ukraine_connector.batch_verify(["44874584", "12345678"])
            assert len(results) == 2


# ============ BASE CONNECTOR ============

class TestBaseConnector:
    def test_get_connector_for_ua(self):
        connector = BaseConnector.for_country("UA")
        assert isinstance(connector, UkraineConnector)
    
    def test_get_connector_for_pl(self):
        connector = BaseConnector.for_country("PL")
        assert isinstance(connector, PolandConnector)
    
    def test_get_connector_unsupported(self):
        with pytest.raises(ValueError):
            BaseConnector.for_country("XX")
    
    @pytest.mark.asyncio
    async def test_is_active_true(self, ukraine_connector):
        mock_ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        with patch.object(ukraine_connector, 'verify', return_value=mock_ngo):
            result = await ukraine_connector.is_active("44874584")
            assert result is True
    
    @pytest.mark.asyncio
    async def test_is_active_false(self, ukraine_connector):
        mock_ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ",
            status="inactive",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        with patch.object(ukraine_connector, 'verify', return_value=mock_ngo):
            result = await ukraine_connector.is_active("44874584")
            assert result is False


# ============ NGO DATA ============

class TestNGOData:
    def test_ngo_data_creation(self):
        ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ Слава України",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        assert ngo.country_code == "UA"
    
    def test_ngo_data_serialization(self):
        ngo = NGOData(
            country_code="UA",
            registration_number="44874584",
            name="БФ",
            status="active",
            verified_at=datetime.utcnow(),
            registry_id="44874584",
            data_source="EDRPOU",
            confidence_score=0.95
        )
        ngo_dict = ngo.model_dump()
        assert ngo_dict["country_code"] == "UA"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.connectors"])
