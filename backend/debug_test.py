import google.generativeai as genai
from app.core.settings import settings

# Configure the API
genai.configure(api_key=settings.gemini_api_key)

# Define tools in the format that works with the API
tools = [
    {
        'name': 'add_task',
        'description': 'Add a new task to the user\'s task list.',
        'parameters': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'string', 'description': 'The ID of the user'},
                'title': {'type': 'string', 'description': 'The title of the task'},
                'description': {'type': 'string', 'description': 'The description of the task'}
            },
            'required': ['user_id', 'title']
        }
    }
]

try:
    # Try initializing the model with tools
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=tools
    )
    print('Model with tools initialized successfully!')
    
    # Test a simple query
    chat = model.start_chat()
    response = chat.send_message("Add a task to buy groceries")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f'Error with tools: {e}')
    
    # Try without tools
    try:
        model_no_tools = genai.GenerativeModel(
            model_name='gemini-2.5-flash'
        )
        print('Model without tools initialized successfully!')
        
        response = model_no_tools.generate_content("Hello")
        print(f"Response without tools: {response.text}")
    except Exception as e2:
        print(f'Error even without tools: {e2}')