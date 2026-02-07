"""
Level 3: Task Expansion Agent

This module implements LLM #2 - the contextualization layer.
It converts abstract task identifiers into claim-specific executable instructions.

CRITICAL CONSTRAINTS (per architecture spec):
- CANNOT add or remove tasks (task list is fixed from Level 2)
- CANNOT alter verification scope
- CAN ONLY fill parameters and execution details

This layer provides flexibility and human-readable instructions
without letting creativity alter verification correctness.
"""

from typing import List, Optional, Dict, Any
import json

from ..models.claim import Claim
from ..models.task import ExpandedTask
from ..level2.task_graph import VERIFICATION_TASK_GRAPH, TaskGraphNode
from ..utils.llm_client import LLMClient, MockLLMClient, create_llm_client
from ..config import LLMConfig


# System prompt for the task expansion agent
EXPANDER_SYSTEM_PROMPT = """You are a Task Expansion Agent for a verification system.

You receive a verification task identifier and a claim. Your job is to fill in
claim-specific parameters that make the task executable.

For each task, output STRICT JSON with this structure:
{
  "parameters": {
    "<param_name>": <value>,
    ...
  },
  "instructions": "<human-readable execution instructions>"
}

RULES:
1. Extract specific values from the claim (numbers, thresholds, targets)
2. Fill in reasonable defaults for unspecified parameters
3. Make instructions clear and actionable
4. Keep parameters measurable and verifiable

CRITICAL CONSTRAINTS:
- You CANNOT add new tasks
- You CANNOT remove tasks
- You CANNOT change the verification scope
- You can ONLY contextualize the given task

Output ONLY the JSON structure above."""


# Default parameter templates for each task type
# These provide structure for LLM expansion
TASK_PARAMETER_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "baseline_correctness_check": {
        "test_cases": "standard",
        "coverage_threshold": 0.8,
        "timeout_seconds": 300,
    },
    "input_validation_test": {
        "boundary_types": ["min", "max", "empty", "null", "overflow"],
        "fuzz_iterations": 100,
    },
    "throughput_benchmark": {
        "target_rps": None,  # Must be extracted from claim
        "duration_minutes": 5,
        "warmup_seconds": 30,
        "acceptable_error_rate": 0.01,
    },
    "latency_profile": {
        "percentiles": ["p50", "p95", "p99"],
        "sample_size": 1000,
        "target_p99_ms": None,
    },
    "sustained_load_test": {
        "duration_minutes": 30,
        "target_rps": None,
        "stability_threshold": 0.95,
    },
    "auth_boundary_test": {
        "auth_types": ["unauthenticated", "invalid_token", "expired_token"],
        "expected_behavior": "reject",
    },
    "rate_limiting_test": {
        "burst_size": 100,
        "sustained_rate": 50,
        "expected_limit": None,
    },
    "injection_vulnerability_scan": {
        "injection_types": ["sql", "xss", "command"],
        "payloads_per_type": 50,
    },
    "concurrent_user_test": {
        "concurrent_users": 100,
        "session_duration_seconds": 60,
        "ramp_up_seconds": 30,
    },
}


class TaskExpander:
    """
    Level 3: Task Expansion Agent
    
    Converts abstract task identifiers into claim-specific executable instructions.
    
    This is LLM #2 in the 3-level architecture.
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[LLMConfig] = None):
        """
        Initialize the task expander.
        
        Args:
            llm_client: Pre-configured LLM client. If None, creates one from config.
            config: LLM configuration. Used only if llm_client is None.
        """
        if llm_client is not None:
            self.llm = llm_client
        elif config is not None:
            self.llm = create_llm_client(config)
        else:
            self.llm = MockLLMClient()
    
    def expand_tasks(
        self, 
        task_ids: List[str], 
        claim: str | Claim,
        clarifications: Optional[Dict[str, str]] = None
    ) -> List[ExpandedTask]:
        """
        Expand a list of task IDs into executable task specifications.
        
        Args:
            task_ids: Canonical task identifiers from Level 2
            claim: Original claim text or Claim object
            clarifications: Optional answers to ambiguity questions
            
        Returns:
            List of ExpandedTask with filled parameters
        """
        # Normalize claim
        claim_text = claim.text if isinstance(claim, Claim) else claim
        
        expanded_tasks = []
        for task_id in task_ids:
            task_node = VERIFICATION_TASK_GRAPH.get(task_id)
            if task_node is None:
                # Skip unknown tasks (shouldn't happen in normal flow)
                continue
            
            expanded = self._expand_single_task(task_id, task_node, claim_text, clarifications)
            expanded_tasks.append(expanded)
        
        return expanded_tasks
    
    def _expand_single_task(
        self,
        task_id: str,
        task_node: TaskGraphNode,
        claim_text: str,
        clarifications: Optional[Dict[str, str]] = None
    ) -> ExpandedTask:
        """Expand a single task with claim-specific parameters."""
        
        # Get template defaults
        template = TASK_PARAMETER_TEMPLATES.get(task_id, {})
        
        # Always run heuristic extraction first
        heuristic_data = self._heuristic_expand(task_id, claim_text, template)
        
        # Build expansion prompt
        prompt = self._build_expansion_prompt(task_id, task_node, claim_text, template, clarifications)
        
        # Get LLM expansion
        try:
            response = self.llm.complete(prompt, EXPANDER_SYSTEM_PROMPT)
            llm_data = self._parse_expansion_response(response)
        except (ValueError, json.JSONDecodeError):
            llm_data = {"parameters": {}, "instructions": None}
        
        # Merge: template -> LLM -> heuristic (heuristic wins for extracted values)
        parameters = {**template}
        parameters.update(llm_data.get("parameters", {}))
        # Heuristic extracted values override LLM defaults (only for non-None values)
        for key, value in heuristic_data.get("parameters", {}).items():
            if value is not None:
                parameters[key] = value
        
        instructions = llm_data.get("instructions") or heuristic_data.get("instructions", f"Execute {task_id} verification")
        
        return ExpandedTask(
            task_id=task_id,
            description=task_node.description,
            parameters=parameters,
            instructions=instructions,
            min_validators=task_node.min_validators,
            estimated_minutes=task_node.estimated_minutes,
            required_skills=task_node.required_skills or list(task_node.dimensions),
        )
    
    def _build_expansion_prompt(
        self,
        task_id: str,
        task_node: TaskGraphNode,
        claim_text: str,
        template: Dict[str, Any],
        clarifications: Optional[Dict[str, str]] = None
    ) -> str:
        """Build the expansion prompt for a task."""
        prompt = f"""Task to expand: {task_id}
Task description: {task_node.description}

Original claim: "{claim_text}"

Parameter template (fill in None values from claim, adjust others as needed):
{json.dumps(template, indent=2)}
"""
        
        if clarifications:
            prompt += f"\nClarifications provided:\n{json.dumps(clarifications, indent=2)}"
        
        prompt += "\n\nOutput the JSON with filled parameters and instructions."
        
        return prompt
    
    def _parse_expansion_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM expansion response."""
        # Handle markdown code blocks
        if "```json" in response:
            json_start = response.index("```json") + 7
            json_end = response.index("```", json_start)
            response = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.index("```") + 3
            json_end = response.index("```", json_start)
            response = response[json_start:json_end].strip()
        
        return json.loads(response)
    
    def _heuristic_expand(
        self,
        task_id: str,
        claim_text: str,
        template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback heuristic expansion when LLM fails.
        
        Extracts common patterns from claim text.
        """
        parameters = dict(template)
        
        # Extract numeric targets from claim
        import re
        
        # Look for RPS/throughput values
        rps_match = re.search(r'(\d+(?:,\d+)?)\s*(?:req(?:uest)?s?/?s(?:ec(?:ond)?)?|rps)', claim_text.lower())
        if rps_match:
            rps_value = int(rps_match.group(1).replace(',', ''))
            if "target_rps" in parameters:
                parameters["target_rps"] = rps_value
        
        # Look for latency values
        latency_match = re.search(r'(\d+)\s*(?:ms|millisecond)', claim_text.lower())
        if latency_match:
            latency_value = int(latency_match.group(1))
            if "target_p99_ms" in parameters:
                parameters["target_p99_ms"] = latency_value
        
        # Look for percentage values
        percent_match = re.search(r'(\d+(?:\.\d+)?)\s*%', claim_text)
        if percent_match:
            percent_value = float(percent_match.group(1)) / 100
            if "acceptable_error_rate" in parameters:
                parameters["acceptable_error_rate"] = percent_value
        
        # Look for duration values
        duration_match = re.search(r'(\d+)\s*(?:minute|min|hour|hr)', claim_text.lower())
        if duration_match:
            duration_value = int(duration_match.group(1))
            if "duration_minutes" in parameters:
                if "hour" in claim_text.lower() or "hr" in claim_text.lower():
                    duration_value *= 60
                parameters["duration_minutes"] = duration_value
        
        # Generate basic instructions
        instructions = f"Execute {task_id} verification against the system under test."
        
        return {
            "parameters": parameters,
            "instructions": instructions
        }


def expand_tasks(
    task_ids: List[str],
    claim: str | Claim,
    llm_client: Optional[LLMClient] = None,
    clarifications: Optional[Dict[str, str]] = None
) -> List[ExpandedTask]:
    """
    Convenience function to expand tasks.
    
    Args:
        task_ids: Canonical task identifiers from Level 2
        claim: Original claim text or Claim object
        llm_client: Optional LLM client
        clarifications: Optional answers to ambiguity questions
        
    Returns:
        List of ExpandedTask with filled parameters
    """
    expander = TaskExpander(llm_client=llm_client)
    return expander.expand_tasks(task_ids, claim, clarifications)
