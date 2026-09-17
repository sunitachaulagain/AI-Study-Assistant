from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_current_user
from backend.app.models.user import User
from backend.app.models.document import Document
from backend.app.models.chunk import Chunk

from backend.app.services.chunking import chunk_text
from backend.app.services.embedding_service import generate_embeddings_batch

from pypdf import PdfReader

import os


router = APIRouter()


class DocumentRequest(BaseModel):
    title: str


@router.get("/documents")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .all()
    )

    return {
        "documents": documents
    }


@router.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "document": document
    }


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete associated chunks first
    db.query(Chunk).filter(
        Chunk.document_id == document_id
    ).delete(
        synchronize_session=False
    )

    # Delete document from database
    db.delete(db_document)

    db.commit()

    # Delete physical PDF file if it exists
    if db_document.file_path and os.path.exists(db_document.file_path):
        os.remove(db_document.file_path)

    return {
        "message": "Document deleted successfully"
    }


@router.put("/documents/{document_id}")
def update_document(
    document_id: int,
    document: DocumentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if db_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db_document.title = document.title

    db.commit()
    db.refresh(db_document)

    return {
        "message": "Document updated successfully",
        "document": db_document
    }


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Make sure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # Read uploaded file
    contents = await file.read()

    # Save PDF
    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:
        # Extract text from PDF
        reader = PdfReader(file_path)

        all_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                all_text += text + "\n"

        all_text = all_text.strip()

        if not all_text:
            os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        # Create document
        new_document = Document(
            title=file.filename,
            file_path=file_path,
            content=all_text,
            user_id=current_user.id
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        # Split document into chunks
        chunks = chunk_text(all_text)

        if not chunks:
            db.delete(new_document)
            db.commit()

            os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail="Could not create text chunks from this document."
            )

        # Create embeddings in batch and save chunks
        embeddings = generate_embeddings_batch(chunks)

        for index, (chunk_content, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            new_chunk = Chunk(
                document_id=new_document.id,
                chunk_index=index,
                content=chunk_content,
                embedding=embedding
            )
            db.add(new_chunk)

        db.commit()

        return {
            "message": "PDF uploaded and processed successfully!",
            "document": {
                "id": new_document.id,
                "title": new_document.title,
                "file_path": new_document.file_path,
                "user_id": new_document.user_id
            },
            "chunks_created": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()

        # Remove partially created document
        if "new_document" in locals() and new_document.id:
            existing_document = (
                db.query(Document)
                .filter(Document.id == new_document.id)
                .first()
            )

            if existing_document:
                db.delete(existing_document)
                db.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(error)}"
        )