import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
import uuid
from app.db.mysql import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import candidate_service
from app.services.resume_processor import process_resume

router = APIRouter()


@router.post("/", response_model=CandidateResponse)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    return candidate_service.create_candidate(payload, db)


@router.get("/", response_model=list[CandidateResponse])
def list_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).order_by(Candidate.id.desc()).all()

@router.post("/upload-resume", response_model=CandidateResponse)
def upload_resume(
    background_tasks: BackgroundTasks,
    full_name: str = Form(...),
    email: str = Form(None),
    phone: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = "uploads/resumes"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    candidate = Candidate(
        full_name=full_name,
        email=email,
        phone=phone,
        resume_file=file_path,
        status="processing"
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    background_tasks.add_task(process_resume, candidate.id, file_path)

    return candidate