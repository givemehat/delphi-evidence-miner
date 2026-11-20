from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class MarketQuestion(BaseModel):
    market_id: str
    question: str
    category: str
    created_at: datetime
    resolution_deadline: datetime
    current_probability: float = Field(ge=0.0, le=1.0)
    status: str = "active"

class RawEvidence(BaseModel):
    source_url: str
    source_domain: str
    extracted_text: str
    published_date: Optional[datetime] = None

class ScoredEvidence(BaseModel):
    source_url: str
    source_domain: str
    credibility_score: float = Field(ge=0.0, le=1.0)
    recency_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    overall_confidence: float = Field(ge=0.0, le=1.0)
    indicated_probability: float = Field(ge=0.0, le=1.0)
    summary: str

class EvidencePayload(BaseModel):
    market_id: str
    agent_id: str
    evidence_items: List[ScoredEvidence]
    aggregated_probability_estimate: float = Field(ge=0.0, le=1.0)
    payout_address: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SubmissionVerdict(BaseModel):
    submission_id: str
    market_id: str
    accepted: bool
    reward_earned_usdc: float
    verdict_rationale: str
    processed_at: datetime
