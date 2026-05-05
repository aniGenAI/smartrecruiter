from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.mysql import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter()


@router.post("/", response_model=JobResponse)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(
        title=payload.title,
        description=payload.description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.id.desc()).all()
