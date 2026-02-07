"""
Claim data models for Verifi.
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ClaimDimension(str, Enum):
    """
    Verification dimensions that a claim can be classified into.
    These are the semantic categories that determine which verification tasks apply.
    """
    PERFORMANCE = "performance"
    CORRECTNESS = "correctness"
    SECURITY = "security"
    REPRODUCIBILITY = "reproducibility"
    COMPATIBILITY = "compatibility"
    DOCUMENTATION = "documentation"
    RELIABILITY = "reliability"
    SCALABILITY = "scalability"


class Claim(BaseModel):
    """
    A technical claim submitted for verification.
    
    Attributes:
        text: Raw natural-language claim text
        context: Optional additional context (e.g., project description)
        metadata: Optional metadata (e.g., submitter info, timestamps)
    """
    text: str = Field(..., description="Raw natural-language claim text")
    context: Optional[str] = Field(None, description="Additional context about the claim")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "My API can handle 2000 requests per second with low latency.",
                "context": "REST API built with FastAPI, deployed on AWS",
                "metadata": {"submitter_id": "dev_123", "project": "payment-api"}
            }
        }
