from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.message import ConversationCreate, MessageCreate
from app.services.message_service import ConversationService, MessageService
from app.core.settings import settings

# Import Google Generative AI
import google.generativeai as genai

router = APIRouter(prefix="/chat", tags=["chat"])

# Models
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    user_id: str  # Required for identifying the user


class ToolCall(BaseModel):
    type: str
    params: dict


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]
    timestamp: str


# Simple in-memory conversation state storage (in production, use Redis or database)
conversation_states: Dict[str, Dict[str, Any]] = {}


async def execute_mcp_tool(tool_name: str, db_session: AsyncSession, **kwargs):
    """
    Execute MCP tools dynamically based on the tool name
    """
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


@router.post("/{user_id}", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    db_session: AsyncSession = Depends(get_async_session)
):
    """
    Initiates a conversation with the AI assistant or continues an existing conversation.
    """
    # Initialize services
    conversation_service = ConversationService(db_session)
    message_service = MessageService(db_session)

    # Parse conversation ID
    conversation_id = None
    if request.conversation_id:
        try:
            conversation_id = uuid.UUID(request.conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

    # If no conversation ID provided, create a new one
    if not conversation_id:
        conversation_data = ConversationCreate(user_id=user_id)
        conversation = await conversation_service.create_conversation(conversation_data)
        conversation_id = conversation.id
    else:
        # Verify conversation exists
        existing_conversation = await conversation_service.get_conversation_by_id(conversation_id)
        if not existing_conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    # Get conversation history
    messages = await message_service.get_messages_by_conversation(conversation_id)

    # Create user message
    user_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=request.message
    )
    user_message = await message_service.create_message(user_message_data)

    # Prepare conversation history for Gemini
    gemini_history = []
    for msg in messages:
        gemini_history.append({
            "role": msg.role,
            "parts": [msg.content]
        })

    # Add the current user message
    gemini_history.append({
        "role": "user",
        "parts": [request.message]
    })

    # Check if we're in a multi-step conversation state
    conversation_key = str(conversation_id)
    current_state = conversation_states.get(conversation_key, {})

    # Handle multi-step conversation for update task
    if current_state.get("waiting_for") == "task_selection_for_update":
        # User has provided a task name, now ask for the new name
        # First, get all tasks for the user to match the provided name
        from mcp.read_all_tasks_tool import execute as read_all_tasks_execute
        all_tasks_result = await read_all_tasks_execute(db_session, user_id=user_id)

        # Find the task that matches the user's input
        matched_task = None
        user_input_task_name = request.message.strip().lower()
        for task in all_tasks_result.get("tasks", []):
            if user_input_task_name in task["title"].lower() or task["title"].lower() in user_input_task_name:
                matched_task = task
                break

        if matched_task:
            # Store the matched task ID for the next step
            conversation_states[conversation_key] = {
                "waiting_for": "new_task_name",
                "original_task_id": matched_task["id"],
                "original_task_title": matched_task["title"]
            }

            response_text = f"I found the task '{matched_task['title']}'. What would you like the new name to be?"
            tool_calls = []
        else:
            # Task not found, ask again
            response_text = f"I couldn't find a task matching '{request.message}'. Could you please specify the task name again?"
            tool_calls = []

        # Create assistant message
        assistant_message_data = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        assistant_message = await message_service.create_message(assistant_message_data)

        # Create response
        response_obj = ChatResponse(
            conversation_id=str(conversation_id),
            response=response_text,
            tool_calls=tool_calls,
            timestamp=datetime.now().isoformat()
        )

        return response_obj

    elif current_state.get("waiting_for") == "new_task_name":
        # User has provided the new name, now ask for description
        original_task_id = current_state.get("original_task_id")
        original_task_title = current_state.get("original_task_title")

        # Store the new name for the next step
        conversation_states[conversation_key] = {
            "waiting_for": "new_task_description",
            "original_task_id": original_task_id,
            "original_task_title": original_task_title,
            "new_task_name": request.message
        }

        response_text = f"What would you like the new description to be for the task '{original_task_title}'? (Reply with just the description or 'skip' to keep the current description)"
        tool_calls = []

        # Create assistant message
        assistant_message_data = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        assistant_message = await message_service.create_message(assistant_message_data)

        # Create response
        response_obj = ChatResponse(
            conversation_id=str(conversation_id),
            response=response_text,
            tool_calls=tool_calls,
            timestamp=datetime.now().isoformat()
        )

        return response_obj

    elif current_state.get("waiting_for") == "new_task_description":
        # User has provided the new description (or skipped), now update the task
        original_task_id = current_state.get("original_task_id")
        original_task_title = current_state.get("original_task_title")
        new_task_name = current_state.get("new_task_name")
        new_description = request.message if request.message.lower() != "skip" else None

        # Clear the conversation state
        if conversation_key in conversation_states:
            del conversation_states[conversation_key]

        # Prepare update parameters
        update_params = {
            "user_id": user_id,
            "task_id": original_task_id,
            "title": new_task_name
        }
        if new_description and new_description.lower() != "skip":
            update_params["description"] = new_description

        # Execute the update task tool
        result = await execute_mcp_tool("update_task", db_session, **update_params)

        response_text = f"Task '{original_task_title}' has been updated to '{new_task_name}'."
        tool_calls = [{"type": "update_task", "params": update_params}]

        # Create assistant message
        assistant_message_data = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        assistant_message = await message_service.create_message(assistant_message_data)

        # Create response
        response_obj = ChatResponse(
            conversation_id=str(conversation_id),
            response=response_text,
            tool_calls=tool_calls,
            timestamp=datetime.now().isoformat()
        )

        return response_obj

    # If not in a multi-step conversation, proceed with normal Gemini flow
    # Configure Gemini with API key
    genai.configure(api_key=settings.gemini_api_key)

    # Define the tools for Gemini with more detailed descriptions
    from mcp.add_task_tool import get_input_schema as add_task_schema, name as add_task_name
    from mcp.update_task_tool import get_input_schema as update_task_schema, name as update_task_name
    from mcp.read_task_tool import get_input_schema as read_task_schema, name as read_task_name
    from mcp.read_all_tasks_tool import get_input_schema as read_all_tasks_schema, name as read_all_tasks_name
    from mcp.complete_task_tool import get_input_schema as complete_task_schema, name as complete_task_name
    from mcp.delete_task_tool import get_input_schema as delete_task_schema, name as delete_task_name

    tools = [
        {
            "name": add_task_name,
            "description": "Add a new task to the user's task list. Use this when the user wants to create a new task. Parameters: user_id (required), title (required), description (optional).",
            "parameters": add_task_schema()
        },
        {
            "name": update_task_name,
            "description": "Update an existing task in the user's task list. Use this when the user wants to modify a task's title, description, priority, or completion status. Parameters: user_id (required), task_id (required), title (optional), description (optional), completed (optional), priority (optional).",
            "parameters": update_task_schema()
        },
        {
            "name": read_task_name,
            "description": "Read a specific task from the user's task list. Use this when the user wants to view details of a specific task. Parameters: user_id (required), task_id (required).",
            "parameters": read_task_schema()
        },
        {
            "name": read_all_tasks_name,
            "description": "Read all tasks from the user's task list. Use this when the user wants to view all their tasks or a filtered list. Parameters: user_id (required), status (optional - 'all', 'pending', 'completed'), priority (optional).",
            "parameters": read_all_tasks_schema()
        },
        {
            "name": complete_task_name,
            "description": "Mark a task as completed in the user's task list. Use this when the user wants to mark a task as done. Parameters: user_id (required), task_id (required).",
            "parameters": complete_task_schema()
        },
        {
            "name": delete_task_name,
            "description": "Delete a task from the user's task list. Use this when the user wants to remove a task. Parameters: user_id (required), task_id (required).",
            "parameters": delete_task_schema()
        }
    ]

    # Initialize the model with tools
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=tools
    )

    # Start a chat with history
    chat = model.start_chat(history=gemini_history)

    # Send the message to Gemini - this will always generate a response from LLM
    response = chat.send_message(request.message)

    # Process the response - this comes directly from Gemini
    response_text = response.text
    tool_calls = []

    # Check if Gemini wants to call any tools
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

                # Add user_id to the parameters if not already present
                if 'user_id' not in args_dict:
                    args_dict['user_id'] = user_id

                # Add to tool calls
                tool_call = {
                    "type": function_name,
                    "params": args_dict
                }
                tool_calls.append(tool_call)

                # Execute the tool
                result = await execute_mcp_tool(function_name, db_session, **args_dict)
                # Feed the result back to Gemini for final response
                follow_up_response = chat.send_message(str(result))
                # Update the response text with the follow-up from Gemini
                response_text = follow_up_response.text

    # Check if user wants to update a task and Gemini didn't recognize it
    user_message_lower = request.message.lower()
    if "update" in user_message_lower and ("task" in user_message_lower or "change" in user_message_lower or "modify" in user_message_lower):
        # User wants to update a task but Gemini didn't call the update tool
        # Enter multi-step conversation mode
        conversation_states[conversation_key] = {
            "waiting_for": "task_selection_for_update"
        }

        # Get user's tasks to ask which one to update
        from mcp.read_all_tasks_tool import execute as read_all_tasks_execute
        all_tasks_result = await read_all_tasks_execute(db_session, user_id=user_id)

        if all_tasks_result.get("tasks"):
            response_text = "Which task would you like to update? Please specify the task name."
            tool_calls = []
        else:
            response_text = "You don't have any tasks to update. Would you like to add a new task instead?"
            tool_calls = []

    # Create assistant message
    assistant_message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=response_text  # This is always from Gemini
    )
    assistant_message = await message_service.create_message(assistant_message_data)

    # Create response
    response_obj = ChatResponse(
        conversation_id=str(conversation_id),
        response=response_text,  # This is always from Gemini
        tool_calls=[ToolCall(type=tc["type"], params=tc["params"]) for tc in tool_calls],
        timestamp=datetime.now().isoformat()
    )

    return response_obj