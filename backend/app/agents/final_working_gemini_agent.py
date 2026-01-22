"""
Working Gemini Agent for handling user queries using the Google Gemini API.
This agent uses the gemini-2.5-flash model to provide intelligent responses
and can interact with the database through available tools.
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum

import google.generativeai as genai
from app.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Enumeration for agent status"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING_FOR_INPUT = "waiting_for_input"


class GeminiAgent:
    """
    A working Gemini-powered agent that can handle user queries and interact with the database
    through predefined tools.
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

        # Define available tools for the agent using the function_declarations format
        self.tools = [
            {
                "function_declarations": [
                    {
                        "name": "add_task",
                        "description": "Add a new task to the user's task list. Use this when the user wants to create a new task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "title": {"type": "string", "description": "The title of the task"},
                                "description": {"type": "string", "description": "The description of the task"}
                            },
                            "required": ["user_id", "title"]
                        }
                    },
                    {
                        "name": "update_task",
                        "description": "Update an existing task in the user's task list. Use this when the user wants to modify a task's title, description, priority, or completion status.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "task_id": {"type": "string", "description": "The ID of the task to update"},
                                "title": {"type": "string", "description": "The new title of the task"},
                                "description": {"type": "string", "description": "The new description of the task"},
                                "completed": {"type": "boolean", "description": "Whether the task is completed"},
                                "priority": {"type": "string", "description": "The priority of the task (low, medium, high)"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    },
                    {
                        "name": "read_task",
                        "description": "Read a specific task from the user's task list. Use this when the user wants to view details of a specific task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "task_id": {"type": "string", "description": "The ID of the task to read"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    },
                    {
                        "name": "read_all_tasks",
                        "description": "Read all tasks from the user's task list. Use this when the user wants to view all their tasks or a filtered list.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "status": {"type": "string", "description": "Filter by status (all, pending, completed)"},
                                "priority": {"type": "string", "description": "Filter by priority (low, medium, high)"}
                            },
                            "required": ["user_id"]
                        }
                    },
                    {
                        "name": "complete_task",
                        "description": "Mark a task as completed in the user's task list. Use this when the user wants to mark a task as done.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "task_id": {"type": "string", "description": "The ID of the task to mark as completed"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    },
                    {
                        "name": "delete_task",
                        "description": "Delete a task from the user's task list. Use this when the user wants to remove a task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "task_id": {"type": "string", "description": "The ID of the task to delete"}
                            },
                            "required": ["user_id", "task_id"]
                        }
                    }
                ]
            }
        ]

        # Initialize the model with tools
        self.model_with_tools = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.tools,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )

        self.status = AgentStatus.IDLE
        self.chat_history = []

    async def process_query(self, query: str, user_id: str, db_session: AsyncSession) -> Dict[str, Any]:
        """
        Process a user query using the Gemini agent

        Args:
            query: The user's query
            user_id: The ID of the user making the query
            db_session: Database session for interacting with the database

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        self.status = AgentStatus.PROCESSING

        try:
            # Prepare conversation history for the model
            gemini_history = []
            for entry in self.chat_history:
                gemini_history.append({
                    "role": entry["role"],
                    "parts": [entry["content"]]
                })

            # Add the current query to history
            gemini_history.append({
                "role": "user",
                "parts": [query]
            })

            # Start a chat with history
            chat = self.model_with_tools.start_chat(history=gemini_history)

            # Send the query to Gemini
            response = chat.send_message(query)

            # Process the response
            response_text = response.text if response.text else "I processed your request."
            tool_calls = []

            # Check if any tools were called
            if hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        # Extract function name and arguments
                        function_call = part.function_call
                        function_name = function_call.name

                        # Convert args to dict
                        args_dict = {}
                        for key, value in function_call.args.items():
                            args_dict[key] = value

                        # Ensure user_id is included
                        if 'user_id' not in args_dict:
                            args_dict['user_id'] = user_id

                        # Add to tool calls
                        tool_call = {
                            "name": function_name,
                            "arguments": args_dict
                        }
                        tool_calls.append(tool_call)

                        # Execute the tool
                        result = await self._execute_tool(function_name, db_session, **args_dict)

                        # Feed the result back to Gemini for final response
                        follow_up_response = chat.send_message(f"Result of {function_name}: {str(result)}")

                        # Update the response text with the follow-up from Gemini
                        if follow_up_response.text:
                            response_text = follow_up_response.text

            # Update chat history
            self.chat_history.append({"role": "user", "content": query})
            self.chat_history.append({"role": "model", "content": response_text})

            # Limit history to prevent it from growing too large
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]

            self.status = AgentStatus.IDLE

            return {
                "response": response_text,
                "tool_calls": tool_calls,
                "status": self.status.value
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            self.status = AgentStatus.IDLE
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": [],
                "status": self.status.value
            }

    async def _execute_tool(self, tool_name: str, db_session: AsyncSession, **kwargs) -> Any:
        """
        Execute a tool based on its name

        Args:
            tool_name: Name of the tool to execute
            db_session: Database session
            **kwargs: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        # Import the appropriate tool function based on the name
        if tool_name == "add_task":
            from mcp.add_task_tool import execute as add_task_execute
            return await add_task_execute(db_session, **kwargs)
        elif tool_name == "update_task":
            from mcp.update_task_tool import execute as update_task_execute
            return await update_task_execute(db_session, **kwargs)
        elif tool_name == "read_task":
            from mcp.read_task_tool import execute as read_task_execute
            return await read_task_execute(db_session, **kwargs)
        elif tool_name == "read_all_tasks":
            from mcp.read_all_tasks_tool import execute as read_all_tasks_execute
            return await read_all_tasks_execute(db_session, **kwargs)
        elif tool_name == "complete_task":
            from mcp.complete_task_tool import execute as complete_task_execute
            return await complete_task_execute(db_session, **kwargs)
        elif tool_name == "delete_task":
            from mcp.delete_task_tool import execute as delete_task_execute
            return await delete_task_execute(db_session, **kwargs)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history = []
        self.status = AgentStatus.IDLE

    async def get_available_models(self) -> List[str]:
        """Get a list of available Gemini models"""
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return()


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

    print("\nWorking GeminiAgent with gemini-2.5-flash model initialized successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())