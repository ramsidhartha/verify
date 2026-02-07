"""
Validator Matching Service

Matches tasks to validators based on skills and reputation,
with weighted randomness to prevent collusion.
"""

import random
from typing import List, Dict, Optional

from .database import db


def select_validators(
    task_id: str,
    required_skills: List[str],
    min_validators: int,
    exclude_wallet: str = None,
    min_reputation: float = 0.6
) -> List[Dict]:
    """
    Select validators for a task using weighted random selection.
    
    Algorithm:
    1. Filter by required skills (must have at least one)
    2. Filter by minimum reputation
    3. Exclude claim author
    4. Weighted random selection (higher reputation = higher chance)
    
    Returns list of selected validator profiles.
    """
    # Get qualified validators from database
    qualified = db.get_qualified_validators(required_skills, min_reputation)
    
    # Exclude claim author
    if exclude_wallet:
        qualified = [v for v in qualified if v["wallet"] != exclude_wallet]
    
    # If not enough validators, lower threshold or return what we have
    if len(qualified) < min_validators:
        # For hackathon: just return all qualified
        return qualified
    
    # Weighted random selection
    # Weight = reputation score (0.6 to 1.0 range)
    weights = [v["reputation"] for v in qualified]
    
    # Select without replacement
    selected = []
    remaining = list(qualified)
    remaining_weights = list(weights)
    
    for _ in range(min_validators):
        if not remaining:
            break
        
        # Weighted random choice
        total = sum(remaining_weights)
        r = random.random() * total
        cumulative = 0
        for i, (validator, weight) in enumerate(zip(remaining, remaining_weights)):
            cumulative += weight
            if cumulative >= r:
                selected.append(validator)
                remaining.pop(i)
                remaining_weights.pop(i)
                break
    
    return selected


def get_available_tasks_for_validator(wallet: str) -> List[Dict]:
    """
    Get tasks that a validator can work on.
    
    Filters:
    - Task is open (not enough validators yet)
    - Validator has required skills
    - Validator not already assigned
    - Validator is not the claim author
    """
    user = db.get_user(wallet)
    if not user:
        return []
    
    return db.get_tasks_for_validator(wallet, user["skills"])


def check_consensus(task_id: str) -> Optional[str]:
    """
    Check if task has reached consensus.
    
    Returns: "pass", "fail", or None if pending
    """
    task = db.get_task(task_id)
    if not task:
        return None
    
    results = task.get("results", [])
    min_validators = task.get("min_validators", 2)
    
    if len(results) < min_validators:
        return None  # Not enough votes yet
    
    passes = sum(1 for r in results if r["passed"])
    return "pass" if passes > len(results) / 2 else "fail"
