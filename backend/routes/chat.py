from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse
from services.gemini import generate_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        reply = generate_response(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
