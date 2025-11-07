from fastapi import APIRouter, Depends, HTTPException
from app.services.chat_service import ChatService
from app.dependencies import get_chat_service
from app.models.chat_models import ChatRequest, ChatResponse


router = APIRouter()
@router.post("/chat", response_model=ChatResponse)
async def chat_with_pib_pandasai(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        response = chat_service.process_chat_query(request.query)
        return ChatResponse(response=response)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



@router.post("/chat-report", response_model=ChatResponse)
async def chat_with_pib_pandasai(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        response = chat_service.process_chat_report(request.query)
        return ChatResponse(response=response)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/analysis_metrics", response_model=ChatResponse)
async def chat_analysis_metrics(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        response = chat_service.process_chat_analysis_metrics(request.query)
        return ChatResponse(response=response)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

