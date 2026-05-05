from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.mysql import get_db

from app.services.LLM.ollama_service import ollama_service
from app.services.LLM.mistral_service import mistral_service
from app.schemas.evaluation import EvaluationResponse
from app.services.evaluation_service import evaluation_service

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.post("/test-llm")
def test_llm(payload: PromptRequest):
    #result = ollama_service.generate(payload.prompt)
    result = mistral_service.generate(payload.prompt)
    return {
        "response": result
    }

@router.post("/{candidate_id}/{job_id}", response_model=EvaluationResponse)
def evaluate_candidate(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    result = evaluation_service.evaluate_candidate(candidate_id, job_id, db)

    if not result:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")

    return result