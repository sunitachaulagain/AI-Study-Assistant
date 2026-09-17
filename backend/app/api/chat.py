import asyncio
from functools import partial

from fastapi import APIRouter, Depends

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.rag import answer_question
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.services.stats_service import record_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    loop = asyncio.get_event_loop()

    answer = await loop.run_in_executor(
        None,
        partial(
            answer_question,
            question=request.question,
            user_id=current_user.id
        )
    )

    await loop.run_in_executor(
        None,
        partial(record_question, user_id=current_user.id)
    )

    return ChatResponse(answer=answer)
