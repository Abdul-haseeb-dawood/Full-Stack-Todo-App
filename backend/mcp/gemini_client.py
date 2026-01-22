import os
import google.generativeai as genai
from app.core.settings import settings
from typing import Dict, Any, Optional

class GeminiClient:
    def __init__(self):
        # Initialize the Gemini API with the key from settings
        api_key = settings.gemini_api_key
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in settings")

        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash which is available and supports generateContent
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a response using the Gemini API

        Args:
            prompt: The user's input/prompt
            context: Additional context about tasks, etc.

        Returns:
            The response as a string
        """
        try:
            # Prepare the full prompt with context if available
            full_prompt = f"""
            You are an AI assistant for a todo application. The user can ask you to:
            - Add tasks: "Add task: [task title]"
            - Update tasks: "Update task '[old title]' to '[new title]'"
            - Delete tasks: "Delete task '[task title]'"
            - Complete tasks: "Complete task '[task title]'"
            - List tasks: "Show my tasks"

            For these operations, respond with a JSON-like format indicating the action:
            - For adding: "ACTION:add_task|TITLE:[task title]"
            - For updating: "ACTION:update_task|OLD_TITLE:[old title]|NEW_TITLE:[new title]"
            - For deleting: "ACTION:delete_task|TITLE:[task title]"
            - For completing: "ACTION:complete_task|TITLE:[task title]"
            - For listing: "ACTION:list_tasks"
            - For general chat: "ACTION:general|RESPONSE:[your response]"

            Current user input: {prompt}
            """

            if context:
                full_prompt += f"\n\nAdditional context: {context}"

            # Generate content using the Gemini API
            response = await self.model.generate_content_async(full_prompt)

            # Return the text response
            return response.text if response.text else "I couldn't process that request."

        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"

# Global instance
gemini_client = None

def get_gemini_client() -> GeminiClient:
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client