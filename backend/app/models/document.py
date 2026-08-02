from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title : Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    file_path : Mapped[str] = mapped_column(
        String,
        nullable=False
    )
