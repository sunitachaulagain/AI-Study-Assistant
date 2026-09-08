from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.chunk import Chunk
from backend.app.models.document import Document
from backend.app.services.embedding_service import generate_embedding


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
    query = "What are the main causes of road accidents in Nepal?"

    # Test with an existing user
    user_id = 3

    results = retrieve_chunks(
        query,
        user_id=user_id
    )

    print(f"\nQuery: {query}")
    print(f"User ID: {user_id}")
    print(f"Found {len(results)} relevant chunks\n")

    for i, chunk in enumerate(results, 1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print("\nContent:")
        print(chunk.content)