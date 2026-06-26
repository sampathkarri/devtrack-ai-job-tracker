from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from models.application import Application
from models.user import User

from services.auth_service import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    total = len(applications)

    saved = 0
    applied = 0
    oa = 0
    interview = 0
    offer = 0
    rejected = 0

    for app in applications:

        if app.status.value == "Saved":
            saved += 1

        elif app.status.value == "Applied":
            applied += 1

        elif app.status.value == "OA":
            oa += 1

        elif app.status.value == "Interview":
            interview += 1

        elif app.status.value == "Offer":
            offer += 1

        elif app.status.value == "Rejected":
            rejected += 1

    return {
        "total_applications": total,
        "saved": saved,
        "applied": applied,
        "oa": oa,
        "interview": interview,
        "offer": offer,
        "rejected": rejected
    }