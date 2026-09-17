from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.deps import get_current_user
from backend.app.models.user import User

from backend.app.schemas.study_plan import (
    StudyPlanCreate,
    StudyPlanUpdate,
    StudyPlanResponse
)

from backend.app.services.study_plan_service import (
    create_plan,
    get_user_plans,
    get_plan,
    update_plan,
    delete_plan,
    get_plan_stats
)


router = APIRouter(
    prefix="/study-plans",
    tags=["Study Plans"]
)


@router.post("/", response_model=StudyPlanResponse)
def create_study_plan(
    request: StudyPlanCreate,
    current_user: User = Depends(get_current_user)
):

    if not request.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required."
        )

    if not request.subject.strip():
        raise HTTPException(
            status_code=400,
            detail="Subject is required."
        )

    if request.priority not in ("low", "medium", "high"):
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium, or high."
        )

    if request.estimated_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Estimated hours must be greater than zero."
        )

    return create_plan(
        user_id=current_user.id,
        data=request.model_dump()
    )


@router.get("/", response_model=list[StudyPlanResponse])
def list_study_plans(
    current_user: User = Depends(get_current_user)
):
    return get_user_plans(user_id=current_user.id)


@router.get("/stats")
def study_plan_stats(
    current_user: User = Depends(get_current_user)
):
    return get_plan_stats(user_id=current_user.id)


@router.get("/{plan_id}", response_model=StudyPlanResponse)
def get_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user)
):
    plan = get_plan(
        user_id=current_user.id,
        plan_id=plan_id
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Study plan not found."
        )

    return plan


@router.put("/{plan_id}", response_model=StudyPlanResponse)
def update_study_plan(
    plan_id: int,
    request: StudyPlanUpdate,
    current_user: User = Depends(get_current_user)
):
    update_data = request.model_dump(exclude_unset=True)

    if "priority" in update_data:
        if update_data["priority"] not in ("low", "medium", "high"):
            raise HTTPException(
                status_code=400,
                detail="Priority must be low, medium, or high."
            )

    if "status" in update_data:
        if update_data["status"] not in ("pending", "in_progress", "completed"):
            raise HTTPException(
                status_code=400,
                detail="Status must be pending, in_progress, or completed."
            )

    if "estimated_hours" in update_data:
        if update_data["estimated_hours"] <= 0:
            raise HTTPException(
                status_code=400,
                detail="Estimated hours must be greater than zero."
            )

    plan = update_plan(
        user_id=current_user.id,
        plan_id=plan_id,
        data=update_data
    )

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Study plan not found."
        )

    return plan


@router.delete("/{plan_id}")
def delete_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user)
):
    success = delete_plan(
        user_id=current_user.id,
        plan_id=plan_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Study plan not found."
        )

    return {"message": "Study plan deleted successfully."}
