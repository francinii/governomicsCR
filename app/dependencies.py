from app.clients.groq_client import GroqClient
from app.services.chat_service import ChatService
from fastapi import Depends

def get_groq_client():
    return GroqClient()

def get_chat_service(groq_client: GroqClient = Depends(get_groq_client)):
    return ChatService(groq_client)
