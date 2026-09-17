import logging

from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.chunk import Chunk
from backend.app.models.document import Document
from backend.app.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)


def retrieve_chunks(
    query: str,
    user_id: int,
    top_k: int = 5
):
    db: Session = SessionLocal()

    try:
        query_embedding = generate_embedding(query)

        results = (
            db.query(Chunk)
            .join(Document, Chunk.document_id == Document.id)
            .filter(Document.user_id == user_id)
            .order_by(
                Chunk.embedding.cosine_distance(query_embedding)
            )
            .limit(top_k)
            .all()
        )

        return results

    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    query = "What are the main causes of road accidents in Nepal?"

    # Test with an existing user
    user_id = 3

    results = retrieve_chunks(
        query,
        user_id=user_id
    )

    logger.info(f"Query: {query}")
    logger.info(f"User ID: {user_id}")
    logger.info(f"Found {len(results)} relevant chunks")

    for i, chunk in enumerate(results, 1):
        logger.info(f"Result {i} | Document ID: {chunk.document_id} | Chunk index: {chunk.chunk_index}")
        logger.debug(f"Content: {chunk.content}")