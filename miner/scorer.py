from datetime import datetime, timezone
import math
from typing import List
from miner.models import RawEvidence, ScoredEvidence

DOMAIN_TRUST_WEIGHTS = {
    "reuters.com": 0.95,
    "apnews.com": 0.95,
    "bloomberg.com": 0.93,
    "wsj.com": 0.92,
    "ft.com": 0.92,
    "coindesk.com": 0.85,
    "cointelegraph.com": 0.80,
    "theblock.co": 0.86,
    "sec.gov": 0.99,
    "federalreserve.gov": 0.99,
    "github.com": 0.88,
}

class CredibilityScorer:
    @staticmethod
    def calculate_recency_score(published_at: datetime | None) -> float:
        if not published_at:
            return 0.5
        now = datetime.now(timezone.utc)
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        diff_hours = max(0.0, (now - published_at).total_seconds() / 3600.0)
        # Exponential decay: half-life of 48 hours
        return math.exp(-math.log(2) * (diff_hours / 48.0))

    @staticmethod
    def calculate_domain_trust(domain: str) -> float:
        cleaned = domain.lower().replace("www.", "")
        return DOMAIN_TRUST_WEIGHTS.get(cleaned, 0.60)

    @classmethod
    def evaluate_evidence(cls, raw: RawEvidence, question_context: str) -> ScoredEvidence:
        domain_trust = cls.calculate_domain_trust(raw.source_domain)
        recency = cls.calculate_recency_score(raw.published_date)
        
        # Keyword overlap proxy for relevance
        q_words = set(question_context.lower().split())
        body_words = set(raw.extracted_text.lower().split())
        overlap = len(q_words.intersection(body_words)) / max(1, len(q_words))
        relevance = min(1.0, 0.4 + (overlap * 0.6))
        
        overall = (domain_trust * 0.45) + (recency * 0.25) + (relevance * 0.30)
        
        # Simple sentiment / direction signal
        text_lower = raw.extracted_text.lower()
        if "approved" in text_lower or "confirmed" in text_lower or "record" in text_lower:
            prob = 0.82
        elif "denied" in text_lower or "rejected" in text_lower or "delayed" in text_lower:
            prob = 0.18
        else:
            prob = 0.50

        return ScoredEvidence(
            source_url=raw.source_url,
            source_domain=raw.source_domain,
            credibility_score=round(domain_trust, 4),
            recency_score=round(recency, 4),
            relevance_score=round(relevance, 4),
            overall_confidence=round(overall, 4),
            indicated_probability=prob,
            summary=raw.extracted_text[:200]
        )
