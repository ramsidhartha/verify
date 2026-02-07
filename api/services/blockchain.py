"""
Blockchain Service - Mock Implementation

For hackathon demo: Simulates blockchain interactions.
Same interface as real blockchain - easy to swap later.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib


class MockBlockchain:
    """
    Mock blockchain that simulates VerifiTrust.sol contract.
    
    Real integration would use web3.py or similar.
    """
    
    def __init__(self):
        # Simulate contract state
        self.validators: Dict[str, Dict] = {}
        self.task_validations: Dict[int, List[Dict]] = {}
        self.events: List[Dict] = []
        self.block_number = 1
    
    def _emit_event(self, event_name: str, data: Dict):
        """Emit an event (for frontend to listen to)."""
        event = {
            "event": event_name,
            "data": data,
            "blockNumber": self.block_number,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.events.append(event)
        self.block_number += 1
        return event
    
    def register_validator(self, wallet: str) -> Dict:
        """
        Simulates: VerifiTrust.registerValidator()
        
        Anyone can become a validator.
        """
        if wallet in self.validators:
            raise Exception("Already registered")
        
        self.validators[wallet] = {
            "wallet": wallet,
            "reputation": 0,
            "totalTasksCompleted": 0,
            "isActive": True
        }
        
        event = self._emit_event("ValidatorRegistered", {"validator": wallet})
        
        return {
            "success": True,
            "tx_hash": f"0x{hashlib.sha256(wallet.encode()).hexdigest()[:64]}",
            "event": event
        }
    
    def submit_proof(self, wallet: str, task_id: int, evidence_hash: str, outcome: bool) -> Dict:
        """
        Simulates: VerifiTrust.submitProof()
        
        Submit verification proof and earn reputation.
        """
        if wallet not in self.validators:
            raise Exception("Not a registered validator")
        
        if not self.validators[wallet]["isActive"]:
            raise Exception("Validator is not active")
        
        # Record the proof
        if task_id not in self.task_validations:
            self.task_validations[task_id] = []
        
        verification = {
            "taskId": task_id,
            "evidenceHash": evidence_hash,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat(),
            "validator": wallet
        }
        self.task_validations[task_id].append(verification)
        
        # Update reputation (+10 for each task)
        self.validators[wallet]["reputation"] += 10
        self.validators[wallet]["totalTasksCompleted"] += 1
        
        # Emit events
        proof_event = self._emit_event("ProofSubmitted", {
            "taskId": task_id,
            "validator": wallet,
            "outcome": outcome,
            "evidenceHash": evidence_hash
        })
        
        rep_event = self._emit_event("ReputationIncreased", {
            "validator": wallet,
            "newScore": self.validators[wallet]["reputation"]
        })
        
        return {
            "success": True,
            "tx_hash": f"0x{hashlib.sha256(f'{wallet}{task_id}'.encode()).hexdigest()[:64]}",
            "events": [proof_event, rep_event],
            "new_reputation": self.validators[wallet]["reputation"]
        }
    
    def get_validations(self, task_id: int) -> List[Dict]:
        """
        Simulates: VerifiTrust.getValidations()
        
        Get all validations for a task.
        """
        return self.task_validations.get(task_id, [])
    
    def get_validator(self, wallet: str) -> Optional[Dict]:
        """Get validator info."""
        return self.validators.get(wallet)
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """Get recent blockchain events (for frontend)."""
        return self.events[-limit:][::-1]


# Global blockchain instance
blockchain = MockBlockchain()


# === API Functions (called by backend routes) ===

def register_on_chain(wallet: str) -> Dict:
    """Register validator on blockchain."""
    try:
        return blockchain.register_validator(wallet)
    except Exception as e:
        return {"success": False, "error": str(e)}


def submit_proof_on_chain(wallet: str, task_id: str, evidence_hash: str, passed: bool) -> Dict:
    """Submit verification proof to blockchain."""
    try:
        # Convert task_id string to int for contract
        task_id_int = abs(hash(task_id)) % (10**9)
        return blockchain.submit_proof(wallet, task_id_int, evidence_hash, passed)
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_blockchain_validations(task_id: str) -> List[Dict]:
    """Get validations from blockchain."""
    task_id_int = abs(hash(task_id)) % (10**9)
    return blockchain.get_validations(task_id_int)


def get_blockchain_events(limit: int = 10) -> List[Dict]:
    """Get recent blockchain events."""
    return blockchain.get_recent_events(limit)
