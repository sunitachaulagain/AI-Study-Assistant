import logging

from backend.app.database.database import Base, engine

from backend.app.models.document import Document
from backend.app.models.chunk import Chunk
from backend.app.models.user import User

logger = logging.getLogger(__name__)

logger.info("Creating database tables...")

Base.metadata.create_all(bind=engine)

logger.info("Database tables created successfully.")