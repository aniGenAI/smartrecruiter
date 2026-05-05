from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class EvaluationResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    fit_score: Optional[float]
    confidence_score: Optional[float]
    recommendation: Optional[str]
    evaluation_data: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True