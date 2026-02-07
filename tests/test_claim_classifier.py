"""
Tests for Level 1: Claim Classification Agent
"""

import pytest
from src.models.claim import Claim, ClaimDimension
from src.models.classification import ClassificationResult
from src.level1.claim_classifier import ClaimClassifier, classify_claim
from src.utils.llm_client import MockLLMClient


class TestClassificationResult:
    """Test ClassificationResult model."""
    
    def test_valid_classification(self):
        """Test creating a valid classification."""
        result = ClassificationResult(
            dimensions={"performance": 0.8, "correctness": 0.5},
            red_flags=["tested only on staging"],
            ambiguities=["auth model unclear"]
        )
        assert result.dimensions["performance"] == 0.8
        assert len(result.red_flags) == 1
        assert len(result.ambiguities) == 1
    
    def test_dimension_validation(self):
        """Test that dimension weights must be 0-1."""
        with pytest.raises(ValueError):
            ClassificationResult(
                dimensions={"performance": 1.5},  # Invalid
                red_flags=[],
                ambiguities=[]
            )
    
    def test_get_active_dimensions(self):
        """Test active dimension filtering."""
        result = ClassificationResult(
            dimensions={
                "performance": 0.8,
                "correctness": 0.1,
                "security": 0.3
            },
            red_flags=[],
            ambiguities=[]
        )
        
        active = result.get_active_dimensions(threshold=0.2)
        assert "performance" in active
        assert "security" in active
        assert "correctness" not in active


class TestClaimClassifier:
    """Test ClaimClassifier."""
    
    def test_classify_performance_claim(self):
        """Test classification of a performance-focused claim."""
        classifier = ClaimClassifier()
        
        result = classifier.classify("My API handles 2000 requests per second with low latency")
        
        assert result.dimensions.get("performance", 0) > 0.3
    
    def test_classify_security_claim(self):
        """Test classification of a security-focused claim."""
        classifier = ClaimClassifier()
        
        result = classifier.classify("My API securely authenticates all users with OAuth2")
        
        assert result.dimensions.get("security", 0) >= 0.2
    
    def test_red_flag_detection(self):
        """Test that red flags are detected."""
        classifier = ClaimClassifier()
        
        result = classifier.classify("This works on my machine in staging")
        
        # Should detect staging and local machine red flags
        assert len(result.red_flags) > 0
    
    def test_ambiguity_detection(self):
        """Test that ambiguities are detected."""
        classifier = ClaimClassifier()
        
        result = classifier.classify("My API handles 2000 rps")
        
        # Should detect auth model ambiguity
        assert any("auth" in amb.lower() for amb in result.ambiguities)
    
    def test_classify_with_mock_llm(self):
        """Test classification with mock LLM client."""
        mock_llm = MockLLMClient()
        mock_llm.set_response(
            "2000 req",
            '{"dimensions": {"performance": 0.9}, "red_flags": [], "ambiguities": []}'
        )
        
        classifier = ClaimClassifier(llm_client=mock_llm)
        result = classifier.classify("My API handles 2000 req/s")
        
        assert result.dimensions.get("performance", 0) >= 0.5


class TestConvenienceFunction:
    """Test convenience function."""
    
    def test_classify_claim_function(self):
        """Test the classify_claim convenience function."""
        result = classify_claim("My system is fast and secure")
        
        assert isinstance(result, ClassificationResult)
        assert "performance" in result.dimensions or "security" in result.dimensions
