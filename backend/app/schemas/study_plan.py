from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class StudyPlanCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    subject: str
    due_date: date
    priority: str = "medium"
    estimated_hours: float = 1.0


class StudyPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    estimated_hours: Optional[float] = None


class StudyPlanResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = ""
    subject: str
    due_date: date
    priority: str
    status: str
    estimated_hours: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
