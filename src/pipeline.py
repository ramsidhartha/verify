"""
Verifi AI Reasoning Core Pipeline

End-to-end orchestration of the 3-level architecture:
1. Level 1: Claim Classification Agent (LLM #1 - semantic understanding)
2. Level 2: Task Graph Traversal Engine (deterministic rules)
3. Level 3: Task Expansion Agent (LLM #2 - contextualization)

This pipeline enforces the architectural separation of concerns:
- LLMs handle understanding and contextualization
- Rules handle verification logic
- Neither can override the other
"""

from typing import Optional, Dict, List
from dataclasses import dataclass

from .models.claim import Claim
from .models.classification import ClassificationResult
from .models.task import ExpandedTask, VerificationPlan
from .level1.claim_classifier import ClaimClassifier
from .level2.graph_traversal import GraphTraversalEngine
from .level3.task_expander import TaskExpander
from .utils.llm_client import LLMClient, MockLLMClient
from .config import LLMConfig, GraphConfig


@dataclass
class PipelineConfig:
    """Configuration for the verification pipeline."""
    llm_config: Optional[LLMConfig] = None
    graph_config: Optional[GraphConfig] = None
    use_mock_llm: bool = True  # Default to mock for safe testing


class VerificationPipeline:
    """
    End-to-end verification pipeline.
    
    Orchestrates the 3-level architecture to convert claims into
    executable verification plans.
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Pipeline configuration
        """
        self.config = config or PipelineConfig()
        
        # Initialize LLM client
        if self.config.use_mock_llm:
            self._llm = MockLLMClient()
        elif self.config.llm_config:
            from .utils.llm_client import create_llm_client
            self._llm = create_llm_client(self.config.llm_config)
        else:
            self._llm = MockLLMClient()
        
        # Initialize components
        self._classifier = ClaimClassifier(llm_client=self._llm)
        self._graph_engine = GraphTraversalEngine(config=self.config.graph_config)
        self._expander = TaskExpander(llm_client=self._llm)
    
    def process_claim(
        self,
        claim: str | Claim,
        clarifications: Optional[Dict[str, str]] = None
    ) -> VerificationPlan:
        """
        Process a claim through the full verification pipeline.
        
        Pipeline stages:
        1. Level 1: Classify the claim (LLM)
        2. Level 2: Determine required tasks (deterministic)
        3. Level 3: Expand tasks with parameters (LLM)
        
        Args:
            claim: The claim to verify (text or Claim object)
            clarifications: Optional answers to ambiguity questions
            
        Returns:
            VerificationPlan with complete verification specification
        """
        # Normalize input
        if isinstance(claim, str):
            claim_obj = Claim(text=claim)
        else:
            claim_obj = claim
        
        # Stage 1: Classification (Level 1 - LLM)
        classification = self._classifier.classify(claim_obj)
        
        # Check for blocking ambiguities
        warnings = []
        if classification.has_ambiguities() and not clarifications:
            warnings.append(
                f"Unresolved ambiguities may affect verification scope: "
                f"{', '.join(classification.ambiguities)}"
            )
        
        # Add red flags as warnings
        if classification.red_flags:
            warnings.extend([f"Red flag: {flag}" for flag in classification.red_flags])
        
        # Stage 2: Task Selection (Level 2 - Deterministic)
        required_task_ids = self._graph_engine.get_required_tasks(classification)
        
        # Stage 3: Task Expansion (Level 3 - LLM)
        expanded_tasks = self._expander.expand_tasks(
            required_task_ids, 
            claim_obj.text,
            clarifications
        )
        
        # Calculate coverage (assuming all required tasks will be executed)
        coverage = self._graph_engine.calculate_coverage(
            required_task_ids, 
            required_task_ids
        )
        
        return VerificationPlan(
            original_claim=claim_obj.text,
            classification=classification,
            required_task_ids=required_task_ids,
            expanded_tasks=expanded_tasks,
            coverage=coverage,
            warnings=warnings
        )
    
    def get_clarifying_questions(self, claim: str | Claim) -> List[str]:
        """
        Get clarifying questions for ambiguities in a claim.
        
        This is for active learning when ambiguities block verification.
        
        Args:
            claim: The claim to analyze
            
        Returns:
            List of clarifying questions
        """
        # Normalize input
        if isinstance(claim, str):
            claim_obj = Claim(text=claim)
        else:
            claim_obj = claim
        
        classification = self._classifier.classify(claim_obj)
        
        questions = []
        for ambiguity in classification.ambiguities:
            # Convert ambiguities into questions
            if "authentication" in ambiguity.lower():
                questions.append("Is the API authenticated or public? What authentication mechanism is used?")
            elif "environment" in ambiguity.lower() or "deploy" in ambiguity.lower():
                questions.append("What is the target deployment environment?")
            elif "database" in ambiguity.lower():
                questions.append("What database type and version is being used?")
            elif "scale" in ambiguity.lower() or "load" in ambiguity.lower():
                questions.append("What is the expected user load and scale requirements?")
            else:
                questions.append(f"Please clarify: {ambiguity}")
        
        return questions
    
    def explain(self, claim: str | Claim) -> Dict[str, List[str]]:
        """
        Get an explanation of why each task was selected.
        
        Useful for auditing and debugging.
        
        Args:
            claim: The claim to analyze
            
        Returns:
            Mapping of task_id -> list of selection reasons
        """
        if isinstance(claim, str):
            claim_obj = Claim(text=claim)
        else:
            claim_obj = claim
        
        classification = self._classifier.classify(claim_obj)
        return self._graph_engine.explain_selection(classification)


def process_claim(
    claim: str | Claim,
    config: Optional[PipelineConfig] = None,
    clarifications: Optional[Dict[str, str]] = None
) -> VerificationPlan:
    """
    Convenience function to process a claim.
    
    Args:
        claim: The claim to verify
        config: Optional pipeline configuration
        clarifications: Optional answers to ambiguity questions
        
    Returns:
        VerificationPlan with complete verification specification
    """
    pipeline = VerificationPipeline(config)
    return pipeline.process_claim(claim, clarifications)
