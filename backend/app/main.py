import logging

from fastapi import FastAPI
from backend.app.api import document, auth

from backend.app.database.database import Base, engine
from backend.app.models.document import Document
from backend.app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.quiz import router as quiz_router
from backend.app.models.user_stats import UserStats
from backend.app.models.study_plan import StudyPlan
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.study_plan import router as study_plan_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)
app.include_router(document.router)
app.include_router(quiz_router)
app.include_router(dashboard_router)
app.include_router(study_plan_router)



@app.get("/")
def home():
    return {"message": "Welcome to AI study Assistant API"}
