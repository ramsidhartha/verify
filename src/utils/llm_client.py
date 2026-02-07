"""
LLM client abstraction layer for Verifi.

Provides a unified interface for interacting with different LLM providers,
including OpenAI, Anthropic, and a mock client for testing.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, TypeVar
from pydantic import BaseModel

from ..config import LLMConfig


T = TypeVar('T', bound=BaseModel)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a prompt to the LLM and get a text response.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            The LLM's text response
        """
        pass
    
    def complete_structured(
        self, 
        prompt: str, 
        response_model: Type[T],
        system_prompt: Optional[str] = None
    ) -> T:
        """
        Send a prompt and parse the response into a Pydantic model.
        
        Args:
            prompt: The user prompt
            response_model: Pydantic model class for response parsing
            system_prompt: Optional system prompt for context
            
        Returns:
            Parsed response as the specified Pydantic model
        """
        response = self.complete(prompt, system_prompt)
        
        # Try to extract JSON from the response
        try:
            # Handle responses wrapped in markdown code blocks
            if "```json" in response:
                json_start = response.index("```json") + 7
                json_end = response.index("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.index("```") + 3
                json_end = response.index("```", json_start)
                response = response[json_start:json_end].strip()
            
            data = json.loads(response)
            return response_model(**data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse LLM response as {response_model.__name__}: {e}\nResponse: {response}")


class MockLLMClient(LLMClient):
    """
    Mock LLM client for testing without API calls.
    
    Returns predefined responses based on input patterns.
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config or LLMConfig(provider="mock"))
        self._responses: Dict[str, str] = {}
    
    def set_response(self, pattern: str, response: str) -> None:
        """Set a predefined response for a pattern."""
        self._responses[pattern] = response
    
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Return a predefined response or a default classification."""
        # Check for pattern matches
        for pattern, response in self._responses.items():
            if pattern.lower() in prompt.lower():
                return response
        
        # Default response for classification requests
        if "classify" in prompt.lower() or "classification" in prompt.lower():
            return json.dumps({
                "dimensions": {
                    "performance": 0.5,
                    "correctness": 0.3,
                    "security": 0.2
                },
                "red_flags": [],
                "ambiguities": []
            })
        
        # Default response for expansion requests
        if "expand" in prompt.lower() or "parameter" in prompt.lower():
            return json.dumps({
                "parameters": {
                    "target": "default",
                    "duration": 60
                },
                "instructions": "Execute the verification task"
            })
        
        return "{}"


class OpenAIClient(LLMClient):
    """OpenAI API client."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        config = config or LLMConfig(provider="openai")
        super().__init__(config)
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        return self._client
    
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Send a prompt to OpenAI and get a response."""
        client = self._get_client()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        
        return response.choices[0].message.content


class AnthropicClient(LLMClient):
    """Anthropic API client."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        config = config or LLMConfig(provider="anthropic", model="claude-3-sonnet-20240229")
        super().__init__(config)
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        return self._client
    
    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Send a prompt to Anthropic and get a response."""
        client = self._get_client()
        
        response = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=system_prompt or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text


def create_llm_client(config: Optional[LLMConfig] = None) -> LLMClient:
    """
    Factory function to create an LLM client based on configuration.
    
    Args:
        config: LLM configuration. If None, uses default config.
        
    Returns:
        An LLM client instance
    """
    config = config or LLMConfig()
    
    if config.provider == "mock":
        return MockLLMClient(config)
    elif config.provider == "openai":
        return OpenAIClient(config)
    elif config.provider == "anthropic":
        return AnthropicClient(config)
    else:
        raise ValueError(f"Unknown LLM provider: {config.provider}")
