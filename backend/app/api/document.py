from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_current_user
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.models.document import Document

from pypdf import PdfReader

import os

router = APIRouter()
 

class DocumentRequest(BaseModel):
    title : str

# # create data(insert in database)
# @router.post("/documents")
# def create_document(
#     document: DocumentRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

#     db_document = Document(
#     title=document.title,
#     user_id=current_user.id
# )

#     db.add(db_document)
#     db.commit()
#     db.refresh(db_document)

#     return {
#         "message" : "Document created successfully! ",
#         "documents" : db_document
#     }


# return data from database
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

# return document with document id
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

    db.delete(db_document)
    db.commit()

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

# upload document
@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Read uploaded file
    contents = await file.read()

    # Decide where to save it
    file_path = os.path.join("uploads", file.filename)

    # Save it to disk
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Open the saved PDF
    reader = PdfReader(file_path)

    # Extract all text
    all_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            all_text += text + "\n"

    # Save document to database
    new_document = Document(
        title=file.filename,
        file_path=file_path,
        content=all_text,
        user_id=current_user.id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "PDF upload successfully!",
        "document": {
            "id": new_document.id,
            "title": new_document.title,
            "file_path": new_document.file_path,
            "user_id": new_document.user_id
        }
    }