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


@router.delete("/documents/{document_id}")  
def delete_document(document_id : int):
    for document in documents:
        if document["id"] == document_id:
            documents.remove(document)

            return {
                "message" : "Document deleted successfully",
                "deleted_document" : document
            }

    return{
        "message" : "Document not found"
    }    


@router.put("/documents/{document_id}")
def update_document(document_id : int, document : DocumentRequest):
    for existing_document in documents:
        if existing_document["id"] == document_id:
            existing_document["title"] = document.title

            return {
                "message" : "Document updated successfully",
                "document" : existing_document
            }

    return { 
        "message" : "Document not found"
    }    