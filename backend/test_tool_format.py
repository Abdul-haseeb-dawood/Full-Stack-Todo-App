"""
Test script to determine the correct tool format for the Gemini API
"""

import google.generativeai as genai
from app.core.settings import settings

# Configure the API key
genai.configure(api_key=settings.gemini_api_key)

# Test the model with the correct format
model_name = 'gemini-2.5-flash'

# Define tools in the format that works
tools = [
    {
        "name": "add_task",
        "description": "Add a new task to the user's task list.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "title": {"type": "string", "description": "The title of the task"},
                "description": {"type": "string", "description": "The description of the task"}
            },
            "required": ["user_id", "title"]
        }
    }
]

try:
    # Try initializing the model with tools
    model = genai.GenerativeModel(
        model_name=model_name,
        tools=tools
    )
    print("Model initialized successfully with tools!")
    
    # Test a simple query
    response = model.generate_content("What can you do?")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative format...")
    
    # Alternative format using function declarations
    tools_alt = [
        {
            "function_declarations": [
                {
                    "name": "add_task",
                    "description": "Add a new task to the user's task list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            ]
        }
    ]
    
    try:
        model_alt = genai.GenerativeModel(
            model_name=model_name,
            tools=tools_alt
        )
        print("Alternative format worked!")
        
        # Test a simple query
        response = model_alt.generate_content("What can you do?")
        print(f"Response: {response.text}")
        
    except Exception as e2:
        print(f"Alternative format also failed: {e2}")