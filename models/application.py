from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Float,
    ForeignKey,
    Enum,
    DateTime
)

from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class ApplicationStatus(str, enum.Enum):
    SAVED = "Saved"
    APPLIED = "Applied"
    OA = "OA"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    company = Column(String(100), nullable=False, index=True)

    role = Column(String(100), nullable=False)

    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.SAVED
    )

    jd_text = Column(Text, nullable=True)

    match_score = Column(Float, nullable=True)

    location = Column(String(100), nullable=True)

    applied_date = Column(Date, nullable=True)

    followup_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
class Note(Base):
    __tablename__ = "app_notes"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id")
    )

    content = Column(Text, nullable=False)

    ai_tag_suggestion = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application")
class StatusLog(Base):
    __tablename__ = "status_logs"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id")
    )

    old_status = Column(
        Enum(ApplicationStatus),
        nullable=True
    )

    new_status = Column(
        Enum(ApplicationStatus),
        nullable=False
    )

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    application = relationship("Application")