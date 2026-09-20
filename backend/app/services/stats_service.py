from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database.database import SessionLocal
from backend.app.models.user_stats import UserStats
from backend.app.models.document import Document
from backend.app.models.chunk import Chunk
from backend.app.models.subject import Subject


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

        # Per-subject document and chunk counts
        subject_rows = (
            db.query(
                Subject.id,
                Subject.name,
                func.count(Document.id).label("doc_count")
            )
            .outerjoin(
                Document,
                (Document.subject_id == Subject.id)
                & (Document.user_id == user_id)
            )
            .filter(Subject.user_id == user_id)
            .group_by(Subject.id, Subject.name)
            .all()
        )

        subject_stats = []
        for row in subject_rows:
            chunk_count = (
                db.query(func.count(Chunk.id))
                .join(Document, Chunk.document_id == Document.id)
                .filter(
                    Document.user_id == user_id,
                    Document.subject_id == row.id
                )
                .scalar()
            )
            subject_stats.append({
                "subject_id": row.id,
                "subject_name": row.name,
                "document_count": row.doc_count,
                "chunk_count": chunk_count
            })

        # Unassigned documents count
        unassigned_doc_count = (
            db.query(func.count(Document.id))
            .filter(
                Document.user_id == user_id,
                Document.subject_id.is_(None)
            )
            .scalar()
        )

        unassigned_chunk_count = (
            db.query(func.count(Chunk.id))
            .join(Document, Chunk.document_id == Document.id)
            .filter(
                Document.user_id == user_id,
                Document.subject_id.is_(None)
            )
            .scalar()
        )

        return {
            "questions_asked": stats.questions_asked,
            "quizzes_completed": stats.quizzes_completed,
            "study_progress": round(progress),
            "subject_stats": subject_stats,
            "unassigned_documents": unassigned_doc_count,
            "unassigned_chunks": unassigned_chunk_count
        }

    finally:
        db.close()