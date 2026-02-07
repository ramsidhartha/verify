"""
Users Routes

Endpoints for user registration and profile management.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from ..schemas import UserProfile, UserCreate, UserUpdate
from ..services.database import db


router = APIRouter()


@router.post("/register", response_model=UserProfile)
async def register_user(user: UserCreate):
    """
    Register a new user (validator or claimer).
    
    Users can be both validators and claimers with the same wallet.
    """
    # Check if already exists
    existing = db.get_user(user.wallet)
    if existing:
        return UserProfile(**existing)
    
    # Create new user
    created = db.create_user(user.wallet, user.skills)
    return UserProfile(**created)


@router.get("/{wallet}", response_model=UserProfile)
async def get_user(wallet: str):
    """Get user profile by wallet address."""
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)


@router.patch("/{wallet}", response_model=UserProfile)
async def update_user(wallet: str, updates: UserUpdate):
    """Update user profile (add skills, etc.)."""
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {}
    if updates.skills is not None:
        update_data["skills"] = updates.skills
    
    updated = db.update_user(wallet, update_data)
    return UserProfile(**updated)


@router.post("/{wallet}/skills")
async def add_skills(wallet: str, skills: List[str]):
    """Add skills to user profile."""
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Merge skills (no duplicates)
    current_skills = set(user["skills"])
    new_skills = current_skills.union(set(skills))
    
    updated = db.update_user(wallet, {"skills": list(new_skills)})
    return {"skills": updated["skills"]}


@router.get("/{wallet}/stats")
async def get_user_stats(wallet: str):
    """Get user statistics (as claimer and validator)."""
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get claims by this user
    claims = db.get_claims_by_author(wallet)
    
    # Get tasks assigned to this user
    all_tasks = list(db.tasks.values())
    assigned_tasks = [t for t in all_tasks if wallet in t["assigned_validators"]]
    completed_tasks = [t for t in assigned_tasks if any(r["validator"] == wallet for r in t["results"])]
    
    return {
        "wallet": wallet,
        "as_claimer": {
            "total_claims": len(claims),
            "verified_claims": sum(1 for c in claims if c["status"] == "completed"),
            "pending_claims": sum(1 for c in claims if c["status"] in ["pending", "in_progress"])
        },
        "as_validator": {
            "reputation": user["reputation"],
            "skills": user["skills"],
            "assigned_tasks": len(assigned_tasks),
            "completed_tasks": len(completed_tasks),
            "pending_tasks": len(assigned_tasks) - len(completed_tasks)
        }
    }
