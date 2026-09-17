from pydantic import BaseModel
from typing import List


class QuizRequest(BaseModel):
    topic: str = ""


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


class QuizCompletionRequest(BaseModel):
    score: int
    total_questions: int