"""
Simple Gemini Agent for handling user queries using the Google Gemini API.
This agent uses the gemini-1.5-flash model to provide intelligent responses.
"""

import logging
from typing import Dict, Any, Optional
from enum import Enum

import google.generativeai as genai
from app.core.settings import settings


logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Enumeration for agent status"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING_FOR_INPUT = "waiting_for_input"


class GeminiAgent:
    """
    A simplified Gemini-powered agent that can handle user queries.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini Agent

        Args:
            api_key: Gemini API key. If not provided, will use the one from settings
        """
        self.api_key = api_key or settings.gemini_api_key
        if not self.api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=self.api_key)

        # Initialize the model with the gemini-2.5-flash model (latest available)
        self.model_name = 'gemini-2.5-flash'
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )

        self.status = AgentStatus.IDLE

    async def process_query(self, query: str) -> str:
        """
        Process a user query using the Gemini agent

        Args:
            query: The user's query

        Returns:
            The agent's response
        """
        self.status = AgentStatus.PROCESSING

        try:
            # Send the query to Gemini
            response = self.model.generate_content(query)

            # Process the response
            response_text = response.text if response.text else "I processed your request."

            self.status = AgentStatus.IDLE

            return response_text

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            self.status = AgentStatus.IDLE
            return f"Sorry, I encountered an error processing your request: {str(e)}"

    async def get_available_models(self) -> list:
        """Get a list of available Gemini models"""
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []


# Example usage function
async def example_usage():
    """
    Example of how to use the GeminiAgent
    """
    # Create an instance of the agent
    agent = GeminiAgent()

    # Print available models
    models = await agent.get_available_models()
    print("Available models:", models[:3])  # Show first 3 models

    # Test the agent with a sample query
    sample_query = "Hello, how are you today?"
    print(f"\nQuery: {sample_query}")

    response = await agent.process_query(sample_query)
    print(f"Agent Response: {response}")

    print("\nGeminiAgent initialized and working successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())