from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.api.deps import get_db, get_current_user
from backend.app.models.user import User
from backend.app.models.subject import Subject
from backend.app.models.document import Document


router = APIRouter(prefix="/subjects", tags=["Subjects"])


class SubjectCreate(BaseModel):
    name: str


class SubjectUpdate(BaseModel):
    name: str


@router.post("/")
def create_subject(
    request: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    name = request.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Subject name cannot be empty"
        )

    existing = (
        db.query(Subject)
        .filter(
            Subject.user_id == current_user.id,
            Subject.name == name
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="A subject with this name already exists"
        )

    subject = Subject(
        name=name,
        user_id=current_user.id
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    return {
        "id": subject.id,
        "name": subject.name,
        "created_at": subject.created_at.isoformat() if subject.created_at else None,
        "document_count": 0
    }


@router.get("/")
def list_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subjects = (
        db.query(Subject)
        .filter(Subject.user_id == current_user.id)
        .order_by(Subject.name)
        .all()
    )

    result = []
    for subject in subjects:
        doc_count = (
            db.query(func.count(Document.id))
            .filter(
                Document.user_id == current_user.id,
                Document.subject_id == subject.id
            )
            .scalar()
        )
        result.append({
            "id": subject.id,
            "name": subject.name,
            "created_at": subject.created_at.isoformat() if subject.created_at else None,
            "document_count": doc_count
        })

    return {"subjects": result}


@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    request: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subject = (
        db.query(Subject)
        .filter(
            Subject.id == subject_id,
            Subject.user_id == current_user.id
        )
        .first()
    )

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    name = request.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Subject name cannot be empty"
        )

    existing = (
        db.query(Subject)
        .filter(
            Subject.user_id == current_user.id,
            Subject.name == name,
            Subject.id != subject_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="A subject with this name already exists"
        )

    subject.name = name
    db.commit()
    db.refresh(subject)

    return {
        "id": subject.id,
        "name": subject.name,
        "created_at": subject.created_at.isoformat() if subject.created_at else None
    }


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subject = (
        db.query(Subject)
        .filter(
            Subject.id == subject_id,
            Subject.user_id == current_user.id
        )
        .first()
    )

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.subject_id == subject_id
    ).update({"subject_id": None})

    db.delete(subject)
    db.commit()

    return {"message": "Subject deleted successfully"}
