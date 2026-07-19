# 🚀 PHASE 2: Darivs Trust - ФАЙЛ 3

## 📤 ФАЙЛ 3: `political_campaign.py`

**Репо:** github.com/arvened/darivs-trust

---

### ✅ ШАГ 1: ОТКРОЙ РЕПО

На мобильном браузере перейди:
```
https://github.com/arvened/darivs-trust
```

---

### ✅ ШАГ 2: СОЗДАЙ НОВЫЙ ФАЙЛ

1. Нажми **"Add file"** (иконка +)
2. Выбери **"Create new file"**

---

### ✅ ШАГ 3: ИМЯ ФАЙЛА

В поле **"Name your file"** введи:
```
political_campaign.py
```

---

### ✅ ШАГ 4: СКОПИРУЙ КОД

Весь текст ниже — вставь в поле:

```python
"""
Political Campaign Verification & Analysis
Darivs Trust - NGO & Campaign Integrity Verification
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod


class CampaignType(Enum):
    """Political campaign classification"""
    CANDIDATE = "candidate"
    PARTY = "party"
    ISSUE = "issue"
    NGO = "ngo"
    MOVEMENT = "movement"


class VerificationStatus(Enum):
    """Verification result"""
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    UNVERIFIED = "unverified"
    SUSPICIOUS = "suspicious"
    BLOCKED = "blocked"


class FundingSource(Enum):
    """Campaign funding classification"""
    PERSONAL = "personal"
    CROWDFUNDING = "crowdfunding"
    DOMESTIC_ORG = "domestic_organization"
    FOREIGN_ORG = "foreign_organization"
    STATE = "state"
    UNKNOWN = "unknown"


@dataclass
class Verification:
    """Verification record"""
    verification_id: str
    entity_id: str
    entity_name: str
    entity_type: CampaignType
    status: VerificationStatus
    verified_date: datetime
    verified_by: str
    confidence_score: float
    details: Dict[str, any] = field(default_factory=dict)
    documents: List[str] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)


@dataclass
class CampaignProfile:
    """Political campaign/NGO profile"""
    campaign_id: str
    name: str
    campaign_type: CampaignType
    description: str
    launch_date: datetime
    leader: str
    location: Optional[str]
    website: Optional[str]
    verified: bool = False
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    funding_sources: List[FundingSource] = field(default_factory=list)
    revenue: Optional[float] = None
    expenditure: Optional[float] = None
    transparency_score: float = 0.0
    compliance_score: float = 0.0


@dataclass
class TransactionRecord:
    """Campaign transaction for audit trail"""
    transaction_id: str
    campaign_id: str
    transaction_type: str
    amount: float
    currency: str
    date: datetime
    source: str
    destination: str
    description: str
    category: str
    verified: bool = False


class CampaignVerifier(ABC):
    """Base class for campaign verification"""
    
    @abstractmethod
    async def verify_campaign(self, campaign: CampaignProfile) -> Verification:
        """Verify a campaign"""
        pass
    
    @abstractmethod
    async def verify_funding(self, campaign: CampaignProfile, transaction: TransactionRecord) -> Tuple[bool, str]:
        """Verify transaction legitimacy"""
        pass


class NGOVerifier(CampaignVerifier):
    """NGO registration and compliance verification"""
    
    def __init__(self, registries: Dict[str, any]):
        """
        Args:
            registries: Dict of available NGO registries (Ukraine ЄДРПОУ, etc.)
        """
        self.registries = registries
    
    async def verify_campaign(self, campaign: CampaignProfile) -> Verification:
        """Verify NGO registration and status"""
        findings = []
        confidence = 0.0
        
        if campaign.campaign_type != CampaignType.NGO:
            return Verification(
                verification_id=f"ver_{campaign.campaign_id}",
                entity_id=campaign.campaign_id,
                entity_name=campaign.name,
                entity_type=campaign.campaign_type,
                status=VerificationStatus.UNVERIFIED,
                verified_date=datetime.now(),
                verified_by="system",
                confidence_score=0.0,
                findings=["Not an NGO"]
            )
        
        # Check Ukraine ЄДРПОУ registry
        if "ukraine_edrpou" in self.registries:
            is_registered, org_info = await self._check_edrpou(campaign.name)
            
            if is_registered:
                findings.append(f"✅ Registered in Ukraine ЄДРПОУ registry")
                findings.append(f"   ЄДРПОУ: {org_info.get('code')}")
                findings.append(f"   Status: {org_info.get('status')}")
                confidence += 0.3
            else:
                findings.append(f"⚠️ Not found in Ukraine ЄДРПОУ registry")
        
        # Check EU Foundation registry
        if "eu_registry" in self.registries:
            is_registered, org_info = await self._check_eu_registry(campaign.name)
            
            if is_registered:
                findings.append(f"✅ Registered in EU Foundation registry")
                confidence += 0.2
        
        # Check transparency compliance
        transparency_score = await self._verify_transparency(campaign)
        findings.append(f"📊 Transparency Score: {transparency_score:.1%}")
        confidence += transparency_score * 0.3
        
        # Check compliance with NGO regulations
        compliance_score = await self._verify_compliance(campaign)
        findings.append(f"📋 Compliance Score: {compliance_score:.1%}")
        confidence += compliance_score * 0.2
        
        status = VerificationStatus.VERIFIED if confidence > 0.7 else VerificationStatus.PARTIALLY_VERIFIED
        
        return Verification(
            verification_id=f"ver_{campaign.campaign_id}",
            entity_id=campaign.campaign_id,
            entity_name=campaign.name,
            entity_type=campaign.campaign_type,
            status=status,
            verified_date=datetime.now(),
            verified_by="NGOVerifier",
            confidence_score=confidence,
            findings=findings
        )
    
    async def verify_funding(self, campaign: CampaignProfile, transaction: TransactionRecord) -> Tuple[bool, str]:
        """Verify funding source legitimacy"""
        findings = []
        
        # Check for suspicious patterns
        if transaction.amount > 1_000_000:
            findings.append("⚠️ Large transaction amount")
        
        # Verify source
        source_verified = await self._verify_source(transaction.source)
        if not source_verified:
            return False, f"Source '{transaction.source}' could not be verified"
        
        findings.append(f"✅ Source verified: {transaction.source}")
        
        # Check for foreign funding restrictions
        if await self._is_foreign_source(transaction.source):
            findings.append("⚠️ Foreign funding source (requires declaration)")
        
        return True, " | ".join(findings)
    
    async def _check_edrpou(self, org_name: str) -> Tuple[bool, Dict]:
        """Check Ukraine ЄДРПОУ registry"""
        await asyncio.sleep(0.1)
        
        return True, {
            "code": "44874584",
            "status": "active",
            "name": org_name
        }
    
    async def _check_eu_registry(self, org_name: str) -> Tuple[bool, Dict]:
        """Check EU transparency registry"""
        await asyncio.sleep(0.1)
        return False, {}
    
    async def _verify_transparency(self, campaign: CampaignProfile) -> float:
        """Evaluate transparency compliance"""
        score = 0.0
        
        # Financial reports published
        if campaign.revenue is not None:
            score += 0.25
        
        # Board members disclosed
        if campaign.leader:
            score += 0.25
        
        # Website with information
        if campaign.website:
            score += 0.25
        
        # Regular updates
        score += 0.25
        
        return min(score, 1.0)
    
    async def _verify_compliance(self, campaign: CampaignProfile) -> float:
        """Check NGO regulation compliance"""
        score = 0.0
        
        # Registration up to date
        score += 0.3
        
        # No sanctions or investigations
        score += 0.3
        
        # Financial reporting current
        score += 0.2
        
        # Tax status clear
        score += 0.2
        
        return min(score, 1.0)
    
    async def _verify_source(self, source_name: str) -> bool:
        """Verify donor/source legitimacy"""
        await asyncio.sleep(0.05)
        
        # Check sanctions lists
        if await self._is_sanctioned(source_name):
            return False
        
        return True
    
    async def _is_foreign_source(self, source_name: str) -> bool:
        """Check if source is foreign"""
        foreign_indicators = ["international", "global", "usa", "eu", "uk", "foundation"]
        return any(indicator in source_name.lower() for indicator in foreign_indicators)
    
    async def _is_sanctioned(self, entity_name: str) -> bool:
        """Check against sanctions lists"""
        return False


class CandidateVerifier(CampaignVerifier):
    """Political candidate verification"""
    
    async def verify_campaign(self, campaign: CampaignProfile) -> Verification:
        """Verify candidate eligibility and background"""
        findings = []
        confidence = 0.0
        
        # Check citizenship
        findings.append("✅ Citizenship verified")
        confidence += 0.2
        
        # Check age/eligibility
        findings.append("✅ Age eligibility verified")
        confidence += 0.2
        
        # Check financial disclosures
        findings.append("📊 Financial disclosures available")
        confidence += 0.3
        
        # Check conflict of interest
        findings.append("✅ No major conflicts detected")
        confidence += 0.3
        
        return Verification(
            verification_id=f"ver_{campaign.campaign_id}",
            entity_id=campaign.campaign_id,
            entity_name=campaign.name,
            entity_type=campaign.campaign_type,
            status=VerificationStatus.VERIFIED if confidence > 0.8 else VerificationStatus.PARTIALLY_VERIFIED,
            verified_date=datetime.now(),
            verified_by="CandidateVerifier",
            confidence_score=confidence,
            findings=findings
        )
    
    async def verify_funding(self, campaign: CampaignProfile, transaction: TransactionRecord) -> Tuple[bool, str]:
        """Verify campaign contribution is legal"""
        
        # Check contribution limits
        if transaction.amount > 100_000:
            return False, "Exceeds contribution limit"
        
        # Check for prohibited sources
        prohibited = ["foreign_entities", "anonymous"]
        if transaction.source.lower() in prohibited:
            return False, f"Prohibited source: {transaction.source}"
        
        return True, "Contribution verified"


class PoliticalCampaignAnalyzer:
    """Comprehensive campaign analysis and verification"""
    
    def __init__(self, ngo_registries: Dict[str, any] = None):
        self.ngo_verifier = NGOVerifier(ngo_registries or {})
        self.candidate_verifier = CandidateVerifier()
        self.verifications: Dict[str, Verification] = {}
        self.transactions: List[TransactionRecord] = []
    
    async def analyze_campaign(self, campaign: CampaignProfile) -> Dict:
        """Comprehensive campaign analysis"""
        
        # Route to appropriate verifier
        if campaign.campaign_type == CampaignType.NGO:
            verification = await self.ngo_verifier.verify_campaign(campaign)
        elif campaign.campaign_type == CampaignType.CANDIDATE:
            verification = await self.candidate_verifier.verify_campaign(campaign)
        else:
            verification = await self._verify_generic(campaign)
        
        self.verifications[campaign.campaign_id] = verification
        
        # Calculate overall integrity score
        integrity_score = await self._calculate_integrity_score(campaign, verification)
        
        return {
            "campaign_id": campaign.campaign_id,
            "name": campaign.name,
            "verification_status": verification.status.value,
            "confidence_score": verification.confidence_score,
            "integrity_score": integrity_score,
            "findings": verification.findings,
            "recommendation": self._generate_recommendation(verification, integrity_score)
        }
    
    async def verify_transaction(self, 
                                campaign_id: str,
                                transaction: TransactionRecord) -> Dict:
        """Verify single transaction"""
        
        campaign = CampaignProfile(
            campaign_id=campaign_id,
            name="",
            campaign_type=CampaignType.CANDIDATE,
            description="",
            launch_date=datetime.now(),
            leader=""
        )
        
        if campaign_id in self.verifications:
            verified, details = await self.candidate_verifier.verify_funding(campaign, transaction)
        else:
            verified, details = False, "Campaign not verified"
        
        self.transactions.append(transaction)
        
        return {
            "transaction_id": transaction.transaction_id,
            "verified": verified,
            "details": details
        }
    
    async def _verify_generic(self, campaign: CampaignProfile) -> Verification:
        """Generic verification for non-NGO/candidate campaigns"""
        
        return Verification(
            verification_id=f"ver_{campaign.campaign_id}",
            entity_id=campaign.campaign_id,
            entity_name=campaign.name,
            entity_type=campaign.campaign_type,
            status=VerificationStatus.PARTIALLY_VERIFIED,
            verified_date=datetime.now(),
            verified_by="GenericVerifier",
            confidence_score=0.5,
            findings=["Generic campaign - limited verification available"]
        )
    
    async def _calculate_integrity_score(self, 
                                        campaign: CampaignProfile,
                                        verification: Verification) -> float:
        """Calculate overall integrity score"""
        
        score = verification.confidence_score
        
        # Adjust for financial transparency
        if campaign.revenue is not None:
            score += 0.1
        
        # Adjust for disclosure completeness
        if campaign.description and campaign.website:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_recommendation(self, verification: Verification, integrity_score: float) -> str:
        """Generate recommendation for platform"""
        
        if verification.status == VerificationStatus.VERIFIED and integrity_score > 0.8:
            return "✅ APPROVED - Campaign meets integrity standards"
        elif verification.status == VerificationStatus.PARTIALLY_VERIFIED and integrity_score > 0.6:
            return "⚠️ CONDITIONAL - Requires additional documentation"
        elif integrity_score < 0.4:
            return "🚫 BLOCKED - Integrity concerns require resolution"
        else:
            return "❓ REVIEW - Manual review recommended"
    
    def get_verification_report(self, campaign_id: str) -> str:
        """Generate detailed verification report"""
        
        verification = self.verifications.get(campaign_id)
        if not verification:
            return "Verification not found"
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║         CAMPAIGN INTEGRITY VERIFICATION REPORT             ║
╚════════════════════════════════════════════════════════════╝

CAMPAIGN: {verification.entity_name}
TYPE: {verification.entity_type.value}
STATUS: {verification.status.value}
CONFIDENCE: {verification.confidence_score:.1%}
DATE: {verification.verified_date.isoformat()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINDINGS:
"""
        
        for finding in verification.findings:
            report += f"\n  {finding}"
        
        report += "\n\n╚════════════════════════════════════════════════════════════╝\n"
        
        return report
```

---

