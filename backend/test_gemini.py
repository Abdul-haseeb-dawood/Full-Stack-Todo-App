import asyncio
from app.core.settings import settings
import google.generativeai as genai

def test_gemini_integration():
    """Test if Gemini API integration works correctly"""
    try:
        # Configure the API key
        genai.configure(api_key=settings.gemini_api_key)

        # Test if the API key is valid by listing models
        models = genai.list_models()
        print("Available models:")
        for model in models:
            print(f"  - {model.name}")

        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Test a simple prompt
        response = model.generate_content("Hello, how are you?")
        print(f"\nGemini response: {response.text}")

        # Test with tools
        tools = [
            {
                "name": "add_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "The task description (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        ]

        # Initialize model with tools
        model_with_tools = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=tools
        )

        # Test with tool calling
        chat = model_with_tools.start_chat()
        response_with_tools = chat.send_message("I want to add a task to buy groceries")

        print(f"\nResponse with tools: {response_with_tools.text}")

        # Check if any function calls were made
        if hasattr(response_with_tools.candidates[0], 'content') and response_with_tools.candidates[0].content.parts:
            for part in response_with_tools.candidates[0].content.parts:
                if hasattr(part, 'function_call'):
                    print(f"Function called: {part.function_call.name}")
                    print(f"Arguments: {dict(part.function_call.args)}")

        print("\nGemini integration test passed!")
        return True

    except Exception as e:
        print(f"Gemini integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_integration()
    if success:
        print("\nGemini is properly configured and working!")
    else:
        print("\nGemini configuration needs to be fixed.")