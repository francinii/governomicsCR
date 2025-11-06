from fastapi import APIRouter
from .chat_endpoints import router as chat_router

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/pib-chat", tags=["pib-chat"])
