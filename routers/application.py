from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.application import Application
from models.user import User

from schemas.application import (
    ApplicationCreate,
    ApplicationUpdate
)

from services.auth_service import get_current_user


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_application = Application(
        company=application.company,
        role=application.role,
        location=application.location,
        jd_text=application.jd_text,
        user_id=current_user.id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application created successfully",
        "application_id": new_application.id
    }


@router.get("/")
def get_applications(
    search: str = "",
    status: str = "",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Application).filter(
        Application.user_id == current_user.id
    )

    # Search by company
    if search:
        query = query.filter(
            Application.company.ilike(f"%{search}%")
        )

    # Filter by status
    if status:
        query = query.filter(
            Application.status == status
        )

    # Pagination
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    skip = (page - 1) * limit

    applications = query.offset(skip).limit(limit).all()

    return applications


@router.get("/{application_id}")
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.put("/{application_id}")
def update_application(
    application_id: int,
    updated_data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.company = updated_data.company
    application.role = updated_data.role
    application.location = updated_data.location
    application.jd_text = updated_data.jd_text

    db.commit()
    db.refresh(application)

    return {
        "message": "Application updated successfully"
    }


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }