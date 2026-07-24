from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

documents = []

class DocumentRequest(BaseModel):
    title : str


@router.post("/documents")
def create_document(document : DocumentRequest):
    documents.append(document.title)

    return { 
        "message" : "Document created successfully! ",
        "documents" : documents
    }

@router.get("/documents")
def get_documents():
    return {
        "documents" : documents
    }