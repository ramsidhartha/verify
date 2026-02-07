"""
Task-related models for Level 2 and Level 3.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from .classification import ClassificationResult


class TaskNode(BaseModel):
    """
    A node in the verification task graph.
    
    This represents a verification primitive that can be executed.
    Part of the static, versioned verification ontology.
    """
    id: str = Field(..., description="Unique task identifier")
    description: str = Field(..., description="Human-readable task description")
    dimensions: List[str] = Field(..., description="Dimensions this task verifies")
    dependencies: List[str] = Field(default_factory=list, description="Task IDs that must complete first")
    mandatory: bool = Field(False, description="Whether this task is always required")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "throughput_benchmark",
                "description": "Measure sustained request throughput",
                "dimensions": ["performance"],
                "dependencies": ["baseline_correctness_check"],
                "mandatory": False
            }
        }


class ExpandedTask(BaseModel):
    """
    A task with filled parameters from Level 3 (Task Expansion Agent).
    
    This is a contextualized version of a TaskNode with claim-specific parameters.
    """
    task_id: str = Field(..., description="Canonical task identifier")
    description: str = Field(..., description="Task description")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Claim-specific parameters for execution"
    )
    instructions: Optional[str] = Field(None, description="Human-readable execution instructions")
    # NEW: Validator requirements (from Level 2 task graph)
    min_validators: int = Field(2, description="Minimum validators needed for consensus")
    estimated_minutes: int = Field(30, description="Estimated time to complete task")
    required_skills: List[str] = Field(default_factory=list, description="Skills needed to validate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "throughput_benchmark",
                "description": "Measure sustained request throughput",
                "parameters": {
                    "target_rps": 2000,
                    "duration_minutes": 10,
                    "acceptable_error_rate": "≤1%",
                    "environment": "production-like"
                },
                "instructions": "Run load test targeting 2000 req/s for 10 minutes...",
                "min_validators": 2,
                "estimated_minutes": 30,
                "required_skills": ["performance", "load_testing"]
            }
        }


class VerificationPlan(BaseModel):
    """
    Complete verification plan output from the pipeline.
    
    Contains the original claim, classification, required tasks, and coverage metrics.
    """
    original_claim: str = Field(..., description="Original claim text")
    classification: ClassificationResult = Field(..., description="Level 1 classification output")
    required_task_ids: List[str] = Field(..., description="Ordered list of required task IDs")
    expanded_tasks: List[ExpandedTask] = Field(..., description="Tasks with filled parameters")
    coverage: float = Field(..., ge=0.0, le=1.0, description="Verification coverage score")
    warnings: List[str] = Field(default_factory=list, description="Any warnings or notes")
    
    def get_task_count(self) -> int:
        """Return the number of tasks in the plan."""
        return len(self.expanded_tasks)
    
    def has_warnings(self) -> bool:
        """Check if the plan has any warnings."""
        return len(self.warnings) > 0
