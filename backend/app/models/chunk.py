from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from pgvector.sqlalchemy import Vector

from backend.app.database.database import Base


class Chunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False
    )