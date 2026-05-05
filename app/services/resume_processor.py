from sqlalchemy.orm import Session

from app.db.mysql import SessionLocal
from app.models.candidate import Candidate
from app.agents.parser_agent import parser_agent
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
from app.util.pdf import extract_pdf_text


def process_resume(candidate_id: int, file_path: str):
    db: Session = SessionLocal()

    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

        if not candidate:
            return

        # Step 1: Extract PDF text
        resume_text = extract_pdf_text(file_path)
        print("extraction complted")
        # Step 2: Parse candidate
        parsed_data = parser_agent.parse_resume(resume_text)
        print("parsing completed")
        # Step 3: Update candidate
        candidate.resume_text = resume_text
        candidate.parsed_data = parsed_data
        candidate.status = "completed"

        db.commit()
        db.refresh(candidate)

        # Step 4: Store embedding
        embedding_text = " ".join([
            resume_text,
            " ".join(parsed_data.get("skills", [])),
            parsed_data.get("experience_summary", "")
        ])

        vector = embedding_service.encode(embedding_text)

        qdrant_service.upsert_candidate_embedding(
            candidate_id=candidate.id,
            vector=vector,
            payload={
                "candidate_id": candidate.id,
                "full_name": candidate.full_name,
                "skills": parsed_data.get("skills", [])
            }
        )

    except Exception:
        if candidate:
            candidate.status = "failed"
            db.commit()
    finally:
        db.close()