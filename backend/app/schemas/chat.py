from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    question: str
    subject_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str