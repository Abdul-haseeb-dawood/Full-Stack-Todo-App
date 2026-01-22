import google.generativeai as genai
from app.core.settings import settings

# Configure the API
genai.configure(api_key=settings.gemini_api_key)

# Test if the model can be initialized
try:
    model = genai.GenerativeModel(model_name='models/gemini-2.5-flash')
    print('Model initialized successfully')
    
    # Test a simple query
    response = model.generate_content('Hello')
    print('Response received:', response.text[:100])
except Exception as e:
    print(f'Error: {e}')
    
    # Try without the "models/" prefix
    try:
        model = genai.GenerativeModel(model_name='gemini-2.5-flash')
        print('Model initialized successfully without prefix')
        
        # Test a simple query
        response = model.generate_content('Hello')
        print('Response received:', response.text[:100])
    except Exception as e2:
        print(f'Error without prefix: {e2}')