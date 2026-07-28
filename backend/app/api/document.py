from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import session

from backend.app.database.database import SessionLocal
from backend.app.models.document import Document
from fastapi import Depends

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
    db : session = Depends(get_db)
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
def get_documents(db : session = Depends(get_db)):
    documents = db.query(Document).all()
    return {
        "documents" : documents
    }


# delete document
@router.delete("/documents/{document_id}")  
def delete_document(
    document_id : int,
    db: session = Depends(get_db)
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
    db: session = Depends(get_db)
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
  