from pydantic import BaseModel
from typing import Optional


class ApplicationCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    jd_text: Optional[str] = None
class ApplicationUpdate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    jd_text: Optional[str] = None
class NoteCreate(BaseModel):
    content: str
from models.application import ApplicationStatus

class StatusUpdate(BaseModel):
    new_status: ApplicationStatus
class MatchRequest(BaseModel):
    resume_text: str
    job_description: str