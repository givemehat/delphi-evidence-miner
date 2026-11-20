from datetime import datetime, timezone
import pytest
from miner.models import MarketQuestion, RawEvidence
from miner.scorer import CredibilityScorer
from miner.pipeline import EvidenceMiningPipeline

def test_domain_trust_scoring():
    reuters_score = CredibilityScorer.calculate_domain_trust("reuters.com")
    assert reuters_score >= 0.90
    unknown_score = CredibilityScorer.calculate_domain_trust("randomblog.xyz")
    assert unknown_score == 0.60

def test_evidence_pipeline():
    raw = RawEvidence(
        source_url="https://reuters.com/news/article",
        source_domain="reuters.com",
        extracted_text="Milestone officially confirmed and approved.",
        published_date=datetime.now(timezone.utc)
    )
    scored = CredibilityScorer.evaluate_evidence(raw, "Is the milestone approved?")
    assert scored.overall_confidence > 0.70
    assert scored.indicated_probability > 0.80

@pytest.mark.asyncio
async def test_full_pipeline_process():
    pipeline = EvidenceMiningPipeline(agent_id="test-agent", payout_address="0x0000000000000000000000000000000000000000")
    market = MarketQuestion(
        market_id="mkt-1",
        question="Will L2 throughput reach 10,000 TPS?",
        category="scalability",
        created_at=datetime.now(timezone.utc),
        resolution_deadline=datetime.now(timezone.utc),
        current_probability=0.50
    )
    payload = await pipeline.process_market(market)
    assert payload is not None
    assert payload.market_id == "mkt-1"
    assert len(payload.evidence_items) > 0
