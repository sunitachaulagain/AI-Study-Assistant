from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.user_stats import UserStats


def get_or_create_stats(
    user_id: int,
    db: Session
) -> UserStats:

    stats = (
        db.query(UserStats)
        .filter(UserStats.user_id == user_id)
        .first()
    )

    if stats:
        return stats

    stats = UserStats(
        user_id=user_id,
        questions_asked=0,
        quizzes_completed=0,
        total_quiz_score=0,
        total_quiz_questions=0
    )

    db.add(stats)
    db.commit()
    db.refresh(stats)

    return stats


def record_question(user_id: int):

    db = SessionLocal()

    try:
        stats = get_or_create_stats(
            user_id=user_id,
            db=db
        )

        stats.questions_asked += 1

        db.commit()

    finally:
        db.close()


def record_quiz_completion(
    user_id: int,
    score: int,
    total_questions: int
):

    db = SessionLocal()

    try:
        stats = get_or_create_stats(
            user_id=user_id,
            db=db
        )

        stats.quizzes_completed += 1

        stats.total_quiz_score += score

        stats.total_quiz_questions += total_questions

        db.commit()

    finally:
        db.close()


def get_dashboard_stats(user_id: int):

    db = SessionLocal()

    try:
        stats = get_or_create_stats(
            user_id=user_id,
            db=db
        )

        if stats.total_quiz_questions > 0:
            progress = (
                stats.total_quiz_score
                / stats.total_quiz_questions
            ) * 100
        else:
            progress = 0

        return {
            "questions_asked": stats.questions_asked,
            "quizzes_completed": stats.quizzes_completed,
            "study_progress": round(progress)
        }

    finally:
        db.close()