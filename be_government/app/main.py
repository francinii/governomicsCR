from fastapi import FastAPI
from app.api.v1.endpoints.__init__ import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/hello")
async def read_hello():
    """
    Test endpoint that returns a simple greeting message.
    """
    return {"message": "Hello from FastAPI in be_governments!"}
