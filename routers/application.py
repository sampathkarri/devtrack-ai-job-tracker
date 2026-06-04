from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from models.application import (
    Application,
    Note,
    StatusLog
)
from models.user import User

from schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    NoteCreate
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    return applications
from fastapi import HTTPException
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
from schemas.application import (
    ApplicationCreate,
    ApplicationUpdate
)
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
@router.post("/{application_id}/notes")
def add_note(
    application_id: int,
    note_data: NoteCreate,
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

    note = Note(
        application_id=application.id,
        content=note_data.content
    )

    db.add(note)

    db.commit()

    db.refresh(note)

    return {
        "message": "Note added successfully",
        "note_id": note.id
    }
@router.get("/{application_id}/notes")
def get_notes(
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

    notes = db.query(Note).filter(
        Note.application_id == application_id
    ).all()

    return notes
from schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    NoteCreate,
    StatusUpdate
)
@router.post("/{application_id}/status")
def update_status(
    application_id: int,
    status_data: StatusUpdate,
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

    old_status = application.status

    application.status = status_data.new_status

    status_log = StatusLog(
        application_id=application.id,
        old_status=old_status,
        new_status=status_data.new_status
    )

    db.add(status_log)

    db.commit()

    return {
        "message": "Status updated successfully"
    }