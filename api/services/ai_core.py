"""
AI Core Service

Wrapper around the Verifi AI Core pipeline for the API.
Uses direct component imports to avoid relative import issues.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Add verifi root to path for src imports
verifi_root = Path(__file__).parent.parent.parent
if str(verifi_root) not in sys.path:
    sys.path.insert(0, str(verifi_root))

# Import components directly
from src.models.claim import Claim
from src.models.classification import ClassificationResult
from src.level1.claim_classifier import ClaimClassifier
from src.level2.graph_traversal import GraphTraversalEngine
from src.level3.task_expander import TaskExpander
from src.utils.llm_client import MockLLMClient


class SimplePipeline:
    """
    Simplified pipeline for API use.
    Avoids relative import issues in src/pipeline.py.
    """
    
    def __init__(self):
        self.llm = MockLLMClient()
        self.classifier = ClaimClassifier(llm_client=self.llm)
        self.traversal = GraphTraversalEngine()
        self.expander = TaskExpander(llm_client=self.llm)
    
    def process_claim(self, claim: Claim) -> Dict[str, Any]:
        # Level 1: Classify
        classification = self.classifier.classify(claim)
        
        # Level 2: Get required tasks
        required_task_ids = self.traversal.get_required_tasks(classification)
        
        # Level 3: Expand tasks
        expanded_tasks = self.expander.expand_tasks(required_task_ids, claim.text)
        
        # Calculate coverage
        coverage = self.traversal.calculate_coverage(classification, required_task_ids)
        
        return {
            "classification": classification,
            "expanded_tasks": expanded_tasks,
            "coverage": coverage,
            "warnings": []
        }


# Global pipeline instance
_pipeline = None


def get_pipeline() -> SimplePipeline:
    """Get or create the verification pipeline."""
    global _pipeline
    if _pipeline is None:
        _pipeline = SimplePipeline()
    return _pipeline


def process_claim(claim_text: str, context: str = None) -> Dict[str, Any]:
    """
    Process a claim through the AI Core.
    
    Returns a dict with:
    - classification: dimension weights, red flags, ambiguities
    - tasks: list of expanded tasks with validator requirements
    - coverage: verification coverage score
    """
    pipeline = get_pipeline()
    
    # Create claim object
    claim = Claim(text=claim_text, context=context)
    
    # Process through pipeline
    result = pipeline.process_claim(claim)
    
    # Convert to API format
    return {
        "classification": {
            "dimensions": result["classification"].dimensions,
            "red_flags": result["classification"].red_flags,
            "ambiguities": result["classification"].ambiguities
        },
        "tasks": [
            {
                "task_id": task.task_id,
                "description": task.description,
                "instructions": task.instructions,
                "parameters": task.parameters,
                "min_validators": task.min_validators,
                "estimated_minutes": task.estimated_minutes,
                "required_skills": task.required_skills
            }
            for task in result["expanded_tasks"]
        ],
        "coverage": result["coverage"],
        "warnings": result["warnings"]
    }
