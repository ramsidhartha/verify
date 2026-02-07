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


# Global database instance (for hackathon simplicity)
db = MockDatabase()
