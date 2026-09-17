from fastapi import APIRouter, Depends

from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.services.stats_service import get_dashboard_stats


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def dashboard_stats(
    current_user: User = Depends(get_current_user)
):

    return get_dashboard_stats(
        user_id=current_user.id
    )