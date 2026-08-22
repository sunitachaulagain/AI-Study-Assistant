from fastapi import APIRouter

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.rag import answer_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = answer_question(
        question=request.question
    )

    return ChatResponse(
        answer=answer
    )