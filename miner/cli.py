import argparse
import asyncio
from datetime import datetime, timezone
from miner.models import MarketQuestion
from miner.pipeline import EvidenceMiningPipeline

async def main():
    parser = argparse.ArgumentParser(description="Autonomous Delphi Evidence Mining Agent")
    parser.add_argument("--dry-run", action="store_true", help="Execute single pass without live submission")
    parser.add_argument("--loop", action="store_true", help="Run in continuous polling loop")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval in seconds")
    parser.add_argument("--payout", default="0xFFE286685fB8C12c3d59728DA29E44a637C22d3d", help="EVM payout address")
    args = parser.parse_args()

    pipeline = EvidenceMiningPipeline(agent_id="delphi-agent-givemehat", payout_address=args.payout)

    sample_market = MarketQuestion(
        market_id="delphi-mkt-2026-q4",
        question="Will global settlement volumes on Base exceed 500M transactions in Q4 2026?",
        category="crypto_infrastructure",
        created_at=datetime.now(timezone.utc),
        resolution_deadline=datetime.now(timezone.utc),
        current_probability=0.45
    )

    print(f"[*] Processing Market: {sample_market.question}")
    payload = await pipeline.process_market(sample_market)
    if payload:
        print("[+] Validated Evidence Payload Generated:")
        print(payload.model_dump_json(indent=2))
    else:
        print("[-] Insufficient high-confidence evidence found.")

if __name__ == "__main__":
    asyncio.run(main())
