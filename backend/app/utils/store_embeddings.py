from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from backend.app.database.database import SessionLocal
from backend.app.models.document import Document
from backend.app.models.chunk import Chunk

from backend.app.utils.chunking import chunk_text


DOCUMENT_ID = 1


print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


with SessionLocal() as session:

    document = session.get(Document, DOCUMENT_ID)

    if document is None:
        raise ValueError(f"Document with id {DOCUMENT_ID} not found.")

    print(f"Processing document: {document.title}")

    chunks = chunk_text(document.content)

    print(f"Number of chunks: {len(chunks)}")

    embeddings = model.encode(
        chunks,
        show_progress_bar=True
    )

    print("Embeddings generated.")

    for index, (chunk_text_value, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        chunk = Chunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk_text_value,
            embedding=embedding.tolist()
        )

        session.add(chunk)

    session.commit()

    print(f"Stored {len(chunks)} chunks in PostgreSQL.")