from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    sender: str
    content: str
    timestamp: str

class UserResponse(BaseModel):
    id: int
    username: str