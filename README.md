# Verifi - Web3 x AI Code Verification Protocol

A decentralized protocol that turns code verification into a verifiable, on-chain reputation system.

## Architecture

```
verifi/
├── src/           # AI Core (Python)
├── api/           # Backend API (FastAPI)
├── frontend/      # Landing Page (React + Vite)
├── blockchain/    # Smart Contracts (Solidity + Hardhat)
└── demo.py        # Full flow demonstration
```

## Quick Start

### Run Demo
```bash
python3 demo.py
```

### Run API Server
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```
API docs at http://localhost:8000/docs

### Run Frontend
```bash
cd frontend
npm install
npm run dev
```

## How It Works

1. **Claim** - Developer submits code claim with stated properties
2. **AI Task Breakdown** - AI analyzes claim, generates verification tasks
3. **Human Verification** - Community validators verify each task
4. **On-chain Proof** - Results recorded on blockchain with reputation updates

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/claims` | POST | Submit claim, get verification tasks |
| `/claims/{id}` | GET | Get claim status |
| `/tasks` | GET | Get available tasks for validator |
| `/tasks/{id}/accept` | POST | Accept a task |
| `/tasks/{id}/submit` | POST | Submit verification result |
| `/users/register` | POST | Register user/validator |

## Tech Stack

- **AI Core**: Python, Pydantic
- **Backend**: FastAPI, Python
- **Frontend**: React, Vite, TailwindCSS
- **Blockchain**: Solidity, Hardhat, Polygon

## License

MIT
