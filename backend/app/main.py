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