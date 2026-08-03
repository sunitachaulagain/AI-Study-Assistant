from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.models.document import Document

import os

router = APIRouter()


# helper function
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()    

class DocumentRequest(BaseModel):
    title : str

# create data(insert in database)
@router.post("/documents")
def create_document(
    document : DocumentRequest,
    db : Session = Depends(get_db)
    ):

    db_document = Document(
        title = document.title
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return {
        "message" : "Document created successfully! ",
        "documents" : db_document
    }


# return data from database
@router.get("/documents/{document_id}")
def get_documents(db : Session = Depends(get_db)):
    documents = db.query(Document).all()
    return {
        "documents" : documents
    }


# delete document
@router.delete("/documents/{document_id}")  
def delete_document(
    document_id : int,
    db: Session = Depends(get_db)
     ):

    db_document = (
         db.query(Document)
         .filter(Document.id == document_id)
         .first()
    )     

    db.delete(db_document)
    db.commit()
    return {
            "message" : "Document deleted successfully",
            }
 

# update document
@router.put("/documents/{document_id}")
def update_document(
    document_id : int, 
    document : DocumentRequest,
    db: Session = Depends(get_db)
    ):

    db_document = (
        db.query(Document).filter(Document.id == document_id).first()
    )

    if db_document is None:
            return {
                "message" : "Document not found"
            }

    db_document.title = document.title
    db.commit()
    db.refresh(db_document)

    return {
            "message" : "Document updated successfully",
            "document" : db_document
            }


@router.post("/upload")
async def upload_pdf(
    file : UploadFile = File(...),
    db : Session = Depends(get_db)
):
    contents = await file.read()
    file_path = os.path.join("uploads", file.filename)
    print(file_path)

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    new_document = Document(
        title = file.filename,
        file_path = file_path
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return{
        "message" : "PDF upload successfully!",
        "documeny" : {
            "id" : new_document.id,
            "title" : new_document.title,
            "file_path" : new_document.file_path
        }
    }
