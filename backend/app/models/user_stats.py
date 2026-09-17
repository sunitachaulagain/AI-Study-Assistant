from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    questions_asked: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    quizzes_completed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    total_quiz_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    total_quiz_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )