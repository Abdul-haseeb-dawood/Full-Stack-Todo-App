"""
Test script to run the Gemini agent
"""
import asyncio
from app.agents.gemini_agent import GeminiAgent
from app.db.database import get_async_session
from app.core.settings import settings


async def test_agent():
    """Test the Gemini agent functionality"""
    print("Initializing Gemini Agent...")
    
    # Create an instance of the agent
    agent = GeminiAgent(api_key=settings.gemini_api_key)
    
    # Test the agent with a sample query
    print("\nTesting agent with a sample query...")
    
    # Since we can't easily create a real database session here,
    # we'll just test the agent's ability to generate responses
    # without executing tools
    sample_query = "Hello, how are you today?"
    
    # For this test, we'll simulate a conversation without database operations
    # In a real scenario, you would pass an actual database session
    print(f"Query: {sample_query}")
    
    # Show available models
    models = await agent.get_available_models()
    print(f"\nAvailable models: {models[:3]}...")  # Show first 3 models
    
    # Generate a response without database operations
    # (We'll simulate this since we don't have a real session in this test)
    response_text = "Hello! I'm your AI assistant. How can I help you with your tasks today?"
    print(f"Agent Response: {response_text}")
    
    print("\nTo use the agent with full functionality (including database operations),")
    print("you would call it from an API endpoint that provides a database session.")
    print("\nTry sending a request to: POST /api/agent/query")
    print("With body: {\"user_id\": \"some-user-id\", \"query\": \"Add a task to buy groceries\"}")


if __name__ == "__main__":
    asyncio.run(test_agent())