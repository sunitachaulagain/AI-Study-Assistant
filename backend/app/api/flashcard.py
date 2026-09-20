import asyncio
import re
from functools import partial

from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_current_user
from backend.app.models.user import User

from backend.app.schemas.flashcard import (
    FlashcardRequest,
    FlashcardResponse,
    FlashcardItem,
)

from backend.app.services.flashcard_service import generate_flashcards
from backend.app.database.database import SessionLocal
from backend.app.models.chat_message import ChatMessage


router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"]
)


def shorten_answer(text: str, max_sentences: int = 2) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    shortened = ' '.join(sentences[:max_sentences])
    if len(sentences) > max_sentences:
        shortened += '...'
    return shortened


@router.get("/history", response_model=FlashcardResponse)
def get_flashcard_history(
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        messages = (
            db.query(ChatMessage)
            .filter(
                ChatMessage.user_id == current_user.id,
                ChatMessage.role == "assistant"
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(20)
            .all()
        )

        cards = []
        for msg in messages:
            # Get the corresponding user question
            user_msg = (
                db.query(ChatMessage)
                .filter(
                    ChatMessage.user_id == current_user.id,
                    ChatMessage.role == "user",
                    ChatMessage.created_at <= msg.created_at
                )
                .order_by(ChatMessage.created_at.desc())
                .first()
            )

            if user_msg:
                cards.append(FlashcardItem(
                    front=user_msg.content,
                    back=shorten_answer(msg.content)
                ))

        return {"cards": cards}
    finally:
        db.close()


@router.post("/", response_model=FlashcardResponse)
async def create_flashcards(
    request: FlashcardRequest,
    current_user: User = Depends(get_current_user)
):

    loop = asyncio.get_running_loop()

    cards = await loop.run_in_executor(
        None,
        partial(
            generate_flashcards,
            user_id=current_user.id,
            topic=request.topic,
            number_of_cards=request.number_of_cards,
            subject_id=request.subject_id
        )
    )

    if not cards:
        raise HTTPException(
            status_code=404,
            detail="No relevant study material found in your documents."
        )

    return {
        "cards": cards
    }
