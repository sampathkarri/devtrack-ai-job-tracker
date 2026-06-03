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
