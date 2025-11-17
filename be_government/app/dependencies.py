from app.services.chat_service import ChatService
from fastapi import Depends

def get_chat_service():
    return ChatService()
