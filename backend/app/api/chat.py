import asyncio
from functools import partial

from fastapi import APIRouter, Depends

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.rag import answer_question
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.services.stats_service import record_question
from backend.app.database.database import SessionLocal
from backend.app.models.chat_message import ChatMessage


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def save_chat_messages(user_id: int, question: str, answer: str, subject_id: int = None):
    db = SessionLocal()
    try:
        db.add(ChatMessage(
            user_id=user_id,
            role="user",
            content=question,
            subject_id=subject_id
        ))
        db.add(ChatMessage(
            user_id=user_id,
            role="assistant",
            content=answer,
            subject_id=subject_id
        ))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    loop = asyncio.get_running_loop()

    answer = await loop.run_in_executor(
        None,
        partial(
            answer_question,
            question=request.question,
            user_id=current_user.id,
            subject_id=request.subject_id
        )
    )

    await loop.run_in_executor(
        None,
        partial(record_question, user_id=current_user.id)
    )

    await loop.run_in_executor(
        None,
        partial(
            save_chat_messages,
            user_id=current_user.id,
            question=request.question,
            answer=answer,
            subject_id=request.subject_id
        )
    )

    return ChatResponse(answer=answer)
