from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.chat_service import ChatService
from app.dependencies import get_chat_service
from app.models.chat_models import ChatRequest, ChatResponse


router = APIRouter()

@router.post("/report", response_model=ChatResponse)
async def chat_report(
    request: Request,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    # Apply rate limiting using the limiter from app state

    try:
        response = chat_service.report_generation(chat_request.question)
        return ChatResponse(response=response)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/general_information", response_model=ChatResponse)
async def chat_general_information(
    request: Request,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        response = chat_service.general_information(chat_request.question)
        return ChatResponse(response=response)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")