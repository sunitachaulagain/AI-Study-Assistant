import asyncio
from functools import partial

from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_current_user
from backend.app.models.user import User

from backend.app.schemas.quiz import (
    QuizRequest,
    QuizResponse,
    QuizCompletionRequest
)

from backend.app.services.quiz_service import generate_quiz
from backend.app.services.stats_service import record_quiz_completion


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.post("/", response_model=QuizResponse)
async def create_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_user)
):

    loop = asyncio.get_event_loop()

    questions = await loop.run_in_executor(
        None,
        partial(
            generate_quiz,
            user_id=current_user.id,
            topic=request.topic,
            subject_id=request.subject_id
        )
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No relevant study material found in your documents."
        )

    return {
        "questions": questions
    }


@router.post("/complete")
async def complete_quiz(
    request: QuizCompletionRequest,
    current_user: User = Depends(get_current_user)
):

    if request.total_questions <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total questions must be greater than zero."
        )

    if request.score < 0:
        raise HTTPException(
            status_code=400,
            detail="Score cannot be negative."
        )

    if request.score > request.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Score cannot be greater than total questions."
        )

    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        None,
        partial(
            record_quiz_completion,
            user_id=current_user.id,
            score=request.score,
            total_questions=request.total_questions
        )
    )

    return {
        "message": "Quiz completion recorded successfully."
    }
