import asyncio
from datetime import datetime, timezone
from typing import List
from miner.models import MarketQuestion, RawEvidence, EvidencePayload
from miner.scorer import CredibilityScorer

class EvidenceMiningPipeline:
    def __init__(self, agent_id: str, payout_address: str, min_confidence: float = 0.70):
        self.agent_id = agent_id
        self.payout_address = payout_address
        self.min_confidence = min_confidence

    async def retrieve_evidence_candidates(self, market: MarketQuestion) -> List[RawEvidence]:
        # Simulated multi-source evidence extraction for demonstration
        return [
            RawEvidence(
                source_url=f"https://reuters.com/markets/{market.market_id}",
                source_domain="reuters.com",
                extracted_text=f"Official data confirms market resolution conditions for {market.question} have been verified.",
                published_date=datetime.now(timezone.utc)
            ),
            RawEvidence(
                source_url=f"https://bloomberg.com/news/{market.market_id}",
                source_domain="bloomberg.com",
                extracted_text=f"Regulatory filings indicate confirmed milestone attainment aligned with {market.question}.",
                published_date=datetime.now(timezone.utc)
            )
        ]

    async def process_market(self, market: MarketQuestion) -> EvidencePayload | None:
        raw_items = await self.retrieve_evidence_candidates(market)
        scored_items = [CredibilityScorer.evaluate_evidence(item, market.question) for item in raw_items]
        
        qualifying = [item for item in scored_items if item.overall_confidence >= self.min_confidence]
        if not qualifying:
            return None

        # Weighted probability estimate
        total_weight = sum(q.overall_confidence for q in qualifying)
        weighted_prob = sum(q.indicated_probability * q.overall_confidence for q in qualifying) / total_weight

        return EvidencePayload(
            market_id=market.market_id,
            agent_id=self.agent_id,
            evidence_items=qualifying,
            aggregated_probability_estimate=round(weighted_prob, 4),
            payout_address=self.payout_address
        )
