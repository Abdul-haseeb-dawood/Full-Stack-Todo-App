import asyncio
import httpx
import json

async def test_chat_api():
    """Test the chat API with the new functionality"""
    base_url = "http://localhost:8000/api/chat"
    
    # Test creating a new conversation and adding a task
    async with httpx.AsyncClient() as client:
        # Test 1: Add a task
        payload1 = {
            "message": "Add a task to buy groceries",
            "user_id": "test_user_123"
        }
        
        print("Testing: Add a task to buy groceries")
        response1 = await client.post(f"{base_url}/test_user_123", json=payload1)
        print(f"Status: {response1.status_code}")
        print(f"Response: {json.dumps(response1.json(), indent=2)}")
        print("-" * 50)
        
        # Test 2: List all tasks
        payload2 = {
            "message": "Show me all my tasks",
            "user_id": "test_user_123"
        }
        
        print("Testing: Show me all my tasks")
        response2 = await client.post(f"{base_url}/test_user_123", json=payload2)
        print(f"Status: {response2.status_code}")
        print(f"Response: {json.dumps(response2.json(), indent=2)}")
        print("-" * 50)
        
        # Test 3: Complete a task (this would require knowing the task ID)
        # For now, we'll just test the pattern recognition
        payload3 = {
            "message": "Complete task 1",
            "user_id": "test_user_123"
        }
        
        print("Testing: Complete task 1")
        response3 = await client.post(f"{base_url}/test_user_123", json=payload3)
        print(f"Status: {response3.status_code}")
        print(f"Response: {json.dumps(response3.json(), indent=2)}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_chat_api())