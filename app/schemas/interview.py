from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str
    transcript: Optional[List[Dict[str, Any]]]
    created_at: datetime

    class Config:
        from_attributes = True