from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class CandidateCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    resume_text: Optional[str] = None


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
    created_at: datetime
    status: str

    class Config:
        from_attributes = True