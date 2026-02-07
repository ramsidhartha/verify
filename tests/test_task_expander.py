"""
Tests for Level 3: Task Expansion Agent
"""

import pytest
from src.models.claim import Claim
from src.models.task import ExpandedTask
from src.level3.task_expander import TaskExpander, expand_tasks
from src.utils.llm_client import MockLLMClient


class TestTaskExpander:
    """Test TaskExpander."""
    
    def test_expand_single_task(self):
        """Test expanding a single task."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["throughput_benchmark"],
            "My API handles 2000 requests per second"
        )
        
        assert len(tasks) == 1
        assert tasks[0].task_id == "throughput_benchmark"
        assert tasks[0].parameters is not None
    
    def test_expand_multiple_tasks(self):
        """Test expanding multiple tasks."""
        expander = TaskExpander()
        
        task_ids = ["baseline_correctness_check", "throughput_benchmark", "latency_profile"]
        tasks = expander.expand_tasks(
            task_ids,
            "My API handles 2000 rps with p99 under 50ms"
        )
        
        assert len(tasks) == 3
        assert [t.task_id for t in tasks] == task_ids
    
    def test_extracts_rps_from_claim(self):
        """Test that RPS values are extracted from claim."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["throughput_benchmark"],
            "My API handles 2000 requests per second"
        )
        
        params = tasks[0].parameters
        # Should have extracted target_rps
        assert params.get("target_rps") == 2000
    
    def test_extracts_latency_from_claim(self):
        """Test that latency values are extracted from claim."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["latency_profile"],
            "Response time p99 under 100ms"
        )
        
        params = tasks[0].parameters
        # Should have extracted latency target
        assert params.get("target_p99_ms") == 100
    
    def test_extracts_percentage_from_claim(self):
        """Test that percentage values are extracted."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["throughput_benchmark"],
            "API with less than 1% error rate"
        )
        
        params = tasks[0].parameters
        assert params.get("acceptable_error_rate") == 0.01
    
    def test_handles_unknown_task(self):
        """Test that unknown tasks are skipped gracefully."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["unknown_task_xyz", "baseline_correctness_check"],
            "Test claim"
        )
        
        # Unknown task should be skipped
        assert len(tasks) == 1
        assert tasks[0].task_id == "baseline_correctness_check"
    
    def test_includes_description(self):
        """Test that expanded tasks have descriptions."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["baseline_correctness_check"],
            "Test claim"
        )
        
        assert tasks[0].description is not None
        assert len(tasks[0].description) > 0
    
    def test_with_clarifications(self):
        """Test expansion with clarifications provided."""
        expander = TaskExpander()
        
        tasks = expander.expand_tasks(
            ["auth_boundary_test"],
            "My API is secure",
            clarifications={"auth_type": "OAuth2"}
        )
        
        assert len(tasks) == 1
        # Should use clarification info
        assert tasks[0].task_id == "auth_boundary_test"
    
    def test_with_claim_object(self):
        """Test expansion with Claim object instead of string."""
        expander = TaskExpander()
        
        claim = Claim(text="My API handles 1000 rps", context="REST API")
        tasks = expander.expand_tasks(
            ["throughput_benchmark"],
            claim
        )
        
        assert len(tasks) == 1
        assert tasks[0].parameters.get("target_rps") == 1000


class TestConvenienceFunction:
    """Test convenience function."""
    
    def test_expand_tasks_function(self):
        """Test the expand_tasks convenience function."""
        tasks = expand_tasks(
            ["baseline_correctness_check"],
            "Test claim"
        )
        
        assert isinstance(tasks, list)
        assert len(tasks) == 1
        assert isinstance(tasks[0], ExpandedTask)
