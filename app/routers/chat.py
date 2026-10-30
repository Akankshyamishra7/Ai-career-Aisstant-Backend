from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api", tags=["Career Chatbot"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_career_assistant(payload: ChatRequest):
    """
    AI Career Chatbot answering questions related to jobs, resume improvement,
    skill development, and interview readiness.
    """
    return await ai_service.chat(
        user_message=payload.message,
        context=payload.context,
        chat_history=payload.chat_history
    )
