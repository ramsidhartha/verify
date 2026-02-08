"""
Mock Database Service

For hackathon: In-memory storage that simulates Firebase.
Replace with real Firebase later (just swap the import).
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class MockDatabase:
    """
    In-memory database for development/testing.
    Same interface as Firebase, so easy to swap.
    """
    
    def __init__(self):
        self.users: Dict[str, Dict] = {}
        self.claims: Dict[str, Dict] = {}
        self.tasks: Dict[str, Dict] = {}
    
    # =========================================================================
    # Users
    # =========================================================================
    
    def create_user(self, wallet: str, skills: List[str] = None) -> Dict:
        """Create or update a user profile."""
        if wallet in self.users:
            return self.users[wallet]
        
        user = {
            "wallet": wallet,
            "skills": skills or [],
            "reputation": 0.5,  # Start at 50%
            "active_tasks": [],
            "completed_tasks": 0,
            "created_at": datetime.utcnow().isoformat()
        }
        self.users[wallet] = user
        return user
    
    def get_user(self, wallet: str) -> Optional[Dict]:
        """Get user by wallet address."""
        return self.users.get(wallet)
    
    def update_user(self, wallet: str, updates: Dict) -> Optional[Dict]:
        """Update user fields."""
        if wallet not in self.users:
            return None
        self.users[wallet].update(updates)
        return self.users[wallet]
    
    def get_qualified_validators(self, required_skills: List[str], min_reputation: float = 0.6) -> List[Dict]:
        """Get validators who have required skills and meet reputation threshold."""
        qualified = []
        for user in self.users.values():
            # Check reputation
            if user["reputation"] < min_reputation:
                continue
            # Check skills (must have at least one matching skill)
            user_skills = set(user["skills"])
            required = set(required_skills)
            if not user_skills.intersection(required):
                continue
            qualified.append(user)
        return qualified
    
    # =========================================================================
    # Claims
    # =========================================================================
    
    def create_claim(self, claim_text: str, author: str, tasks: List[Dict], coverage: float) -> Dict:
        """Create a new claim with its tasks."""
        claim_id = f"claim_{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow().isoformat()
        
        claim = {
            "claim_id": claim_id,
            "claim_text": claim_text,
            "author": author,
            "status": "pending",
            "tasks": [t["task_id"] for t in tasks],
            "coverage": coverage,
            "created_at": now,
            "updated_at": now
        }
        self.claims[claim_id] = claim
        
        # Create task records
        for task in tasks:
            task_id = f"task_{claim_id}_{task['task_id']}"
            self.tasks[task_id] = {
                "task_id": task_id,
                "claim_id": claim_id,
                "task_type": task["task_id"],
                "description": task["description"],
                "instructions": task.get("instructions", ""),
                "parameters": task.get("parameters", {}),
                "min_validators": task.get("min_validators", 2),
                "estimated_minutes": task.get("estimated_minutes", 30),
                "required_skills": task.get("required_skills", []),
                "assigned_validators": [],
                "results": [],
                "status": "open",
                "created_at": now
            }
        
        return claim
    
    def get_claim(self, claim_id: str) -> Optional[Dict]:
        """Get claim by ID."""
        return self.claims.get(claim_id)
    
    def update_claim_status(self, claim_id: str, status: str) -> Optional[Dict]:
        """Update claim status."""
        if claim_id not in self.claims:
            return None
        self.claims[claim_id]["status"] = status
        self.claims[claim_id]["updated_at"] = datetime.utcnow().isoformat()
        return self.claims[claim_id]
    
    def get_claims_by_author(self, wallet: str) -> List[Dict]:
        """Get all claims by an author."""
        return [c for c in self.claims.values() if c["author"] == wallet]
    
    # =========================================================================
    # Tasks
    # =========================================================================
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def get_open_tasks(self) -> List[Dict]:
        """Get all open tasks."""
        return [t for t in self.tasks.values() if t["status"] == "open"]
    
    def get_tasks_for_validator(self, wallet: str, skills: List[str]) -> List[Dict]:
        """Get open tasks matching validator's skills."""
        matching = []
        for task in self.tasks.values():
            if task["status"] != "open":
                continue
            # Check if already assigned (max validators)
            if len(task["assigned_validators"]) >= task["min_validators"]:
                continue
            # Check if already assigned to this validator
            if wallet in task["assigned_validators"]:
                continue
            # Check skill match
            task_skills = set(task["required_skills"])
            user_skills = set(skills)
            if task_skills.intersection(user_skills):
                matching.append(task)
        return matching
    
    def assign_task(self, task_id: str, wallet: str) -> Optional[Dict]:
        """Assign validator to task."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        if wallet not in task["assigned_validators"]:
            task["assigned_validators"].append(wallet)
            if task["status"] == "open":
                task["status"] = "in_progress"
        return task
    
    def submit_result(self, task_id: str, wallet: str, passed: bool, evidence: str = None) -> Optional[Dict]:
        """Submit task result."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        result = {
            "validator": wallet,
            "passed": passed,
            "evidence_hash": evidence,
            "submitted_at": datetime.utcnow().isoformat()
        }
        task["results"].append(result)
        
        # Check if we have enough results for consensus
        if len(task["results"]) >= task["min_validators"]:
            task["status"] = "completed"
            # Simple majority consensus
            passes = sum(1 for r in task["results"] if r["passed"])
            task["consensus"] = "pass" if passes > len(task["results"]) / 2 else "fail"
        
        return task
    
    def get_claim_tasks(self, claim_id: str) -> List[Dict]:
        """Get all tasks for a claim."""
        return [t for t in self.tasks.values() if t["claim_id"] == claim_id]
    
    def seed_demo_data(self):
        """Populate with demo data for showcase."""
        
        # =====================================================================
        # 5 Validator Profiles
        # =====================================================================
        validators = [
            {
                "wallet": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",  # vitalik.eth
                "skills": ["solidity", "security", "cryptography", "distributed-systems"],
                "reputation": 0.98,
                "completed_tasks": 1240,
                "display_name": "vitalik.eth"
            },
            {
                "wallet": "0x3a1F8B92C5462BD7F9C23A7539C8801fE56a8d91",
                "skills": ["python", "machine-learning", "data-science", "tensorflow"],
                "reputation": 0.92,
                "completed_tasks": 456,
                "display_name": "alex_dev.eth"
            },
            {
                "wallet": "0x7B12C4E82f9A41D8F02B5C7a64819C33a91Fe2cD",
                "skills": ["rust", "performance", "benchmarking", "systems"],
                "reputation": 0.87,
                "completed_tasks": 278,
                "display_name": "rust_master.eth"
            },
            {
                "wallet": "0x9D5c6a2E1B34f8A67C0E9d2F5A38B91C7E64Df03",
                "skills": ["circom", "cryptography", "zero-knowledge", "math"],
                "reputation": 0.94,
                "completed_tasks": 189,
                "display_name": "zk_wizard.eth"
            },
            {
                "wallet": "0x2E8F6C9A0B51D4e7F3a28C1E6D9B74A05F32Ce81",
                "skills": ["solidity", "defi", "math", "security"],
                "reputation": 0.89,
                "completed_tasks": 342,
                "display_name": "defi_chad.eth"
            }
        ]
        
        for v in validators:
            self.users[v["wallet"]] = {
                "wallet": v["wallet"],
                "skills": v["skills"],
                "reputation": v["reputation"],
                "active_tasks": [],
                "completed_tasks": v["completed_tasks"],
                "display_name": v.get("display_name", v["wallet"][:10] + "..."),
                "created_at": "2024-01-15T10:00:00"
            }
        
        # =====================================================================
        # 3 Demo Claims with Tasks (matching frontend)
        # =====================================================================
        
        now = datetime.utcnow().isoformat()
        
        # Claim 1: DeFi Protocol (from task-detail.html)
        claim1_id = "claim_8921"
        self.claims[claim1_id] = {
            "claim_id": claim1_id,
            "claim_text": "Protocol Implementation: Lending V2 - Interest rate model behaves linearly within 0-80% utilization and exponentially thereafter",
            "author": "0x3a1F8B92C5462BD7F9C23A7539C8801fE56a8d91",
            "status": "pending",
            "tasks": ["task_8921_T001", "task_8921_T002"],
            "coverage": 85.0,
            "created_at": now,
            "updated_at": now
        }
        self.tasks["task_8921_T001"] = {
            "task_id": "task_8921_T001",
            "claim_id": claim1_id,
            "task_type": "T001",
            "description": "Protocol Implementation: DeFi Lending",
            "instructions": "Execute check_interest_model.py against testnet. Verify utilization > 80% has 3x rate multiplier per 10% increase.",
            "parameters": {"contract_address": "0x..."},
            "min_validators": 3,
            "estimated_minutes": 120,
            "required_skills": ["solidity", "defi", "math", "security"],
            "assigned_validators": [],
            "results": [],
            "status": "pending",
            "reward": 500,
            "created_at": now
        }
        self.tasks["task_8921_T002"] = {
            "task_id": "task_8921_T002",
            "claim_id": claim1_id,
            "task_type": "T002",
            "description": "Liquidation Parameter Validation",
            "instructions": "Verify liquidation threshold triggers correctly at 150% collateral ratio.",
            "parameters": {},
            "min_validators": 2,
            "estimated_minutes": 60,
            "required_skills": ["solidity", "defi"],
            "assigned_validators": [],
            "results": [],
            "status": "pending",
            "reward": 300,
            "created_at": now
        }
        
        # Claim 2: ML Model (from marketplace.html)
        claim2_id = "claim_8945"
        self.claims[claim2_id] = {
            "claim_id": claim2_id,
            "claim_text": "ML Model achieves 94.5% accuracy on NFT price prediction using historical sales data",
            "author": "0x7B12C4E82f9A41D8F02B5C7a64819C33a91Fe2cD",
            "status": "in_progress",
            "tasks": ["task_8945_T001"],
            "coverage": 75.0,
            "created_at": now,
            "updated_at": now
        }
        self.tasks["task_8945_T001"] = {
            "task_id": "task_8945_T001",
            "claim_id": claim2_id,
            "task_type": "T001",
            "description": "ML Model Validation: NFT Pricing",
            "instructions": "Audit inference pipeline and data sanitization. Run model on test set and verify accuracy claim.",
            "parameters": {"model_url": "https://huggingface.co/..."},
            "min_validators": 2,
            "estimated_minutes": 90,
            "required_skills": ["python", "machine-learning", "tensorflow", "data-science"],
            "assigned_validators": ["0x3a1F8B92C5462BD7F9C23A7539C8801fE56a8d91"],
            "results": [],
            "status": "in_progress",
            "reward": 350,
            "created_at": now
        }
        
        # Claim 3: ZK Circuit (from marketplace.html)
        claim3_id = "claim_9012"
        self.claims[claim3_id] = {
            "claim_id": claim3_id,
            "claim_text": "ZK-Circuit for private voting produces valid Groth16 proofs with proper nullifier generation",
            "author": "0x9D5c6a2E1B34f8A67C0E9d2F5A38B91C7E64Df03",
            "status": "pending",
            "tasks": ["task_9012_T001"],
            "coverage": 90.0,
            "created_at": now,
            "updated_at": now
        }
        self.tasks["task_9012_T001"] = {
            "task_id": "task_9012_T001",
            "claim_id": claim3_id,
            "task_type": "T001",
            "description": "ZK-Circuit: Private Voting",
            "instructions": "Verify Groth16 proof correctness. Check nullifier generation prevents double voting.",
            "parameters": {"circuit_file": "vote.circom"},
            "min_validators": 3,
            "estimated_minutes": 180,
            "required_skills": ["circom", "cryptography", "zero-knowledge"],
            "assigned_validators": [],
            "results": [],
            "status": "pending",
            "reward": 750,
            "created_at": now
        }


# Global database instance (for hackathon simplicity)
db = MockDatabase()

# Initialize with demo data
db.seed_demo_data()
