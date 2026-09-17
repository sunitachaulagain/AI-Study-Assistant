import logging
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
from backend.app.services.embedding_service import generate_embeddings_batch

logger = logging.getLogger(__name__)


def ingest_document(file_path: str, user_id: int):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    db: Session = SessionLocal()

    try:
        # Check whether this document already exists
        existing_document = (
            db.query(Document)
            .filter(Document.file_path == str(path))
            .first()
        )

        # If the document exists, use it instead of creating a duplicate
        if existing_document:
            document = existing_document

            # Make sure the document belongs to the current user
            if document.user_id != user_id:
                raise ValueError(
                    "This document belongs to another user."
                )

            logger.info(
                f"Document already exists in database "
                f"(ID: {document.id})."
            )

            # Check whether chunks already exist
            existing_chunks = (
                db.query(Chunk)
                .filter(Chunk.document_id == document.id)
                .count()
            )

            if existing_chunks > 0:
                logger.info(
                    f"Document already has {existing_chunks} chunks."
                )
                logger.info("Skipping ingestion.")
                return

            logger.info("No chunks found. Processing existing document...")

        else:
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

            # Create document record
            document = Document(
                title=path.stem,
                file_path=str(path),
                content=cleaned_text,
                user_id=user_id,
            )

            db.add(document)
            db.flush()

            logger.info(f"Created new document. ID: {document.id}")

        # If existing document has content, use it
        if document.content:
            cleaned_text = document.content

        else:
            # Read PDF if content is empty
            from pypdf import PdfReader

            reader = PdfReader(file_path)

            all_text = ""

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    all_text += text + "\n"

            cleaned_text = clean_text(all_text)

            document.content = cleaned_text

        # Split into sentences
        sentences = split_sentences(cleaned_text)

        # Create chunks
        chunks = chunk_text(
            sentences,
            chunk_size=500,
            overlap=100,
        )

        logger.info(f"Extracted/processed characters: {len(cleaned_text)}")
        logger.info(f"Sentences: {len(sentences)}")
        logger.info(f"Chunks: {len(chunks)}")

        # Generate embeddings in batch and save chunks
        embeddings = generate_embeddings_batch(chunks)

        for index, (chunk_content, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            db_chunk = Chunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk_content,
                embedding=embedding,
            )
            db.add(db_chunk)

            if index % 10 == 0:
                logger.debug(
                    f"Processed chunk {index}/{len(chunks)}"
                )

        db.commit()

        logger.info("Document ingestion completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    ingest_document(
        "uploads/chapter 1.pptx.pdf",
        user_id=3
    )