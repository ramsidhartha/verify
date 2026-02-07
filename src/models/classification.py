"""
Classification output models for Level 1 (Claim Classification Agent).
"""

from typing import Dict, List
from pydantic import BaseModel, Field, field_validator


class ClassificationResult(BaseModel):
    """
    Output from Level 1: Claim Classification Agent.
    
    Contains semantic understanding of the claim without any verification logic.
    This is the ONLY output from the LLM classification step.
    
    Attributes:
        dimensions: Mapping of dimension names to weights (0.0 to 1.0)
        red_flags: List of potential issues or concerns detected
        ambiguities: List of unclear aspects that may affect verification scope
    """
    dimensions: Dict[str, float] = Field(
        ..., 
        description="Mapping of claim dimensions to their weights (0.0 to 1.0)"
    )
    red_flags: List[str] = Field(
        default_factory=list,
        description="Potential issues or concerns detected in the claim"
    )
    ambiguities: List[str] = Field(
        default_factory=list,
        description="Unclear aspects that may affect verification scope"
    )
    
    @field_validator('dimensions')
    @classmethod
    def validate_dimensions(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Ensure all dimension weights are between 0 and 1."""
        for dim, weight in v.items():
            if not 0.0 <= weight <= 1.0:
                raise ValueError(f"Dimension weight for '{dim}' must be between 0.0 and 1.0, got {weight}")
        return v
    
    def get_active_dimensions(self, threshold: float = 0.2) -> List[str]:
        """Return dimensions with weight above threshold."""
        return [dim for dim, weight in self.dimensions.items() if weight >= threshold]
    
    def has_ambiguities(self) -> bool:
        """Check if there are unresolved ambiguities."""
        return len(self.ambiguities) > 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "dimensions": {
                    "performance": 0.75,
                    "correctness": 0.2,
                    "security": 0.05
                },
                "red_flags": ["tested only on staging"],
                "ambiguities": ["authentication model not specified"]
            }
        }
