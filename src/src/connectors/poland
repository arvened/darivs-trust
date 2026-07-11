"""Poland NGO Registry Connector (KRS)"""

from typing import Dict, Any, Optional
from datetime import datetime
import httpx
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

from src.connectors.base import (
    BaseConnector,
    NGOData,
    RegistryNotFoundError,
    RegistryTimeoutError,
    RegistryConnectionError,
    VerificationError,
    CachedConnector,
)


class PolandConnector(CachedConnector):
    """Connector for Poland NGO Registry (KRS)"""
    
    KRS_API_BASE = "https://api.eregister.eu.org"
    ALTERNATIVE_API = "https://www.gov.pl/api/v1/register"
    
    @property
    def country_code(self) -> str:
        return "PL"
    
    @property
    def registry_name(self) -> str:
        return "KRS (Polish National Court Register)"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def verify(
        self,
        registration_number: str,
        **kwargs
    ) -> NGOData:
        """Verify Poland NGO by KRS registration number"""
        
        cached = self._get_cached(registration_number)
        if cached:
            return cached
        
        if not self._validate_krs(registration_number):
            raise VerificationError(f"Invalid KRS format: {registration_number}")
        
        try:
            ngo_data = await self._lookup_krs(registration_number)
            self._set_cached(registration_number, ngo_data)
            return ngo_data
            
        except asyncio.TimeoutError:
            raise RegistryTimeoutError(
                f"Timeout verifying {registration_number} in KRS registry"
            )
        except httpx.ConnectError:
            raise RegistryConnectionError(
                f"Cannot connect to KRS registry"
            )
        except httpx.HTTPError as e:
            raise VerificationError(f"KRS API error: {str(e)}")
    
    async def _lookup_krs(self, krs: str) -> NGOData:
        """Look up NGO in KRS registry"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                data = await self._query_krs_api(client, krs)
                return self._parse_krs_response(krs, data)
            except (RegistryNotFoundError, VerificationError):
                try:
                    data = await self._query_alternative_api(client, krs)
                    return self._parse_alternative_response(krs, data)
                except VerificationError:
                    raise RegistryNotFoundError(
                        f"NGO with KRS {krs} not found in registries"
                    )
    
    async def _query_krs_api(
        self,
        client: httpx.AsyncClient,
        krs: str
    ) -> Dict[str, Any]:
        """Query primary KRS API"""
        endpoint = f"{self.KRS_API_BASE}/organization/{krs}"
        
        response = await client.get(
            endpoint,
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            raise RegistryNotFoundError(f"KRS {krs} not found")
        
        response.raise_for_status()
        return response.json()
    
    async def _query_alternative_api(
        self,
        client: httpx.AsyncClient,
        krs: str
    ) -> Dict[str, Any]:
        """Query alternative Polish registry API"""
        endpoint = f"{self.ALTERNATIVE_API}/krs"
        
        response = await client.get(
            endpoint,
            params={
                "number": krs,
                "format": "json"
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            raise RegistryNotFoundError(f"KRS {krs} not found")
        
        response.raise_for_status()
        data = response.json()
        
        if not data or not data.get("data"):
            raise RegistryNotFoundError(f"KRS {krs} not found")
        
        return data["data"][0] if isinstance(data["data"], list) else data["data"]
    
    def _parse_krs_response(
        self,
        krs: str,
        data: Dict[str, Any]
    ) -> NGOData:
        """Parse primary API response"""
        return NGOData(
            country_code="PL",
            registration_number=krs,
            name=data.get("name", ""),
            legal_name=data.get("legal_name"),
            status=self._normalize_status(data.get("status", "unknown")),
            registration_date=self._parse_date(data.get("registration_date")),
            address=data.get("address"),
            city=data.get("city"),
            postal_code=data.get("postal_code"),
            email=data.get("email"),
            phone=data.get("phone"),
            website=data.get("website"),
            registry_id=krs,
            registry_url=f"https://www.gov.pl/web/rejestry/krs?number={krs}",
            verified_at=datetime.utcnow(),
            data_source="KRS",
            confidence_score=0.95
        )
    
    def _parse_alternative_response(
        self,
        krs: str,
        data: Dict[str, Any]
    ) -> NGOData:
        """Parse alternative API response"""
        return NGOData(
            country_code="PL",
            registration_number=krs,
            name=data.get("name", ""),
            legal_name=data.get("legal_name"),
            status=self._normalize_status(data.get("status", "unknown")),
            registration_date=self._parse_date(data.get("registration_date")),
            address=data.get("address"),
            city=data.get("city"),
            postal_code=data.get("postal_code"),
            email=data.get("email"),
            phone=data.get("phone"),
            website=data.get("website"),
            registry_id=krs,
            registry_url=f"https://www.gov.pl/web/rejestry",
            verified_at=datetime.utcnow(),
            data_source="KRS (via gov.pl)",
            confidence_score=0.85
        )
    
    @staticmethod
    def _validate_krs(krs: str) -> bool:
        """Validate KRS format"""
        if not krs or not str(krs).isdigit():
            return False
        
        if len(str(krs)) != 10:
            return False
        
        return True
    
    @staticmethod
    def _normalize_status(status: str) -> str:
        """Normalize status to standard format"""
        status_lower = status.lower() if status else "unknown"
        
        mappings = {
            "aktywna": "active",
            "nieaktywna": "inactive",
            "zawieszona": "suspended",
            "likwidowana": "liquidated",
            "rozwiązana": "liquidated",
            "wznowiona": "active",
        }
        
        return mappings.get(status_lower, status_lower)
    
    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parse date from various formats"""
        if not date_str:
            return None
        
        formats = [
            "%Y-%m-%d",
            "%d.%m.%Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%d-%m-%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
        
        return None
