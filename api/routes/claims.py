"""
Claims Routes

Endpoints for submitting and tracking claims.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..schemas import ClaimSubmit, ClaimResponse, ClaimStatus
from ..services.database import db
from ..services.ai_core import process_claim


router = APIRouter()


@router.post("/", response_model=ClaimResponse)
async def submit_claim(claim: ClaimSubmit):
    """
    Submit a new claim for verification.
    
    This endpoint:
    1. Processes the claim through the AI Core
    2. Creates tasks for validators
    3. Returns the claim ID and task summary
    """
    # Ensure user exists
    if not db.get_user(claim.wallet):
        db.create_user(claim.wallet)
    
    # Process through AI Core
    result = process_claim(claim.claim_text, claim.context)
    
    # Store in database
    claim_record = db.create_claim(
        claim_text=claim.claim_text,
        author=claim.wallet,
        tasks=result["tasks"],
        coverage=result["coverage"]
    )
    
    return ClaimResponse(
        claim_id=claim_record["claim_id"],
        claim_text=claim.claim_text,
        status="pending",
        task_count=len(result["tasks"]),
        coverage=result["coverage"],
        created_at=datetime.fromisoformat(claim_record["created_at"])
    )


@router.get("/{claim_id}", response_model=ClaimStatus)
async def get_claim_status(claim_id: str):
    """
    Get real-time status of a claim.
    
    Returns task progress and overall status.
    """
    claim = db.get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    # Get tasks for this claim
    tasks = db.get_claim_tasks(claim_id)
    
    # Count completed
    completed = sum(1 for t in tasks if t["status"] == "completed")
    
    # Build task summaries
    task_summaries = [
        {
            "task_id": t["task_id"],
            "task_type": t["task_type"],
            "status": t["status"],
            "validators_assigned": len(t["assigned_validators"]),
            "results_submitted": len(t["results"]),
            "consensus": t.get("consensus")
        }
        for t in tasks
    ]
    
    return ClaimStatus(
        claim_id=claim["claim_id"],
        claim_text=claim["claim_text"],
        status=claim["status"],
        author=claim["author"],
        tasks=task_summaries,
        completed_tasks=completed,
        total_tasks=len(tasks),
        coverage=claim["coverage"],
        created_at=datetime.fromisoformat(claim["created_at"]),
        updated_at=datetime.fromisoformat(claim["updated_at"])
    )


@router.get("/by-wallet/{wallet}")
async def get_claims_by_wallet(wallet: str):
    """Get all claims submitted by a wallet."""
    claims = db.get_claims_by_author(wallet)
    return {"claims": claims}
