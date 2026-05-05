from fastapi import APIRouter
from app.api.routes import candidate, job, interview, evaluation

api_router = APIRouter()

api_router.include_router(candidate.router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(job.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(interview.router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(evaluation.router, prefix="/evaluations", tags=["Evaluations"])