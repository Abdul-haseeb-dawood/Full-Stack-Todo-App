from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add the backend directory to the Python path to import from mcp
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, backend_dir)

from mcp.agent import get_gemini_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the Gemini agent that can interact with the todo app
    """
    try:
        response = await get_gemini_response(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")