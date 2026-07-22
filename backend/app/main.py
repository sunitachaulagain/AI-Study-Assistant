from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"message" : "Welcome to AI study Assistant API"}


@app.get("/about")
def about():
    return {
        "Project" : "AI Study Assistant",
        "Version" : "1.0.0",
        "developer" : "Sunita"

    }

@app.get("/health")
def health():
    return {
        "status" : "server is running successfully!"
    }

@app.get("/documents/{document_id}")
def get_document(document_id: int):
    return {
        "document_id" : document_id,
        "message" : "Document found successfully"
    }

@app.get("/search")
def search(subject : str):
    return {
        "subject" : subject
    }


# post method

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question : str


class chatResponse(BaseModel):
    status : str
    answer : str

@app.post("/chat", response_model=chatResponse)
def chat(request : ChatRequest):
    return { 
        "status" : "success",
        "answer" : f" you asked : {request.question}"

    }
