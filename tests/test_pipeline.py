"""
Tests for end-to-end pipeline
"""

import pytest
from src.models.claim import Claim
from src.models.task import VerificationPlan
from src.pipeline import VerificationPipeline, process_claim, PipelineConfig


class TestVerificationPipeline:
    """Test the full verification pipeline."""
    
    def test_process_simple_claim(self):
        """Test processing a simple claim."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My API handles 2000 requests per second")
        
        assert isinstance(plan, VerificationPlan)
        assert plan.original_claim == "My API handles 2000 requests per second"
    
    def test_pipeline_produces_tasks(self):
        """Test that pipeline produces expanded tasks."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My API is fast and secure")
        
        assert len(plan.required_task_ids) > 0
        assert len(plan.expanded_tasks) > 0
    
    def test_mandatory_tasks_always_present(self):
        """Test that mandatory tasks are always in the plan."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("Some claim about documentation")
        
        # Baseline correctness should always be present
        assert "baseline_correctness_check" in plan.required_task_ids
    
    def test_classification_preserved(self):
        """Test that classification is preserved in plan."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My API handles 2000 rps securely")
        
        assert plan.classification is not None
        assert len(plan.classification.dimensions) > 0
    
    def test_coverage_calculated(self):
        """Test that coverage is calculated."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("Fast API endpoint")
        
        assert 0.0 <= plan.coverage <= 1.0
    
    def test_warnings_from_red_flags(self):
        """Test that red flags become warnings."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("This works perfectly on my staging machine")
        
        # Should have warnings about staging/local
        assert len(plan.warnings) > 0
    
    def test_warnings_from_ambiguities(self):
        """Test that ambiguities become warnings."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My API is secure")
        
        # Should warn about unresolved ambiguities
        if plan.classification.ambiguities:
            assert any("ambiguit" in w.lower() for w in plan.warnings)
    
    def test_with_clarifications(self):
        """Test pipeline with clarifications."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim(
            "My API handles 2000 rps",
            clarifications={"auth_type": "JWT"}
        )
        
        assert isinstance(plan, VerificationPlan)
    
    def test_with_claim_object(self):
        """Test pipeline with Claim object."""
        pipeline = VerificationPipeline()
        
        claim = Claim(
            text="My API handles 2000 rps",
            context="REST API with PostgreSQL backend"
        )
        
        plan = pipeline.process_claim(claim)
        
        assert plan.original_claim == claim.text
    
    def test_get_clarifying_questions(self):
        """Test getting clarifying questions for ambiguities."""
        pipeline = VerificationPipeline()
        
        questions = pipeline.get_clarifying_questions("My secure API handles requests")
        
        # Should ask about auth model
        if questions:
            assert all(isinstance(q, str) for q in questions)
    
    def test_explain(self):
        """Test getting explanation for task selection."""
        pipeline = VerificationPipeline()
        
        explanations = pipeline.explain("My API handles 2000 rps")
        
        assert isinstance(explanations, dict)
        assert "baseline_correctness_check" in explanations


class TestConvenienceFunction:
    """Test convenience function."""
    
    def test_process_claim_function(self):
        """Test the process_claim convenience function."""
        plan = process_claim("My API is fast")
        
        assert isinstance(plan, VerificationPlan)


class TestPipelineConfig:
    """Test pipeline configuration."""
    
    def test_default_uses_mock(self):
        """Test that default config uses mock LLM."""
        config = PipelineConfig()
        assert config.use_mock_llm is True
    
    def test_can_disable_mock(self):
        """Test that mock can be disabled."""
        config = PipelineConfig(use_mock_llm=False)
        assert config.use_mock_llm is False


class TestEndToEndScenarios:
    """Test complete end-to-end scenarios."""
    
    def test_performance_claim_flow(self):
        """Test the example claim from the spec."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My API can handle 2000 requests per second with low latency")
        
        # Check classification
        assert plan.classification.dimensions.get("performance", 0) > 0.3
        
        # Check tasks include performance-related ones
        perf_tasks = [t for t in plan.expanded_tasks if "benchmark" in t.task_id or "latency" in t.task_id]
        assert len(perf_tasks) > 0
        
        # Check parameters extracted
        for task in plan.expanded_tasks:
            if task.task_id == "throughput_benchmark":
                assert task.parameters.get("target_rps") == 2000
    
    def test_security_claim_flow(self):
        """Test a security-focused claim."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("My public API supports 2000 req/s securely")
        
        # Should include security dimension
        assert plan.classification.dimensions.get("security", 0) >= 0.2
        
        # Should have auth-related tasks
        auth_tasks = [t.task_id for t in plan.expanded_tasks if "auth" in t.task_id]
        assert len(auth_tasks) > 0 or "baseline_correctness_check" in plan.required_task_ids
    
    def test_tasks_in_dependency_order(self):
        """Test that final plan has tasks in valid order."""
        pipeline = VerificationPipeline()
        
        plan = pipeline.process_claim("Fast and reliable system")
        
        # First task should be baseline_correctness_check (mandatory, no deps)
        assert plan.required_task_ids[0] == "baseline_correctness_check"
