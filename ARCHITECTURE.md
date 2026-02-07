# Verifi Architecture

## System Overview

```
+------------------+     +------------------+     +------------------+
|    Frontend      |     |    Backend API   |     |   Blockchain     |
|   (React/HTML)   | --> |    (FastAPI)     | --> |   (Hardhat)      |
+------------------+     +------------------+     +------------------+
                               |
                               v
                        +------------------+
                        |    AI Core       |
                        |    (Python)      |
                        +------------------+
```

---

## Components

### 1. Frontend (`/frontend`)

Static HTML/CSS website with pages:

| Page | File | Purpose |
|------|------|---------|
| Landing | `index.html` | Hero, problem/solution, CTA |
| Quests | `quests.html` | Task board for validators |
| Submit | `submit.html` | Claim submission form |
| Profile | `profile.html` | User stats, reputation |
| Task | `task.html` | Task detail and execution |

**Stack:** HTML, CSS, Vite (optional React components in `/src`)

---

### 2. Backend API (`/api`)

RESTful API built with FastAPI.

```
api/
├── main.py           # App entry, CORS, routers
├── schemas.py        # Pydantic request/response models
├── routes/
│   ├── claims.py     # POST /claims, GET /claims/{id}
│   ├── tasks.py      # GET /tasks, POST /tasks/{id}/accept
│   └── users.py      # POST /users/register, GET /users/{wallet}
├── services/
│   ├── ai_core.py    # Wrapper for AI pipeline
│   ├── blockchain.py # Mock blockchain interactions
│   ├── database.py   # Mock Firestore (in-memory)
│   └── matching.py   # Validator selection algorithm
└── config/
    ├── contract.json # Contract address + network
    └── VerifiTrust.json # Contract ABI
```

**Key Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/claims/` | Submit claim, get generated tasks |
| GET | `/claims/{id}` | Get claim status |
| GET | `/tasks/` | Get available tasks for validator |
| POST | `/tasks/{id}/accept` | Accept a task |
| POST | `/tasks/{id}/submit` | Submit verification result |

---

### 3. AI Core (`/src`)

Three-level pipeline for claim processing:

```
Claim Text
    │
    v
┌─────────────────────────────────────────┐
│ Level 1: Claim Classifier               │
│ - Analyzes claim dimensions             │
│ - Outputs: security, performance,       │
│   correctness, compatibility scores     │
└─────────────────────────────────────────┘
    │
    v
┌─────────────────────────────────────────┐
│ Level 2: Task Graph                     │
│ - 30+ predefined verification tasks     │
│ - DAG structure with dependencies       │
│ - Traverses based on classification     │
└─────────────────────────────────────────┘
    │
    v
┌─────────────────────────────────────────┐
│ Level 3: Task Expander                  │
│ - Fills task parameters from claim      │
│ - Sets min_validators, estimated_time   │
│ - Assigns required_skills               │
└─────────────────────────────────────────┘
    │
    v
List of ExpandedTasks (20 tasks typical)
```

**Files:**

```
src/
├── pipeline.py              # Main orchestrator
├── level1/
│   └── claim_classifier.py  # Dimension analysis
├── level2/
│   ├── task_graph.py        # Task DAG definition
│   └── graph_traversal.py   # BFS traversal
├── level3/
│   └── task_expander.py     # Parameter filling
├── models/
│   ├── claim.py             # Claim model
│   ├── classification.py    # Classification result
│   └── task.py              # Task models
└── utils/
    └── llm_client.py        # Mock LLM (swappable)
```

---

### 4. Blockchain (`/blockchain`)

Solidity smart contract for on-chain reputation.

**Contract: `VerifiTrust.sol`**

```solidity
// Key functions
function registerValidator() external
function submitProof(uint256 taskId, string evidenceHash, bool outcome) external
function getValidator(address) external view returns (Validator)

// Events
event ValidatorRegistered(address indexed wallet)
event ProofSubmitted(address indexed validator, uint256 taskId, bool outcome)
event ReputationIncreased(address indexed validator, uint256 newScore)
```

**Deployed:** Local Hardhat node (chain ID: 31337)

**Contract Address:** `0x5FbDB2315678afecb367f032d93F642f64180aa3`

---

## Data Flow

### Claim Submission Flow

```
1. User submits claim via frontend
         │
         v
2. POST /claims → Backend receives claim
         │
         v
3. AI Core processes:
   - Classifier analyzes dimensions
   - Task graph traversed
   - Tasks expanded with parameters
         │
         v
4. Tasks stored in database
         │
         v
5. Frontend shows generated tasks
```

### Verification Flow

```
1. Validator views /quests
         │
         v
2. POST /tasks/{id}/accept
         │
         v
3. Validator performs verification
         │
         v
4. POST /tasks/{id}/submit with result
         │
         v
5. Backend checks consensus
         │
         v
6. Blockchain.submitProof() called
         │
         v
7. Reputation updated on-chain
```

---

## Validator Selection Algorithm

```python
def select_validators(task, exclude_author):
    1. Filter by required_skills
    2. Filter by min_reputation (0.6)
    3. Exclude claim author
    4. Weighted random selection by reputation
    5. Return min_validators count
```

---

## Consensus Mechanism

```
- Each task requires min_validators (2-5)
- Majority vote determines outcome
- Agreed validators get +10 reputation
- Disagreed validators may lose reputation
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, Vite, React (optional) |
| Backend | Python, FastAPI, Pydantic |
| AI | Python, Mock LLM (swappable to OpenAI) |
| Blockchain | Solidity, Hardhat, ethers.js |
| Database | In-memory (mock Firestore) |

---

## Running Locally

```bash
# Backend API
cd verifi
pip install -r requirements.txt
uvicorn api.main:app --reload

# Frontend (static)
cd frontend
open index.html  # or use Live Server

# Blockchain (optional)
cd blockchain
npx hardhat node

# Demo
python3 demo.py
```

---

## Future Enhancements

1. **Firebase** - Replace mock database
2. **Real LLM** - OpenAI/Anthropic integration
3. **Testnet Deployment** - Polygon Amoy
4. **IPFS** - Evidence storage
5. **Token Rewards** - ERC-20 incentives
