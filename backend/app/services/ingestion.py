from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.document import Document
from backend.app.models.chunk import Chunk
from backend.app.utils.chunking import (
    clean_text,
    split_sentences,
    chunk_text,
)
from backend.app.services.embedding_service import generate_embedding


def ingest_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Database session
    db: Session = SessionLocal()

    try:
        # Check whether this document has already been ingested
        existing_document = (
            db.query(Document)
            .filter(Document.file_path == str(path))
            .first()
        )

        if existing_document:
            print(
                f"Document already exists in database "
                f"(ID: {existing_document.id})."
            )
            print("Skipping ingestion.")
            return

        # Read PDF
        from pypdf import PdfReader

        reader = PdfReader(file_path)

        all_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                all_text += text + "\n"

        # Clean text
        cleaned_text = clean_text(all_text)

        # Split into sentences
        sentences = split_sentences(cleaned_text)

        # Create chunks
        chunks = chunk_text(
            sentences,
            chunk_size=500,
            overlap=100,
        )

        print(f"Extracted characters: {len(all_text)}")
        print(f"Cleaned characters: {len(cleaned_text)}")
        print(f"Sentences: {len(sentences)}")
        print(f"Chunks: {len(chunks)}")

        # Create document record
        document = Document(
            title=path.stem,
            file_path=str(path),
            content=cleaned_text,
        )

        db.add(document)
        db.flush()

        print(f"Document ID: {document.id}")

        # Generate embeddings and save chunks
        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(chunk)

            db_chunk = Chunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )

            db.add(db_chunk)

            if index % 10 == 0:
                print(f"Processed chunk {index}/{len(chunks)}")

        db.commit()

        print("Document ingestion completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    ingest_document(
        "uploads/AI_for_Road_Safety_in_Nepal_Reviewed.pdf"
    )