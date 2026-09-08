from fastapi import APIRouter, Depends

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.rag import answer_question
from backend.app.api.deps import get_current_user
from backend.app.models.user import User


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    answer = answer_question(
        question=request.question,
        user_id=current_user.id
    )

    return ChatResponse(
        answer=answer
    )