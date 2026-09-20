"""
Abstract Base Connector for NGO Registry Verification
Defines interface for all registry connectors (Ukraine, Poland, etc.)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel


class NGOData(BaseModel):
    """Standardized NGO data from registry"""
    
    country_code: str  # ISO 3166-1 alpha-2 (UA, PL, etc.)
    registration_number: str
    name: str
    legal_name: Optional[str] = None
    status: str  # active, inactive, suspended, etc.
    registration_date: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Registry-specific data
    registry_id: str  # Unique ID from registry
    registry_url: Optional[str] = None  # Link to registry entry
    
    # Verification metadata
    verified_at: datetime
    data_source: str  # Registry name
    confidence_score: float  # 0.0-1.0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class VerificationError(Exception):
    """Base exception for verification errors"""
    pass


class RegistryNotFoundError(VerificationError):
    """NGO not found in registry"""
    pass


class RegistryTimeoutError(VerificationError):
    """Registry API timeout"""
    pass


class RegistryConnectionError(VerificationError):
    """Cannot connect to registry"""
    pass


class BaseConnector(ABC):
    """
    Abstract base connector for NGO registries
    
    All registry connectors must implement:
    - verify(): Verify single NGO
    - batch_verify(): Verify multiple NGOs
    - is_active(): Check if NGO is currently active
    """
    
    def __init__(self, timeout: int = 30, retries: int = 3):
        """
        Initialize connector
        
        Args:
            timeout: Request timeout in seconds
            retries: Number of retry attempts
        """
        self.timeout = timeout
        self.retries = retries
    
    @property
    @abstractmethod
    def country_code(self) -> str:
        """ISO 3166-1 alpha-2 country code (UA, PL, etc.)"""
        pass
    
    @property
    @abstractmethod
    def registry_name(self) -> str:
        """Human-readable registry name (ЄДРПОУ, KRS, etc.)"""
        pass
    
    @abstractmethod
    async def verify(
        self,
        registration_number: str,
        **kwargs
    ) -> NGOData:
        """
        Verify NGO in registry
        
        Args:
            registration_number: Registry-specific ID
            **kwargs: Additional lookup parameters
            
        Returns:
            NGOData: Standardized NGO data
            
        Raises:
            RegistryNotFoundError: NGO not found
            RegistryTimeoutError: API timeout
            RegistryConnectionError: Cannot connect
            VerificationError: Other errors
        """
        pass
    
    async def batch_verify(
        self,
        registration_numbers: List[str],
        stop_on_error: bool = False
    ) -> List[tuple[str, Optional[NGOData], Optional[Exception]]]:
        """
        Verify multiple NGOs
        
        Args:
            registration_numbers: List of registry IDs
            stop_on_error: Stop on first error
            
        Returns:
            List of (reg_number, ngo_data, error) tuples
        """
        results = []
        
        for reg_num in registration_numbers:
            try:
                ngo_data = await self.verify(reg_num)
                results.append((reg_num, ngo_data, None))
            except VerificationError as e:
                if stop_on_error:
                    raise
                results.append((reg_num, None, e))
        
        return results
    
    async def is_active(self, registration_number: str) -> bool:
        """
        Check if NGO is currently active
        
        Args:
            registration_number: Registry ID
Returns:
            bool: True if active, False otherwise
        """
        try:
            ngo_data = await self.verify(registration_number)
            return ngo_data.status.lower() in ['active', 'активна', 'aktywna']
        except VerificationError:
            return False
    
    @staticmethod
    def for_country(country_code: str) -> 'BaseConnector':
        """
        Factory method to get connector for country
        
        Args:
            country_code: ISO 3166-1 alpha-2 code
            
        Returns:
            BaseConnector: Appropriate connector
            
        Raises:
            ValueError: Country not supported
        """
        from src.connectors.ukraine import UkraineConnector
        from src.connectors.poland import PolandConnector
        
        connectors = {
            'UA': UkraineConnector,
            'PL': PolandConnector,
        }
        
        connector_class = connectors.get(country_code.upper())
        if not connector_class:
            raise ValueError(f"Unsupported country: {country_code}")
        
        return connector_class()


class CachedConnector(BaseConnector):
    """
    Connector with caching support
    
    Caches verified NGOs to reduce API calls
    """
    
    def __init__(self, timeout: int = 30, retries: int = 3, cache_ttl: int = 3600):
        """
        Initialize connector with cache
        
        Args:
            timeout: Request timeout
            retries: Number of retries
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        super().__init__(timeout, retries)
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[NGOData, datetime]] = {}
    
    def _get_cached(self, registration_number: str) -> Optional[NGOData]:
        """Get NGO from cache if valid"""
        if registration_number in self._cache:
            ngo_data, cached_at = self._cache[registration_number]
            age = (datetime.utcnow() - cached_at).total_seconds()
            
            if age < self.cache_ttl:
                return ngo_data
            else:
                del self._cache[registration_number]
        
        return None
    
    def _set_cached(self, registration_number: str, ngo_data: NGOData) -> None:
        """Store NGO in cache"""
        self._cache[registration_number] = (ngo_data, datetime.utcnow())
    
    def clear_cache(self) -> None:
        """Clear all cached entries"""
        self._cache.clear()
    
    def cache_size(self) -> int:
        """Get current cache size"""
        return len(self._cache)
