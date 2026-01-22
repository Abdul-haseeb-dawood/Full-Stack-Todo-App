"""
API router for the Gemini Agent functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.agents.gemini_agent import GeminiAgent
from app.core.settings import settings


router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQueryRequest(BaseModel):
    """Request model for agent queries"""
    user_id: str
    query: str
    conversation_id: Optional[str] = None


class ToolCall(BaseModel):
    """Model for representing tool calls made by the agent"""
    name: str
    arguments: Dict[str, Any]


class AgentQueryResponse(BaseModel):
    """Response model for agent queries"""
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]
    status: str


@router.post("/query", response_model=AgentQueryResponse)
async def query_agent(
    request: AgentQueryRequest,
    db_session: AsyncSession = Depends(get_async_session)
):
    """
    Query the Gemini agent for intelligent responses
    """
    try:
        # Validate inputs
        if not request.user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not request.query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Create an instance of the agent
        agent = GeminiAgent(api_key=settings.gemini_api_key)
        
        # Process the query
        result = await agent.process_query(
            query=request.query,
            user_id=request.user_id,
            db_session=db_session
        )
        
        # Generate or use provided conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        return AgentQueryResponse(
            conversation_id=conversation_id,
            response=result["response"],
            tool_calls=[ToolCall(name=call["name"], arguments=call["arguments"]) for call in result["tool_calls"]],
            status=result["status"]
        )
    
    except ValueError as ve:
        # This would happen if the API key is not configured
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/reset-conversation/{conversation_id}")
async def reset_conversation(conversation_id: str):
    """
    Reset the conversation history for a specific conversation
    """
    try:
        # Create an instance of the agent
        agent = GeminiAgent(api_key=settings.gemini_api_key)
        
        # Reset the conversation
        agent.reset_conversation()
        
        return {"message": f"Conversation {conversation_id} has been reset"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset conversation: {str(e)}")


@router.get("/available-models")
async def get_available_models():
    """
    Get a list of available Gemini models
    """
    try:
        agent = GeminiAgent(api_key=settings.gemini_api_key)
        models = await agent.get_available_models()
        return {"models": models}
    
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get available models: {str(e)}")