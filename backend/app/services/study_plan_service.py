from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database.database import SessionLocal
from backend.app.models.study_plan import StudyPlan


def create_plan(user_id: int, data: dict) -> dict:
    db = SessionLocal()
    try:
        plan = StudyPlan(
            user_id=user_id,
            title=data["title"],
            description=data.get("description", ""),
            subject=data["subject"],
            due_date=data["due_date"],
            priority=data.get("priority", "medium"),
            status="pending",
            estimated_hours=data.get("estimated_hours", 1.0),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return _plan_to_dict(plan)
    finally:
        db.close()


def get_user_plans(user_id: int) -> list:
    db = SessionLocal()
    try:
        plans = (
            db.query(StudyPlan)
            .filter(StudyPlan.user_id == user_id)
            .order_by(StudyPlan.due_date.asc())
            .all()
        )
        return [_plan_to_dict(p) for p in plans]
    finally:
        db.close()


def get_plan(user_id: int, plan_id: int) -> dict | None:
    db = SessionLocal()
    try:
        plan = (
            db.query(StudyPlan)
            .filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            )
            .first()
        )
        return _plan_to_dict(plan) if plan else None
    finally:
        db.close()


def update_plan(user_id: int, plan_id: int, data: dict) -> dict | None:
    db = SessionLocal()
    try:
        plan = (
            db.query(StudyPlan)
            .filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            )
            .first()
        )

        if not plan:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(plan, key, value)

        plan.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(plan)
        return _plan_to_dict(plan)
    finally:
        db.close()


def delete_plan(user_id: int, plan_id: int) -> bool:
    db = SessionLocal()
    try:
        plan = (
            db.query(StudyPlan)
            .filter(
                StudyPlan.id == plan_id,
                StudyPlan.user_id == user_id
            )
            .first()
        )

        if not plan:
            return False

        db.delete(plan)
        db.commit()
        return True
    finally:
        db.close()


def get_plan_stats(user_id: int) -> dict:
    db = SessionLocal()
    try:
        plans = (
            db.query(StudyPlan)
            .filter(StudyPlan.user_id == user_id)
            .all()
        )

        status_counts = {"pending": 0, "in_progress": 0, "completed": 0}
        subject_counts = {}
        total_hours = 0.0

        for plan in plans:
            if plan.status in status_counts:
                status_counts[plan.status] += 1

            subject_counts[plan.subject] = (
                subject_counts.get(plan.subject, 0) + 1
            )

            total_hours += plan.estimated_hours

        return {
            "total": len(plans),
            "status_counts": status_counts,
            "subject_counts": subject_counts,
            "total_estimated_hours": round(total_hours, 1)
        }
    finally:
        db.close()


def _plan_to_dict(plan: StudyPlan) -> dict:
    return {
        "id": plan.id,
        "user_id": plan.user_id,
        "title": plan.title,
        "description": plan.description or "",
        "subject": plan.subject,
        "due_date": plan.due_date.isoformat(),
        "priority": plan.priority,
        "status": plan.status,
        "estimated_hours": plan.estimated_hours,
        "created_at": plan.created_at.isoformat(),
        "updated_at": plan.updated_at.isoformat()
    }
