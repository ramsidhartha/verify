"""
API Request/Response Schemas

Pydantic models for API validation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# =============================================================================
# User/Validator Schemas
# =============================================================================

class UserProfile(BaseModel):
    """User profile (both claimers and validators)."""
    wallet: str = Field(..., description="Wallet address")
    skills: List[str] = Field(default_factory=list, description="Validator skills")
    reputation: float = Field(0.5, ge=0.0, le=1.0, description="Reputation score 0-1")
    active_tasks: List[str] = Field(default_factory=list, description="Currently assigned tasks")
    completed_tasks: int = Field(0, description="Total completed tasks")


class UserCreate(BaseModel):
    """Create a new user profile."""
    wallet: str
    skills: List[str] = []


class UserUpdate(BaseModel):
    """Update user profile."""
    skills: Optional[List[str]] = None


# =============================================================================
# Claim Schemas
# =============================================================================

class ClaimSubmit(BaseModel):
    """Submit a new claim for verification."""
    claim_text: str = Field(..., min_length=10, description="The claim to verify")
    wallet: str = Field(..., description="Claimant wallet address")
    context: Optional[str] = Field(None, description="Additional context")


class ClaimResponse(BaseModel):
    """Response after submitting a claim."""
    claim_id: str
    claim_text: str
    status: str  # "pending", "in_progress", "completed", "disputed"
    task_count: int
    coverage: float
    created_at: datetime


class ClaimStatus(BaseModel):
    """Detailed claim status with task progress."""
    claim_id: str
    claim_text: str
    status: str
    author: str
    tasks: List[Dict[str, Any]]
    completed_tasks: int
    total_tasks: int
    coverage: float
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Task Schemas
# =============================================================================

class TaskSummary(BaseModel):
    """Task summary for listing."""
    task_id: str
    claim_id: str
    task_type: str
    description: str
    min_validators: int
    estimated_minutes: int
    required_skills: List[str]
    status: str  # "open", "accepted", "completed"
    reward_estimate: str  # e.g., "0.05 ETH"


class TaskDetail(BaseModel):
    """Full task details for execution."""
    task_id: str
    claim_id: str
    task_type: str
    description: str
    instructions: str
    parameters: Dict[str, Any]
    min_validators: int
    estimated_minutes: int
    required_skills: List[str]
    assigned_validators: List[str]
    deadline: Optional[datetime]
    status: str


class TaskAccept(BaseModel):
    """Accept a task."""
    wallet: str


class TaskResult(BaseModel):
    """Submit task result."""
    wallet: str
    passed: bool
    evidence_hash: Optional[str] = None
    notes: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


class TaskResultResponse(BaseModel):
    """Response after submitting result."""
    task_id: str
    status: str  # "submitted", "consensus_reached", "disputed"
    consensus: Optional[str] = None  # "pass", "fail", "pending"
    total_submissions: int
    required_submissions: int
