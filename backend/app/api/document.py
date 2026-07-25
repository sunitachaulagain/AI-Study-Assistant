from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

documents = []
next_id = 1

class DocumentRequest(BaseModel):
    title : str


@router.post("/documents")
def create_document(document : DocumentRequest):
    global next_id

    new_document = {
        "id" : next_id,
        "title" : document.title
    }

    documents.append(new_document)
    next_id += 1

    return {
        "message" : "Document created successfully! ",
        "documents" : documents
    }


@router.get("/documents/{document_id}")
def get_documents(document_id : int):
    for document in documents:
        if document["id"] == document_id:
            return document
    return {
        "message" : "Document not found"
    }