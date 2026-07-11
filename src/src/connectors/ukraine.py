"""Ukraine NGO Registry Connector (ЄДРПОУ)"""

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


class UkraineConnector(CachedConnector):
    """Connector for Ukraine NGO Registry (ЄДРПОУ)"""
    
    EDRPOU_API_BASE = "https://dracs.pru.gov.ua/api"
    ALTERNATIVE_API = "https://data.gov.ua/api/3/action"
    
    @property
    def country_code(self) -> str:
        return "UA"
    
    @property
    def registry_name(self) -> str:
        return "ЄДРПОУ (Unified State Register)"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def verify(
        self,
        registration_number: str,
        **kwargs
    ) -> NGOData:
        """Verify Ukraine NGO by ЄДРПОУ registration number"""
        
        cached = self._get_cached(registration_number)
        if cached:
            return cached
        
        if not self._validate_edrpou(registration_number):
            raise VerificationError(f"Invalid EDRPOU format: {registration_number}")
        
        try:
            ngo_data = await self._lookup_edrpou(registration_number)
            self._set_cached(registration_number, ngo_data)
            return ngo_data
            
        except asyncio.TimeoutError:
            raise RegistryTimeoutError(
                f"Timeout verifying {registration_number} in EDRPOU registry"
            )
        except httpx.ConnectError:
            raise RegistryConnectionError(
                f"Cannot connect to EDRPOU registry"
            )
        except httpx.HTTPError as e:
            raise VerificationError(f"EDRPOU API error: {str(e)}")
    
    async def _lookup_edrpou(self, edrpou: str) -> NGOData:
        """Look up NGO in EDRPOU registry"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                data = await self._query_edrpou_api(client, edrpou)
                return self._parse_edrpou_response(edrpou, data)
            except (RegistryNotFoundError, VerificationError):
                try:
                    data = await self._query_alternative_api(client, edrpou)
                    return self._parse_alternative_response(edrpou, data)
                except VerificationError:
                    raise RegistryNotFoundError(
                        f"NGO with EDRPOU {edrpou} not found in registries"
                    )
    
    async def _query_edrpou_api(
        self,
        client: httpx.AsyncClient,
        edrpou: str
    ) -> Dict[str, Any]:
        """Query primary EDRPOU API"""
        endpoint = f"{self.EDRPOU_API_BASE}/organizations/{edrpou}"
        
        response = await client.get(
            endpoint,
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            raise RegistryNotFoundError(f"EDRPOU {edrpou} not found")
        
        response.raise_for_status()
        return response.json()
    
    async def _query_alternative_api(
        self,
        client: httpx.AsyncClient,
        edrpou: str
    ) -> Dict[str, Any]:
        """Query alternative Ukrainian data API"""
        endpoint = f"{self.ALTERNATIVE_API}/package_search"
        
        response = await client.get(
            endpoint,
            params={
                "q": f"edrpou:{edrpou}",
                "rows": 1
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            raise RegistryNotFoundError(f"EDRPOU {edrpou} not found")
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get("result", {}).get("results"):
            raise RegistryNotFoundError(f"EDRPOU {edrpou} not found")
        
        return data["result"]["results"][0]
    
    def _parse_edrpou_response(
        self,
        edrpou: str,
        data: Dict[str, Any]
    ) -> NGOData:
        """Parse primary API response"""
        return NGOData(
            country_code="UA",
            registration_number=edrpou,
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
            registry_id=edrpou,
            registry_url=f"https://dracs.pru.gov.ua/search?edrpou={edrpou}",
            verified_at=datetime.utcnow(),
            data_source="EDRPOU",
            confidence_score=0.95
        )
    
    def _parse_alternative_response(
        self,
        edrpou: str,
        data: Dict[str, Any]
    ) -> NGOData:
        """Parse alternative API response"""
        extras = data.get("extras", {})
        
        return NGOData(
            country_code="UA",
            registration_number=edrpou,
            name=data.get("title", ""),
            legal_name=data.get("name"),
            status=self._normalize_status(extras.get("status", "unknown")),
            registration_date=self._parse_date(extras.get("registration_date")),
            address=extras.get("address"),
            city=extras.get("city"),
            postal_code=extras.get("postal_code"),
            email=extras.get("email"),
            phone=extras.get("phone"),
            website=extras.get("website"),
            registry_id=edrpou,
            registry_url=f"https://data.gov.ua/api/3/action/package_show?id={data.get('id')}",
            verified_at=datetime.utcnow(),
            data_source="EDRPOU (via data.gov.ua)",
            confidence_score=0.85
        )
    
    @staticmethod
    def _validate_edrpou(edrpou: str) -> bool:
        """Validate EDRPOU format"""
        if not edrpou or not str(edrpou).isdigit():
            return False
        
        if len(str(edrpou)) != 8:
            return False
        
        return True
    
    @staticmethod
    def _normalize_status(status: str) -> str:
        """Normalize status to standard format"""
        status_lower = status.lower() if status else "unknown"
        
        mappings = {
            "активна": "active",
            "неактивна": "inactive",
            "припинена": "liquidated",
            "зупинена": "suspended",
            "активная": "active",
            "неактивная": "inactive",
            "прекращена": "liquidated",
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
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
        
        return None
