from fastapi import APIRouter
from models.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        reply=f"Mock response to: {request.message}"
    )
