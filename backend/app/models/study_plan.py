from datetime import date, datetime
from sqlalchemy import ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True,
        default=""
    )

    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending"
    )

    estimated_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
