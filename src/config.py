"""
Configuration and constants for Verifi AI reasoning core.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """Configuration for LLM clients."""
    provider: str = "openai"  # "openai", "anthropic", or "mock"
    model: str = "gpt-4"
    api_key: Optional[str] = None
    temperature: float = 0.1  # Low temperature for deterministic outputs
    max_tokens: int = 2000
    
    def __post_init__(self):
        if self.api_key is None:
            if self.provider == "openai":
                self.api_key = os.environ.get("OPENAI_API_KEY")
            elif self.provider == "anthropic":
                self.api_key = os.environ.get("ANTHROPIC_API_KEY")


@dataclass
class GraphConfig:
    """Configuration for task graph traversal."""
    dimension_threshold: float = 0.2  # Minimum weight to activate a dimension
    include_mandatory: bool = True  # Always include mandatory tasks
    max_tasks: int = 20  # Maximum tasks to return


# Default configurations
DEFAULT_LLM_CONFIG = LLMConfig()
DEFAULT_GRAPH_CONFIG = GraphConfig()
