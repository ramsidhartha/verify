"""
Tests for Level 2: Task Graph Traversal Engine
"""

import pytest
from src.models.classification import ClassificationResult
from src.level2.task_graph import (
    VERIFICATION_TASK_GRAPH,
    get_task_node,
    get_all_task_ids,
    get_tasks_by_dimension,
    get_mandatory_tasks,
    get_graph_version,
)
from src.level2.graph_traversal import GraphTraversalEngine, get_required_tasks
from src.config import GraphConfig


class TestTaskGraph:
    """Test the static task graph."""
    
    def test_graph_has_nodes(self):
        """Test that the graph contains nodes."""
        assert len(VERIFICATION_TASK_GRAPH) > 0
    
    def test_mandatory_tasks_exist(self):
        """Test that mandatory tasks are defined."""
        mandatory = get_mandatory_tasks()
        assert len(mandatory) > 0
        assert any(node.id == "baseline_correctness_check" for node in mandatory)
    
    def test_get_task_node(self):
        """Test retrieving a specific task node."""
        node = get_task_node("throughput_benchmark")
        assert node is not None
        assert node.id == "throughput_benchmark"
        assert "performance" in node.dimensions
    
    def test_get_all_task_ids(self):
        """Test getting all task IDs."""
        ids = get_all_task_ids()
        assert "baseline_correctness_check" in ids
        assert "throughput_benchmark" in ids
        assert "auth_boundary_test" in ids
    
    def test_get_tasks_by_dimension(self):
        """Test filtering tasks by dimension."""
        perf_tasks = get_tasks_by_dimension("performance")
        assert len(perf_tasks) > 0
        assert all("performance" in t.dimensions for t in perf_tasks)
    
    def test_graph_version(self):
        """Test that graph version is defined."""
        version = get_graph_version()
        assert version is not None
        assert "." in version  # Semantic versioning


class TestGraphTraversalEngine:
    """Test the graph traversal engine."""
    
    def test_always_includes_mandatory(self):
        """Test that mandatory tasks are always included."""
        engine = GraphTraversalEngine()
        
        # Even with minimal classification, mandatory should be included
        classification = ClassificationResult(
            dimensions={"documentation": 0.5},
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = engine.get_required_tasks(classification)
        assert "baseline_correctness_check" in tasks
    
    def test_activates_by_dimension(self):
        """Test that tasks are activated by dimension weight."""
        engine = GraphTraversalEngine()
        
        classification = ClassificationResult(
            dimensions={"performance": 0.8, "correctness": 0.3},
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = engine.get_required_tasks(classification)
        
        # Should include performance tasks
        assert "throughput_benchmark" in tasks
        assert "latency_profile" in tasks
    
    def test_includes_dependencies(self):
        """Test that dependencies are automatically included."""
        engine = GraphTraversalEngine()
        
        # sustained_load_test depends on throughput_benchmark
        classification = ClassificationResult(
            dimensions={"performance": 0.9},
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = engine.get_required_tasks(classification)
        
        if "sustained_load_test" in tasks:
            # Its dependencies should also be present
            assert "throughput_benchmark" in tasks
            assert "baseline_correctness_check" in tasks
    
    def test_topological_order(self):
        """Test that tasks are in valid topological order."""
        engine = GraphTraversalEngine()
        
        classification = ClassificationResult(
            dimensions={"performance": 0.9, "security": 0.7},
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = engine.get_required_tasks(classification)
        
        # Dependencies should come before dependents
        for i, task_id in enumerate(tasks):
            node = get_task_node(task_id)
            if node:
                for dep_id in node.dependencies:
                    if dep_id in tasks:
                        dep_index = tasks.index(dep_id)
                        assert dep_index < i, f"{dep_id} should come before {task_id}"
    
    def test_respects_threshold(self):
        """Test that dimension threshold is respected."""
        config = GraphConfig(dimension_threshold=0.5)
        engine = GraphTraversalEngine(config)
        
        # Low-weight dimension should not activate tasks
        classification = ClassificationResult(
            dimensions={"security": 0.3},  # Below threshold
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = engine.get_required_tasks(classification)
        
        # Should only include mandatory, not security tasks
        assert "auth_boundary_test" not in tasks
    
    def test_explain_selection(self):
        """Test that selection can be explained."""
        engine = GraphTraversalEngine()
        
        classification = ClassificationResult(
            dimensions={"performance": 0.8},
            red_flags=[],
            ambiguities=[]
        )
        
        explanations = engine.explain_selection(classification)
        
        assert len(explanations) > 0
        # Mandatory task should have explanation
        assert "baseline_correctness_check" in explanations
        assert any("Mandatory" in reason for reason in explanations["baseline_correctness_check"])
    
    def test_calculate_coverage(self):
        """Test coverage calculation."""
        engine = GraphTraversalEngine()
        
        required = ["task_a", "task_b", "task_c"]
        executed = ["task_a", "task_b"]
        
        # With equal weights, should be 2/3
        coverage = engine.calculate_coverage(executed, required)
        
        # Coverage should be reasonable (accounting for weights)
        assert 0 < coverage < 1
    
    def test_deterministic(self):
        """Test that traversal is deterministic."""
        engine = GraphTraversalEngine()
        
        classification = ClassificationResult(
            dimensions={"performance": 0.8, "security": 0.6},
            red_flags=[],
            ambiguities=[]
        )
        
        # Run multiple times
        results = [engine.get_required_tasks(classification) for _ in range(5)]
        
        # All should be identical
        assert all(r == results[0] for r in results)


class TestConvenienceFunction:
    """Test convenience function."""
    
    def test_get_required_tasks_function(self):
        """Test the get_required_tasks convenience function."""
        classification = ClassificationResult(
            dimensions={"correctness": 0.7},
            red_flags=[],
            ambiguities=[]
        )
        
        tasks = get_required_tasks(classification)
        
        assert isinstance(tasks, list)
        assert "baseline_correctness_check" in tasks
