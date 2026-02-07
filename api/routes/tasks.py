"""
Tasks Routes

Endpoints for validators to get, accept, and submit task results.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from ..schemas import TaskSummary, TaskDetail, TaskAccept, TaskResult, TaskResultResponse
from ..services.database import db
from ..services.matching import get_available_tasks_for_validator, check_consensus
from ..services.blockchain import submit_proof_on_chain, get_blockchain_events


router = APIRouter()


@router.get("/", response_model=List[TaskSummary])
async def get_available_tasks(wallet: str):
    """
    Get available tasks for a validator.
    
    Filters tasks based on:
    - Validator's registered skills
    - Task still needs more validators
    - Validator not already assigned
    """
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Register first.")
    
    tasks = get_available_tasks_for_validator(wallet)
    
    return [
        TaskSummary(
            task_id=t["task_id"],
            claim_id=t["claim_id"],
            task_type=t["task_type"],
            description=t["description"],
            min_validators=t["min_validators"],
            estimated_minutes=t["estimated_minutes"],
            required_skills=t["required_skills"],
            status=t["status"],
            reward_estimate="0.05 ETH"  # Placeholder
        )
        for t in tasks
    ]


@router.get("/{task_id}", response_model=TaskDetail)
async def get_task_detail(task_id: str):
    """Get full task details for execution."""
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskDetail(
        task_id=task["task_id"],
        claim_id=task["claim_id"],
        task_type=task["task_type"],
        description=task["description"],
        instructions=task["instructions"],
        parameters=task["parameters"],
        min_validators=task["min_validators"],
        estimated_minutes=task["estimated_minutes"],
        required_skills=task["required_skills"],
        assigned_validators=task["assigned_validators"],
        deadline=None,  # TODO: Calculate based on accept time
        status=task["status"]
    )


@router.post("/{task_id}/accept")
async def accept_task(task_id: str, accept: TaskAccept):
    """
    Accept a task as a validator.
    
    This assigns the validator to the task.
    """
    # Verify user exists
    user = db.get_user(accept.wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get task
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if task is still open
    if len(task["assigned_validators"]) >= task["min_validators"]:
        raise HTTPException(status_code=400, detail="Task already has enough validators")
    
    # Check if already assigned
    if accept.wallet in task["assigned_validators"]:
        raise HTTPException(status_code=400, detail="Already assigned to this task")
    
    # Assign
    updated_task = db.assign_task(task_id, accept.wallet)
    
    return {
        "status": "accepted",
        "task_id": task_id,
        "message": "Task accepted. Complete within 24 hours.",
        "validators_assigned": len(updated_task["assigned_validators"]),
        "validators_needed": updated_task["min_validators"]
    }


@router.post("/{task_id}/submit", response_model=TaskResultResponse)
async def submit_result(task_id: str, result: TaskResult):
    """
    Submit task verification result.
    
    Validator reports whether the claim passed/failed for this task.
    """
    # Verify user
    user = db.get_user(result.wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get task
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify validator is assigned
    if result.wallet not in task["assigned_validators"]:
        raise HTTPException(status_code=403, detail="You are not assigned to this task")
    
    # Check if already submitted
    existing = [r for r in task["results"] if r["validator"] == result.wallet]
    if existing:
        raise HTTPException(status_code=400, detail="Already submitted result")
    
    # Submit result
    updated_task = db.submit_result(task_id, result.wallet, result.passed, result.evidence_hash)
    
    # Check consensus
    consensus = check_consensus(task_id)
    
    # Submit to blockchain (always, for proof trail)
    blockchain_result = submit_proof_on_chain(
        wallet=result.wallet,
        task_id=task_id,
        evidence_hash=result.evidence_hash or "no_evidence",
        passed=result.passed
    )
    
    return TaskResultResponse(
        task_id=task_id,
        status="submitted",
        consensus=consensus,
        total_submissions=len(updated_task["results"]),
        required_submissions=updated_task["min_validators"]
    )


@router.get("/my-tasks/{wallet}")
async def get_my_tasks(wallet: str):
    """Get tasks assigned to a validator."""
    user = db.get_user(wallet)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all tasks where this user is assigned
    all_tasks = [db.get_task(tid) for tid in db.tasks.keys()]
    my_tasks = [t for t in all_tasks if t and wallet in t["assigned_validators"]]
    
    return {"tasks": my_tasks}
