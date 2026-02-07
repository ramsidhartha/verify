"""
Level 2: Graph Traversal Engine

This module implements DETERMINISTIC traversal of the verification task graph.
Given a classification result, it produces an ordered list of required tasks.

CRITICAL CONSTRAINTS (per architecture spec):
- NO LLM calls - this is pure deterministic logic
- MUST be replayable - same input always produces same output
- MUST be explainable - can show exactly why each task was selected
- MUST NOT invent tasks - only select from the predefined graph

This is the core enforcement layer that prevents LLM hallucination
from affecting verification correctness.
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque

from .task_graph import (
    VERIFICATION_TASK_GRAPH, 
    TaskGraphNode,
    get_task_node,
    get_mandatory_tasks,
)
from ..models.classification import ClassificationResult
from ..config import GraphConfig, DEFAULT_GRAPH_CONFIG


class GraphTraversalEngine:
    """
    Deterministic graph traversal engine.
    
    Converts classification results into ordered task lists using only
    predefined rules and the static task graph.
    
    This is NOT an LLM - it is pure infrastructure code.
    """
    
    def __init__(self, config: Optional[GraphConfig] = None):
        """
        Initialize the traversal engine.
        
        Args:
            config: Graph traversal configuration
        """
        self.config = config or DEFAULT_GRAPH_CONFIG
        self._graph = VERIFICATION_TASK_GRAPH
    
    def get_required_tasks(
        self, 
        classification: ClassificationResult
    ) -> List[str]:
        """
        Get ordered list of required task IDs based on classification.
        
        This is the main entry point for Level 2.
        
        Algorithm:
        1. Identify mandatory tasks (always included)
        2. Activate tasks based on dimension weights above threshold
        3. Recursively add all dependencies
        4. Topologically sort for execution order
        
        Args:
            classification: The classification result from Level 1
            
        Returns:
            Ordered list of canonical task identifiers
        """
        # Step 1: Start with mandatory tasks
        activated_tasks: Set[str] = set()
        for node in get_mandatory_tasks():
            activated_tasks.add(node.id)
        
        # Step 2: Activate tasks based on dimensions
        active_dimensions = classification.get_active_dimensions(
            threshold=self.config.dimension_threshold
        )
        
        for task_id, node in self._graph.items():
            if self._should_activate(node, active_dimensions, classification):
                activated_tasks.add(task_id)
        
        # Step 3: Add all dependencies (transitive closure)
        all_required = self._add_dependencies(activated_tasks)
        
        # Step 4: Topological sort for execution order
        ordered_tasks = self._topological_sort(all_required)
        
        # Step 5: Respect max tasks limit
        if len(ordered_tasks) > self.config.max_tasks:
            ordered_tasks = self._prioritize_tasks(ordered_tasks)[:self.config.max_tasks]
        
        return ordered_tasks
    
    def _should_activate(
        self, 
        node: TaskGraphNode, 
        active_dimensions: List[str],
        classification: ClassificationResult
    ) -> bool:
        """
        Determine if a task should be activated based on dimensions.
        
        A task is activated if ANY of its dimensions is active.
        """
        for dimension in node.dimensions:
            if dimension in active_dimensions:
                return True
        return False
    
    def _add_dependencies(self, activated_tasks: Set[str]) -> Set[str]:
        """
        Add all transitive dependencies for activated tasks.
        
        Uses BFS to traverse the dependency graph.
        """
        all_required = set(activated_tasks)
        queue = deque(activated_tasks)
        
        while queue:
            task_id = queue.popleft()
            node = self._graph.get(task_id)
            if node is None:
                continue
                
            for dep_id in node.dependencies:
                if dep_id not in all_required:
                    all_required.add(dep_id)
                    queue.append(dep_id)
        
        return all_required
    
    def _topological_sort(self, task_ids: Set[str]) -> List[str]:
        """
        Topologically sort tasks so dependencies come before dependents.
        
        Uses Kahn's algorithm for stable, deterministic ordering.
        """
        # Build in-degree map for the subgraph
        in_degree: Dict[str, int] = {task_id: 0 for task_id in task_ids}
        
        for task_id in task_ids:
            node = self._graph.get(task_id)
            if node:
                for dep_id in node.dependencies:
                    if dep_id in task_ids:
                        in_degree[task_id] += 1
        
        # Start with nodes that have no dependencies (in the subgraph)
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        sorted_tasks: List[str] = []
        
        while queue:
            # Sort queue for deterministic ordering
            queue = deque(sorted(queue))
            task_id = queue.popleft()
            sorted_tasks.append(task_id)
            
            # Reduce in-degree for dependents
            for other_id in task_ids:
                other_node = self._graph.get(other_id)
                if other_node and task_id in other_node.dependencies:
                    in_degree[other_id] -= 1
                    if in_degree[other_id] == 0:
                        queue.append(other_id)
        
        # Check for cycles (should never happen in a well-formed graph)
        if len(sorted_tasks) != len(task_ids):
            remaining = task_ids - set(sorted_tasks)
            raise ValueError(f"Cycle detected in task graph involving: {remaining}")
        
        return sorted_tasks
    
    def _prioritize_tasks(self, ordered_tasks: List[str]) -> List[str]:
        """
        Prioritize tasks when we need to limit the total count.
        
        Prioritization order:
        1. Mandatory tasks (always first)
        2. Higher risk_weight tasks
        3. Tasks with fewer dependencies (more foundational)
        """
        def priority_key(task_id: str) -> Tuple[int, float, int]:
            node = self._graph.get(task_id)
            if node is None:
                return (1, 0.0, 0)
            
            return (
                0 if node.mandatory else 1,  # Mandatory first
                -node.risk_weight,  # Higher weight = higher priority
                len(node.dependencies),  # Fewer deps = higher priority
            )
        
        # Re-sort by priority, maintaining topological validity
        mandatory = [t for t in ordered_tasks if self._graph.get(t, TaskGraphNode("", "", [], [])).mandatory]
        non_mandatory = [t for t in ordered_tasks if t not in mandatory]
        
        # Sort non-mandatory by priority
        non_mandatory.sort(key=priority_key)
        
        return mandatory + non_mandatory
    
    def explain_selection(
        self, 
        classification: ClassificationResult
    ) -> Dict[str, List[str]]:
        """
        Explain why each task was selected.
        
        Returns a mapping of task_id -> list of reasons.
        This is for auditability and debugging.
        """
        required_tasks = self.get_required_tasks(classification)
        explanations: Dict[str, List[str]] = {}
        
        for task_id in required_tasks:
            node = self._graph.get(task_id)
            if node is None:
                continue
                
            reasons = []
            
            # Check if mandatory
            if node.mandatory:
                reasons.append("Mandatory task - always required")
            
            # Check which dimensions activated it
            active_dims = classification.get_active_dimensions(self.config.dimension_threshold)
            matching_dims = [d for d in node.dimensions if d in active_dims]
            if matching_dims:
                reasons.append(f"Activated by dimensions: {', '.join(matching_dims)}")
            
            # Check if it's a dependency of another selected task
            for other_id in required_tasks:
                other_node = self._graph.get(other_id)
                if other_node and task_id in other_node.dependencies:
                    reasons.append(f"Required as dependency of: {other_id}")
                    break
            
            explanations[task_id] = reasons if reasons else ["Unknown reason"]
        
        return explanations
    
    def calculate_coverage(
        self, 
        executed_tasks: List[str], 
        required_tasks: List[str]
    ) -> float:
        """
        Calculate verification coverage score.
        
        Formula: weighted_executed / weighted_required
        
        Args:
            executed_tasks: Tasks that have been executed
            required_tasks: Tasks that were required
            
        Returns:
            Coverage score between 0.0 and 1.0
        """
        if not required_tasks:
            return 1.0
        
        def get_weight(task_id: str) -> float:
            node = self._graph.get(task_id)
            return node.risk_weight if node else 1.0
        
        required_weight = sum(get_weight(t) for t in required_tasks)
        executed_weight = sum(get_weight(t) for t in executed_tasks if t in required_tasks)
        
        return executed_weight / required_weight if required_weight > 0 else 1.0


def get_required_tasks(
    classification: ClassificationResult,
    config: Optional[GraphConfig] = None
) -> List[str]:
    """
    Convenience function to get required tasks.
    
    Args:
        classification: The classification result from Level 1
        config: Optional graph configuration
        
    Returns:
        Ordered list of canonical task identifiers
    """
    engine = GraphTraversalEngine(config)
    return engine.get_required_tasks(classification)
