"""
Level 1: Claim Classification Agent

This module implements LLM #1 - the semantic understanding layer.
It classifies claims into dimensions, detects red flags, and identifies ambiguities.

CRITICAL CONSTRAINTS (per architecture spec):
- NO task names
- NO test strategies  
- NO verification instructions
- This agent is a classifier + annotator ONLY
"""

from typing import Optional, List
import json

from ..models.claim import Claim, ClaimDimension
from ..models.classification import ClassificationResult
from ..utils.llm_client import LLMClient, MockLLMClient, create_llm_client
from ..config import LLMConfig


# System prompt for the classification agent
CLASSIFIER_SYSTEM_PROMPT = """You are a Claim Classification Agent for a verification system.

Your ONLY job is to understand what a technical claim is about - NOT how to verify it.

For each claim, you must output STRICT JSON with exactly this structure:
{
  "dimensions": {
    "performance": <0.0-1.0>,
    "correctness": <0.0-1.0>,
    "security": <0.0-1.0>,
    "reproducibility": <0.0-1.0>,
    "compatibility": <0.0-1.0>,
    "documentation": <0.0-1.0>,
    "reliability": <0.0-1.0>,
    "scalability": <0.0-1.0>
  },
  "red_flags": [<list of potential concerns or warning signs>],
  "ambiguities": [<list of unclear aspects that affect verification scope>]
}

RULES:
1. Assign weights between 0.0 and 1.0 for each dimension based on claim relevance
2. Total weights do NOT need to sum to 1.0 - a claim can be 0.8 performance AND 0.7 security
3. Red flags are concerning patterns like "tested only on staging", "works on my machine"
4. Ambiguities are missing details that prevent clear verification scope

CRITICAL: You must NEVER output:
- Task names or test names
- Verification strategies or methodologies
- Testing instructions or procedures
- Recommendations on how to verify

You are a CLASSIFIER and ANNOTATOR only. Output ONLY the JSON structure above."""


# Common red flag patterns to detect
RED_FLAG_PATTERNS = [
    ("staging", "tested only on staging environment"),
    ("local", "tested only locally"),
    ("my machine", "works on my machine claim"),
    ("should work", "uncertain language used"),
    ("probably", "uncertain language used"),
    ("i think", "uncertain language used"),
    ("no tests", "no automated tests mentioned"),
    ("manual test", "only manual testing performed"),
    ("untested", "explicitly marked as untested"),
    ("prototype", "prototype or experimental code"),
    ("poc", "proof of concept code"),
    ("hack", "hacky or temporary solution"),
    ("workaround", "workaround rather than proper fix"),
]

# Ambiguity detection patterns
AMBIGUITY_PATTERNS = [
    ("api", "authentication model not specified"),
    ("auth", "authentication mechanism unclear"),
    ("database", "database type/version not specified"),
    ("scale", "scale targets not quantified"),
    ("load", "expected load not specified"),
    ("concurrent", "concurrency model not specified"),
    ("deploy", "deployment environment not specified"),
    ("cloud", "cloud provider/configuration not specified"),
]


class ClaimClassifier:
    """
    Level 1: Claim Classification Agent
    
    Responsible for semantic understanding of claims.
    Identifies claim dimensions, red flags, and ambiguities.
    
    This is LLM #1 in the 3-level architecture.
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[LLMConfig] = None):
        """
        Initialize the claim classifier.
        
        Args:
            llm_client: Pre-configured LLM client. If None, creates one from config.
            config: LLM configuration. Used only if llm_client is None.
        """
        if llm_client is not None:
            self.llm = llm_client
        elif config is not None:
            self.llm = create_llm_client(config)
        else:
            # Default to mock for testing
            self.llm = MockLLMClient()
    
    def classify(self, claim: str | Claim) -> ClassificationResult:
        """
        Classify a claim into dimensions, red flags, and ambiguities.
        
        Args:
            claim: Either a raw claim string or a Claim object
            
        Returns:
            ClassificationResult with dimensions, red_flags, and ambiguities
        """
        # Normalize input
        if isinstance(claim, str):
            claim = Claim(text=claim)
        
        # Build the classification prompt
        prompt = self._build_prompt(claim)
        
        # Get LLM classification
        try:
            result = self.llm.complete_structured(
                prompt=prompt,
                response_model=ClassificationResult,
                system_prompt=CLASSIFIER_SYSTEM_PROMPT
            )
        except ValueError as e:
            # If LLM fails, fall back to heuristic classification
            result = self._heuristic_classify(claim)
        
        # Enhance with pattern-based detection
        result = self._enhance_with_patterns(result, claim.text)
        
        return result
    
    def _build_prompt(self, claim: Claim) -> str:
        """Build the classification prompt."""
        prompt = f"Classify the following technical claim:\n\n\"{claim.text}\""
        
        if claim.context:
            prompt += f"\n\nAdditional context: {claim.context}"
        
        prompt += "\n\nOutput ONLY the JSON classification structure."
        
        return prompt
    
    def _heuristic_classify(self, claim: Claim) -> ClassificationResult:
        """
        Fallback heuristic classification when LLM fails.
        
        Uses keyword matching for basic dimension detection.
        """
        text = claim.text.lower()
        
        dimensions = {
            "performance": 0.0,
            "correctness": 0.0,
            "security": 0.0,
            "reproducibility": 0.0,
            "compatibility": 0.0,
            "documentation": 0.0,
            "reliability": 0.0,
            "scalability": 0.0,
        }
        
        # Performance keywords
        if any(kw in text for kw in ["fast", "speed", "latency", "throughput", "req/s", "requests per second", "rps", "millisecond", "response time"]):
            dimensions["performance"] = 0.7
        
        # Correctness keywords
        if any(kw in text for kw in ["correct", "accurate", "bug-free", "works", "functional", "returns", "computes"]):
            dimensions["correctness"] = 0.6
        
        # Security keywords
        if any(kw in text for kw in ["secure", "auth", "encrypt", "safe", "protect", "vulnerability", "injection", "xss"]):
            dimensions["security"] = 0.7
        
        # Reproducibility keywords
        if any(kw in text for kw in ["reproducible", "deterministic", "consistent", "repeatable"]):
            dimensions["reproducibility"] = 0.6
        
        # Compatibility keywords
        if any(kw in text for kw in ["compatible", "works with", "supports", "integrates", "cross-platform"]):
            dimensions["compatibility"] = 0.5
        
        # Documentation keywords
        if any(kw in text for kw in ["documented", "readme", "api doc", "specification"]):
            dimensions["documentation"] = 0.5
        
        # Reliability keywords
        if any(kw in text for kw in ["reliable", "stable", "uptime", "availability", "fault", "recover"]):
            dimensions["reliability"] = 0.6
        
        # Scalability keywords
        if any(kw in text for kw in ["scale", "scalable", "horizontal", "vertical", "elastic", "auto-scale"]):
            dimensions["scalability"] = 0.6
        
        return ClassificationResult(
            dimensions=dimensions,
            red_flags=[],
            ambiguities=[]
        )
    
    def _enhance_with_patterns(self, result: ClassificationResult, text: str) -> ClassificationResult:
        """
        Enhance classification with pattern-based red flag and ambiguity detection.
        
        This provides deterministic detection alongside LLM classification.
        """
        text_lower = text.lower()
        
        # Detect red flags
        detected_red_flags = set(result.red_flags)
        for pattern, flag in RED_FLAG_PATTERNS:
            if pattern in text_lower:
                detected_red_flags.add(flag)
        
        # Detect ambiguities
        detected_ambiguities = set(result.ambiguities)
        for pattern, ambiguity in AMBIGUITY_PATTERNS:
            if pattern in text_lower:
                # Only add if the claim mentions it but doesn't specify details
                detected_ambiguities.add(ambiguity)
        
        return ClassificationResult(
            dimensions=result.dimensions,
            red_flags=list(detected_red_flags),
            ambiguities=list(detected_ambiguities)
        )


def classify_claim(claim: str | Claim, llm_client: Optional[LLMClient] = None) -> ClassificationResult:
    """
    Convenience function to classify a claim.
    
    Args:
        claim: The claim text or Claim object
        llm_client: Optional LLM client
        
    Returns:
        ClassificationResult
    """
    classifier = ClaimClassifier(llm_client=llm_client)
    return classifier.classify(claim)
