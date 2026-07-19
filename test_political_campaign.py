# 🚀 PHASE 2: Darivs Trust - ФАЙЛ 4

## 📤 ФАЙЛ 4: `test_political_campaign.py`

**Репо:** github.com/arvened/darivs-trust

---

### ✅ ШАГ 1: СОЗДАЙ НОВЫЙ ФАЙЛ

1. Нажми **"Add file"** (иконка +)
2. Выбери **"Create new file"**

---

### ✅ ШАГ 2: ИМЯ ФАЙЛА

В поле **"Name your file"** введи:
```
test_political_campaign.py
```

---

### ✅ ШАГ 3: СКОПИРУЙ КОД

Весь текст ниже — вставь в поле:

```python
"""
Tests for Political Campaign Verification
"""

import pytest
from datetime import datetime, timedelta
from political_campaign import (
    PoliticalCampaignAnalyzer, CampaignProfile, CampaignType,
    VerificationStatus, TransactionRecord, NGOVerifier
)


class TestNGOVerification:
    """Test NGO verification"""
    
    @pytest.mark.asyncio
    async def test_verify_ukrainian_ngo(self):
        analyzer = PoliticalCampaignAnalyzer(
            ngo_registries={"ukraine_edrpou": {}}
        )
        
        campaign = CampaignProfile(
            campaign_id="ngo_001",
            name="БФ Слава України",
            campaign_type=CampaignType.NGO,
            description="Ukrainian charitable foundation",
            launch_date=datetime.now() - timedelta(days=365),
            leader="Eduard Arbitman",
            website="https://example.com",
            location="Ukraine"
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["campaign_id"] == "ngo_001"
        assert result["confidence_score"] > 0.5
    
    @pytest.mark.asyncio
    async def test_verify_ngo_funding_source(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        transaction = TransactionRecord(
            transaction_id="txn_001",
            campaign_id="ngo_001",
            transaction_type="donation",
            amount=10_000,
            currency="EUR",
            date=datetime.now(),
            source="John Smith Foundation",
            destination="БФ Слава України",
            description="Donation for humanitarian work",
            category="donation"
        )
        
        result = await analyzer.verify_transaction("ngo_001", transaction)
        
        assert "transaction_id" in result
        assert "verified" in result


class TestCandidateVerification:
    """Test candidate verification"""
    
    @pytest.mark.asyncio
    async def test_verify_candidate(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="cand_001",
            name="John Doe",
            campaign_type=CampaignType.CANDIDATE,
            description="Presidential candidate 2026",
            launch_date=datetime.now(),
            leader="John Doe",
            location="Ukraine"
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["verification_status"] == VerificationStatus.VERIFIED.value
        assert result["confidence_score"] > 0.7
    
    @pytest.mark.asyncio
    async def test_reject_large_contribution(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        transaction = TransactionRecord(
            transaction_id="txn_002",
            campaign_id="cand_001",
            transaction_type="donation",
            amount=500_000,
            currency="USD",
            date=datetime.now(),
            source="Unknown Donor",
            destination="John Doe Campaign",
            description="Campaign contribution",
            category="donation"
        )
        
        result = await analyzer.verify_transaction("cand_001", transaction)
        
        assert result["verified"] == False


class TestTransparencyScoring:
    """Test transparency evaluation"""
    
    @pytest.mark.asyncio
    async def test_high_transparency_score(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="camp_001",
            name="Transparent Campaign",
            campaign_type=CampaignType.NGO,
            description="Fully transparent campaign",
            launch_date=datetime.now() - timedelta(days=100),
            leader="Jane Smith",
            website="https://transparent-campaign.org",
            revenue=100_000,
            expenditure=80_000
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["integrity_score"] > 0.6


class TestIntegrityScoring:
    """Test overall integrity assessment"""
    
    @pytest.mark.asyncio
    async def test_integrity_score_calculation(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="integ_001",
            name="Test Campaign",
            campaign_type=CampaignType.NGO,
            description="Test campaign",
            launch_date=datetime.now(),
            leader="Test Leader",
            website="https://test.com",
            revenue=50_000
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert 0 <= result["integrity_score"] <= 1
        assert "recommendation" in result


class TestRecommendationGeneration:
    """Test recommendation generation"""
    
    @pytest.mark.asyncio
    async def test_approved_recommendation(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="rec_001",
            name="Fully Verified Campaign",
            campaign_type=CampaignType.CANDIDATE,
            description="Verified campaign",
            launch_date=datetime.now(),
            leader="Test Candidate",
            website="https://test.com",
            revenue=50_000,
            expenditure=40_000
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert "APPROVED" in result["recommendation"] or "REVIEW" in result["recommendation"]


class TestVerificationReport:
    """Test verification report generation"""
    
    @pytest.mark.asyncio
    async def test_generate_verification_report(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="report_001",
            name="Report Test",
            campaign_type=CampaignType.NGO,
            description="Test",
            launch_date=datetime.now(),
            leader="Test"
        )
        
        await analyzer.analyze_campaign(campaign)
        report = analyzer.get_verification_report("report_001")
        
        assert "VERIFICATION REPORT" in report
        assert "Report Test" in report
        assert "FINDINGS" in report


class TestFundingVerification:
    """Test funding verification"""
    
    @pytest.mark.asyncio
    async def test_verify_domestic_donation(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        transaction = TransactionRecord(
            transaction_id="txn_003",
            campaign_id="cand_002",
            transaction_type="donation",
            amount=50_000,
            currency="USD",
            date=datetime.now(),
            source="Local Business",
            destination="Campaign Fund",
            description="Campaign donation",
            category="donation"
        )
        
        result = await analyzer.verify_transaction("cand_002", transaction)
        
        assert "transaction_id" in result


class TestMultipleCampaigns:
    """Test handling multiple campaigns"""
    
    @pytest.mark.asyncio
    async def test_analyze_multiple_campaigns(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaigns = [
            CampaignProfile(
                campaign_id=f"camp_{i}",
                name=f"Campaign {i}",
                campaign_type=CampaignType.NGO,
                description=f"Campaign {i} description",
                launch_date=datetime.now() - timedelta(days=i*10),
                leader=f"Leader {i}",
                website=f"https://campaign{i}.com"
            )
            for i in range(3)
        ]
        
        results = []
        for campaign in campaigns:
            result = await analyzer.analyze_campaign(campaign)
            results.append(result)
        
        assert len(results) == 3
        assert all("campaign_id" in r for r in results)


class TestCampaignTypes:
    """Test different campaign types"""
    
    @pytest.mark.asyncio
    async def test_verify_movement_campaign(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="mov_001",
            name="Democracy Movement",
            campaign_type=CampaignType.MOVEMENT,
            description="Pro-democracy movement",
            launch_date=datetime.now(),
            leader="Movement Leaders",
            location="Ukraine"
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["campaign_id"] == "mov_001"
    
    @pytest.mark.asyncio
    async def test_verify_issue_campaign(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="iss_001",
            name="Climate Action",
            campaign_type=CampaignType.ISSUE,
            description="Climate change awareness",
            launch_date=datetime.now(),
            leader="Environmentalists",
            location="Global"
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["campaign_id"] == "iss_001"


class TestTransactionCategories:
    """Test different transaction categories"""
    
    @pytest.mark.asyncio
    async def test_verify_expense_transaction(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        transaction = TransactionRecord(
            transaction_id="txn_004",
            campaign_id="cand_003",
            transaction_type="expense",
            amount=15_000,
            currency="USD",
            date=datetime.now(),
            source="Campaign Fund",
            destination="Media Agency",
            description="Advertising expenses",
            category="advertising"
        )
        
        result = await analyzer.verify_transaction("cand_003", transaction)
        
        assert "transaction_id" in result


class TestComplianceChecking:
    """Test compliance checking"""
    
    @pytest.mark.asyncio
    async def test_check_ngo_compliance(self):
        analyzer = PoliticalCampaignAnalyzer(
            ngo_registries={"ukraine_edrpou": {}}
        )
        
        campaign = CampaignProfile(
            campaign_id="ngo_002",
            name="Compliant NGO",
            campaign_type=CampaignType.NGO,
            description="Fully compliant organization",
            launch_date=datetime.now() - timedelta(days=500),
            leader="NGO Director",
            website="https://ngo.org",
            revenue=200_000,
            expenditure=180_000
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert "compliance" in str(result).lower() or "verified" in result["verification_status"]


class TestFinancialData:
    """Test financial data handling"""
    
    @pytest.mark.asyncio
    async def test_handle_financial_transparency(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="fin_001",
            name="Transparent Finance",
            campaign_type=CampaignType.NGO,
            description="Financial transparency test",
            launch_date=datetime.now() - timedelta(days=30),
            leader="Finance Officer",
            revenue=75_000,
            expenditure=65_000
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        assert result["integrity_score"] > 0.5


class TestVerificationStatus:
    """Test verification status transitions"""
    
    @pytest.mark.asyncio
    async def test_verification_status_values(self):
        analyzer = PoliticalCampaignAnalyzer()
        
        campaign = CampaignProfile(
            campaign_id="status_001",
            name="Status Test",
            campaign_type=CampaignType.CANDIDATE,
            description="Test",
            launch_date=datetime.now(),
            leader="Test"
        )
        
        result = await analyzer.analyze_campaign(campaign)
        
        valid_statuses = [
            "verified",
            "partially_verified",
            "unverified",
            "suspicious",
            "blocked"
        ]
        
        assert result["verification_status"] in valid_statuses


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

