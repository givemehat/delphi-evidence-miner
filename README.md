# Delphi Autonomous Evidence Miner

[![CI](https://github.com/givemehat/delphi-evidence-miner/actions/workflows/ci.yml/badge.svg)](https://github.com/givemehat/delphi-evidence-miner/actions)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An autonomous, multi-source evidence mining and verification agent built for on-chain prediction markets (Delphi & Gensyn Agent Arena).

The agent operates in a continuous, automated loop:
1. **Market Ingestion**: Fetches open questions and prediction claims.
2. **Autonomous Retrieval**: Decomposes claims into factual queries and crawls primary web/data sources.
3. **Credibility & Impact Scoring**: Evaluates source reputation, recency, and calculates probability shift vectors.
4. **Structured Submission**: Dispatches validated evidence payloads to the Delphi API and tracks verification verdicts.

---

## Architecture

```text
[Active Prediction Markets]
            │
            ▼
┌───────────────────────┐
│ Claim Ingestion Loop  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐      ┌────────────────────────┐
│ Search & Data Miner   │ ───► │ Multi-Source Retriever │
└───────────┬───────────┘      └────────────────────────┘
            │
            ▼
┌───────────────────────┐
│ Credibility Scorer    │ ◄─── (Domain Authority + Recency + Bias Check)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Delphi Evidence Sink  │ ───► [Delphi Forecaster / Settlement API]
└───────────────────────┘
```

---

## Installation & Setup

```bash
git clone https://github.com/givemehat/delphi-evidence-miner.git
cd delphi-evidence-miner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Configuration

Copy the sample environment file:

```bash
cp .env.example .env
```

Set your configuration values:
- `DELPHI_API_KEY`: Your Delphi Forecaster API key.
- `DELPHI_PAYOUT_ADDRESS`: Your EVM / Base payout address (`0xFFE286685fB8C12c3d59728DA29E44a637C22d3d`).
- `MINER_CYCLE_INTERVAL_SEC`: Polling interval in seconds (default: 60).

---

## Usage

### Run in Dry-Run Mode (Simulation & Scoring Validation)
```bash
python -m miner.cli --dry-run
```

### Run Continuous Autonomous Mining
```bash
python -m miner.cli --loop --interval 120
```

### Run Unit Tests
```bash
pytest
```

---

## License

Apache-2.0
