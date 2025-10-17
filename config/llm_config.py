"""
LLM Configuration
Handles AI calls for truly dynamic agent generation
"""

import os
from typing import Dict, List, Optional
from litellm import completion
import json


class LLMConfig:
    """
    Configuration for LLM calls
    Uses LiteLLM for flexibility across providers
    """
    
    def __init__(
        self,
        model: str = "anthropic/claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize LLM config
        
        Args:
            model: Model to use (LiteLLM format)
            api_key: API key (or use environment variable)
            temperature: Sampling temperature
        """
        self.model = model
        self.temperature = temperature
        
        # Set API key if provided
        if api_key:
            if model.startswith("anthropic/"):
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif model.startswith("gpt"):
                os.environ["OPENAI_API_KEY"] = api_key
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        response_format: Optional[str] = None
    ) -> str:
        """
        Generate completion from LLM
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Max tokens to generate
            response_format: "json" for JSON response
        
        Returns:
            Generated text
        """
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": max_tokens
        }
        
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}
        
        try:
            response = await completion(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  LLM call failed: {e}")
            raise


# Global LLM instance
_llm_instance = None

def get_llm() -> LLMConfig:
    """Get global LLM instance"""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMConfig()
    return _llm_instance


# Test the LLM integration
if __name__ == "__main__":
    import asyncio
    
    async def test_llm():
        """Test LLM integration"""
        
        print("🤖 Testing LLM Integration")
        print("=" * 50)
        
        llm = get_llm()
        
        # Test basic generation
        print("\n1️⃣ Testing basic generation...")
        response = await llm.generate(
            prompt="Say 'Hello from Dialectic!' in a creative way.",
            system_prompt="You are a helpful AI assistant for the Dialectic project."
        )
        print(f"   Response: {response}")
        
        # Test JSON generation
        print("\n2️⃣ Testing JSON generation...")
        response = await llm.generate(
            prompt="Generate a JSON object with two fields: 'agent_type' (string) and 'confidence' (float between 0-1)",
            response_format="json"
        )
        print(f"   Response: {response}")
        
        try:
            data = json.loads(response)
            print(f"   Parsed: {data}")
        except:
            print(f"   Could not parse as JSON")
        
        print("\n✅ LLM integration test complete!")
    
    asyncio.run(test_llm())

