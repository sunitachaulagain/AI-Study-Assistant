from backend.app.database.database import Base, engine

from backend.app.models.document import Document
from backend.app.models.chunk import Chunk


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")