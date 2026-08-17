from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.chunk import Chunk
from backend.app.services.embedding_service import generate_embedding


def retrieve_chunks(
    query: str,
    top_k: int = 5
):
    db: Session = SessionLocal()

    try:
        query_embedding = generate_embedding(query)

        results = (
            db.query(Chunk)
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

    results = retrieve_chunks(query)

    print(f"\nQuery: {query}")
    print(f"Found {len(results)} relevant chunks\n")

    for i, chunk in enumerate(results, 1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print("\nContent:")
        print(chunk.content)