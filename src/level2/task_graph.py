"""
Level 2: Verification Task Graph Definition

This module defines the STATIC, VERSIONED verification ontology as a DAG.
This is infrastructure code - NOT an LLM component.

CRITICAL CONSTRAINTS:
- Graph is STATIC and VERSIONED
- Graph is AUDITABLE (can be inspected, diffed, reviewed)
- Graph NEVER changes at runtime
- All verification logic is encoded HERE, not in LLMs

Graph Structure:
- Nodes = verification primitives (specific tests/checks)
- Edges = dependencies ("A must pass before B is meaningful")
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


# Current graph version - bump this when modifying the graph
GRAPH_VERSION = "2.0.0"  # Bumped: added validator requirements


@dataclass
class TaskGraphNode:
    """A node in the verification task graph."""
    id: str
    description: str
    dimensions: List[str]
    dependencies: List[str]
    mandatory: bool = False
    risk_weight: float = 1.0  # Higher = more important for coverage
    # NEW: Validator requirements
    min_validators: int = 2  # Minimum validators needed for consensus
    estimated_minutes: int = 30  # Estimated time to complete task
    required_skills: List[str] = None  # Skills needed (defaults to dimensions)
    
    def __post_init__(self):
        # Default required_skills to dimensions if not specified
        if self.required_skills is None:
            self.required_skills = list(self.dimensions)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "dimensions": self.dimensions,
            "dependencies": self.dependencies,
            "mandatory": self.mandatory,
            "risk_weight": self.risk_weight,
            "min_validators": self.min_validators,
            "estimated_minutes": self.estimated_minutes,
            "required_skills": self.required_skills,
        }


# =============================================================================
# VERIFICATION TASK GRAPH - The Core Ontology
# =============================================================================
# 
# This graph defines ALL possible verification tasks and their relationships.
# It is the source of truth for what verification means in Verifi.
#
# Modification Policy:
# 1. Any change to this graph requires code review
# 2. Version must be bumped on any change
# 3. Backward compatibility should be maintained where possible
# 4. New nodes should be added, not modify existing node semantics
# =============================================================================

VERIFICATION_TASK_GRAPH: Dict[str, TaskGraphNode] = {
    
    # =========================================================================
    # CORRECTNESS DIMENSION - Foundation of All Verification
    # =========================================================================
    
    "baseline_correctness_check": TaskGraphNode(
        id="baseline_correctness_check",
        description="Verify basic functional correctness - the system does what it claims",
        dimensions=["correctness"],
        dependencies=[],
        mandatory=True,  # ALWAYS required - foundation of verification
        risk_weight=2.0,
        min_validators=3,  # Critical task - need consensus
        estimated_minutes=45,
        required_skills=["testing", "correctness"],
    ),
    
    "input_validation_test": TaskGraphNode(
        id="input_validation_test",
        description="Test input boundary conditions and edge cases",
        dimensions=["correctness", "security"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    "output_format_validation": TaskGraphNode(
        id="output_format_validation",
        description="Verify output format matches specification",
        dimensions=["correctness", "compatibility"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.2,
    ),
    
    "error_handling_test": TaskGraphNode(
        id="error_handling_test",
        description="Test error conditions and exception handling",
        dimensions=["correctness", "reliability"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    # =========================================================================
    # PERFORMANCE DIMENSION
    # =========================================================================
    
    "throughput_benchmark": TaskGraphNode(
        id="throughput_benchmark",
        description="Measure sustained request throughput (requests per second)",
        dimensions=["performance"],
        dependencies=["baseline_correctness_check"],  # Must be correct first
        risk_weight=1.5,
        min_validators=2,
        estimated_minutes=30,
        required_skills=["performance", "load_testing"],
    ),
    
    "latency_profile": TaskGraphNode(
        id="latency_profile",
        description="Measure response time distribution (p50, p95, p99)",
        dimensions=["performance"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    "sustained_load_test": TaskGraphNode(
        id="sustained_load_test",
        description="Extended duration load testing for stability",
        dimensions=["performance", "reliability"],
        dependencies=["throughput_benchmark", "latency_profile"],  # Need baseline first
        risk_weight=1.8,
    ),
    
    "resource_utilization_profile": TaskGraphNode(
        id="resource_utilization_profile",
        description="Measure CPU, memory, and I/O usage under load",
        dimensions=["performance", "scalability"],
        dependencies=["throughput_benchmark"],
        risk_weight=1.3,
    ),
    
    "cold_start_test": TaskGraphNode(
        id="cold_start_test",
        description="Measure initialization and warm-up time",
        dimensions=["performance"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.0,
    ),
    
    # =========================================================================
    # SECURITY DIMENSION
    # =========================================================================
    
    "auth_boundary_test": TaskGraphNode(
        id="auth_boundary_test",
        description="Verify authentication boundaries are enforced",
        dimensions=["security"],
        dependencies=["baseline_correctness_check"],
        risk_weight=2.0,
        min_validators=3,  # Security critical
        estimated_minutes=60,
        required_skills=["security", "auth"],
    ),
    
    "authorization_test": TaskGraphNode(
        id="authorization_test",
        description="Verify authorization rules are correctly enforced",
        dimensions=["security"],
        dependencies=["auth_boundary_test"],
        risk_weight=2.0,
    ),
    
    "rate_limiting_test": TaskGraphNode(
        id="rate_limiting_test",
        description="Verify rate limiting behavior under abuse",
        dimensions=["security", "performance"],
        dependencies=["auth_boundary_test"],
        risk_weight=1.5,
    ),
    
    "injection_vulnerability_scan": TaskGraphNode(
        id="injection_vulnerability_scan",
        description="Test for SQL, command, and other injection vulnerabilities",
        dimensions=["security"],
        dependencies=["input_validation_test"],
        risk_weight=2.5,
        min_validators=3,  # High risk - security critical
        estimated_minutes=90,
        required_skills=["security", "penetration_testing"],
    ),
    
    "data_exposure_test": TaskGraphNode(
        id="data_exposure_test",
        description="Check for unintended data exposure in responses",
        dimensions=["security"],
        dependencies=["baseline_correctness_check"],
        risk_weight=2.0,
    ),
    
    "encryption_verification": TaskGraphNode(
        id="encryption_verification",
        description="Verify data encryption at rest and in transit",
        dimensions=["security"],
        dependencies=["baseline_correctness_check"],
        risk_weight=2.0,
    ),
    
    # =========================================================================
    # RELIABILITY DIMENSION
    # =========================================================================
    
    "failure_recovery_test": TaskGraphNode(
        id="failure_recovery_test",
        description="Test behavior after failures and recovery",
        dimensions=["reliability"],
        dependencies=["error_handling_test"],
        risk_weight=1.8,
    ),
    
    "graceful_degradation_test": TaskGraphNode(
        id="graceful_degradation_test",
        description="Verify system degrades gracefully under stress",
        dimensions=["reliability", "performance"],
        dependencies=["sustained_load_test"],
        risk_weight=1.5,
    ),
    
    "idempotency_test": TaskGraphNode(
        id="idempotency_test",
        description="Verify operations are safely repeatable",
        dimensions=["reliability", "correctness"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    "timeout_handling_test": TaskGraphNode(
        id="timeout_handling_test",
        description="Test timeout scenarios and handling",
        dimensions=["reliability"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.3,
    ),
    
    # =========================================================================
    # SCALABILITY DIMENSION
    # =========================================================================
    
    "horizontal_scaling_test": TaskGraphNode(
        id="horizontal_scaling_test",
        description="Verify performance scales with added instances",
        dimensions=["scalability", "performance"],
        dependencies=["sustained_load_test"],
        risk_weight=1.5,
    ),
    
    "concurrent_user_test": TaskGraphNode(
        id="concurrent_user_test",
        description="Test behavior under high concurrent user load",
        dimensions=["scalability", "performance"],
        dependencies=["throughput_benchmark"],
        risk_weight=1.5,
    ),
    
    "data_volume_test": TaskGraphNode(
        id="data_volume_test",
        description="Test behavior with large data volumes",
        dimensions=["scalability", "performance"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.3,
    ),
    
    # =========================================================================
    # REPRODUCIBILITY DIMENSION
    # =========================================================================
    
    "determinism_test": TaskGraphNode(
        id="determinism_test",
        description="Verify outputs are deterministic given same inputs",
        dimensions=["reproducibility", "correctness"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    "environment_parity_test": TaskGraphNode(
        id="environment_parity_test",
        description="Verify behavior is consistent across environments",
        dimensions=["reproducibility"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.3,
    ),
    
    "build_reproducibility_test": TaskGraphNode(
        id="build_reproducibility_test",
        description="Verify build process produces identical artifacts",
        dimensions=["reproducibility"],
        dependencies=[],
        risk_weight=1.2,
    ),
    
    # =========================================================================
    # COMPATIBILITY DIMENSION
    # =========================================================================
    
    "api_contract_test": TaskGraphNode(
        id="api_contract_test",
        description="Verify API adheres to documented contract",
        dimensions=["compatibility", "correctness"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    "backward_compatibility_test": TaskGraphNode(
        id="backward_compatibility_test",
        description="Verify backward compatibility with previous versions",
        dimensions=["compatibility"],
        dependencies=["api_contract_test"],
        risk_weight=1.8,
    ),
    
    "integration_test": TaskGraphNode(
        id="integration_test",
        description="Verify integration with external systems",
        dimensions=["compatibility"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.5,
    ),
    
    # =========================================================================
    # DOCUMENTATION DIMENSION
    # =========================================================================
    
    "documentation_accuracy_check": TaskGraphNode(
        id="documentation_accuracy_check",
        description="Verify documentation matches actual behavior",
        dimensions=["documentation"],
        dependencies=["baseline_correctness_check"],
        risk_weight=1.0,
    ),
    
    "api_documentation_completeness": TaskGraphNode(
        id="api_documentation_completeness",
        description="Verify all API endpoints are documented",
        dimensions=["documentation"],
        dependencies=[],
        risk_weight=1.0,
    ),
    
    "example_code_verification": TaskGraphNode(
        id="example_code_verification",
        description="Verify example code in documentation works",
        dimensions=["documentation", "correctness"],
        dependencies=["documentation_accuracy_check"],
        risk_weight=1.2,
    ),
}


def get_task_node(task_id: str) -> Optional[TaskGraphNode]:
    """Get a task node by ID."""
    return VERIFICATION_TASK_GRAPH.get(task_id)


def get_all_task_ids() -> List[str]:
    """Get all task IDs in the graph."""
    return list(VERIFICATION_TASK_GRAPH.keys())


def get_tasks_by_dimension(dimension: str) -> List[TaskGraphNode]:
    """Get all tasks that verify a specific dimension."""
    return [
        node for node in VERIFICATION_TASK_GRAPH.values()
        if dimension in node.dimensions
    ]


def get_mandatory_tasks() -> List[TaskGraphNode]:
    """Get all mandatory tasks."""
    return [node for node in VERIFICATION_TASK_GRAPH.values() if node.mandatory]


def get_graph_version() -> str:
    """Get the current graph version."""
    return GRAPH_VERSION
